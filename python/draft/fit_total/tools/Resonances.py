Resonances = {
    # for BW_4390 BW_4700 PHSP
    # 'BW_4390': {
    #     'init': {
    #         'mass': 4.45655262086,
    #         'width': 0.547607592114,
    #         'BrGam': 43.9197006122,
    #         'phase': 0.
    #     },
    #     'min_max': {
    #         'mass':  [4.33, 4.52],
    #         'width': [0., 1.],
    #         'BrGam': [0., 50.],
    #         'phase': [-50., 50.]
    #     },
    #     'constant': ['phase']
    # },

    # for BW_4390 BW_4700
    'BW_4390': {
        'init': {
            'mass':  4.49940126663,
            'width': 0.952011220188,
            'BrGam': 30.3249299629,
            'phase': 0.
        },
        'min_max': {
            'mass':  [4.33, 4.52],
            'width': [0., 1.],
            'BrGam': [0., 50.],
            'phase': [-50., 50.]
        },
        'constant': ['phase']
    },

    # for BW_4390 BW_4700 PHSP
    # 'BW_4700': {
    #     'init': {
    #         'mass': 4.72137092191,
    #         'width': 0.0984536513413,
    #         'BrGam': 7.15587116085,
    #         'phase': 1.10805893512
    #     },
    #     'min_max': {
    #         'mass':  [4.68, 4.74],
    #         'width': [0., 0.1],
    #         'BrGam': [0., 50.],
    #         'phase': [0., 50.]
    #     },
    #     'constant': []
    # },

    # for BW_4390 BW_4700
    'BW_4700': {
        'init': {
            'mass': 4.73463133073,
            'width': 0.266603978464,
            'BrGam': 39.4823124409,
            'phase': 41.8959026583
        },
        'min_max': {
            'mass':  [4.6, 4.74],
            'width': [0., 0.3],
            'BrGam': [0., 500.],
            'phase': [0., 50.]
        },
        'constant': []
    },

    # for BW_4390 BW_4700 PHSP
    'PHSP': {
        'init': {
            'a': 812.107688423,
            'phase': -34.4103915954
        },
        'min_max': {
            'a': [-5000., 5000.],
            'phase': [-50., 50.],
        },
        'constant': []
    },

}
