import threading
import psutil

from .utils import get_newly_created_processes, get_newly_opened_windows
import pygetwindow as pg


class Step:
    def __init__(self, func):
        self.__func = func
        self.__timeout = -1
        self.__killscreen = True

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.__timeout = value
        assert self.__timeout > 0

    @property
    def killscreen(self):
        return self.__killscreen

    @killscreen.setter
    def killscreen(self, value):
        self.__killscreen = value
        assert isinstance(value, bool)

    def __run_with_timeout(self, ctx):
        ctx.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__func, args=(ctx,))
        thread.start()
        thread.join(self.__timeout)
        if thread.is_alive():
            ctx.stopEvent.set()
            thread.join()

    def run(self, ctx):
        """
        Runs the provided function with optional timeout and screen cleanup.
        
        If `killscreen` is set to `True`, this method will kill any newly created processes and close any newly opened windows after the function has completed.
        
        If `timeout` is set to a positive value, the function will be executed in a separate thread and will be terminated if it exceeds the specified timeout.
        
        The function's docstring, if present, will be printed to the console before the function is executed.
        """
        if self.__killscreen:
            currentWindows = pg.getAllWindows()
            currentProcs = [x for x in psutil.process_iter()]

        if self.__func.__doc__:
            for line in self.__func.__doc__.splitlines():
                line = line.strip()
                if not line:
                    continue

                print(line)

        if self.__timeout < 0:
            self.__func(ctx)
        else:
            self.__run_with_timeout(ctx)

        if self.__killscreen:
            newProcs = get_newly_created_processes(currentProcs)
            for proc in newProcs:
                try:
                    proc.kill()
                except Exception as e:
                    print(e)
                    pass
            
            newWnds = get_newly_opened_windows(currentWindows)
            for wnd in newWnds:
                try:
                    wnd.close()
                except Exception as e:
                    print(e)
                    pass


def step(func):
    return Step(staticmethod(func))
