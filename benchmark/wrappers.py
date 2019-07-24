#!/usr/bin/env python3
import json
import os
import subprocess
import random
import string
import sys
import time
from dataclasses import dataclass


@dataclass
class Match:
    count: int
    span: (int, int)
    time: int


class Matcher:
    name = None
    handle_repeats = True  # wether the tool supports (...){start, stop} syntax

    def __init__(self):
        self.timer = None

    def run(self, regex, text_path):
        """
        Get a list of matches of the regexp over the input text.
        """
        return NotImplemented


class ExecMatcher(Matcher):
    binary = None
    parameters = []

    def __init__(self):
        super().__init__()
        self.count = 0

    def run(self, regex: str, text_path: str):
        self.timer = time.time()
        file_null = open(os.devnull, 'w')

        process = subprocess.Popen(
            [os.path.expanduser(self.binary)]
            + self.parameters
            + [regex, text_path],
            stdout=subprocess.PIPE,
            stderr=file_null,
            universal_newlines=True,
        )

        return self.parse_output(process)

    def parse_output(self, proc) -> list:
        ret = []

        try:
            for line in proc.stdout:
                match = self.parse_line(line)

                if match is not None:
                    ret.append(match)
                    self.count = len(ret)
        except KeyboardInterrupt:
            ok_messages = ['', 'y', 'Y', 'yes']
            if (
                input('Test skipped... Continue running? [y]: ')
                not in ok_messages
            ):
                raise KeyboardInterrupt

        return ret

    def parse_line(self, line: str) -> Match:
        return NotImplemented


class SpannerConst(ExecMatcher):
    name = 'spanner_const'
    binary = '/home/remi/stage/SpannersConst/cpp/bin/test'
    handle_repeats = False

    def run(self, regex, text_path):
        self.timer = time.time()
        rgx_path = '/tmp/benchmark.{}.rgx'.format(
            ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        )

        with open(rgx_path, 'w') as f:
            f.write(r'.*!x{{{}}}.*'.format(regex))

        process = subprocess.Popen(
            [os.path.expanduser(self.binary)] + [text_path, rgx_path],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        return self.parse_output(process)

    def parse_line(self, line: str) -> Match:
        # Outputs are in the form (x,;loffset)(,x;roffset)
        left, right = map(
            lambda x: int(x.split(';')[1]), line.rstrip()[1:-1].split(')(')
        )

        elapsed = time.time() - self.timer
        return Match(self.count, [left, right], elapsed)


class DagRs(ExecMatcher):
    name = 'dag_rs'
    binary = '~/code/enum-spanner-rs/target/release/enum-spanner-rs'
    parameters = ['--compare']

    def parse_line(self, line):
        try:
            data = json.loads(line[4:])
        except json.JSONDecodeError:
            return None

        if data['span'] == [-1, -1]:
            data['span'] = None

        elapsed = time.time() - self.timer
        return Match(self.count, data['span'], elapsed)


class NaiveCubicRs(DagRs):
    name = 'naive_cubic_rs'
    parameters = ['--compare', '--naive-cubic']


class NaiveQuadraticRs(DagRs):
    name = 'naive_quadratic_rs'
    parameters = ['--compare', '--naive-quadratic']


class Grep(ExecMatcher):
    name = 'grep'
    binary = '/bin/grep'
    parameters = ['--extended-regexp', '--only-matching', '--byte-offset']
    handle_repeats = False

    def parse_line(self, line):
        start, matched = line.strip().split(':')
        start = int(start)
        elapsed = time.time() - self.timer
        return Match(self.count, (start, start + len(matched)), elapsed)


class RipGrep(ExecMatcher):
    name = 'ripgrep'
    binary = '/usr/bin/rg'
    parameters = ['--only-matching', '--byte-offset']

    def parse_line(self, line):
        start, matched = line.strip().split(':')
        start = int(start)
        elapsed = time.time() - self.timer
        return Match(self.count, (start, start + len(matched)), elapsed)
