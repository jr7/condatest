# condatest

This repository is meant for testing a segfault in conda.
The steps should be performend in a virtualenv  and conda

To install the library and requirements 

`pip install cython` or `conda install cython`

same for `numpy`.

The library is then installed from the root folder with  `pip install .`
Next  step is to execute some code:

```
import condatest 
r = condatest.rdb.ShmReader()
r.get_buffer()
```

This should return a numpy array including ones when using  virualenv.
And a segmentation fault when using conda. 


