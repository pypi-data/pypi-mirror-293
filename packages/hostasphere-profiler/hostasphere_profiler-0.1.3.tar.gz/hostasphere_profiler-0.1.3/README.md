# ![hostasphere](https://avatars.githubusercontent.com/u/164780978?s=30 "logo") hand-e.fr

## Hostasphere - Profiler API

### Description
The Profiling API allows you to measure execution time, memory usage, 
and other metrics related to OpenHosta for Python functions. 
The collected data is sent to your Hostasphere monitoring interface.

### Installation
Install the required dependencies with pip :
```schell
pip install hostasphere-profiler==0.1.3
```

### Usage
To profile a function, use the decorator `@profiler.probe()`:

```python
from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051',
    token='shs_qsdsq8d79qdsq65d4q6d84sqd68qsd64qsd48q68sf'
)

@profiler.probe()
def my_func():
    # Function logic
    pass
```
You can find many examples in the [examples](https://github.com/hand-e-fr/hostasphere/tree/main/api/python3/examples) folder.
