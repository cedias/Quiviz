# Quiviz

Quiviz is a cheap logger for your machine learning experiments.

## Concept:
**Quiviz** provides tools to autolog your experiments.


At import:
- It injects an observable **experiment state** (dictionnary) into your script.
- It autoconfigures a python logger to track metrics in this dictionnary.

To automatically populate this **experiment state**, the function returning the metrics you wish to track should simply return a `dict()` and be decorated with `@quiviz.log`. Values are aggregated by keys, ordered by insertion. 


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



