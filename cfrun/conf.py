PATTERN = "upper({id})"
REPLACE_SPACE = "_"
EXTENSION = ".xml"
ENV = {
    ".c": {
        "compile": "gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -lm -s -O2 -m32 -o {0} {0}.c",
        "execute": "./{0}",
    },
    ".cpp": {
        "compile": "g++ -static -fno-optimize-sibling-calls -fno-strict-aliasing -lm -s -x c++ -O2 -std=c++11 -D__USE_MINGW_ANSI_STDIO=0 -m32 -o {0} {0}.cpp",
        "execute": "./{0}",
    },
    ".py": {
        "compile": "",
        "execute": "python {0}.py",
    },
    ".java": {
        "compile": "javac -cp '.;*' {0}.java",
        "execute": "java -Djava.security.manager -Djava.security.policy=java.policy -Xmx512M -Xss64M -Duser.language=en -Duser.region=US -Duser.variant=US {0}",
    },
    ".scala": {
        "compile": "fsc -cp '.;*' {0}.scala",
        "execute": "JAVA_OPTS='-Djava.security.policy=java.policy -Xmx512M -Xss64M -Duser.language=en -Duser.region=US -Duser.variant=US' scala {0}",
    },
    ".rb": {
        "compile": "",
        "execute": "ruby {0}.rb",
    },
    ".go": {
        "compile": "go build {0}.go",
        "execute": "./{0}",
    },
    ".hs": {
        "compile": "ghc --make -O -o {0} {0}.hs",
        "execute": "./{0}",
    },
}
