#! /usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import os.path
import sys
import time
import subprocess

class Executer(object):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(id, lang):
        return {
                '.cpp': CppExecuter,
                '.c': CExecuter,
                '.java': JavaExecuter,
                '.py': PythonExecuter,
        }[lang](id)

class CppExecuter(Executer):
    def __init__(self, id): super(CppExecuter, self).__init__(id)
    def compile(self):
       return subprocess.call('g++ -static -fno-optimize-sibling-calls -fno-strict-aliasing -lm -s -x c++ -O2 -o {0} {0}.cpp'.format(self.id), shell=True)
    def run(self):
        return './{0}'.format(self.id)

class CExecuter(Executer):
    def __init__(self, id): super(CExecuter, self).__init__(id)
    def compile(self):
       return subprocess.call('gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -lm -s -O2 -o {0} {0}.c'.format(self.id), shell=True)
    def run(self):
        return './{0}'.format(self.id)

class JavaExecuter(Executer):
    def __init__(self, id): super(JavaExecuter, self).__init__(id)
    def compile(self):
        return subprocess.call('javac -cp \'.;*\' {0}.java'.format(self.id), shell=True)
    def run(self):
        return 'java -Xmx256M -Duser.language=en -Duser.region=US -Duser.variant=US {0}'.format(self.id)

class PythonExecuter(Executer):
    def __init__(self, id): super(PythonExecuter, self).__init__(id)
    def compile(self):
        return 0
    def run(self):
        return 'python -O {0}.py'.format(self.id)

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print 'Source code not exist!'
        sys.exit(1)

    id, lang = os.path.splitext(sys.argv[1])
    executer = Executer.get(id, lang)
    
    ret = executer.compile()

    if ret!=0:
        print '>>> failed to Compile the source code!'
        sys.exit(1)

    input_marks = ('input\n', 'Input\n', 'входные данные\n', 'Ввод\n')
    output_marks = ('output\n', 'Output\n', 'выходные данные\n', 'Ответ\n')

    file = open('{0}.cf'.format(id), 'r');
    case = 1
    input_line = file.readline()
    while True:
        if len(input_line)==0:
            break;

        if input_line.startswith('#'):
            input_line = file.readline();
            while len(input_line) != 0 and not reduce(operator.or_, map(input_line.endswith, input_marks)):
                input_line = file.readline();
            case = case+1
            continue

        if not (input_line in input_marks):
            print '>>> input format error!'
            sys.exit(1)

        input_line = file.readline()

        input=''
        while len(input_line) != 0 and not (input_line in output_marks):
            input += input_line
            input_line = file.readline();

        if not (input_line in output_marks):
            print '>>> answer format error!'
            sys.exit(1)

        input_line = file.readline()
        answer=''
        while len(input_line) != 0 and not reduce(operator.or_, map(input_line.endswith, input_marks)):
            answer += input_line
            input_line = file.readline();

        print 'output:'
        start = time.time()
        proc = subprocess.Popen(executer.run(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.stdin.write(input)
        output = ''
        for output_line in iter(proc.stdout.readline,''):
            print output_line,
            output += output_line
        proc.wait()
        end = time.time()

        if proc.returncode != 0:
            result = 'RE'
        elif answer == output:
            result = 'AC'
        else:
            result = 'WA'

        if result != 'AC':
            print 'answer:'
            print answer,

        print '=== Case #{0}: {1} ({2} ms) ===\n'.format(case, result, int((end-start)*1000))
        if result != 'AC':
            raw_input('press enter to continue or <C-c> to leave.')
        case = case+1

if __name__ == '__main__':
    main()
