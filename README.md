# Quiviz

Quiviz is a cheap logger for your machine learning experiments.

--------------------------------------

## Install:
- Clone & install with: `pip install -e .`
(Might Need Visdom)

## Usage:

### Logging decorator:

```
import quiviz

@quiviz.log
def f(x):
    return {"x":x}
```

Logs into `quiviz.quiviz._quiviz_shared_state` and pass to observer:

### Register observer:

```
quiviz.register(<Callable Observer>)
```

### Existing observers:

- Simple log: `LoggingObs`
- Vizdom log: `contrib.LinePlotObs`



