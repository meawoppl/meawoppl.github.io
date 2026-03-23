---
title: "matplotlib/pylab plotting SSH tunnels and backends"
date: 2012-04-01 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

I recently discovered that tunneled connections using matplotlib force X11 to cram the entire figure across a slow SSH connection, even if the figure will never be rendered! To fix this, simply use the backend that requires no X11 support:

```python
import matplotlib
matplotlib.use('Agg')

from matplotlib.pyplot import (plot, figure, psd, hist, savefig, close, title, xlabel, ylabel, axis)
from matplotlib.mlab import detrend_linear
```

This way there is (virtually) no SSH traffic overhead to plotting and saving figures!! Yay! Enjoy!
