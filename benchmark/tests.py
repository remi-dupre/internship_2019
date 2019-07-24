"""
Module listing all the testcases to run.

Please edit variables `regexps` and `tests` and list all tests by importing the
function `tests_iter`.
"""
from dataclasses import dataclass

from wrappers import (
    DagRs,
    Grep,
    Matcher,
    NaiveCubicRs,
    NaiveQuadraticRs,
    RipGrep,
    SpannerConst,
)


def repeat(pattern, min, max):
    ret = ''

    if max is not None:
        for _ in range(max - min):
            ret = '({}{})?'.format(pattern, ret)
    else:
        if min == 0:
            ret = '{}*'.format(pattern)
        else:
            ret = '{}+'.format(pattern)
            min -= 1

    return (pattern * min) + ret


#    ____             __ _
#   / ___|___  _ __  / _(_) __ _
#  | |   / _ \| '_ \| |_| |/ _` |
#  | |__| (_) | | | |  _| | (_| |
#   \____\___/|_| |_|_| |_|\__, |
#                          |___/


regexps = {
    'all_text': {'simple': '^.*$', 'expanded': '^.*$'},
    'dna_codon_1': {
        'simple': r'ATG(...){0,200}(TAG|TAA|TGA)',
        'expanded': (r'ATG' + repeat(r'(...)', 0, 200) + r'(TAG|TAA|TGA)'),
    },
    'dna_codon_2': {
        'simple': r'ATG([^T]..|T([^AG].|[^A][^A]|.[^AG])){0,200}(TAG|TAA|TGA)',
        'expanded': (
            r'ATG'
            + repeat(r'([^T]..|T([^AG].|[^A][^A]|.[^AG]))', 0, 200)
            + r'(TAG|TAA|TGA)'
        ),
    },
}

tests = [
    #  {
    #      'name': 'all_text',
    #      'text': ['/home/remi/stage/datasets/dna.short'],
    #      'expr': ['all_text'],
    #      'runners': [DagRs],
    #  },
    #  {
    #      'name': 'incr_dna',
    #      'text': [
    #          '/home/remi/stage/datasets/dna_1e' + str(i) for i in range(4, 8)
    #      ],
    #      'expr': ['dna_codon_2'],
    #      'runners': [DagRs, Grep],
    #  },
    {
        'name': 'compare_naive',
        'text': [
            '/home/remi/stage/datasets/dna_1e' + str(i) for i in range(4, 7)
        ],
        'expr': ['dna_codon_2'],
        'runners': [
            SpannerConst,
            DagRs,
            Grep,
            RipGrep,
            NaiveQuadraticRs,
            NaiveCubicRs,
        ],
    }
]

#   _     _     _   _
#  | |   (_)___| |_(_)_ __   __ _
#  | |   | / __| __| | '_ \ / _` |
#  | |___| \__ \ |_| | | | | (_| |
#  |_____|_|___/\__|_|_| |_|\__, |
#                           |___/


@dataclass
class Test:
    name: str
    text: str
    expr: str
    runner: Matcher


def tests_iter():
    for test in tests:
        name = test['name']

        for text in test['text']:
            for expr in test['expr']:
                for Runner in test['runners']:
                    yield Test(name, text, expr, Runner())
