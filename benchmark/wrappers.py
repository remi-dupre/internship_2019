#!/usr/bin/env python3
import json
import os
import subprocess
import time
from dataclasses import dataclass


@dataclass
class Match:
    count: int
    span: (int, int)
    time: int


class Matcher:
    name = None

    def __init__(self):
        self.timer = None

    def run(self, regex, text_path):
        """
        Get a list of matches of the regexp over the input text.
        """
        self.timer = time.time()
        return []


class ExecMatcher(Matcher):
    binary = None
    parameters = []

    def __init__(self):
        super().__init__()
        self.count = 0

    def run(self, regex: str, text_path: str):
        super().run(regex, text_path)
        file_null = open(os.devnull, 'w')

        process = subprocess.Popen(
            [os.path.expanduser(self.binary)]
            + self.parameters
            + [regex, text_path],
            stdout=subprocess.PIPE,
            # stderr=file_null,
            universal_newlines=True,
        )

        return self.parse_output(process)

    def parse_output(self, proc) -> list:
        ret = []

        for line in proc.stdout:
            self.count = len(ret)
            match = self.parse_line(line)

            if match is not None:
                ret.append(match)

        return ret

    def parse_line(self, line: str) -> Match:
        return NotImplemented


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


class Grep(ExecMatcher):
    name = 'grep'
    binary = '/bin/grep'
    parameters = ['--extended-regexp', '--only-matching', '--byte-offset']

    def parse_line(self, line):
        start, matched = line.strip().split(':')
        start = int(start)
        elapsed = time.time() - self.timer
        return Match(self.count, (start, start + len(matched)), elapsed)
