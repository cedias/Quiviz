import wrapt
import logging


### Core

_quiviz_naming_func = lambda f,k :f"{k}"
_quiviz_logging_func = lambda m,v:f"{m}\t{v}"


class Observable_Dict(dict):

    def __init__(self):
        super(Observable_Dict,self).__init__()
        self.observers = {}
        self.xp_name = "None"
        self.xp_parameters = {}

    def register(self,callable):
        self.observers[callable.__name__] = callable

    def notify_obs(self,func_ret):
        for obs in self.observers.values():
            obs(self,func_ret)

_quiviz_shared_state = Observable_Dict()


@wrapt.decorator
def log(wrapped, instance, args, kwargs):   

    func_ret = wrapped(*args, **kwargs)

    if not isinstance(func_ret,dict):
        raise TypeError(f"Logged function \"{wrapped.__name__}\" returns \"{type(func_ret)}\" instead of dict")

    for k,v in func_ret.items():
        d_key = _quiviz_naming_func(wrapped,k)
        _quiviz_shared_state.setdefault(d_key,[]).append(v)
    
    _quiviz_shared_state.notify_obs(func_ret)

    return func_ret


class LoggingObs():
    """
    python classic simple logger
    """

    def __init__(self):
        self.__name__= 'PythonLogger'
    
    def __call__(self,d,func_ret):
        for m , v in func_ret.items():
            logging.info(_quiviz_logging_func(m,v))



### Helpers

def register(callable):
    """
    Registers a new observers to shared_dict
    """
    _quiviz_shared_state.register(callable)

def reset():
    """
    Resets shared state
    """
    _quiviz_shared_state.clear()

def name_xp(name):
    """
    Sets the experience name
    """
    _quiviz_shared_state.xp_name = name



