## Pipy
> A native Python wrapper around the command line program: `pip`

Pipy provides a high-level API to `pip` commands executed using a wrapper around a Python `subprocess`.

The Pipy API executes the `subprocess` commands using strict exception handling, type checking, and parsing of
    the input and output involved when communicating with `pip`
## Index
* [**Goal**](#goal)
* [**Motivation**](#motivation)
* [**Install**](#install)
* [**API**](#api)
* [**Notes**](#notes)
* [**Warnings**](#warnings)
* [**License**](#license)

## Goal
To be able to install/uninstall packages while inside a Python environment (ex. shared web interfaces like Databricks, Jupyter Notebook, iPython) which do not natively provide a command line interface to install Python packages.

## Motivation
 When tasked with installing packages from within a Python program or notebook the official recommendation from the Python Software Foundation is to **NOT**  `import pip` and use the internal API methods.
        
The official recommendation from the Python Software Foundation is instead to execute `pip` using the built-in python module `subprocess`  which allows the execution of arbitrary terminal commands.

`...pip is a command line program. While it is implemented in Python, and so is available from your Python code via import pip, you must not use pip's internal APIs in this way. There are a number of reasons for this...` - [Python Software Foundation](https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program)

`Pipy` provides an accessible Python API which follows the recommendation to use `pip` through a
        `subprocess`

## Install

This package has not yet been published to PyPi but can be installed directly by referencing the URL to the latest version on Github. 

See: [Github Releases](https://github.com/mmongeon-sym/pipy/releases)

#### Install from Github (Latest Version)
```bash
pip install https://github.com/mmongeon-sym/pipy/releases/latest/download/pipy.tar.gz
```

#### Uninstall
```bash
pip uninstall pipy
```

## Usage

#### Import
```bash
from pipy import Pipy
```


# API
**Pipy()**

* [**Pipy.freeze()**](#): Return a list of installed packages, ie `pip freeze`
* [**Pipy.list()**](#freezecls-fast-bool--true--return-a-list-of-installed-packages-ie-pip-freeze): Return a list of installed packages, ie `pip list`
* [**Pipy.show(*cls, name: str*)**](#showcls-fast-bool--true-get-information-about-a-package-returns-a-package-object-with-attrs-name-installed-version-ie-pip-show): Return information about an installed package
* [**Pipy.install(*cls, name: str*)**:](#installcls-name-str-no_dependenciestrue-install-a-package-or-list-of-packages-by-name-only-if-not-already-installed-and-available-on-pypi-will-not-upgrade-any-packages-or-installupgrade-extra-dependencies-returns-a-list-of-pypipackage-which-were-installed) Install a package by pypi name only if the package is not already installed.
* [**Pipy.uninstall(*cls, name: str*)**:](#uninstallcls-name-str-uninstall-a-package-by-name--only-if-the-package-is-currently-installed) Uninstall a package by name only if the package is  already installed.
* [**Pipy.search(*cls, name: str*)**](#searchcls-name-str-search-pypi-package-for-a-package-by-name-return-a-list-of-pypipackage-search-results): Search PyPi package repository for a package by name
* [**Pipy.get_pypi_package(*cls, name: str*)**](#get_pypi_packagecls-name-str-return-a-pypipackage-object-for-the-provided-package-name-only-if-the-package-exists-on-pypi): Return a `PyPiPackage` object for the provided package `name` only if the package exists on PyPi
* [**Pipy.get_package(*cls, name: str*)**](#get_packagecls-name-str-return-a-package-object-for-the-provided-package-name): Return a `Package` object for the provided package `name`
* [**Pipy.is_available(*cls, name: str*)**](#is_availablecls-name-str-returns-truefalse-if-the-package-name-is-available-on-pypi-to-be-installed): Returns True/False if the package is available on PyPi to be installed
* [**Pipy.is_installed(*cls, name: str*)**](#is_installedcls-name-str-returns-true-if-the-package-name-is-installed-else-false): Returns True/False if the package is installed


## Pipy()

* ### freeze(cls, fast: bool = True ): Return a list of installed packages, ie `pip freeze`
    > 
    ### Example: List installed packages
    ##### Python
    ```python
    from pipy import Pipy
    Pipy.freeze()
    ```
    ##### Output
    ```console
     FrozenPackage(name='xgboost', installed=True, version='0.90'),
     FrozenPackage(name='wrapt', installed=True, version='1.11.1'),
     FrozenPackage(name='wheel', installed=True, version='0.33.1'),
     ...
     ]
    ```




* ### list(cls, fast: bool = True): Return a list of installed packages, ie `pip list` {#pipy-list}
    > 
    ### Example: List installed packages
    ##### Python
    ```python
    from pipy import Pipy
    Pipy.list()
    ```
    ##### Output
    ```console
     [FrozenPackage(name='xgboost', installed=True, version='0.90'),
     FrozenPackage(name='wrapt', installed=True, version='1.11.1'),
     FrozenPackage(name='wheel', installed=True, version='0.33.1'),
     ...
     ]
    ```

* ### show(cls, fast: bool = True): Get information about a package. Returns a `Package` object with attrs: name, installed, version. ie `pip show`
    >
    ### Example: Show information about the `requests` package
    ##### Python 
    ```python
    from pipy import Pipy
    Pipy.show('requests')
    ```
    ##### Console
    ```console
     Package(name='requests', installed=True, version='2.21.0')
    ```
    ### Example: Sow information about package `not_a_real_package` is not installed
    ##### Python
    ```python
    from pipy import Pipy
    Pipy.show('not_a_real_package')
    ```
    ##### Console
    ```console
     Package(name='not_a_real_package',
             installed=False,
             version=None
             )
    ```

* ### install(cls, name: str, no_dependencies=True): Install a package or `list` of packages by `name`, only if not already installed, and available on PyPi. Will not upgrade any packages, or install/upgrade extra dependencies. Returns a list of `PyPiPackage` which were installed.
    >
    ### Example: Install the package `namedlist`
    ##### Python 
    ```python
      from pipy import Pipy
      Pipy.install('namedlist')
    ```
    ##### Log
    ```console
    2020-03-20T01:25:23+0000[package.install_package][INFO] Installing 1 packages: namedlist
    2020-03-20T01:25:23+0000[package.install_package][INFO] 1 packages will be installed: namedlist
    2020-03-20T01:25:23+0000[package.get_pypi][INFO] Searching PyPi for Package(namedlist) ...
    2020-03-20T01:25:23+0000[package.get_pypi][INFO] Found PyPiPackage(namedlist)(1.7)
    2020-03-20T01:25:23+0000[package.install_package][INFO] Installing PyPiPackage(namedlist)(1.7) ...
    2020-03-20T01:25:25+0000[package.install_package][INFO] Installed PyPiPackage(namedlist)(1.7)
    2020-03-20T01:25:25+0000[package.install_package][INFO] Installed 1 packages: namedlist
    ```
    ##### Console
    ```console
    [PyPiPackage(name='namedlist', 
                installed=True, 
                version='1.7', 
                installed_version='1.7',
                outdated=False, 
                description='Similar to namedtuple, but instances are mutable.',
                url='https://pypi.org/project/namedlist/'
                )
    ]
    ```
    ### Example: Attempt to install the package `namedlist` which is already installed. Returns a `Package` object.
    ##### Python 
    ```python
        from pipy import Pipy
        Pipy.install('namedlist')
    ```
    ##### Log
    ```console
    2020-03-20T01:27:31+0000[package.install_package][INFO] Installing 1 packages: namedlist
    2020-03-20T01:27:31+0000[package.install_package][INFO] 0 packages will be installed: 
    2020-03-20T01:27:31+0000[package.install_package][INFO] 1 packages are already installed: namedlist
    ```
    #### Console
    ```console
        []
    ```
    ### Example: Install a list of packages: `['namedlist', 'pandas']`. `pandas` is already installed, `namedlist` is not yet installed.
    ##### Python 
    ```python
      from pipy import Pipy
      Pipy.install(['namedlist', 'pandas'])
    ```
    ##### Log
    ```console
    2020-03-20T01:33:03+0000[package.install_package][INFO] Installing 2 packages: namedlist, pandas
    2020-03-20T01:33:03+0000[package.install_package][INFO] 1 packages will be installed: namedlist
    2020-03-20T01:33:03+0000[package.install_package][INFO] 1 packages are already installed: pandas
    2020-03-20T01:33:03+0000[package.get_pypi][INFO] Searching PyPi for Package(namedlist) ...
    2020-03-20T01:33:04+0000[package.get_pypi][INFO] Found PyPiPackage(namedlist)(1.7)
    2020-03-20T01:33:04+0000[package.install_package][INFO] Installing PyPiPackage(namedlist)(1.7) ...
    2020-03-20T01:33:05+0000[package.install_package][INFO] Installed PyPiPackage(namedlist)(1.7)
    2020-03-20T01:33:05+0000[package.install_package][INFO] Installed 1 packages: namedlist
    ```
    ##### Console
    ```console
    [PyPiPackage(name='namedlist', 
                installed=True, 
                version='1.7', 
                installed_version='1.7', 
                outdated=False, 
                description='Similar to namedtuple, but instances are mutable.',
                url='https://pypi.org/project/namedlist/'
                )
     ]
    ```
    
* ### uninstall(cls, name: str)): Uninstall a package by `name`,  only if the package is currently installed.
    ### Example: Uninstall the package `namedlist`
    #### Python 
    ```python
        from pipy import Pipy
      Pipy.uninstall('namedlist')
    ```
    
    ##### Log
    ```console
    2020-03-20T01:42:53+0000[package.uninstall_package][INFO] Preparing to uninstall 1 packages: namedlist
    2020-03-20T01:42:53+0000[package.uninstall_package][INFO] 1 packages will be uninstalled:namedlist
    2020-03-20T01:42:53+0000[package.uninstall_package][INFO] Uninstalling Package(namedlist)(1.7) ...
    2020-03-20T01:42:55+0000[package.uninstall_package][INFO] Uninstalled Package(namedlist)(1.7)
    2020-03-20T01:42:55+0000[package.uninstall_package][INFO] Uninstalled 1 packages: namedlist
    ```
    
    ##### Console
    ```console
    Out[77]: [Package(name='namedlist', installed=False, version='1.7')]
    ```

    
* ### search(cls, name: str): Search PyPi package for a package by `name`. Return a list of `PyPiPackage` search results
    >
    ### Example: Search PyPi for the package: `requests`
    ##### Python 
    ```python
        from pipy import Pipy
        Pipy.search('requests')
    ```
    ##### Console
    ```console
    [PyPiPackage(name='requests',
                 installed=True,
                 version='2.23.0',
                 installed_version='2.21.0',
                 outdated=True,
                 description='Python HTTP for Humans.',
                 url='https://pypi.org/project/requests/'
                 ),
    PyPiPackage(name='requests-lb',
                 installed=False,
                 version='0.3.2',
                 installed_version=None,
                 outdated=False,
                 description='A load-balancing wrapper around requests',
                 url='https://pypi.org/project/requests-lb/'),
    PyPiPackage(name='vk-requests',
                 installed=False,
                 version='1.2.0',
                 installed_version=None,
                 outdated=False,
                 description='vk.com requests for humans. API library for vk.com',
                 url='https://pypi.org/project/vk-requests/'),
    ...
    ]

    ```
   

* ### get_package(cls, name: str): Return a `Package` object for the provided package `name`
    >
    ### Example: Package `requests` is installed
    ##### Python 
    ```python
        from pipy import Pipy
        Pipy.get_package('requests')
    ```
    ##### Console
    ```console
        package = Package(name='requests',
                    installed=True,
                    version='2.23.0'
                    )
    ```

    
* ### get_pypi_package(cls, name: str): Return a `PyPiPackage` object for the provided package `name` only if the package exists on PyPi
    >
    ### Example: Package `requests` exists on PyPi and is installed
    ##### Python 
    ```python
        from pipy import Pipy
        Pipy.get_pypi_package('requests')
    ```
    ##### Console
    ```console
    PyPiPackage(name='requests',
                installed=True,
                version='2.23.0',
                installed_version='2.21.0',
                outdated=True,
                description='Python HTTP for Humans.',
                url='https://pypi.org/project/requests/'
                )
    ```
    ### Example: Package which does not exist on PyPi
    ##### Python
    ```python
        from pipy import Pipy
        Pipy.get_pypi_package('not_a_real_package')
    ```
    ##### Console
    ```console
        None
    ```
    
* ### is_available(cls, name: str): Returns True/False if the package `name` is available on PyPi to be installed
    >
    ### Example: Check if the package `requests` is available on PyPi
    ##### Python 
    ```python
    from pipy import Pipy
    Pipy.is_available('requests')
    ```
    ##### Console
    ```console
    True
    ```
    ### Example: Check if the package `not_a_real_package` is available on PyPi
    ##### Python 
    ```python
    from pipy import Pipy
    Pipy.is_available('not_a_real_package')
    ```
    ##### Console
    ```console
    False
    ```
    

* ### is_installed(cls, name: str): Returns `True` if the package `name` is installed, else `False`
    >
    ### Example: Check if the package `requests` is installed
    ##### Python 
    ```python
    from pipy import Pipy
    Pipy.is_installed('requests')
    ```
    ##### Console
    ```console
    True
    ```
    ### Example: Check if the package `not_a_real_package` is installed
    ##### Python 
    ```python
    from pipy import Pipy
    Pipy.is_installed('not_a_real_package')
    ```
    ##### Console
    ```console
    False
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
```
Installing and uninstalling packages in a python environment or virtualenv which is "shared" may affect the execution of other users' code. 
```


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