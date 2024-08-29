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

# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=unused-import
# pylint: disable=wrong-import-position

import os
import random
import time
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Barrier, Value

from pytest import LogCaptureFixture, CaptureFixture, fail, raises

from atbu.common.exception import (
    LockError
)
from atbu.common.process_file_lock import (
    ProcessFileLock,
)

LOGGER = logging.getLogger(__name__)


def setup_module(module):
    pass


def teardown_module(module):
    pass


SUCCESS_CODE = 777
FAILURE_CODE = 111


def expect_acquire_success_func(parent_pid_str):
    try:
        with ProcessFileLock() as l2:
            if not l2.is_lock_held:
                return FAILURE_CODE
        if l2.is_lock_held:
            return FAILURE_CODE
        return SUCCESS_CODE
    except LockError as ex:
        return FAILURE_CODE


def expect_acquire_failure_func(parent_pid_str):
    try:
        with ProcessFileLock() as l2:
            return FAILURE_CODE
    except LockError as ex:
        if ex.message.find(parent_pid_str) == -1:
            return FAILURE_CODE
        return SUCCESS_CODE


g_num = None
g_bar = None
def g_init_func(num, bar):
    global g_num
    global g_bar
    g_num = num
    g_bar = bar


def acquire_inc_dec_loop(lock: ProcessFileLock, test_time_secs):
    g_bar.wait(timeout=10)
    count = 0
    end_time = time.perf_counter() + test_time_secs
    while time.perf_counter() < end_time:
        count +=1
        assert not lock.is_lock_held
        time.sleep(random.uniform(0.01, 0.5))
        with lock.acquire(timeout_seconds=5):
            assert lock.is_lock_held
            with g_num.get_lock():
                g_num.value += 1
            time.sleep(random.uniform(0.01, 0.5))
            assert g_num.value == 1
            with g_num.get_lock():
                g_num.value -= 1
            assert g_num.value == 0
        assert not lock.is_lock_held
    return count


def acquire_inc_dec_value_func(parent_pid_str, test_time_secs):
    l2 = ProcessFileLock()
    num_iters = acquire_inc_dec_loop(
        lock=l2,
        test_time_secs=test_time_secs,
    )
    assert not l2.is_lock_held
    return (SUCCESS_CODE, num_iters)


def test_simple_lock_multiple_processes(tmp_path: Path):

    global g_num
    global g_bar
    g_num = Value("d", 0)
    g_bar = Barrier(2)
    ppe = ProcessPoolExecutor(initializer=g_init_func, initargs=(g_num,g_bar,))

    with ProcessFileLock() as l1:
        assert l1.is_lock_held
    assert not l1.is_lock_held
    future = ppe.submit(expect_acquire_success_func, str(os.getpid()))
    result = future.result()
    assert result == SUCCESS_CODE

    with ProcessFileLock() as l1:
        assert l1.is_lock_held
        future = ppe.submit(expect_acquire_failure_func, str(os.getpid()))
        result = future.result()
        assert result == SUCCESS_CODE
    pass

    TEST_TIME_SECS = 15
    l1 = ProcessFileLock()
    future = ppe.submit(acquire_inc_dec_value_func, str(os.getpid()), TEST_TIME_SECS)
    num_iters = acquire_inc_dec_loop(
        lock=l1,
        test_time_secs=TEST_TIME_SECS,
    )
    result, num_iters_subproc = future.result()
    LOGGER.debug(f"num_iters={num_iters} num_iters_subproc={num_iters_subproc}")

    # This "<n> iteration check" uses an arbitrary value, just ensuring some
    # reasonable number of iterations has occurred.
    assert num_iters > 10
    assert num_iters_subproc > 10

    assert not l1.is_lock_held
    assert result == SUCCESS_CODE
    pass
