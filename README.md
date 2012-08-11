# Installation
The library `lxml` is needed.  Please reference
[here](http://lxml.de/installation.html) for more information.

If you are an Debian/Ubuntu user, simply type:

    $ sudo apt-get install python-lxml

# Usage
Using [Codeforces Problem 198A problem] as an example.

Suppose your source code is named `A.{lang}`, which `{lang}` could be
`cpp`, `c`, `java` or `py` for the current version.

First, download sample tests from the problem page:

    $ cf.py -d http://codeforces.com/problemset/problem/198/A

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

    Or you could added the *problem's name*: (also notice the `replace_space`)
        filename_pattern = upper({id})-lower({name})
        replace_space = -
        test_extension = .xml
    the filename would be 'A-about-bacteria.xml'

This tool is only verifiid on Linux now, but I think it cound be run on
other platforms, although it maybe need a little modify.

Please feel free to fork and any suggesions are welcome.

[Codeforces Problem 198A problem]: http://codeforces.com/problemset/problem/198/A
