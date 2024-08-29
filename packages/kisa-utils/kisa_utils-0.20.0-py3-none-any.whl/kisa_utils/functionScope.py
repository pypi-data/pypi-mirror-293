import inspect
from functools import wraps
import os

def private(func):
    '''
    function is used only in the same module as that in which its defined
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        def f():
            expectedModule = inspect.getfile(func)
            stack = inspect.stack()
            stackCallerModules = []
            for s in stack:
                if '<frozen' in s.filename:
                    # executed due to imports of the original module
                    break
                stackCallerModules.append(s.filename)

            callingModule = stackCallerModules[-1]
            if expectedModule != callingModule:
                raise Exception(f"cant't call private function `{func.__name__}` from external module")

            return func(*args, **kwargs)
        return f()
    return wrapper

def protected(func):
    '''
    function is only allowed to be used in;
    * the module in which its defined
    * submodules starting in the defining module's path
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        def f():
            expectedModule = inspect.getfile(func)
            stack = inspect.stack()
            stackCallerModules = []
            for s in stack:
                if '<frozen' in s.filename:
                    # executed due to imports of the original module
                    break
                stackCallerModules.append(s.filename)

            callingModule = stackCallerModules[-1]
            if not callingModule.startswith(os.path.dirname(expectedModule)):
                raise Exception(f"cant't call private function `{func.__name__}` from external module")

            return func(*args, **kwargs)
        return f()
    return wrapper
