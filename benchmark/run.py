#!/usr/bin/env python3
import math
import os

import argparse
import gzip
import jsonpickle
import matplotlib.pyplot as plt

from tests import tests_iter, regexps
from graphs import graphs_iter


# ----- Parse Command Line Arguments -----

parser = argparse.ArgumentParser(
    description='Enumerate all matches of a regular expression on a text.'
)

parser.set_defaults(run_tests=False, gen_graphs=False)

parser.add_argument(
    '-r',
    '--run-tests',
    dest='run_tests',
    action='store_true',
    help='Run all the specified tests.',
)
parser.add_argument(
    '-g',
    '--gen-graph',
    dest='gen_graphs',
    action='store_true',
    help='Generate all the specified graphs.',
)

args = parser.parse_args()


# ----- Run tests -----

if args.run_tests:
    data = []
    nb_tests = sum(1 for _ in tests_iter())

    for i, test in enumerate(tests_iter()):
        print(
            '({}/{}) {}: running regex `{}` over text `{}` using algorithm `{}`'.format(
                i + 1,
                nb_tests,
                test.name,
                test.expr,
                test.text,
                test.runner.name,
            )
        )
        regex = (
            regexps[test.expr]['simple']
            if test.runner.handle_repeats
            else regexps[test.expr]['expanded']
        )
        matches = test.runner.run(regex, test.text)

        for match in matches:
            data.append(
                {
                    'test': test,
                    'span': match.span,
                    'count': match.count,
                    'time': match.time,
                }
            )

    with gzip.open('results.json.gz', 'wb') as output:
        serialized = jsonpickle.encode(data)
        #  serialized = json.dumps(json.loads(serialized), indent=4)
        output.write(serialized.encode('utf8'))


# ----- Generate graphs -----

if args.gen_graphs:
    with gzip.open('results.json.gz', 'rb') as f:
        serialized = f.read().decode('utf8')
        data = jsonpickle.decode(serialized)

    if not os.path.exists('figures'):
        os.makedirs('figures')

    for graph in graphs_iter():
        print('--- graph:', graph['name'])
        values = dict()

        for point in data:
            pt = dict()

            if not eval(graph['filter'], point):
                continue

            for y_axis, params in graph['y_axis'].items():
                if eval(params['filter'], point):
                    pt[y_axis] = eval(params['key'], point)

            if pt:
                x_value = eval(graph['x_axis'], point)

                if x_value not in values:
                    values[x_value] = pt
                else:
                    values[x_value].update(pt)

        for y_axis, y_params in graph['y_axis'].items():
            # Extract datas
            x_values = sorted(values.keys())
            y_values = [
                values[x][y_axis] if y_axis in values[x] else None
                for x in x_values
            ]

            # Filter out x-coordinates not corresponding to a y value
            x_values = [
                x_values[i]
                for i in range(len(x_values))
                if y_values[i] is not None
            ]
            y_values = [x for x in y_values if x is not None]

            # Plot current curve
            plt.plot(x_values, y_values, label=y_axis)

        for fnc, params in graph['plt_params'].items():
            getattr(plt, fnc)(*params)

        plt.savefig('figures/{}.pdf'.format(graph['name']))
        plt.close()
