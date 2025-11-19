class KinderState :
    def __init__(self, ui_pos, name, population, population_per_px, vegetable_production, obesity_rate, importations, exportations) :
        self.ui_pos = ui_pos
        self.name = name
        self.population = population
        self.alive_population = population
        self.population_per_px = population_per_px
        self.closed_border = False
        self.lockdown = False
        self.initial_vegetable_production = vegetable_production
        self.vegetable_production = vegetable_production
        self.food_ressources = 0
        self.obesity_rate = obesity_rate
        self.importations = importations
        self.exportations = exportations
        


STATES = {
    100 : {
        'ui_pos' : (),
        'name' : None,
        'population' : 1,
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    101 : {
        'ui_pos' : (130, 100),
        'name' : 'Washington',
        'population' : 8115100,
        'vegetable_production' : 13060139,
        'obesity_rate' : 0.28,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    102 : {
        'ui_pos' : (130, 200),
        'name' : 'Oregon',
        'population' : 4291090,
        'vegetable_production' : 2748443,
        'obesity_rate' : 0.281,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    103 : {
        'ui_pos' : (140, 400),
        'name' : 'Californie',
        'population' : 39431000,
        'vegetable_production' : 40375750,
        'obesity_rate' : 0.303,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    104 : {
        'ui_pos' : (275, 200),
        'name' : 'Idaho',
        'population' : 1967000,
        'vegetable_production' : 620535,
        'obesity_rate' : 0.311,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    105 : {
        'ui_pos' : (230, 330),
        'name' : 'Nevada',
        'population' : 3265000,
        'vegetable_production' : 3994128,
        'obesity_rate' : 0.287,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    106 : {
        'ui_pos' : (400, 100),
        'name' : 'Montana',
        'population' : 1153000,
        'vegetable_production' : 1017380,
        'obesity_rate' : 0.285,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    107 : {
        'ui_pos' : (440, 220),
        'name' : 'Wyoming',
        'population' : 584000,
        'vegetable_production' : 381644,
        'obesity_rate' : 0.307,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    108 : {
        'ui_pos' : (350, 330),
        'name' : 'Utah',
        'population' : 3427000,
        'vegetable_production' : 4298150,
        'obesity_rate' : 0.286,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    109 : {
        'ui_pos' : (350, 480),
        'name' : 'Arizona',
        'population' : 7600000,
        'vegetable_production' : 10524284,
        'obesity_rate' : 0.309,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    110 : {
        'ui_pos' : (500, 330),
        'name' : 'Colorado',
        'population' : 6023000,
        'vegetable_production' : 13343881,
        'obesity_rate' : 0.242,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    111 : {
        'ui_pos' : (480, 470),
        'name' : 'Nouveau-Mexique',
        'population' : 2110000,
        'vegetable_production' : 2761990,
        'obesity_rate' : 0.309,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    112 : {
        'ui_pos' : (620, 80),
        'name' : 'Dakota du Nord',
        'population' : 783000,
        'vegetable_production' : 521086,
        'obesity_rate' : 0.331,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    113 : {
        'ui_pos' : (620, 175),
        'name' : 'Dakota du Sud',
        'population' : 919000,
        'vegetable_production' : 1329643,
        'obesity_rate' : 0.332,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    114 : {
        'ui_pos' : (630, 260),
        'name' : 'Nebraska',
        'population' : 1973000,
        'vegetable_production' : 2305674,
        'obesity_rate' : 0.34,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    115 : {
        'ui_pos' : (675, 350),
        'name' : 'Kansas',
        'population' : 2943000,
        'vegetable_production' : 1990939,
        'obesity_rate' : 0.353,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    116 : {
        'ui_pos' : (700, 440),
        'name' : 'Oklahoma',
        'population' : 4060000,
        'vegetable_production' : 5455425,
        'obesity_rate' : 0.364,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    117 : {
        'ui_pos' : (650, 570),
        'name' : 'Texas',
        'population' : 31290000,
        'vegetable_production' : 46593176,
        'obesity_rate' : 0.358,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    118 : {
        'ui_pos' : (770, 130),
        'name' : 'Minnesota',
        'population' : 5787000,
        'vegetable_production' : 8926318,
        'obesity_rate' : 0.307,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    119 : {
        'ui_pos' : (790, 250),
        'name' : 'Iowa',
        'population' : 3200000,
        'vegetable_production' : 4368000,
        'obesity_rate' : 0.365,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    120 : {
        'ui_pos' : (820, 355),
        'name' : 'Missouri',
        'population' : 6217000,
        'vegetable_production' : 8330780,
        'obesity_rate' : 0.34,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    121 : {
        'ui_pos' : (830, 465),
        'name' : 'Arkansas',
        'population' : 3080000,
        'vegetable_production' : 7553201,
        'obesity_rate' : 0.364,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    122 : {
        'ui_pos' : (820, 580),
        'name' : 'Louisiane',
        'population' : 4540000,
        'vegetable_production' : 6963958,
        'obesity_rate' : 0.381,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    123 : {
        'ui_pos' : (1420, 130),
        'name' : 'Maine',
        'population' : 1380000,
        'vegetable_production' : 903900,
        'obesity_rate' : 0.31,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    124 : {
        'ui_pos' : (890, 170),
        'name' : 'Wisconsin',
        'population' : 5890000,
        'vegetable_production' : 8946426,
        'obesity_rate' : 0.323,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    125 : {
        'ui_pos' : (905, 300),
        'name' : 'Illinois',
        'population' : 12710000,
        'vegetable_production' : 29997641,
        'obesity_rate' : 0.324,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    126 : {
        'ui_pos' : (890, 515),
        'name' : 'Mississippi',
        'population' : 2940000,
        'vegetable_production' : 4748732,
        'obesity_rate' : 0.397,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    127 : {
        'ui_pos' : (1015, 195),
        'name' : 'Michigan',
        'population' : 10077000,
        'vegetable_production' : 20242630,
        'obesity_rate' : 0.352,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    128 : {
        'ui_pos' : (980, 310),
        'name' : 'Indiana',
        'population' : 6890000,
        'vegetable_production' : 9841614,
        'obesity_rate' : 0.368,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    129 : {
        'ui_pos' : (1020, 380),
        'name' : 'Kentucky',
        'population' : 4530000,
        'vegetable_production' : 6507648,
        'obesity_rate' : 0.366,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    130 : {
        'ui_pos' : (990, 440),
        'name' : 'Tennessee',
        'population' : 7190000,
        'vegetable_production' : 8164781,
        'obesity_rate' : 0.356,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    131 : {
        'ui_pos' : (965, 530),
        'name' : 'Alabama',
        'population' : 5080000,
        'vegetable_production' : 6225324,
        'obesity_rate' : 0.39,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    132 : {
        'ui_pos' : (1090, 680),
        'name' : 'Floride',
        'population' : 23370000,
        'vegetable_production' : 28177274,
        'obesity_rate' : 0.284,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    133 : {
        'ui_pos' : (1070, 300),
        'name' : 'Ohio',
        'population' : 11880000,
        'vegetable_production' : 23596686,
        'obesity_rate' : 0.355,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    134 : {
        'ui_pos' : (1120, 350),
        'name' : 'Virginie-Occidentale',
        'population' : 1760000,
        'vegetable_production' : 3563842,
        'obesity_rate' : 0.391,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    135 : {
        'ui_pos' : (1175, 380),
        'name' : 'Virginie',
        'population' : 8870000,
        'vegetable_production' : 8524901,
        'obesity_rate' : 0.322,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    136 : {
        'ui_pos' : (1160, 450),
        'name' : 'Caroline du Nord',
        'population' : 11046000,
        'vegetable_production' : 14264105,
        'obesity_rate' : 0.336,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    137 : {
        'ui_pos' : (1120, 505),
        'name' : 'Caroline du Sud',
        'population' : 5420000,
        'vegetable_production' : 7807027,
        'obesity_rate' : 0.362,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    138 : {
        'ui_pos' : (1050, 530),
        'name' : 'Géorgie',
        'population' : 11180000,
        'vegetable_production' : 16913695,
        'obesity_rate' : 0.343,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    139 : {
        'ui_pos' : (1200, 280),
        'name' : 'Pennsylvanie',
        'population' : 13080000,
        'vegetable_production' : 19157023,
        'obesity_rate' : 0.315,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    140 : {
        'ui_pos' : (1220, 330),
        'name' : 'Maryland',
        'population' : 6230000,
        'vegetable_production' : 8161300,
        'obesity_rate' : 0.31,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    141 : {
        'ui_pos' : (1277, 293),
        'name' : 'N.Jersey & Delaware',
        'population' : 10020000,
        'vegetable_production' : 7856711,
        'obesity_rate' : 0.365,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    142 : {
        'ui_pos' : (1270, 220),
        'name' : 'New York',
        'population' : 19870000,
        'vegetable_production' : 45986790,
        'obesity_rate' : 0.263,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    143 : {
        'ui_pos' : (1320, 195),
        'name' : 'Vermont',
        'population' : 650000,
        'vegetable_production' : 410474,
        'obesity_rate' : 0.263,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    144 : {
        'ui_pos' : (1320, 268),
        'name' : 'Connecticut',
        'population' : 3640000,
        'vegetable_production' : 4145658,
        'obesity_rate' : 0.292,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    145 : {
        'ui_pos' : (1350, 215),
        'name' : 'New Hampshire',
        'population' : 1390000,
        'vegetable_production' : 3276380,
        'obesity_rate' : 0.299,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    146 : {
        'ui_pos' : (1360, 255),
        'name' : 'Massach. & R.Island',
        'population' : 7650000,
        'vegetable_production' : 9430948,
        'obesity_rate' : 0.28,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
    255 : {
        'ui_pos' : (),
        'name' : None,
        'population' : 1,
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : [],
        'exportations' : [[0, 0], [0, 0], [0, 0], [0, 0]]
    },
}