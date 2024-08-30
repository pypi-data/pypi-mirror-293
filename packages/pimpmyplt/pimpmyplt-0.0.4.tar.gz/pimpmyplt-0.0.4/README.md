# PimpMyPLT

This package adds an pythonic way to modify your `matplotlib.rcParams` .

# Installation

```console
> pip install pimpmyplt
```

# Usage

```python
import matplotlib.pyplot as plt
import pimpmyplt
from pimpmyplt.pimps import PimpUseTeX, PimpTightLayout, PimpSaveFig

modifications = [
    PimpUseTeX(),
    PimpTightLayout(),
    PimpSaveFig(format="png", dpi=400),
]
composed = pimpmyplt.compose(modifications)
plt.rcParams.update(composed)

print(dict(composed))
```

```
{'savefig.format': 'png', 'savefig.dpi': 400, 'figure.autolayout': True, 'text.usetex': True, 'font.family': 'serif', 'font.serif': 'cm'}
```

# Why?

Well, good question as there are [easy
ways](https://matplotlib.org/stable/users/explain/customizing.html) to modify
the rcParams. PimpMyPLT is just a bit more pythonic. It's easy to write your own
`Pimper` class (like `PimpUseTeX` , ...) and add functionality. But **this project
is in a very early development stage**, so don't rely on it...
