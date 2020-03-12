import pkg_resources
import subprocess
import os
from pkg_resources import DistributionNotFound
import locale



##### The below code is to be copy and pasted into a python shell to install 'pipy' without using pip

def package_is_installed(name: str):
    try:
        pkg = pkg_resources.get_distribution(dist=name)
        if pkg.key is not None and pkg.location is not None:
            if os.path.exists(os.path.join(pkg.location, pkg.key)) is True:
                return True
    except DistributionNotFound as e:
        return False
    return False


def uninstall_package(name: str):
    args = ['pip', 'uninstall', name, '--yes']
    if package_is_installed(name) is True:
        print(f"Uninstalling package: {name}")
        proc = subprocess.Popen(args,
                                bufsize=-1,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=True,
                                shell=False,
                                startupinfo=None,
                                creationflags=0,
                                restore_signals=True,
                                start_new_session=False,
                                encoding=locale.getpreferredencoding()
                                )
        stdout, stderr = proc.communicate(input=None)
        if package_is_installed(name) is True:
            print(f"Failed to uninstall: {name}")
            print(f"[{' '.join(args)}] STDERR: {stderr}")
            print(f"[{' '.join(args)}] STDOUT: {stdout}")
        else:
            print(f"Successfully uninstalled: {name}")
        return stdout, stderr


def install_package_from_url(name: str,
                             url: str
                             ):
    args = ['pip', 'install', url, '--no-cache-dir', '--no-dependencies']
    if package_is_installed(name) is False:
        print(f"Installing '{name}' from url: {url}")
        proc = subprocess.Popen(args,
                                bufsize=-1,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=True,
                                shell=False,
                                startupinfo=None,
                                creationflags=0,
                                restore_signals=True,
                                start_new_session=False,
                                encoding=locale.getpreferredencoding()
                                )
        stdout, stderr = proc.communicate(input=None)
        if package_is_installed(name) is False:
            print(f"Failed to install: {name}")
            print(f"[{' '.join(args)}] STDERR:  {stderr}")
            print(f"[{' '.join(args)}] STDOUT: {stdout}")
        else:
            print(f"Successfully installed: {name}")
    else:
        print(f"Package is already installed: {name}")


# uninstall_package(name='pipy')
install_package_from_url(name='pipy',
                         url='https://github.com/mmongeon-sym/pipy/releases/latest/download/pipy.tar.gz'
                         )
