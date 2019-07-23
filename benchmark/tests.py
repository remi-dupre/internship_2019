from dataclasses import dataclass

from wrappers import (
    DagRs,
    Grep,
    Matcher,
    NaiveCubicRs,
    NaiveQuadraticRs,
    RipGrep,
)


regexps = {
    'all_text': '^.*$',
    'dna_codon_1': r'ATG(...){0,200}(TAG|TAA|TGA)',
    'dna_codon_2': r'ATG([^T]..|T([^AG].|[^A][^A]|.[^AG])){0,200}(TAG|TAA|TGA)',
}

tests = [
    #  {
    #      'name': 'all_text',
    #      'text': ['/home/remi/stage/datasets/dna.short'],
    #      'expr': ['all_text'],
    #      'runners': [DagRs],
    #  },
    {
        'name': 'incr_dna',
        'text': [
            '/home/remi/stage/datasets/dna_1e' + str(i) for i in range(4, 8)
        ],
        'expr': ['dna_codon_2'],
        'runners': [DagRs, Grep],
    },
    {
        'name': 'compare_naive',
        'text': [
            '/home/remi/stage/datasets/dna_1e' + str(i) for i in range(4, 7)
        ],
        'expr': ['dna_codon_2'],
        'runners': [DagRs, Grep, RipGrep, NaiveQuadraticRs, NaiveCubicRs],
    },
]


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
