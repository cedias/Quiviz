import wrapt
import logging



_quiviz_naming_func = lambda f,k :f"{k}"
_quiviz_logging_func = lambda m,v:f"{m}\t{v[-1]}"


class Observable_Dict(dict):

    def __init__(self):
        super(Observable_Dict,self).__init__()
        self.observers = {}
        self.xp_name = "None"
        self.xp_parameters = {}

    def register(self,callable):
        self.observers[callable.__name__] = callable

    def notify_obs(self):
        for obs in self.observers.values():
            obs(self)

_quiviz_shared_state = Observable_Dict()



def register(callable):
    _quiviz_shared_state.register(callable)

def name_xp(name):
    _quiviz_shared_state.xp_name = name

@wrapt.decorator
def log(wrapped, instance, args, kwargs):   

    func_ret = wrapped(*args, **kwargs)

    if not isinstance(func_ret,dict):
        raise TypeError(f"Logged function \"{wrapped.__name__}\" returns \"{type(func_ret)}\" instead of dict")

    for k,v in func_ret.items():
        d_key = _quiviz_naming_func(wrapped,k)
        _quiviz_shared_state.setdefault(d_key,[]).append(v)
    
    _quiviz_shared_state.notify_obs()

    return func_ret


class LoggingObs():
    """
    python classic simple logger
    """

    def __init__(self):
        self.__name__= 'PythonLogger'
        self.split_chr = '_'
        self.history = {}
    
    def __call__(self,d):
        for m , v in d.items():
            if not self.history.get(m,None) == v[-1]: #logs when change
                self.history[m] = v[-1]
                logging.info(_quiviz_logging_func(m,v))
                print(_quiviz_logging_func(m,v))
    
    def log_msg(msg):
        logging.info(msg)



