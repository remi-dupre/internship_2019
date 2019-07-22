graphs = [
    {
        'name': 'enum_speed',
        'plt_params': {
            'title': ['enumeration speed'],
            'xlabel': ['time (s)'],
            'ylabel': ['number of matches in the output'],
        },
        'x_axis': 'time',
        'y_axis': {
            'matches': {
                'key': 'count',
                'filter': (
                    'test.name == "incr_dna"'
                    'and test.runner.name == "dag_rs"'
                    'and test.text[-7:] == "dna_1e7"'
                ),
            },
            #  'impossible': {
            #      'key': 'count',
            #      'filter': 'test == "basic_dna" and expr == "Z"',
            #  },
        },
    },
    {
        'name': 'prec_speed',
        'plt_params': {
            'title': ['precomputation speed'],
            'xscale': ['log'],
            'yscale': ['log'],
            'xlabel': ['size of the input (bytes)'],
            'ylabel': ['duration of the precomputation (s)'],
        },
        'x_axis': 'float(test.text[-3:])',
        'y_axis': {
            'time': {
                'key': 'time',
                'filter': (
                    'test.name == "incr_dna"'
                    'and test.runner.name == "dag_rs"'
                    'and count == 1'
                ),
            }
        },
    },
    {
        'name': 'compare_output',
        'plt_params': {
            'title': ['count of matches outputed for each tool'],
            'xlabel': ['size of the input (bytes)'],
            'xscale': ['log'],
            'ylabel': ['count of matches'],
            'yscale': ['log'],
            'legend': [],
        },
        'x_axis': 'float(test.text[-3:])',
        'y_axis': {
            'dag_rs': {
                'key': 'count',
                'filter': (
                    'test.name == "incr_dna"'
                    'and test.runner.name == "dag_rs"'
                ),
            },
            'grep': {
                'key': 'count',
                'filter': (
                    'test.name == "incr_dna"' 'and test.runner.name == "grep"'
                ),
            },
        },
    },
]


default_fields = {'plt_params': {}}


def graphs_iter():
    for graph in graphs:
        vals = default_fields.copy()
        vals.update(graph)
        yield vals
