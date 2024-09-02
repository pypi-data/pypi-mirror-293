### compress-bins

This package provides the compress_bins() function, a quality-of-life function for creating frequency charts in the numpy-pandas ecosystem.

Usage:
```
import compressbins.compressbins as cb

compressed_bins = cb.compress_bins([0,2,4,6])
print(compressed_bins) # ['0-2','2-4','4-6']
```

We can then use these sbins in creating frequency charts:
```
import pandas as pd
import numpy as np

counts, bins = np.histogram(df, bins=np.arange(10.00, 20.00, 1.00))
cbins = compress_bins(bins)
freqChart = pd.DataFrame({"Cost":cbins, "Count":counts})
print(freqChart)
        Cost  Count
0  10.0-11.0      1
1  11.0-12.0      8
2  12.0-13.0     16
3  13.0-14.0      9
4  14.0-15.0      6
5  15.0-16.0      4
6  16.0-17.0      3
7  17.0-18.0      2
8  18.0-19.0      1
```

