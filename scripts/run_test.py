#!/usr/bin/env python3
"""Runs the given PintOS tests and optionally starts a GDB server.

To run all tests under filesys/base:

    run_test.py filesys/base *

To start debugging the mmap-clean test of the vm module:

    run_test.py --debug vm mmap-clean
"""

import os
import sys
import glob
import subprocess
import re


def list_tests(exp):
    """Lists tests matching a the given expression.

    Args:
        exp: the name of one test or a glob matching multiple tests.

    Returns:
        A list of matching test names.

    Raises:
        SyntaxError: Wildcards are blocked while debugging to avoid hangs.
    """
    if "*" in exp:
        if DEBUG:
            raise SyntaxError("Wildcards not allowed when debugging")
        return [
            x.split("/")[-1]
            for x in glob.glob(
                f"{PINTOS_HOME}/pintos/src/{MODULE}/build/tests/{TESTMODULE}/{exp}"
            )
            if "." not in x
        ]

    return [exp]


def extract_putfiles(test):
    """Formats PintOS arguments for a given test target's putfiles.

    Certain PintOS test targets expect one or more files to be present before
    execution. This function extracts the files and paths from the matching
    makefile target and formats them as PintOS arguments.

    Args:
        test: the name of a test target.

    Returns:
        A list of arguments to be passed to the `pintos` command.
    """
    extracted = []
    with open(f"{PINTOS_HOME}/pintos/src/tests/{TESTMODULE}/Make.tests") as makefile:
        for line in makefile:
            if line.startswith(f"/tests/{TESTMODULE}/{test}_PUTFILES ="):
                (_, files) = line.split("=")
                for filepath in files.split(" "):
                    extracted += [
                        "-p",
                        f"{PINTOS_HOME}/pintos/src/{filepath}",
                        "-a",
                        filepath.split("/")[-1],
                    ]

    return extracted


def run_test(test, debug=False):
    """Run a specific test.

    Args:
        test: the name of the test to run.
        debug: if False, the test is run and output is captured.
            if True, the test is launched as a debug server and output is not
            redirected.

    Returns:
        A subprocess.CompletedProcess object.
    """
    args = (
        [
            "-v",
            "-k",
            "-T",
            "60",
            "--qemu",
            "--filesys-size=2",
            "-p",
            f"{PINTOS_HOME}/pintos/src/{MODULE}/build/tests/{TESTMODULE}/{test}",
            "-a",
            f"{test}",
        ]
        + extract_putfiles(test)
        + ["--swap-size=4", "--", "-q", "-f", "run", f"{test}"]
    )

    if debug:
        args = ["--gdb"] + args

    if DEBUG:
        return subprocess.run([PINTOS] + args, capture_output=False)
    else:
        proc = subprocess.run([PINTOS] + args, capture_output=True)
        print(proc.stdout.decode("utf-8"))
        return proc


def run_all_tests(tests, debug=False):
    """Run all given tests, reprinting their status at the end.

    Args:
        tests: a list of test names to run.
    """
    for testname in tests:
        result = run_test(testname, debug)
        if not DEBUG:
            output = result.stdout.decode("utf-8")
            for line in output.split("\n"):
                match = re.match(f"^{testname}: exit\\((\\d+)\\)$", line)
                if match:
                    exit_code = int(match.groups()[0])
                    if exit_code != 0:
                        print(f"{testname}: FAILED({exit_code})")
                    else:
                        print(f"{testname}: PASSED")


if __name__ == "__main__":
    ARG_INDEX = 0

    if sys.argv[1] == "--debug":
        DEBUG = True
        ARG_INDEX = 1
    else:
        DEBUG = False

    PINTOS_HOME = os.getenv("PINTOS_HOME")
    PINTOS = f"{PINTOS_HOME}/pintos/src/utils/pintos"

    TESTMODULE = MODULE = sys.argv[1 + ARG_INDEX]
    if "/" in MODULE:
        MODULE = sys.argv[1 + ARG_INDEX].split("/")[0]

    # Ensure that the tests have been built
    os.chdir(f"{PINTOS_HOME}/pintos/src/{MODULE}/")
    os.system("make > /dev/null")
    os.chdir("build")

    TESTS = list_tests(sys.argv[2 + ARG_INDEX])
    run_all_tests(TESTS, DEBUG)
