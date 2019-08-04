# Pintos project 3/4 core

## Overview

These projects require you to work as a group and implement a significant
feature in pintos. This will be a significantly larger challenge than the
previous assignments; this is why I have allocated one hour per week per group.

You can consider me, during that hour, as a _fourth team member_, with some
restrictions:

1. I will not write new code for you, but...
   - I will add comments.
   - I will help debug and automate.
   - I will help detangle `git` issues such as merges and bad commits.
2. I will make suggestions to the best of my memory but will not cheat and look
   at complete implementations.
   - This means I might give **bad advice** by accident!
   - If I do so, your group will still need to implement the right thing
     instead - just as if any other group member had a bad idea. :)
   - If you need a canonically correct answer, open an issue and assign it to
     me.
3. I will give approximate progress estimates and suggestions as to what to
   implement next.
4. I will open issues when I discover bugs (might happen outside of office
   hours, too.)
5. I will _never_ intentionally mislead, misdirect, or lie.
   - If I'm not certain of an answer, I will do my best to make that uncertainty
     clear.

## Getting Started

### Assumptions

This guide assumes you have downloaded the correct VM from the course website;
see https://course.ccs.neu.edu/cs5600f18/pintos/vm-setup.html.

These projects _might_ work under WSL or more modern versions of Linux.

### Setup

1. Run `update_path.sh` to add `PINTOS_HOME` to your shell's configuration and
   its utilities directory to your `$PATH`.
   - Restart your shell (or terminal) after this.
   - **You must run `update_path.sh` every time you move your repository.**
   - Note that multiple copies of Pintos can't coexist at this time; you can
     either use multiple VMs or update your `$PINTOS_HOME` to match your current
     project; you might find https://direnv.net/ helpful in automatically
     managing this.
   - When in doubt, start a new shell and run `update_path.sh`; it will tell you
     if it made any changes and what to do.
2. `sudo apt-get -y install qemu` to install QEMU.

### Running a single test

If any of these steps fail completely, check that `echo $PINTOS_HOME` returns
the path to your pintos repository and that QEMU is installed. Error 255 tends
to indicate catastrophic failure - QEMU is not installed - and error 127
indicates configuration failure - `pintos` is not on your `$PATH`.

```bash
cd $PINTOS_HOME/pintos/src/vm
make
cd build
make tests/vm/mmap-clean.result
```

After some time, you should see the following output:

```
FAIL tests/vm/mmap-clean
Test output failed to match any acceptable form.

Acceptable output:
  (mmap-clean) begin
  (mmap-clean) open "sample.txt"
  (mmap-clean) mmap "sample.txt"
  (mmap-clean) write "sample.txt"
  (mmap-clean) munmap "sample.txt"
  (mmap-clean) seek "sample.txt"
  (mmap-clean) read "sample.txt"
  (mmap-clean) file change was retained after munmap
  (mmap-clean) end
Differences in `diff -u' format:
  (mmap-clean) begin
  (mmap-clean) open "sample.txt"
  (mmap-clean) mmap "sample.txt"
- (mmap-clean) write "sample.txt"
- (mmap-clean) munmap "sample.txt"
- (mmap-clean) seek "sample.txt"
- (mmap-clean) read "sample.txt"
- (mmap-clean) file change was retained after munmap
- (mmap-clean) end

(Process exit codes are excluded for matching purposes.)
```

The following files were created by running `tests/vm/mmap-clean.result`:

| Path                                                          | Contents                           |
| ------------------------------------------------------------- | ---------------------------------- |
| `$PINTOS_HOME/pintos/src/vm/build/tests/vm/mmap-clean.output` | Raw test output                    |
| `$PINTOS_HOME/pintos/src/vm/build/tests/vm/mmap-clean.errors` | All errors encountered             |
| `$PINTOS_HOME/pintos/src/vm/build/tests/vm/mmap-clean.result` | Test result (usually FAIL or PASS) |

Note that running `make tests/vm/mmap-clean.result` will do nothing if these
files exist.

It's possible to run a test directly without generating any files or performing
any checks:

`pintos --qemu -k -T 60 -- -q run mmap-clean`

Note that this command **will not** (re)build any test files or libraries.

Note also that `make clean` will remove **all** built files and results. (This
might be more removal than you want.)

### Running all of the tests

**This will take some time, especially for the `thread` project!**

```
cd $PINTOS_HOME/pintos/src/vm
make
cd build
make check # builds and runs _all_ tests in vm
```

## Project 3

Project 3 requires you to implement a virtual memory management system including
support for memory mapped files.

### Errata

1. This repository contains a working "project 2" implementation; ignore
   references that say you will need a working "project 2" implementation.
2. Memory mapping the same file twice must use the same physical memory for full
   credit.
3. The "extra credit" is not extra credit but will be worth approximately 3 out
   of 100 points.
4. The design document template link in the assignment details is broken; use
   [this project 3 design document link](https://course.ccs.neu.edu/cs5600f18/assignments/dd.txt)
   instead.
5. As with all projects in this class, you may use any coding style you like _so
   long as it is consistent within your group_.
   - **IF YOU WANT TO REFORMAT AN EXISTING FILE, FIRST COMMIT THE REFORMAT AND
     THEN COMMIT YOUR CHANGES.**
   - Every commit that mixes formatting with a non-formatting change **will
     result in a 1-point deduction per file**.
   - If you have made a bad commit and need help breaking it up, push it to a
     **new** branch and contact me. (Note that I will expect you to either stop
     making bad commits or learn how to break them apart yourself after the
     first time. :)

### Assignment

**READ THE ERRATA BEFORE READING THE ASSIGNMENT DETAILS.**

Refer to the
[project 3 assignment details](http://www.ccs.neu.edu/home/skotthe/classes/cs5600/fall/2015/pintos/doc/pintos_4.html).

## Project 4

Project 4 requires you to improve the existing pintos filesystem. It does not
require project 3. Specifically, you will add indexed/extensible files,
subdirectories, and a buffer cache to the existing filesystem.

### Errata

1. This repository contains a working "project 2" implementation; ignore
   references that say you will need a working "project 2 or 3" implementation.
2. The design document template link in the assignment details is broken; use
   [this project 4 design document link](https://course.ccs.neu.edu/cs5600f18/assignments/filesys.txt)
   instead.
3. As with all projects in this class, you may use any coding style you like _so
   long as it is consistent within your group_.
   - **IF YOU WANT TO REFORMAT AN EXISTING FILE, FIRST COMMIT THE REFORMAT AND
     THEN COMMIT YOUR CHANGES.**
   - Every commit that mixes formatting with a non-formatting change **will
     result in a 1-point deduction per file**.
   - If you have made a bad commit and need help breaking it up, push it to a
     **new** branch and contact me. (Note that I will expect you to either stop
     making bad commits or learn how to break them apart yourself after the
     first time. :)

### Assignment

**READ THE ERRATA BEFORE READING THE ASSIGNMENT DETAILS.**

Refer to the
[project 4 assignment details](http://www.ccs.neu.edu/home/skotthe/classes/cs5600/fall/2015/pintos/doc/pintos_5.html).

## Difficulty

Project 4 requires roughly twice as many lines of code as project 3 but is
conceptually easier to work on and debug. Furthermore, project 4 is easier to
divide into independent parts. Your group may elect to do _one_ project. Once it
is _completed_, your group may choose to complete the other project _with my
permission_.

Partially completing projects 3 and 4 will result in me applying the highest
single grade from _one_ of the projects. (e.g. 75/100 on project 3 and 60/100 on
project 4 would mean I discard project 4; your class project grade is now the
average of projects 1, 2, and 3.)

These projects must be worked on as a group. If two group members complete
project 3 and one member completes project 4, those two members will receive a
grade for project 3 and the other member will receive a grade for project 4. All
three members should expect to lose some of their 5 "instructor discretion"
points for ignoring the assignment. :)

Rewards for completing both projects _as a group_ TBD; I do not expect any group
to be able to complete both to a satisfactory (80/100 or higher) standard in the
remaining time and do not want to encourage the level of overwork required to do
so!

## Grading (common to project 3 and 4)

100 total points:

- Design document (30 points)
  - Design document is complete (covers all changes made)
  - Design document is accurate (descriptions match source code)
  - Design document arguments are appropriate and rational
- Function (50 points)
  - Relevant tests (vm or filesys depending on project) pass
  - Existing tests (outside of vm or filesys) do not regress (if they passed
    before, they should still pass!)
  - All functionality in assignment details is implemented
- Style (20 points)
  - Code style _is documented_; a `.clang-format` file suffices
  - Code style _is comprehensive_; a style of "no lines longer than 80" is not
    enough
  - Code style is consistent for all added code
  - **Note the errata sections above!**

This project's grading is significantly less rigid than previous assignments.
The use of office hours to clarify and check in is _highly encouraged and
expected_.
