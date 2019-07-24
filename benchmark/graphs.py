#    ____             __ _
#   / ___|___  _ __  / _(_) __ _
#  | |   / _ \| '_ \| |_| |/ _` |
#  | |__| (_) | | | |  _| | (_| |
#   \____\___/|_| |_|_| |_|\__, |
#                          |___/

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
        'name': 'enum_speed_with_naives_10k',
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
                    'and test.text[-3:] == "1e5"'
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
            'SpannerConst': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e5"'
                    'and test.runner.name == "spanner_const"'
                ),
            },
        },
    },
    {
        'name': 'enum_speed_with_naives_100k',
        'plt_params': {
            'title': ['enumeration speed (100kB input)'],
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
                    'and test.text[-3:] == "1e6"'
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
                    'and test.text[-3:] == "1e6"'
                    'and test.runner.name == "grep"'
                ),
            },
            'ripgrep': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e6"'
                    'and test.runner.name == "ripgrep"'
                ),
            },
            'dag_rs': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e6"'
                    'and test.runner.name == "dag_rs"'
                ),
            },
            'SpannerConst': {
                'key': 'count',
                'filter': (
                    'test.name == "compare_naive"'
                    'and test.text[-3:] == "1e6"'
                    'and test.runner.name == "spanner_const"'
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

#   _     _     _   _
#  | |   (_)___| |_(_)_ __   __ _
#  | |   | / __| __| | '_ \ / _` |
#  | |___| \__ \ |_| | | | | (_| |
#  |_____|_|___/\__|_|_| |_|\__, |
#                           |___/


def graphs_iter():
    for graph in graphs:
        vals = default_fields.copy()
        vals.update(graph)
        yield vals
