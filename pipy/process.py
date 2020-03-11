import locale
import os
import subprocess
from collections import OrderedDict

from .assertions import assert_bool, assert_int, assert_list, assert_str
from .logging import get_logger


class Process(object):

    def __init__(self,
                 args: list,
                 timeout: int = 15,
                 shell: bool = False
                 ):

        self.args = assert_list(value=args, name='args')
        self.args_str = assert_str(value=" ".join(self.args), name='args')
        self.timeout = assert_int(value=timeout, name='timeout')
        self.shell = assert_bool(value=shell, name='shell')
        self.encoding = assert_str(value=locale.getpreferredencoding(), name='encoding')
        self.linesep = assert_str(value=os.linesep, name='linesep')


        self.status_code: int = None
        self.return_code: int = None
        self.pid: int = None
        self.stdin: str = None
        self.stdout: str = None
        self.stderr: str = None
        self.failed = False

        self.keys = ('args',
                     'pid',
                     'timeout',
                     'shell',
                     'encoding',
                     'linesep',
                     'status_code',
                     'return_code',
                     'stdin',
                     'stdout',
                     'stderr',
                     )

        self.log = get_logger()

    def __dict__(self):
        return OrderedDict(zip(self.keys, (
                self.args_str,
                self.pid,
                self.timeout,
                self.shell,
                self.encoding,
                self.linesep,
                self.status_code,
                self.return_code,
                self.stdin,
                self.stdout,
                self.stderr
                )))

    @property
    def _log_base(self):
        return "[Command({CMD})]".format(CMD=self.args_str, PID=self.pid)

    @property
    def stdout_lines(self):
        if self.stdout is not None:
            lines = [str(line).strip() for line in self.stdout.splitlines()]
            return lines

    def build_log_str(self, msg: str, name: str = None):
        if name is not None:
            return "{LOG_BASE}[{NAME}]: {MSG}".format(LOG_BASE=self._log_base, NAME=name, MSG=msg)
        else:
            return "{LOG_BASE}: {MSG}".format(LOG_BASE=self._log_base, MSG=msg)

    def p_open(self):
        try:
            proc = subprocess.Popen(args=self.args,
                                    bufsize=-1,
                                    executable=None,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    close_fds=True,
                                    shell=self.shell,
                                    cwd=None,
                                    env=None,
                                    universal_newlines=False,
                                    startupinfo=None,
                                    creationflags=0,
                                    restore_signals=True,
                                    start_new_session=False,
                                    encoding=self.encoding,
                                    errors=None
                                    )
            return proc
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                self.log.error(self.build_log_str(msg="Command not found: {CMD}".format(CMD=" ".join(self.args),
                                                                                        name=None)))

                raise e

    def run(self, stdin: str = None, raise_exception: bool = True):
        self.stdin = assert_str(stdin, name='stdin', allow_none=True)
        proc = self.p_open()
        stdout, stderr = self.communicate(proc=proc, stdin=stdin, raise_exception=raise_exception)
        return stdout, stderr

    def communicate(self, proc, stdin=None, raise_exception: bool = True):
        try:
            stdout, stderr = proc.communicate(input=stdin, timeout=self.timeout)
            self.pid = proc.pid
            self.status_code = proc.poll()
            self.return_code = proc.returncode
            if stderr is not None:
                self.stderr = stderr

            if stdout is not None:
                self.stdout = stdout
            if self.return_code is None:
                self.return_code = 1
                self.failed = True
            if isinstance(self.return_code, int) and self.return_code > 0 or self.return_code < 0:
                self.failed = True
                if raise_exception is True:
                    self.log.error(self.build_log_str(
                            msg="Exited with non-zero status {STATUS}: {STDERR}".format(STATUS=self.return_code,
                                                                                        NEWLINE=self.linesep,
                                                                                        STDERR=self.stderr),
                            name='STDOUT')
                            )
                    raise subprocess.CalledProcessError(returncode=self.return_code,
                                                        cmd=self.args,
                                                        output=self.stdout,
                                                        stderr=self.stderr)

            return stdout, stderr

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                self.log.error(self.build_log_str("Command not found: {CMD}".format(CMD=" ".join(proc.args))))
            if isinstance(e, subprocess.TimeoutExpired):
                self.status_code = proc.poll()
                proc.kill()
                self.return_code = proc.returncode
                self.log.error(self.build_log_str(msg="Timeout after {TIMEOUT}s with {RETURN_CODE} status".format(
                        TIMEOUT=self.timeout,
                        RETURN_CODE=self.return_code
                        ),

                        ))
            if isinstance(e, subprocess.SubprocessError):
                self.status_code = proc.poll()
                self.return_code = proc.returncode
                self.log.error(
                        self.build_log_str("Exited with status: {RETURN_CODE}".format(RETURN_CODE=self.return_code)))
            raise e
        finally:
            pass
