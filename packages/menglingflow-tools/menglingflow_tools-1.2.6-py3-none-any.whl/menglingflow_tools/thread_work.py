from threading import Thread, get_ident
import traceback
import os
import logging
import time
import asyncio
import subprocess
import warnings
try:
    from menglingtool.queue import Mqueue
except ModuleNotFoundError:
    subprocess.check_call(['pip','install', "menglingtool"])
    from menglingtool.queue import Mqueue

# 便捷获取log对象
def getLogger(name, level=logging.INFO, log_path=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(log_path) if log_path else logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class WorkPool:
    def __init__(self, logger: logging.Logger = None) -> None:
        self.logger = logger if logger else getLogger(f'pid-{get_ident()}')
        self.task_queue = Mqueue()
        self._alive = False
    
    def getTaskNum(self) -> int:
        return self.task_queue.qsize()
    
    def is_alive(self) -> bool:
        return self._alive
    
    def stop(self):
        self._alive = False
    
    def start(self, *, getGood = None, getResult, good_num: int = 3,
                        is_put_args=False,
                        is_put_kwargs=False,
                        is_put_time=True) -> list:
        assert not self._alive, '任务已启动!'
        self.logger.info(f'PID-{os.getpid()} worker num: {good_num}')
        self._alive = True
        
        def _worker():
            gooder = getGood() if getGood else None
            while self._alive:
                que, index, args, kwargs = self.task_queue.get()
                sd = time.time()
                try:
                    result = getResult(gooder, *args, **kwargs) if gooder else getResult(*args, **kwargs)
                    err = None
                except:
                    err = traceback.format_exc()
                    result = None

                self.logger.info(f'args:{args}, kwargs:{kwargs}, is_err:{bool(err)}')
                rdt = {'index': index, 'result': result, 'err':err}
                if is_put_args: rdt['args'] = args
                if is_put_kwargs: rdt['kwargs'] = kwargs
                if is_put_time: rdt['time'] = time.time() - sd
                que.put(rdt)

        ts = [Thread(target=_worker, daemon=True) for _ in range(good_num)]
        [t.start() for t in ts]
        return ts


    def arg_in_task_puts(self, vs: list, jump: bool = False) -> Mqueue: 
        return self.all_in_task_puts([[(v,), {}] for v in vs], jump=jump)


    def args_in_task_puts(self, argss: list, jump: bool = False) -> Mqueue:
        return self.all_in_task_puts([[args, {}] for args in argss], jump=jump)


    def kwargs_in_task_puts(self, kwargss: list, jump: bool = False) -> Mqueue:
        return self.all_in_task_puts([[(), kwargs] for kwargs in kwargss], jump=jump)


    def all_in_task_puts(self, args_and_kwargs: list, jump: bool = False) -> Mqueue:
        if len(args_and_kwargs)<=0: 
            warnings.warn("task_put参数数量小于1!")
            return None
        result_queue = Mqueue(maxsize=len(args_and_kwargs))
        self.task_queue.puts(*[(result_queue, i, *args_kwargs) for i, args_kwargs in enumerate(args_and_kwargs)], jump=jump)
        return result_queue


    @staticmethod
    def getResults(result_queue: Mqueue, is_sorded=True, timeout = None) -> list[dict]:
        if result_queue is None: 
            warnings.warn("等待队列为None!")
            return []
        t = 0
        while not result_queue.full():
            if timeout and t >= timeout: raise TimeoutError(f'process:{result_queue.qsize()}/{result_queue.maxsize}  timeout:{timeout}s')
            time.sleep(1)
            t+=1
        ls = result_queue.to_list()
        return sorted(ls, key = lambda x: x['index']) if is_sorded else ls

    @staticmethod
    async def async_getResults(result_queue: Mqueue, is_sorded=True, timeout = None) -> list[dict]:
        if result_queue is None: 
            warnings.warn("等待队列为None!")
            return []
        t = 0
        while not result_queue.full():
            if timeout and t >= timeout: raise TimeoutError(f'process:{result_queue.qsize()}/{result_queue.maxsize}  timeout:{timeout}s')
            await asyncio.sleep(1)
            t+=1
        ls = result_queue.to_list()
        return sorted(ls, key = lambda x: x['index']) if is_sorded else ls
