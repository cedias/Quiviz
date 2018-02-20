# Quiviz

Quiviz is a cheap logger for your machine learning experiments.

--------------------------------------
## Concept:
**Quiviz** provides a decorator to autolog your experiments. at import, it injects an observable **state** dict into your script which is automatically populated from your logged output function. Values are aggregated by keys. Moreover, it autoconfigures a python logger to track those metrics.

It adopts convention over configuration: 
**Quiviz** is meant for self packaged scripts (a typical ml experiment script) with metrics which evolve over time (such as accuracy). Values are aggregated by keys. To log those values, the function returning them should simply return a `dict()` and be decorated with the `quiviz.log` decorator.

```python
@quiviz.log
def f(x):
    acc = x
    return {"accuracy":acc}
    
for x in range(100):
    f(x)
    
# -> quiviz will log {"accuracy": [0,...,99]} into injected state dict quiviz.quiviz._quiviz_shared_state
```


## Install:
- Clone & install with: `pip install -e .`

## Usage (see exemple.py):

1. `import quiviz`
2. Decorate logged function with `@quiviz.log`
3. Run



### Observers API:

Under the hood, **Quiviz** is a dictionnary implementing the observable pattern. Each time the state dictionnary is updated some observers are notified. By default, the **core** logger observer is started. An observer is just a **Callable** object which takes as arguments two dictionnaries: the full state dict and the added subset.

- New observers can be added with `quiviz.register(<Callable Observer>)`

A minimal observer looks like this:
```python
def printObs(state,new_values):
   do_things(...)

quiviz.register(printObs) # will call do_things whenever values are added to quiviz observable dict.
```


### Existing Observers (see quiviz.contrib):
- Vizdom continuous logging: `contrib.LinePlotObs`



