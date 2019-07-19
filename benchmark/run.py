#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os

from tests import tests
from graphs import graphs


data = []

for test in tests:
    for Runner in test['runners']:
        for expr in test['expr']:
            for text in test['text']:
                matches = Runner().run(expr, text)

                for match in matches:
                    data.append(
                        {
                            'test': test['name'],
                            'text': text,
                            'expr': expr,
                            'runner': Runner.name,
                            'span': match.span,
                            'count': match.count,
                            'time': match.time,
                        }
                    )


# Generate graphs
if not os.path.exists('figures'):
    os.makedirs('figures')


for graph in graphs:
    print('--- graph:', graph['title'])
    values = dict()

    for point in data:
        pt = dict()

        for y_axis, params in graph['y_axis'].items():
            if eval(params['filter'], point):
                pt[y_axis] = point[params['key']]

        if pt:
            x_value = point[graph['x_axis']]
            if x_value not in values:
                values[x_value] = pt
            else:
                values[x_value].update(pt)

    plt.title(graph['title'])
    plt.xlabel(graph['x_label'])

    for y_axis, y_params in graph['y_axis'].items():
        x_values = sorted(values.keys())
        y_values = [
            values[x][y_axis] if y_axis in values[x] else None
            for x in x_values
        ]

        plt.plot(x_values, y_values)
        plt.ylabel(y_params['label'])

    plt.savefig('figures/{}.pdf'.format(graph['name']))
