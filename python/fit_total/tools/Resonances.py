Resonances = {
    'BW_4390': {
        'init': {
            'mass':  4.47373139148,
            'width': 0.540121261871,
            'BrGam': 5.07919506012,
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

    'BW_4230': {
        'init': {
            'mass': 4.2191,
            'width': 0.05,
            'BrGam': 1.,
            'phase': 1.
        },
        'min_max': {
            'mass':  [4.20, 4.34],
            'width': [0., 1.],
            'BrGam': [-50., 50.],
            'phase': [-50., 50.]
        },
        'constant': ['mass', 'width']
    },

    'BW_4700': {
        'init': {
            'mass': 4.72174581917,
            'width': 0.0915455515991,
            'BrGam': 3.76003790411,
            'phase': 10.9854460416
        },
        'min_max': {
            'mass':  [4.68, 4.74],
            'width': [0., 0.1],
            'BrGam': [0., 50.],
            'phase': [0., 50.]
        },
        'constant': []
    },

    # 'BW_4700': {
    #     'init': {
    #         'mass': 4.74,
    #         'width': 0.1,
    #         'BrGam': 1.,
    #         'phase': 1.
    #     },
    #     'min_max': {
    #         'mass':  [4.68, 4.74],
    #         'width': [0., 0.3],
    #         'BrGam': [0., 50.],
    #         'phase': [0., 50.]
    #     },
    #     'constant': []
    # },

    'BW_4900': {
        'init': {
            'mass': 4.914,
            'width': 0.1,
            'BrGam': 1.,
            'phase': 1.
        },
        'min_max': {
            'mass':  [4.89, 4.99],
            'width': [0., 1.],
            'BrGam': [0., 50.],
            'phase': [0., 50.]
        },
        'constant': []
    },

    'PHSP': {
        'init': {
            'a': 1647.94200931,
            'phase': -20.5959762144
        },
        'min_max': {
            'a': [-5000., 5000.],
            'phase': [-50., 50.],
        },
        'constant': []
    },

    # 'PHSP': {
    #     'init': {
    #         'a': 1600,
    #         'phase': 10,
    #     },
    #     'min_max': {
    #         'a': [-5000., 3000.],
    #         'phase': [-50., 50.],
    #     },
    #     'constant': []
    # },

}
