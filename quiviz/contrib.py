class LinePlotObs():
    """
    Visdom Observer which groups by metrics and uses function as line legend.
    => Splits on split_char attribute default: "_" (ie: train_mse => ["train","mse"])
        -> metric is last (mse)
        -> line name is first (train)
            => plots on window titled "mse" under the name "train"
    """
    def __init__(self,env="main",visdom=None,set_metrics=set()):
        self.visdom = __import__('visdom')
        
        if visdom is None:
            self.viz = self.visdom.Visdom(env=env)
        
        self.plots = {}
        self.set_metrics = set_metrics
        self.__name__= 'LinePlotObs'
        self.split_chr = '_'
        

    def __call__(self,d,func_ret):

        for plot_name, v in self.group_plots(d).items():
                plt = self.plots.setdefault(plot_name,LinePlot(self.viz,f"{plot_name}"))

                for line,values in v:
                    plt(line,values)
                    

    def group_plots(self,d):
        """
        aggregate values for plotting call returns plot_name : [(line_name,[values])]
        """
        metrics = {}
        for k,v in d.items():
            if type(v) is list: #only care for lists of values
                sk = k.split(self.split_chr)

                # train_mse => ["train","mse"]
                metric = sk[-1]
                plt_key = " ".join(sk[:-1])

                if (metric in self.set_metrics or len(self.set_metrics) == 0):
                    metrics.setdefault(metric,[]).append((plt_key,v))
        return metrics
        

class LinePlot():
    """
    Helper to plot lines in torch with Visdom
    Callable("plot_name",[value1,value2])
    """

    def __init__(self,viz,name="plot",opt_dict={}):
        self.visdom = __import__('visdom')
        self.torch = __import__('torch')
        self.viz = viz
        self.name = name
        self.win = None
        self.opt_dict = opt_dict
        self.opt_dict["title"] = self.name

    def _checks(self,values):
        
        """
        Performs transformations
        a) Changes to Tensor if int/float/array.
        b) returns indexes
        """
        def to_tensor(var):
            if type(var) in [int, float, list]:
                return self.torch.Tensor([var])
            else:
                return var

        y = to_tensor(values) # a)
        x = to_tensor(list(range(len(values))))

        return x,y

    def update(self,name,x):
        
        x,y = self._checks(x)

        if self.win is None:
            self.win = self.viz.line( Y=y,name=name,opts=self.opt_dict)
        else:
            self.viz.line( Y=y[-1],X=x[-1], win=self.win,name=name, update='replace',opts=self.opt_dict)

    def __call__(self,name,values):
       
        self.update(name,values)