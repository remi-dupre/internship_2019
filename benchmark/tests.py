from wrappers import DagRs


tests = [
    {
        'name': 'basic_dna',
        'text': ['/home/remi/stage/datasets/dna.short'],
        'expr': [r'ATG(...){0,500}(TAG|TAA|TGA)', 'Z'],
        'runners': [DagRs],
    }
]
