import logging
import os
from threading import Event
from time import sleep
from zuu.stdpkg.time import sleep_until

from .ext import Step

class Ctx:
    def __init__(self):
        self.stopEvent: Event = None
        self.__vars = {}

    @property
    def vars(self):
        return self.__vars

    def wait(self):
        while True:
            if self.stopEvent.is_set():
                break
            sleep(0.1)

class Runner:
    """
    The `Runner` class is responsible for executing a set of steps defined in a target class. It provides the following functionality:
    
    """
    def __init__(
        self, 
        cls: type,
        start_immediately: bool = True, 
        wait_for: str = None,
        debug : bool = True
    ):
        if debug:
            from zuu.stdpkg.logging import basic_debug
            basic_debug()

        self.__target = cls
        self.__ctx = Ctx()
        self.__check_target()

        self.__runtime_selective_steps = os.environ.get('ZUTO_SKIP_STEPS', '').split(',')

        if wait_for:
            sleep_until(wait_for)

        if start_immediately:
            self.exec()

    def __check_target(self):
        pass

    def __iter_target_steps(self):
        for k, v in self.__target.__dict__.items():
            if k in self.__runtime_selective_steps:
                logging.debug(f'skipping {k}...')
                continue

            if isinstance(v, Step):
                yield k, v

    def exec(self):
        """
        Executes the steps defined in the target class.
        
        This method iterates through the steps defined in the target class and runs each one, printing the name of the step before executing it. If the target class has a docstring, it will also print the contents of the docstring before running the steps.
        """
        if self.__target.__doc__:
            for line in self.__target.__doc__.splitlines():
                line = line.strip()
                if not line:
                    continue
                print(line)

        for k, v in self.__iter_target_steps():
            logging.debug(f'running {k}...')
            print(f"running func: {k.replace("_", " ")}")
            v.run(self.__ctx)
