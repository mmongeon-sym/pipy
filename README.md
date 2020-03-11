## Pipy
> A native Python wrapper around the command line program: `pip`

Pipy provides a high-level API to `pip` commands executed using a wrapper around a Python `subprocess`.

The Pipy API executes the `subprocess` commands using strict exception handling, type checking, and parsing of
    the input and output involved when communicating with `pip`


## Motivation
 When tasked with installing packages from within a Python program or notebook the official recommendation from the Python Software Foundation is to **NOT**  `import pip` and use the internal API methods.
        
The recommendation is instead to execute `pip` using the built-in python module `subprocess`  which allows the execution of arbitrary terminal commands.

"...pip is a command line program. While it is implemented in Python, and so is available from your Python code via import pip, you must not use pip’s internal APIs in this way. There are a number of reasons for this..." 
[Python Software Foundation](https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program)

Pipy() provides an accessible Python API which follows the recommendation to use `pip` through a
        `subprocess`

## Install

#### Install from Github
```bash
pip install https://github.com/mmongeon-sym/pipy/releases/latest/download/pipy.tar.gz
```

## Usage

#### Import
```bash
from pipy import Pipy
```
#### Pipy.list()
> List installed packages
```bash
from pipy import Pipy
Pipy.list()
```
#### Pipy.install(name: str)
> List installed packages
```bash
from pipy import Pipy
Pipy.install('requests')
```


## Notes

**Packages share dependencies**

By default, pip installs packages with all `dependencies`, which are requested by the package. Any of these
dependency packages can have their own dependencies. A single packgae can be a shared dependency of many
packages.

When dependencies are referenced on install by a package they are specified by requesting a specific version
of the package or range of versions. Ex. widget-maker==1.0.0 or widget-maker>=1.1.0. The concept of package
versioning is important to maintain the ability to create always reproducible codebases including all
dependencies, frozen at that specific version.

**Packages require specific versions of dependencies**
When a new package is installed which references a new version of a dependency than what is installed,
it is possible that the existing library could be overwritten by the new version, with the chance of
breaking the execution in other code which expects to be using a previous version's code.


**Example: Shared package is updated, breaking another package**
    Databricks version 5.5 has built-in module pandas v20 which references python-dateutil v 1.1 as
a dependency. User needs to install package boxsdk v2.0 which requires python-dateutil v1.5. Without
additional controls, pip install installs boxsdk and inherintly updates python-dateutil from v1.1 to
v1.5. Pandas is written with very tight controls around its usage, and its usage of dependencies. There
is an update to python-dateutil in 1.5 which breaks it's usage in Pandas v20.


## Warnings
        Installing and uninstalling packages in a python environment or virtualenv which is "shared" may affect the
        execution of other users' code when a new, removed or updated package has been modified in a way which breaks
        chain of  execution when another package references the (modified) package when as a dependency.

## Features
What makes your project stand out?

## Code Example
Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## API Reference


## License
```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>

```