Using [Codeforces Problem 198A problem] as an example.

Suppose your source code is named `A.{lang}`, which `{lang}` could be
cpp, c, java or py for the current version.

First, copy the sample tests section into file A.cf.

    input
    3 1 3 5
    output
    2
    input
    1 4 4 7
    output
    3
    input
    2 2 4 100
    output
    0

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

This tool is only verifiid on Linux now, but I think it cound be run on
other platforms, although maybe need a little modify.

Please feel free to fork and any suggesions are welcome.

[Codeforces Problem 198A problem]: http://codeforces.com/problemset/problem/198/A
