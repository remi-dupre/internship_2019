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
            }
        },
    },
    {
        'name': 'enum_speed_with_naives',
        'plt_params': {
            'title': ['enumeration speed (10kB input)'],
            'xlabel': ['time (s)'],
            'xscale': ['log'],
            'ylabel': ['number of matches outputed yet'],
            'yscale': ['log'],
            'legend': [],
        },
        'x_axis': 'time',
        'y_axis': {
            'naive O(n²)': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e5"'
                    'and test.runner.name == "naive_quadratic_rs"'
                ),
            },
            'naive O(n³)': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e6"'
                    'and test.runner.name == "naive_cubic_rs"'
                ),
            },
            'grep': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e5"'
                    'and test.runner.name == "grep"'
                ),
            },
            'ripgrep': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e5"'
                    'and test.runner.name == "ripgrep"'
                ),
            },
            'dag_rs': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e5"'
                    'and test.runner.name == "dag_rs"'
                ),
            },
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
