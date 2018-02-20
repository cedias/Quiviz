# Quiviz

Quiviz is a cheap logger for your machine learning experiments.

--------------------------------------

## Install:
- Clone & install with: `pip install -e .`
(Might Need Visdom)

## Usage (see exemple.py):

### Logging decorator:

```python
import quiviz

@quiviz.log
def f(x):
    return {"x":x}
```

Logs into `quiviz.quiviz._quiviz_shared_state`

### Register observer:

```python
quiviz.register(<Callable Observer>)
```


### Existing other observers (see quiviz.contrib):
- Vizdom log: `contrib.LinePlotObs`



