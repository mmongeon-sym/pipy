import os

import pkgutil
import re

import pkg_resources
from pkg_resources import DistributionNotFound
import importlib
import importlib.util
from .logging import get_logger
from .process import Process
from .dataclass import DataClass

import dataclasses

RE_SEARCH_RESULT = re.compile(
        r'^(?P<name>[A-Za-z0-9\-]+)\s\((?P<version>[.0-9\-A-Za-z]+)\)\s+\-\s(?P<description>.+)$')
RE_SEARCH_RESULT_INSTALLED = re.compile(
        r'^\s*(?P<is_installed>INSTALLED|LATEST)?\:?\s*(?P<version>[^\)\s]+)\s?\(?(?P<is_latest>latest)?\)?$')


class PackageHelper(object):
    log = get_logger()

    @classmethod
    def is_installed(cls, name):
        try:
            pkg = pkg_resources.get_distribution(dist=name)
            if pkg.key is not None and pkg.location is not None:
                if os.path.exists(os.path.join(pkg.location, pkg.key)) is True:
                    return True
        except DistributionNotFound as e:
            return False


    @classmethod
    def search_pypi(cls, name):
        # cls.log.info(f"Searching PyPi for Package({name}) ...")
        args = ['pip', 'search', name]
        cmd = Process(args=args, timeout=30, shell=False)
        cmd.run(raise_exception=True)

        results = []

        result_idx = 0
        for idx, item in enumerate(cmd.stdout_lines):
            matches = RE_SEARCH_RESULT.match(item)
            if matches is not None:
                search_result = matches.groupdict()
                search_result['installed'] = False
                search_result['installed_version'] = None
                search_result['outdated'] = False
                search_result['url'] = cls.get_url(name)
                # search_result['path'] = None
                results.append(search_result)
                result_idx = result_idx + 1
            matches = RE_SEARCH_RESULT_INSTALLED.match(item)
            if matches is not None:
                groups = matches.groupdict()
                if 'is_latest' in groups:
                    # print(results[result_idx])
                    if groups['is_latest'] == 'latest':
                        results[result_idx - 1]['outdated'] = False
                        results[result_idx - 1]['installed_version'] = groups['version']
                if 'is_installed' in groups:
                    # print(results[result_idx])
                    if groups['is_installed'] == 'INSTALLED':
                        results[result_idx - 1]['installed'] = True
                        # results[result_idx - 1]['path'] = cls.get_path(name=name)
                        results[result_idx - 1]['installed_version'] = groups['version']
                    if groups['is_installed'] == 'LATEST':
                        results[result_idx - 1]['installed'] = True
                        results[result_idx - 1]['outdated'] = True
        results = sorted(results, key=lambda k: len(k['name']))
        results = [PyPiPackage(name=result['name'],
                               version=result['version'],
                               installed=result['installed'],
                               installed_version=result['installed_version'],
                               outdated=result['outdated'],
                               description=result['description']
                               ) for result in results]
        # cls.log.info(f"Searching PyPiPackage({name}) returned {len(results)} results")
        return results

    @classmethod
    def get_pypi(cls, name):
        cls.log.info(f"Searching PyPi for Package({name}) ...")
        results = cls.search_pypi(name)
        if results is not None and len(results) > 0:
            for result in results:
                if getattr(result, 'name') == name:
                    cls.log.info(f"Found PyPiPackage({name})({result.version})")
                    return result
        return None

    @classmethod
    def get_package(cls, name):
        pkg = Package(name=name)
        return pkg

    @classmethod
    def get_module(cls, name):
        mod = importlib.util.find_spec(name)
        if mod is not None:
            return mod
        else:
            return None

    @classmethod
    def load_module(cls, name):
        mod = cls.get_module(name=name)
        if name is not None:
            return mod.loader.load_module()
        else:
            return None

    @classmethod
    def get_path(cls, name):
        mod = cls.get_module(name=name)
        if mod is not None:
            return mod.loader.path
        else:
            return None

    @classmethod
    def get_url(cls, name):
        return "https://pypi.org/project/{}/".format(name)

    @classmethod
    def get_dir(cls, name):
        path = cls.get_path(name=name)
        if path is not None:
            return os.path.dirname(path)
        else:
            return None

    @classmethod
    def import_module(cls, name):
        return cls.load_module(name=name)

    @classmethod
    def get_version(cls, name):
        try:
            pkg = pkg_resources.get_distribution(dist=name)
            if pkg.key is not None and pkg.location is not None:
                if os.path.exists(os.path.join(pkg.location, pkg.key)) is True:
                    if pkg is not None:
                        if hasattr(pkg, 'version') and getattr(pkg, 'version') is not None:
                            return getattr(pkg, 'version')
        except DistributionNotFound as e:
            pkg = None
        return None

    @classmethod
    def get_installed_packages(cls):
        packages = []
        for pkg in pkg_resources.working_set:
            packages.append(FrozenPackage(name=pkg.key, version=pkg.version, installed=True))
        return packages

    @classmethod
    def list_packages(cls):
        args = ['pip', 'list', '--format', 'freeze']
        cmd = Process(args=args, timeout=30, shell=False)
        cmd.run(raise_exception=False)
        results = []
        for line in cmd.stdout_lines:
            name, version = line.split("==")
            package = FrozenPackage(name=name, version=version, installed=True)
            results.append(package)
        return results

    @classmethod
    def show_package(cls, name):
        d = {}
        args = ['pip', 'show', name]
        cmd = Process(args=args, timeout=30, shell=False)
        cmd.run(raise_exception=False)
        if cmd.return_code != 0:
            return None

        for l in cmd.stdout_lines:
            splits = l.split(":")
            key = splits[0].strip().replace("-", "_").lower()
            value = "".join(splits[1:]).strip()
            if len(value) == 0:
                value = None
            d[key] = value

        if 'requires' in d and d['requires'] is not None and len(d['requires']) > 0 and d['requires'] is not None:
            if "," in d['requires']:
                d['requires'] = [Package(name=req.strip()) for req in d['requires'].split(",")]
            else:
                d['requires'] = Package(name=d['requires'])
        if 'required_by' in d and d['required_by'] is not None and len(d['required_by']) > 0 and d[
            'required_by'] is not None:
            if "," in d['required_by']:
                d['required_by'] = [Package(name=req.strip()) for req in d['required_by'].split(",")]
            else:
                d['required_by'] = Package(name=d['required_by'])

        p = InstalledPackage(name=d['name'],
                             version=d['version'],
                             summary=d['summary'],
                             author=d['author'],
                             author_email=d['author_email'],
                             installed=True,
                             requires=d['requires'],
                             required_by=d['required_by'],
                             project_url=d['home_page'].replace("http", "https").replace("https//", "https://"),
                             package_url=PackageHelper.get_url(name=d['name'])
                             )

        return p

    @classmethod
    def install_package(cls, name, no_dependencies=True, upgrade=False):
        if isinstance(name, list) or isinstance(name, tuple):
            packages = [Package(name=n) for n in name]
            names_s = ", ".join(name)
        else:
            packages = [Package(name=name)]
            names_s = name
        already_installed_packages = [p for p in packages if p.installed is True]
        not_installed_packages = [p for p in packages if p.installed is False]
        installed_packages = []

        cls.log.info(f"Installing {len(packages)} packages: {names_s}")

        cls.log.info(f"{len(not_installed_packages)} packages will be installed: " + \
                     f"{', '.join(n.name for n in not_installed_packages)}")
        if len(already_installed_packages) > 0:
            cls.log.info(f"{len(already_installed_packages)} packages are already installed: " + \
                         f"{', '.join(n.name for n in already_installed_packages)}")

        for pkg in not_installed_packages:
            name = pkg.name
            pkg = cls.get_pypi(name)
            if pkg is None:
                raise ModuleNotFoundError(f"PyPiPackage({name}) does not exist")
            ### TODO: Re-instate the below code to enable updating existing packages during install
            # if pkg['installed'] is True and pkg['outdated'] is not True:
            #     cls.log.info(f"PyPiPackage({name})({pkg['installed_version']}) is already installed")
            #     return pkg
            # if pkg['outdated'] is True:
            #     cls.log.info(
            #         f"PyPiPackage({name})({pkg['installed_version']}) is installed, but is not the latest version (
            #         {pkg['version']}")
            #     if upgrade is False:
            #         return pkg
            cls.log.info(f"Installing PyPiPackage({name})({pkg.version}) ...")
            args = ['pip', 'install', name]
            if no_dependencies is True:
                args.append('--no-dependencies')
            if upgrade is True:
                args.append('--upgrade')
                args.append('--upgrade-strategy only-if-needed')

            cmd = Process(args=args, timeout=30, shell=False)
            cmd.run(raise_exception=False)
            new_pkg = cls.get_package(name)

            if new_pkg.installed is True:
                pkg['installed'] = True
                pkg['installed_version'] = pkg['version']
                pkg['outdated'] = False
                cls.log.info(f"Installed PyPiPackage({name})({pkg['version']})")
                installed_packages.append(pkg)
            else:
                raise ModuleNotFoundError(f"Failed to install PyPiPackage({name})({pkg['version']}")
        if len(installed_packages) > 0:
            cls.log.info(f"Installed {len(installed_packages)} packages: " + \
                         f"{', '.join(n.name for n in installed_packages)}")
        return installed_packages

    @classmethod
    def uninstall_package(cls, name):
        if isinstance(name, list) or isinstance(name, tuple):
            packages = [Package(name=n) for n in name]
            names_s = ", ".join(name)
        else:
            packages = [Package(name=name)]
            names_s = name
        installed_packages = [p for p in packages if p.installed is True]
        not_installed_packages = [p for p in packages if p.installed is False]

        uninstalled_packages = []

        cls.log.info(f"Preparing to uninstall {len(packages)} packages: {names_s}")
        if len(installed_packages) > 0:
            cls.log.info(f"{len(installed_packages)} packages will be uninstalled:" + \
                         f"{', '.join(n.name for n in installed_packages)}")
        if len(not_installed_packages) > 0:
            cls.log.info(f"{len(not_installed_packages)}/{len(packages)} packages are already uninstalled: " + \
                         f"{', '.join(n.name for n in not_installed_packages)}")
        for pkg in installed_packages:
            name = pkg.name
            cls.log.info(f"Uninstalling Package({name})({pkg.version}) ...")
            args = ['pip', 'uninstall', name, '--yes']
            cmd = Process(args=args, timeout=30, shell=False)
            cmd.run(raise_exception=False)
            new_pkg = cls.get_package(name)
            if new_pkg.installed is False:
                pkg.installed = False
                pkg.version = cmd.stdout_lines[-1].split(" ")[-1].split("-")[-1]
                cls.log.info(f"Uninstalled Package({name})({pkg.version})")
                uninstalled_packages.append(pkg)
            else:
                raise ModuleNotFoundError(f"Failed to uninstall Package({name})")
        if len(uninstalled_packages) > 0:
            cls.log.info(
                f"Uninstalled {len(uninstalled_packages)} packages: {', '.join(n.name for n in uninstalled_packages)}")

        return uninstalled_packages


class PackageClassMethods(object):
    """
    Class Methods shared by all Package Dataclasses

    Includes helper methods to install, uninstall, and reference the PyPi version of the package.

    Methods
        install(no_dependencies): Install a package
        uninstall(): Uninstall a package
        pypi(): Search PyPi for the package and return it's information, if found.

    Usage
        # Create a new class :obj:`Package` which inherits :obj:`PackageClassMethods`
        class Package(PackageClassMethods)

    Notes
        This class can only be inherited by another class, the methods will not work on their own without a parent
        object with a `name` attribute


    References
        :obj:`PackageHelper.install_package`
        :obj:`PackageHelper.uninstall_package`
        :obj: `PackageHelper.get_pypi`


    """
    name = NotImplementedError

    def install(self, no_dependencies: bool = True):
        """
        Install a package

        Executes 'pip install`, will not upgrade or install (overwrite) a package if already installed

        Args:
            no_dependencies (:obj: `bool`, optional): If True, execute `pip install` with `--no-dependencies`.
                Defaults to True.

        Returns:
            `obj`: Package(installed=True)

        Usage:
            pkg = Package(name='boxsdk')
            pkg.install()

        """
        return PackageHelper.install_package(name=self.name, no_dependencies=no_dependencies)

    def uninstall(self):
        """
        Uninstall a package

        Executes 'pip uninstall --yes`

        Returns:
            `obj`: Package(installed=True)

        Usage:
            pkg = Package(name='boxsdk')
            pkg.uninstall()
        """
        return PackageHelper.uninstall_package(name=self.name)

    def pypi(self):
        """
        Search PyPi for the package and return it's information, if found.

        Returns:
            `obj`: PyPiPackage: if package is available on PyPi

        Usage:
            pkg = Package(name='boxsdk')
            pkg.pypi()

        """
        return PackageHelper.get_pypi(name=self.name)


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Package(PackageClassMethods, DataClass):
    """
    Dataclass representing any Package.

    This class does not make any prior assumptions if the package is installed or where the package was installed from.

    A new instance of :obj:`Package` can be initialized with the `name` of the package

    Parameters
        name(:obj:`str`, required): Package name

    Attributes
        installed(:obj:`bool`): Returns :obj:`True` if the package is installed, else returns :obj:`False`
        version(:obj:`str`): Returns :obj:`str` containg the version of the package (if installed)

    References
        `obj`: PackageClassMethods
        `obj`: DataClass
        `obj`: dataclasses.dataclass

    Methods
        install(no_dependencies): Install a package
        uninstall(): Uninstall a package
        pypi(): Search PyPi for the package and return it's information, if found.


    Usage
        # A new instance of :obj:`Package` can be initialized with the `name` of the package

        pkg = Package(name='boxsdk')
        str(pkg) # Package(name='boxsdk', installed=True, version='2.7.1')
        pkg.installed # True/False
        pkg.version # 2.7.1

    """
    name: str = dataclasses.field(init=True)
    installed: bool = dataclasses.field(init=False, default=None)
    version: str = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        self.__init_typecheck__()
        if self.installed is None:
            self.installed = PackageHelper.is_installed(name=self.name)
        if self.version is None:
            self.version = PackageHelper.get_version(name=self.name)
        self.__post_init_typecheck__(allow_none=True)


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class FrozenPackage(PackageClassMethods, DataClass):
    """
    Dataclass which represents the results of `pip show`, `pip freeze` or other methods of returning installed packages

    Parameters
        name(:obj:`str`, required): Package name
        installed(:obj:`bool`, required): True if installed, else False
        version(:obj:`str`, required): Installed package name

    References
        `obj`: PackageClassMethods
        `obj`: DataClass
        `obj`: dataclasses.dataclass

    Methods
        install(no_dependencies): Install a package
        uninstall(): Uninstall a package
        pypi(): Search PyPi for the package and return it's information, if found.

    Usage
        pkg = FrozenPackage(name='boxsdk', installed=True, version='2.7.1')
        str(pkg) # FrozenPackage(name='boxsdk', installed=True, version='2.7.1')
        pkg.installed # True/False
        pkg.version # 2.7.1

    Warnings
        A new instance of :obj:`FrozenPackage` should not be created by the user. This class is used by methods which
        return installed packages.

    """
    name: str = dataclasses.field(init=True)
    installed: bool = dataclasses.field(init=True)
    version: str = dataclasses.field(init=True)

    def __post_init__(self):
        self.__init_typecheck__()
        if self.installed is None:
            self.installed = PackageHelper.is_installed(name=self.name)
        self.__post_init_typecheck__(allow_none=True)


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class PyPiPackage(PackageClassMethods, DataClass):
    """
    Dataclass which represents a package available on PyPi

    Represents the results returned from `pip search`

    Parameters
        name(:obj:`str`, required): Package name
        installed(:obj:`bool`, required): True if installed, else False
        version(:obj:`str`, required): Version number available on PyPi
        installed_version(:obj:`str`, required): Installed package version number
        outdated(:obj:`bool`, required): Returns True if there is an update available on PyPi
        description(:obj:`str`, required): Description of the package as provided by PyPi

    References
        `obj`: PackageClassMethods
        `obj`: DataClass
        `obj`: dataclasses.dataclass

    Methods
        install(no_dependencies): Install a package
        uninstall(): Uninstall a package
        pypi(): Search PyPi for the package and return it's information, if found.

    Attributes
        url(:obj:`str`): PyPi URL of the package

    See Also
        :obj:`PackageHelper.get_pyi`
        :obj: `PackageHelper.search_pypi`

    Warnings
        A new instance of :obj:`PyPiPackage` should not be created by the user. Instances of this class are returned
        by methods which return packages only found on PyPi

    """
    name: str = dataclasses.field(init=True)
    installed: bool = dataclasses.field(init=True)
    version: str = dataclasses.field(init=True)
    installed_version: str = dataclasses.field(init=True, default=None)
    outdated: bool = dataclasses.field(init=True, default=None)
    description: str = dataclasses.field(default=None, init=True)
    url: str = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        self.__init_typecheck__(allow_none=True)
        if self.url is None:
            self.url = PackageHelper.get_url(name=self.name)
        self.__post_init_typecheck__(allow_none=True)


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class InstalledPackage(PackageClassMethods, DataClass):
    """
    Dataclass which represents an installed package

    Represents the results returned from `pip show`

    Parameters
        name(:obj:`str`, required): Package name
        installed(:obj:`bool`, required): True if installed, else False
        version(:obj:`str`, required): Version number available on PyPi
        summary(:obj:`str`, required): Summary of the package as provided by PyPi
        author(:obj:`str`, required): Name of the package author as provided by PyPi
        author_email(:obj:`str`, required): Email of the package author as provided by PyPi
        package_url(:obj:`str`, required): PyPi URL of the package
        project_url(:obj:`str`, required): URL of the project's homepage or source code, ex. Github
        requires(:obj:`list`, required): List of :obj:`Package` dependencies which are required by this package
        required_by(:obj:`list`, required): List of :obj:`Package` where this package is a dependency of another project

    References
        `obj`: PackageClassMethods
        `obj`: DataClass
        `obj`: dataclasses.dataclass

    Methods
        install(no_dependencies): Install a package
        uninstall(): Uninstall a package
        pypi(): Search PyPi for the package and return it's information, if found.

    Attributes
        url(:obj:`str`): PyPi URL of the package

    See Also
        :obj:`PackageHelper.show_package`

    Warnings
        A new instance of :obj:`InstalledPackage` should not be created by the user.
        Instances of this class are returned by methods which return installed packages
    """
    name: str = dataclasses.field(init=True)
    installed: bool = dataclasses.field(init=True)
    version: str = dataclasses.field(init=True)
    summary: str = dataclasses.field(init=True)
    author: str = dataclasses.field(init=True)
    author_email: str = dataclasses.field(init=True)
    package_url: str = dataclasses.field(init=True, default=None)
    project_url: str = dataclasses.field(init=True, default=None)

    requires: list = dataclasses.field(init=True, default=None)
    required_by: list = dataclasses.field(init=True, default=None)

    def __post_init__(self):
        self.__init_typecheck__(allow_none=True)
        self.__post_init_typecheck__(allow_none=True)
