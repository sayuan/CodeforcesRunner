# Installation
The library `lxml` is needed.  Please reference
[here](http://lxml.de/installation.html) for more information.

If you are an Debian/Ubuntu user, simply type:

    $ sudo apt-get install python-lxml

# Usage
Using [Codeforces Problem 198A problem
](http://codeforces.com/problemset/problem/198/A) as an example.

## Donwload Sample Tests
The url of this problem is
<http://codeforces.com/problemset/problem/198/A>.  Please notice the
**contest_id** is **198** and the **problem_id** is **A**.

    $ cf.py -c 198 -p A     # download this problem
    $ cf.py -c 198          # download all problems in this contest

There is another url <http://codeforces.com/contest/198/problem/A> which
indicated the same problem.  You can see the contest_id and problem_id
is same, so it wouldn't be a problem.

## Running the Tests
Suppose your source code is named `A.{lang}`, which `{lang}` could be
`cpp`, `c`, `java` or `py` for the current version.

Then, simple run `cf.py A.{lang}`, you will get the result like this:

    $ cf.py A.java
    output:
    2
    === Case #1: AC (85 ms) ===

    output:
    2
    answer:
    3
    === Case #2: WA (83 ms) ===

    press enter to continue or <C-c> to leave.
    output:
    Exception in thread "main" java.lang.Exception
            at A.<init>(A.java:12)
            at A.main(A.java:18)
    answer:
    0
    === Case #3: RE (95 ms) ===

    press enter to continue or <C-c> to leave.

## Configurations
The file `cf.conf' contains the compile & execute commands of support
languages, so you could add more commands to support more languages
easily by yourself.

The section [global] in `cf.conf` contains some setting about the *test
file*'s name.  Since the *source code*'s name and the *test file*'s name
must be exactly same, you could change these settings to follow your
naming convension.  For example:

In the default setting:

    filename_pattern = upper({id})
    replace_space = _
    test_extension = .xml

the filename would be 'A.xml'

Or you could added the *contest id* and *problem's name*: (also notice the
`replace_space`)

    filename_pattern = {contest}-upper({id})-lower({name})
    replace_space = -
    test_extension = .xml

the filename would be 'A-about-bacteria.xml'

# About
This tool is only verifiid on Linux now, but I think it could be run on
other platforms, although it maybe need a little modify.

Please feel free to fork and any suggesions are welcome.
