# Copyright 2023 Ashley R. Thomas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import time
import atexit
if os.name == "posix":
    import fcntl

from .exception import LockError, InvalidStateError

class ProcessFileLock:
    """This is a simple per-process file-based lock. This class only uses Python
    functions and libraries, achieving its goals using two different approaches
    depending on whether the OS is Windows or Linux...

    On Windows, file existence is used to determine if a lock is held. This
    is achieved using the "x+" mode which fails if a file already exists. This
    works in combination with using os.unlink to attempt to delete the file
    which, on Windows, will fail if the file is truly open and held, and is not
    an orphaned lock file.

    On Linux, the fcntl.lockf API is supported so true non-blocking locking
    can be used. Since Linux allows processes to delete or overwrite files
    opened non-exclusively by other processes, the lock files are opened
    with "a+" after which fcntl.lockf is used to acquire an fnctl process
    lock which, if successful, means the lock acquire was successful, else
    it means some other process is holding the lock.

    Each instance of this class should be considered single-threaded, and each
    lock file guards a resource against multiprocess access, not multiple threads
    within the same process.

    For both Windows and Linux, the pid of the process holding the lock is
    written to the lock file for diagnostic purposes only, not as a requirement
    for this class. Given latency from time of successful acquire to the pid
    of the acquiring process being written, the pid within the lock file may
    reflect a past owner.
    """

    DEFAULT_FILE_NAME = ".simple_file_lock"

    def __init__(self, filename = DEFAULT_FILE_NAME, diag_name = "") -> None:
        self._diag_name = diag_name
        self._filename = os.path.abspath(filename)
        os.makedirs(name=os.path.dirname(self._filename), exist_ok=True)
        self._file = None
        atexit.register(self.release)
        pass

    @property
    def is_lock_held(self):
        return self._file is not None

    def acquire(self, timeout_seconds = 0):
        if timeout_seconds < 0:
            raise ValueError(f"timeout_seconds must be 0 or greater seconds.")
        while True:
            try:
                if os.name == "nt":
                    self._acquire_windows()
                elif os.name == "posix":
                    self._acquire_posix()
                else:
                    raise InvalidStateError(message=f"Unexpected os: {os.name}")
                return self
            except LockError:
                if timeout_seconds == 0:
                    raise
                wait_seconds_now = min(timeout_seconds, 0.050)
                time.sleep(wait_seconds_now)
                timeout_seconds = timeout_seconds - wait_seconds_now

    def release(self):
        if os.name == "nt":
            self._release_windows()
        elif os.name == "posix":
            self._release_posix()
        else:
            raise InvalidStateError(message=f"Unexpected os: {os.name}")

    def _get_pid_str(self):
        pid_str = "<not_found>"
        try:
            with open(self._filename, "a+") as f:
                f.seek(0)
                pid_str = f.read(20)
        except Exception:
            pass
        return pid_str

    def _write_pid_str(self):
        self._file.seek(0)
        self._file.truncate()
        self._file.write(str(os.getpid()))
        self._file.flush()

    def _get_lock_acquire_failure_error_message(self):
        return (
            f"SimpleFileLock cannot acquire the lock. "
            f"The process last holding the lock was '{self._get_pid_str()}'. "
            f"The lock file is '{os.path.abspath(self._filename)}'."
        )

    def _acquire_windows(self):
        if self._file is not None:
            return

        #
        # First attempt:
        #
        try:
            self._file = open(self._filename, "x+")
            # Lock held here, the point where the file exists.
        except FileExistsError as ex:
            try:
                # See if old lock file was orphaned.
                os.unlink(self._filename)
            except Exception:
                pass

        #
        # Second attempt, if applicable:
        #
        try:
            # If the above open failed, try again.
            if self._file is None:
                self._file = open(self._filename, "x+")
                # Lock held here, the point where the file exists.
        except FileExistsError as ex:
            raise LockError(
                message=self._get_lock_acquire_failure_error_message(),
                cause=self._diag_name,
            ).with_traceback(ex.__traceback__) from ex

        #
        # Success, write this process's pid to the file (for diag purposes as needed).
        #
        try:
            self._write_pid_str()
        except Exception:
            try:
                self._file.close()
            except Exception:
                pass
            self._file = None
            raise

    def _release_windows(self):
        if self._file is None:
            return
        self._file.close()
        self._file = None
        try:
            os.unlink(self._filename)
        except Exception:
            pass
        # Unlocked here, the point where the file no longer exists.

    def _acquire_posix(self):
        self._file = open(self._filename, "a+")
        try:
            fcntl.lockf(self._file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Lock held here, the point where the file exists.
            self._write_pid_str()
        except BlockingIOError as ex:
            self._file.close()
            self._file = None
            raise LockError(
                message=self._get_lock_acquire_failure_error_message(),
                cause=self._diag_name,
            ).with_traceback(ex.__traceback__) from ex

    def _release_posix(self):
        if self._file is None:
            return
        fcntl.lockf(self._file, fcntl.LOCK_UN)
        self._file.close()
        self._file = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return False
