from __future__ import annotations

from logging import *
import sys
import io
from types import FunctionType
from typing import Callable, Union
from functools import wraps
from pathlib import Path
from datetime import datetime
import threading

__lock__ = threading.Lock() 

class OutputLogger(io.TextIOBase):

    def __init__(
        self, 
        logger: Logger,  
        output_name :str =  'stdout',
        level: int = INFO
    ) -> None:
        
        super().__init__()
        self.output_name = output_name
        self.logger = logger
        self.level = level

    def __enter__(self) -> None:
        self.original_stream = getattr(sys, self.output_name)
        setattr(sys, self.output_name, self)

    def __exit__(self, _x, _y, _z) -> None:
        setattr(sys, self.output_name, self.original_stream)

    def write(self, s) -> None:
        if s := s.strip():
            self.logger.log(self.level, s)
    
def log_output(
    fun: Callable = None, 
    *, 
    name: str = 'root',
    logger: Logger | None = None,
    stdout_level: int = INFO, 
    stderr_level: int = ERROR
):
    """

If a function uses print or yields some output, capture it and log it
using the logging module.

Optional keyword arguments:
    * logger:  logger, by default root legger logging
    * stdout:  logging level of the standard output (by default INFO)
    * stderr:  logging level of the standard error (by default ERROR)

Example use:

    from obstechutils import logging

    @log_output
    def f():
        ... # calls functions that use print

    if __name__ == "__main__":
        logging.enhancedConfig()     # basic logger with better defaults
        # logging.periodFileConfig() # logger with daily log file
        f()                          # redirects all print to logger

"""
    logger = getLogger(name)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with OutputLogger(logger, 'stdout', level=stdout_level):
                with OutputLogger(logger, 'stderr', level=stderr_level):
                    return f(*args, **kwargs)
        
        return wrapper

    if fun:
        return decorator(fun)

    return decorator

class PeriodicFileHandler(FileHandler):
    
    def __init__(
        self, 
        pattern: str, 
        encoding: str | None = None, 
        delay: bool = False
    ) -> None:
       
        self.pattern = pattern
        filename = datetime.now().strftime(self.pattern)
        super().__init__(filename, 'a', encoding, delay)

    def emit(
        self, 
        record: LogRecord
    ) -> None:

        date = datetime.fromtimestamp(record.created)
        new_filename = datetime.now().strftime(self.pattern)
        if self.stream is None:
            self.baseFileName = new_filename
        elif self.baseFilename != new_filename:
            self.close()
            self.baseFilename = new_filename

        super().emit(record)
    
def enhancedConfig(
    format: str = "{asctime} {levelname:8} {message}",
    style: str = '{',
    datefmt: str = "%Y-%m%dT%I:%M:%S",
    level: int = INFO,
    force: bool = True,
):
    """Configure the loggers' format with 'better' defaults."""

    with __lock__:

        basicConfig(
            format=format, style=style,
            datefmt=datefmt, level=level,
            force=force
)


def periodicFileConfig(
    name: str = 'root',
    format: str = "{asctime} {levelname:8} {message}",
    style: str = '{',
    datefmt: str = '%Y-%m%dT%H:%M:%S-UTC%z',
    level: int = INFO,
    basename: str = 'dailylog', 
    path: Path = Path('.'), 
    stampfmt: str = '%Y%m%d',
    force: bool = True,
):
    """Configure a logger to use both logfile and console, changing the file each time the time stamp changes, by default, daily."""
        
    enhancedConfig(format=format, datefmt=datefmt, level=level, force=force)
    
    with __lock__:

        logger = getLogger(name)
        path.mkdir(parents=True, exist_ok=True)
        pattern = f"{path}/{basename}-{stampfmt}.log"
        
        if not force:

            # if already configured, do nothing
            for handler in logger.handlers:
                if isinstance(handler, PeriodicFileHandler):
                    if handler.pattern == pattern:
                        return
        else:
            
            for handler in logger.handlers:
                logger.removeHandler(handler)
        
        filehandler = PeriodicFileHandler(pattern)
        formatter = Formatter(format, datefmt, style=style)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
