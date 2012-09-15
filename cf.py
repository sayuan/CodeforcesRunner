#! /usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import os.path
import sys
import time
import re
import subprocess
import urllib2
import ConfigParser
from optparse import *
from lxml import etree

CODEFORCES_URL = 'http://codeforces.com'

class Enviroment:
    def __init__(self, compile_cmd, execute_cmd):
        self.compile_cmd = compile_cmd
        self.execute_cmd = execute_cmd

class Preferences:
    def __init__(self):
        self.filename_pattern = 'upper({id})'
        self.replace_space = '_'
        self.test_extension = '.xml'
        self.envs = {
                '.cpp'   : Enviroment('g++ -static -fno-optimize-sibling-calls -fno-strict-aliasing -lm -s -x c++ -O2 -m32 -o {0} {0}.cpp', './{0}'),
                '.c'     : Enviroment('gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -lm -s -O2 -m32 -o {0} {0}.c', './{0}'),
                '.java'  : Enviroment('javac -cp \'.;*\' {0}.java', 'java -Xmx256M -Duser.language=en -Duser.region=US -Duser.variant=US {0}'),
                '.py'    : Enviroment('', 'python -O {0}.py'),
                '.scala' : Enviroment('scalac -cp \'.;*\' {0}.scala', 'scala -J-Xmx256M -J-Duser.language=en -J-Duser.region=US -J-Duser.variant=US {0}'),
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
    config.add_section('global')
    config.set('global', 'filename_pattern', pref.filename_pattern)
    config.set('global', 'replace_space', pref.replace_space)
    config.set('global', 'test_extension', pref.test_extension)
    for lang, env in pref.envs.items():
        config.add_section(lang)
        config.set(lang, 'compile_cmd', env.compile_cmd)
        config.set(lang, 'execute_cmd', env.execute_cmd)

def config_get(config, section, option, default):
    if not config.has_option(section, option): return default
    return config.get(section, option)

def load_preferences(pref, config):
    pref.filename_pattern = config_get(config, 'global', 'filename_pattern', pref.filename_pattern)
    pref.replace_space = config_get(config, 'global', 'replace_space', pref.replace_space)
    pref.test_extension = config_get(config, 'global', 'test_extension', pref.test_extension)
    for sections in config.sections():
        if sections == 'global': continue
        pref.envs[sections] = Enviroment(config.get(sections, 'compile_cmd'), config.get(sections, 'execute_cmd'))

def add_options():
    usage = '%prog [options] [source code]'
    parser = OptionParser(usage=usage)
    parser.add_option( '-s', '--strict', action="store_true", default=False, help='Strict comparison.')
    parser.add_option( '-c', '--contest', dest='contest_id', help='Download the specific contest. '
            'If the PROBLEM_ID isn\'t specific, then download all problems in the contest.')
    parser.add_option( '-p', '--problem', dest='problem_id', help='Download the specific problem. '
            'The CONTEST_ID is required.')
    return parser.parse_args()

def token_list(output):
    return output.split();

def check_result(answer, output):
    if options.strict:
        return answer == output
    else:
        return token_list(answer) == token_list(output)

def download_contest(contest_id):
    contest_url = '/'.join((CODEFORCES_URL, 'contest', contest_id))
    contest_page = urllib2.urlopen(contest_url)
    tree = etree.HTML(contest_page.read())
    for i in tree.xpath(".//table[contains(@class, 'problems')]//td[contains(@class, 'id')]/a"):
        download_problem(contest_id, i.text.strip())

def download_problem(contest_id, problem_id):
    node_to_string = lambda node: ''.join([node.text]+map(etree.tostring, node.getchildren()))

    problem_url = '/'.join((CODEFORCES_URL, 'contest', contest_id, 'problem', problem_id))
    problem_page = urllib2.urlopen(problem_url)
    tree = etree.HTML(problem_page.read())

    title = tree.xpath('.//div[contains(@class, "problem-statement")]/div/div[contains(@class, "title")]')[0].text
    name = title[3:]

    filename = pref.filename_pattern.format(id=problem_id, name=name)
    filename = re.sub(r'upper\((.*?)\)', lambda x: x.group(1).upper(), filename)
    filename = re.sub(r'lower\((.*?)\)', lambda x: x.group(1).lower(), filename)
    if len(pref.replace_space) > 0:
        filename = filename.replace(' ', pref.replace_space)
    filename += pref.test_extension

    with open(filename, 'w') as f:
        f.write('<tests>\n')
        for (input_node, answer_node) in zip(
                tree.xpath('.//div[contains(@class, "input")]/pre'),
                tree.xpath('.//div[contains(@class, "output")]/pre')):
            f.write('<input><![CDATA[\n')
            f.write(node_to_string(input_node).replace('<br/>', '\n'))
            f.write('\n')
            f.write(']]></input>\n')
            f.write('<answer><![CDATA[\n')
            f.write(node_to_string(answer_node).replace('<br/>', '\n'))
            f.write('\n')
            f.write(']]></answer>\n')
        f.write('</tests>\n')

    print 'contest={0!r}, id={1!r}, problem={2!r} is downloaded.'.format(contest_id, problem_id, name)

def handle_test(executer, case, input_text, answer_text):
    print 'output:'
    start = time.time()
    proc = executer.execute()
    proc.stdin.write(input_text)
    output = ''
    for output_line in iter(proc.stdout.readline,''):
        print output_line,
        output += output_line
    proc.wait()
    print
    end = time.time()

    if proc.returncode != 0:
        result = 'RE'
    elif check_result(answer_text, output):
        result = 'AC'
    else:
        result = 'WA'

    if result != 'AC':
        print 'answer:'
        print answer_text

    print '=== Case #{0}: {1} ({2} ms) ===\n'.format(case, result, int((end-start)*1000))
    if result != 'AC':
        raw_input('press enter to continue or <C-c> to leave.')

def main():
    global options, pref
    (options, args) = add_options()
    pref = Preferences()

    pref_file = os.path.join(os.path.split(os.path.abspath( __file__ ))[0], 'cf.conf')
    config = ConfigParser.RawConfigParser()
    try:
        with open(pref_file, 'r') as f:
            config.readfp(f)
        load_preferences(pref, config)
    except IOError as e:
        pass

    config = ConfigParser.RawConfigParser()
    save_preferences(pref, config)
    with open(pref_file, 'w') as f:
        config.write(f)

    if options.contest_id != None:
        if options.problem_id != None:
            download_problem(options.contest_id, options.problem_id)
        else:
            download_contest(options.contest_id)
        sys.exit(0)

    if len(args) < 1 or not os.path.exists(args[0]):
        print 'Source code not exist!'
        sys.exit(1)

    id, lang = os.path.splitext(args[0])
    executer = Executer(pref.get_env(lang), id)

    ret = executer.compile()

    if ret != 0:
        print '>>> failed to Compile the source code!'
        sys.exit(1)

    with open('{0}.xml'.format(id)) as test_file:
        tree = etree.XML(test_file.read())

        inputs = tree.xpath('./input')
        answers = tree.xpath('./answer')
        case_count = len(inputs)

        for case in xrange(case_count):
            input_text = inputs[case].text[1:-1]
            answer_text = answers[case].text[1:-1]
            handle_test(executer, case, input_text, answer_text)

if __name__ == '__main__':
    main()
