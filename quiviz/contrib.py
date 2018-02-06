import visdom
import torch


class LinePlotObs():
    """
    Visdom Observer which groups by metrics and uses function as line legend.
    => Splits on split_char attribute default: "_" (ie: train_mse => ["train","mse"])
        -> metric is last (mse)
        -> line name is first (train)
            => plots on window titled "mse" under the name "train"
    """
    def __init__(self):
        self.viz = visdom.Visdom()
        self.plots = {}
        self.__name__= 'LinePlotObs'
        self.split_chr = '_'
        self.line_epochs = {}
        

    def __call__(self,d):
        for plot_name, v in self.group_plots(d).items():

            plt = self.plots.setdefault(plot_name,LinePlot(self.viz,f"{d.xp_name}: {plot_name}"))

            for line,values in v:
                p_key = plot_name+line

                if len(values)-1 > self.line_epochs.get(p_key,-1):
                    plt(len(values)-1,values[-1],line)
                    self.line_epochs[p_key] = len(values)-1


    def group_plots(self,d):
        """
        aggregate values for plotting call returns plot_name : [(line_name,[values])]
        """
        metrics = {}
        for k,v in d.items():
            sk = k.split(self.split_chr)
            metric = sk[-1]
            plt_key = " ".join(sk[:-1])
            metrics.setdefault(metric,[]).append((plt_key,v))
        return metrics
        

class LinePlot():
    """
    Helper to plot lines in torch with Visdom
    """

    def __init__(self,viz,name="plot",opt_dict={}):
        self.viz = viz
        self.name = name
        self.win = None
        self.opt_dict = opt_dict
        self.opt_dict["title"] = self.name

    def _checks(self,x,y):
        
        """
        Performs transformations
        a) Changes to Tensor if int/float/array.
        b) Assert Tensors have two dimensions (1,X)
        c) expand x.size(-1) to y.size(-1) if x.size(-1) = 1
        """
        def to_tensor(var):
            if type(var) in [int, float, list]:
                return torch.Tensor([var])
            else:
                return var

        x,y = to_tensor(x),to_tensor(y) # a)
        

        if x.size(-1) == 1 and y.size(-1) != x.size(-1): # c)
            x = x.expand_as(y)

        return x,y

    def update(self,x,y,name="line"):
        x,y = self._checks(x,y)

        if self.win is None:
            self.win = self.viz.line(X=x, Y=y,opts=self.opt_dict) # TODO: Find a way to remove placeholder...
            self.viz.line(X=x, Y=y, win=self.win,name=name, update='append',opts=self.opt_dict)
            

        else:
            self.viz.line(X=x, Y=y, win=self.win,name=name, update='append',opts=self.opt_dict)

    def __call__(self,x,y,name):
        self.update(x,y,name)


