# autoCppToPy
## Q&A
**Q**: What is autoCppToPy?<br>
**A**: autoCppToPy is an easy and fast way to compile C++ code into a Python module
<br><br>
**Q**: How does autoCppToPy work under the hood?
**A**: autoCppToPy uses pybind11 to compile your C++ code into a python module
<br><br>
**Q**: How can I use CppToPy
**A**: autoCppToPy can either be imported into your python code, allowing you to compile any C++ file yourself using autoCppToPy, or it can be used directly in the command line

## CLI Documentation
### Usage
(* = required)
```commandline
python -m cpptopy -f <source file*> --header <header file*> -o <package name*> -l <language name = "C++"> --auto-stubs <generate auto .pyi files = False>
```

### Example
main.hpp:
```cpp
int add(int a, int b);
```

main.cpp:
```cpp
#include "main.hpp"
int add(int a, int b) {
    return a + b
}
```

cli:
```commandline
python -m cpptopy -f "main.cpp" --header "main.hpp" -o "my_module" --auto-stubs True
```

main.py
```python
import my_module
my_module.add(2, 3)  # 5
```
