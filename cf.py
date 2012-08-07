#! /usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import os.path
import sys
import time
import subprocess
import ConfigParser

class Enviroment:
    def __init__(self, compile_cmd, execute_cmd):
        self.compile_cmd = compile_cmd
        self.execute_cmd = execute_cmd

class Prefrences:
    def __init__(self):
        self.envs = {
                '.cpp'   : Enviroment('g++ -static -fno-optimize-sibling-calls -fno-strict-aliasing -lm -s -x c++ -O2 -m32 -o {0} {0}.cpp', './{0}'),
                '.c'     : Enviroment('gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -lm -s -O2 -m32 -o {0} {0}.c', './{0}'),
                '.java'  : Enviroment('javac -cp \'.;*\' {0}.java', 'java -Xmx256M -Duser.language=en -Duser.region=US -Duser.variant=US {0}'),
                '.py'    : Enviroment('', 'python -O {0}.py'),
        }

    def get_env(self, lang):
        return self.envs[lang]

class Executer(object):
    def __init__(self, env, id):
        self.env = env
        self.id = id

    def compile(self):
        if len(self.env.compile_cmd) == 0: return 0
        return subprocess.call(self.env.compile_cmd.format(self.id), shell=True)

    def execute(self):
        return subprocess.Popen(self.env.execute_cmd.format(self.id), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def save_preferences(pref, config):
    for lang, env in pref.envs.items():
        config.add_section(lang)
        config.set(lang, 'compile_cmd', env.compile_cmd)
        config.set(lang, 'execute_cmd', env.execute_cmd)

def load_preferences(pref, config):
    for sections in config.sections():
        if sections == 'global': break
        pref.envs[sections] = Enviroment(config.get(sections, 'compile_cmd'), config.get(sections, 'execute_cmd'))

def token_list(output):
    return output.split();
def check_result(answer, output, strict):
    if(strict):
        return answer == output
    else:
        return token_list(answer) == token_list(output)

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print 'Source code not exist!'
        sys.exit(1)

    pref = Prefrences()

    pref_file = os.path.join(os.path.split(os.path.abspath( __file__ ))[0], 'cf.conf')
    config = ConfigParser.RawConfigParser()
    try:
        with open(pref_file, 'r') as f:
            config.readfp(f)
        load_preferences(pref, config)
    except IOError as e:
        save_preferences(pref, config)
        with open(pref_file, 'w') as f:
            config.write(f)

    strict = len(sys.argv)>=3 and (sys.argv[2] == '--strict' or sys.argv[2] == '-s')
    id, lang = os.path.splitext(sys.argv[1])
    executer = Executer(pref.get_env(lang), id)
    
    ret = executer.compile()

    if ret != 0:
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
        proc = executer.execute()
        proc.stdin.write(input)
        output = ''
        for output_line in iter(proc.stdout.readline,''):
            print output_line,
            output += output_line
        proc.wait()
        end = time.time()
        if proc.returncode != 0:
            result = 'RE'
        elif check_result(answer, output, strict):
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
