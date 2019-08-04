#!/usr/bin/env python3
"""Generate a theia-compatible launch.json with targets for each test.

The JSON produced by this tool should be written to `.theia/launch.json`.
"""

import glob
import json
import os

PINTOS_HOME = os.getenv("PINTOS_HOME")
PROJECTS = {"filesys": ["filesys/base", "filesys/extended"], "vm": ["vm"]}


def test_format(project, subproject, test):
    """Format a single test's launch target.

    Args:
        project: the pintos module/project. (e.g. filesys)
        subproject: the full subproject. (e.g. filesys/base)
            Usually the same as project.
        test: the name of the test. (e.g. mmap-clean)

    Returns:
        A dictionary with Theia's expected launch target format.
    """
    return {
        "name": f"Debug {subproject} {test}",
        "type": "cppdbg",
        "request": "launch",
        "program": f"{PINTOS_HOME}/pintos/src/{project}/build/kernel.o",
        "args": [],
        "stopAtEntry": False,
        "cwd": f"{PINTOS_HOME}",
        "environment": [],
        "externalConsole": False,
        "MIMode": "gdb",
        "miDebuggerPath": f"{PINTOS_HOME}/pintos/src/utils/pintos-gdb",
        "miDebuggerServerAddress": "localhost:1234",
        "debugServerPath": f"{PINTOS_HOME}/scripts/run_test.py",
        "debugServerArgs": f"--debug {subproject} {test}",
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": True,
            }
        ],
    }


def get_configs():
    """Yields a list of all tests under the given PROJECTS.

    Will build each project if needed; safe to run on a clean checkout.

    Returns:
        A generator of dictionaries that match the `configurations` key of
        `launch.json`.
    """
    for (project, subprojects) in PROJECTS.items():
        os.chdir(f"{PINTOS_HOME}/pintos/src/{project}/")
        os.system("make > /dev/null")
        os.chdir("build")

        tests = []

        for subproject in subprojects:
            tests += [
                (project, subproject, x.split("/")[-1])
                for x in glob.glob(
                    f"{PINTOS_HOME}/pintos/src/{project}/build/tests/{subproject}/*"
                )
                if "." not in x
            ]

        for test in tests:
            yield test_format(*test)


def get_launch():
    """Returns a dictionary ready to serialize to `launch.json`.

    Returns:
        A dictionary matching the `launch.json` spec.
    """
    return {"version": "0.2.0", "configurations": list(get_configs())}


print(json.dumps(get_launch(), indent=4, sort_keys=True))
