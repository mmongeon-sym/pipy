from .package import PackageHelper
from .package import Package


class Pipy(object):
    """
    Pipy

    A native Python wrapper around the command line program: `pip`

    Pipy provides a high-level API to `pip` commands executed using a wrapper around a Python `subprocess`.

    The Pipy API executes the `subprocess` commands using strict exception handling, type checking, and parsing of
    the input and output involved when communicating with `pip`

    Usage
        :class:`Pipy()`: Abstract API around the command line program `pip`.
            Examples:
                Pipy.install('boxsdk')
        :class: `Package(name)`: Python object representing a python package.
            Examples:
                from Pipy import Package;
                pkg = Package(name='boxsdk')
                pkg.installed # True/False
                pkg.install() # Intall the package only if not installed already

    Requirement
        To be able to install/uninstall packages while inside a Python environment (ex. shared web interfaces like
        Databricks, Jupyter Notebook, iPython) which do not natively provide a command line interface to install
        Python packages.

    Goals
        Installing and uninstalling packages in a python environment or virtualenv which is "shared" may affect the
        execution of other users' code when a new, removed or updated package has been modified in a way which breaks
        chain of  execution when another package references the (modified) package when as a dependency.

    Notes
         By default, pip installs packages with all `dependencies`, which are requested by the package. Any of these
         dependency packages can have their own dependencies. A single packgae can be a shared dependency of many
         packages.

         When dependencies are referenced on install by a package they are specified by requesting a specific version
         of the package or range of versions. Ex. widget-maker==1.0.0 or widget-maker>=1.1.0. The concept of package
         versioning is important to maintain the ability to create always reproducible codebases including all
         dependencies, frozen at that specific version.

         When a new package is installed which references a new version of a dependency than what is installed,
         it is possible that the existing library could be overwritten by the new version, with the chance of
         breaking the execution in other code which expects to be using a previous version's code.
            Example:
                Databricks version 5.5 has built-in module pandas v20 which references python-dateutil v 1.1 as
            a dependency. User needs to install package boxsdk v2.0 which requires python-dateutil v1.5. Without
            additional controls, pip install installs boxsdk and inherintly updates python-dateutil from v1.1 to
            v1.5. Pandas is written with very tight controls around its usage, and its usage of dependencies. There
            is an update to python-dateutil in 1.5 which breaks it's usage in Pandas v20.


    Motivation:
        When tasked with installing packages from within a Python program or notebook the official recommendation
        from the Python Software Foundation is to not `import pip` and use the internal API methods, and to execute
        'pip' using the python `subprocess` module which allows the execution of arbitrary terminal commands.

        "...pip is a command line program. While it is implemented in Python, and so is available from your Python
        code via import pip, you must not use pip’s internal APIs in this way. There are a number of reasons for
        this..."
            See: https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program

        :class:Pipy() provides an accessible Python API which follows the recommendation to use `pip` through a
        `subprocess`


    """

    @classmethod
    def list(cls, fast: bool = True):
        """
        Return a list of installed packages, ie `pip list`

        See Also
            `pip list`: https://pip.pypa.io/en/stable/reference/pip_list

        Args:
         fast(:obj:`bool`, required): If True, default to using an un-documented (but faster <1s vs 6s)
                                      method of obtaining installed packages.
                                      If False, use `pip list` which can take up to 10s sometimes.

        Returns:
         :obj:`list`: list of :obj:`InstalledPackage`

        """
        if fast is True:
            return PackageHelper.get_installed_packages()
        return PackageHelper.list_packages()

    @classmethod
    def freeze(cls, fast: bool = True):
        """
        Return a list of installed packages, ie `pip freeze`

        See Also
            `pip freeze`: https://pip.pypa.io/en/stable/reference/pip_freeze

        Args:
         fast(:obj:`bool`, required): If True, default to using an un-documented (but faster <1s vs 6s)
                                      method of obtaining installed packages.
                                      If False, use `pip list` which can take up to 10s sometimes.

        Returns:
         :obj:`list`: list of :obj:`InstalledPackage`

        """

    @classmethod
    def show(cls, name: str, fast: bool = True):
        """
        Return information about an installed package

        See Also
            `pip show`: https://pip.pypa.io/en/stable/reference/pip_show

        Args:
            name(:obj:`str`, required): package name
            fast(:obj:`bool`, required): If True, default to using an un-documented (but faster <1s vs 6s)
                                    method of obtaining installed packages.
                                    If False, use `pip list` which can take up to 10s sometimes.

        Returns:
            :obj:`list`: list of :obj:`InstalledPackage`

        """
        if fast is True:
            return Package(name=name)
        return PackageHelper.show_package(name=name)

    @classmethod
    def install(cls, name: str, no_dependencies=True):
        """
        Install a package by pypi name only if the package is not already installed.

        By default, no extra dependencies are installed or updated as a safeguard

        See Also
            `pip install`: https://pip.pypa.io/en/stable/reference/pip_install

        Args:
            name(:obj:`str`, required): package name
            no_dependencies(:obj:`bool`, required): If True, do not install extra dependencies (default)

        Returns:
            :obj:`InstalledPackage`: Package.installed will be True

        """
        return PackageHelper.install_package(name=name, no_dependencies=no_dependencies)

    @classmethod
    def uninstall(cls, name: str):
        """
        Uninstall a package by name only if the package is  already installed.


        See Also
            `pip uninstall`: https://pip.pypa.io/en/stable/reference/pip_uninstall

        Args:
          name(:obj:`str`, required): package name

        Returns:
          obj:`Package`: Package.installed will be False

        """
        return PackageHelper.uninstall_package(name=name)

    @classmethod
    def search(cls, name: str):
        """
        Search PyPi package repository for a package by name


        See Also
              `pip uninstall`: https://pip.pypa.io/en/stable/reference/pip_search

        Args:
            name(:obj:`str`, required): package name


        Returns:
            :obj:`list`: obj:`Package`

        """
        return PackageHelper.search_pypi(name=name)

    @classmethod
    def get_package(cls, name: str):
        """
         Search PyPi package repository for a package by name, only return the package if the name matches exactly

         See Also
               `pip uninstall`: https://pip.pypa.io/en/stable/reference/pip_search

         Args:
             name(:obj:`str`, required): package name


         Returns:
             obj:`Package`

         """
        return PackageHelper.get_pypi(name=name)

    @classmethod
    def is_available(cls, name: str):
        """
        Returns True/False if the package is available on PyPi to be installed

       See Also
            :method:`Pipy.get_package`
            `pip search`: https://pip.pypa.io/en/stable/reference/pip_search

       Args:
           name(:obj:`str`, required): package name

       Returns:
           obj:`bool`: True if the package is available on PyPi

       """
        pkg = PackageHelper.get_pypi(name=name)
        if pkg is not None:
            return pkg
        return None

    @classmethod
    def is_installed(cls, name: str):
        """
        Returns True/False if the package is installed

       See Also
            :method:`Pipy.get_package`

       Args:
           name(:obj:`str`, required): package name

       Returns:
           obj:`bool`: True if the package is installed

       """
        pkg = cls.get_package(name=name)
        if pkg is not None and pkg.installed is True:
            return True
        return False
