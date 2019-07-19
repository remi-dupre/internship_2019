graphs = [
    {
        'name': 'enum_speed',
        'title': 'enumeration speed',
        'x_axis': 'time',
        'x_label': 'time (s)',
        'y_axis': {
            'matches': {
                'key': 'count',
                'label': 'number of matches in the output',
                'filter': 'test == "basic_dna" and expr == "ATG(...){0,500}(TAG|TAA|TGA)"',
            },
            #  'impossible': {
            #      'key': 'count',
            #      'filter': 'test == "basic_dna" and expr == "Z"',
            #  },
        },
    }
]
