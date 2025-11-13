class KinderState :
    def __init__(self, name, population, population_per_px, vegetable_production, obesity_rate, importations, exportations) :
        self.name = name
        self.alive_population = population
        self.population_per_px = population_per_px
        self.dead_or_infected_population = 0
        self.open_frontiere = True
        self.lockdown = False
        self.vegetable_production = vegetable_production
        self.food_ressources = 0
        self.obesity_rate = obesity_rate
        self.importations = importations
        self.exportations = exportations
        
        

STATES = {
    101 : {
        'name' : 'Washington',
        'population' : 8115100,
        'population_per_px' : 575.171,
        'vegetable_production' : 7500000,
        'obesity_rate' : 0.28,
        'importations' : [],
        'exportations' : [],
    },
    
    102 : {
        'name' : 'Oregon',
        'population' : 4291090,
        'population_per_px' : 213.614,
        'vegetable_production' : 1230000,
        'obesity_rate' : 0.281,
        'importations' : [],
        'exportations' : [],
    },

    103 : {
        'name' : 'Californie',
        'population' : 39431000,
        'population_per_px' : 1328.672,
        'vegetable_production' : 35000000,
        'obesity_rate' : 0.303,
        'importations' : [],
        'exportations' : [],
    },

    104 : {
        'name' : 'Idaho',
        'population' : 1967000,
        'population_per_px' : 114.473,
        'vegetable_production' : 3500000,
        'obesity_rate' : 0.311,
        'importations' : [],
        'exportations' : [],
    },

    105 : {
        'name' : 'Nevada',
        'population' : 3265000,
        'population_per_px' : 146.301,
        'vegetable_production' : 900000,
        'obesity_rate' : 0.287,
        'importations' : [],
        'exportations' : [],
    },

    106 : {
        'name' : 'Montana',
        'population' : 1153000,
        'population_per_px' : 36.590,
        'vegetable_production' : 670500,
        'obesity_rate' : 0.285,
        'importations' : [],
        'exportations' : [],
    },

    107 : {
        'name' : 'Wyoming',
        'population' : 584000,
        'population_per_px' : 30.187,
        'vegetable_production' : 400000,
        'obesity_rate' : 0.307,
        'importations' : [],
        'exportations' : [],
    },

    108 : {
        'name' : 'Utah',
        'population' : 3427000,
        'population_per_px' : 213.135,
        'vegetable_production' : 800000,
        'obesity_rate' : 0.286,
        'importations' : [],
        'exportations' : [],
    },

    109 : {
        'name' : 'Arizona',
        'population' : 7600000,
        'population_per_px' : 358.017,
        'vegetable_production' : 1400000,
        'obesity_rate' : 0.309,
        'importations' : [],
        'exportations' : [],
    },

    110 : {
        'name' : 'Colorado',
        'population' : 6023000,
        'population_per_px' : 302.313,
        'vegetable_production' : 5500000,
        'obesity_rate' : 0.242,
        'importations' : [],
        'exportations' : [],
    },

    111 : {
        'name' : 'Nouveau-Mexique',
        'population' : 2110000,
        'population_per_px' : 100.744,
        'vegetable_production' : 1750000,
        'obesity_rate' : 0.309,
        'importations' : [],
        'exportations' : [],
    },

    112 : {
        'name' : 'Dakota du Nord',
        'population' : 783000,
        'population_per_px' : 51.496,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.331,
        'importations' : [],
        'exportations' : [],
    },

    113 : {
        'name' : 'Dakota du Sud',
        'population' : 919000,
        'population_per_px' : 57.959,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.332,
        'importations' : [],
        'exportations' : [],
    },

    114 : {
        'name' : 'Nebraska',
        'population' : 1973000,
        'population_per_px' : 126.110,
        'vegetable_production' : 29000000,
        'obesity_rate' : 0.34,
        'importations' : [],
        'exportations' : [],
    },

    115 : {
        'name' : 'Kansas',
        'population' : 2943000,
        'population_per_px' : 193.325,
        'vegetable_production' : 63000000,
        'obesity_rate' : 0.353,
        'importations' : [],
        'exportations' : [],
    },

    116 : {
        'name' : 'Oklahoma',
        'population' : 4060000,
        'population_per_px' : 376.065,
        'vegetable_production' : 4500000,
        'obesity_rate' : 0.364,
        'importations' : [],
        'exportations' : [],
    },

    117 : {
        'name' : 'Texas',
        'population' : 31290000,
        'population_per_px' : 657.187,
        'vegetable_production' : 60000000,
        'obesity_rate' : 0.358,
        'importations' : [],
        'exportations' : [],
    },

    118 : {
        'name' : 'Minnesota',
        'population' : 5787000,
        'population_per_px' : 326.524,
        'vegetable_production' : 35000000,
        'obesity_rate' : 0.307,
        'importations' : [],
        'exportations' : [],
    },

    119 : {
        'name' : 'Iowa',
        'population' : 3200000,
        'population_per_px' : 293.604,
        'vegetable_production' : 32000000,
        'obesity_rate' : 0.365,
        'importations' : [],
        'exportations' : [],
    },

    120 : {
        'name' : 'Missouri',
        'population' : 6217000,
        'population_per_px' : 466.076,
        'vegetable_production' : 5000000,
        'obesity_rate' : 0.34,
        'importations' : [],
        'exportations' : [],
    },

    121 : {
        'name' : 'Arkansas',
        'population' : 3080000,
        'population_per_px' : 340.783,
        'vegetable_production' : 3000000,
        'obesity_rate' : 0.364,
        'importations' : [],
        'exportations' : [],
    },

    122 : {
        'name' : 'Louisiane',
        'population' : 4540000,
        'population_per_px' : 577.755,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.381,
        'importations' : [],
        'exportations' : [],
    },

    123 : {
        'name' : 'Maine',
        'population' : 1380000,
        'population_per_px' : 216.063,
        'vegetable_production' : 600000,
        'obesity_rate' : 0.31,
        'importations' : [],
        'exportations' : [],
    },

    124 : {
        'name' : 'Wisconsin',
        'population' : 5890000,
        'population_per_px' : 513.155,
        'vegetable_production' : 30000000,
        'obesity_rate' : 0.323,
        'importations' : [],
        'exportations' : [],
    },

    125 : {
        'name' : 'Illinois',
        'population' : 12710000,
        'population_per_px' : 1178.816,
        'vegetable_production' : 50000000,
        'obesity_rate' : 0.324,
        'importations' : [],
        'exportations' : [],
    },

    126 : {
        'name' : 'Mississippi',
        'population' : 2940000,
        'population_per_px' : 363.681,
        'vegetable_production' : 1500000,
        'obesity_rate' : 0.397,
        'importations' : [],
        'exportations' : [],
    },

    127 : {
        'name' : 'Michigan',
        'population' : 10077000,
        'population_per_px' : 1013.986,
        'vegetable_production' : 7500000,
        'obesity_rate' : 0.352,
        'importations' : [],
        'exportations' : [],
    },

    128 : {
        'name' : 'Indiana',
        'population' : 6890000,
        'population_per_px' : 1011.301,
        'vegetable_production' : 36000000,
        'obesity_rate' : 0.368,
        'importations' : [],
        'exportations' : [],
    },

    129 : {
        'name' : 'Kentucky',
        'population' : 4530000,
        'population_per_px' : 568.167,
        'vegetable_production' : 10000000,
        'obesity_rate' : 0.366,
        'importations' : [],
        'exportations' : [],
    },

    130 : {
        'name' : 'Tennessee',
        'population' : 7190000,
        'population_per_px' : 1014.820,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.356,
        'importations' : [],
        'exportations' : [],
    },

    131 : {
        'name' : 'Alabama',
        'population' : 5080000,
        'population_per_px' : 546.295,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.39,
        'importations' : [],
        'exportations' : [],
    },

    132 : {
        'name' : 'Floride',
        'population' : 23370000,
        'population_per_px' : 2862.216,
        'vegetable_production' : 9000000,
        'obesity_rate' : 0.284,
        'importations' : [],
        'exportations' : [],
    },

    133 : {
        'name' : 'Ohio',
        'population' : 11880000,
        'population_per_px' : 1531.717,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.355,
        'importations' : [],
        'exportations' : [],
    },

    134 : {
        'name' : 'Virginie-Occidentale',
        'population' : 1760000,
        'population_per_px' : 404.504,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.391,
        'importations' : [],
        'exportations' : [],
    },

    135 : {
        'name' : 'Virginie',
        'population' : 8870000,
        'population_per_px' : 1049.331,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.322,
        'importations' : [],
        'exportations' : [],
    },

    136 : {
        'name' : 'Caroline du Nord',
        'population' : 11046000,
        'population_per_px' : 1259.377,
        'vegetable_production' : 23760000,
        'obesity_rate' : 0.336,
        'importations' : [],
        'exportations' : [],
    },

    137 : {
        'name' : 'Caroline du Sud',
        'population' : 5420000,
        'population_per_px' : 1061.704,
        'vegetable_production' : 1500000,
        'obesity_rate' : 0.362,
        'importations' : [],
        'exportations' : [],
    },

    138 : {
        'name' : 'Géorgie',
        'population' : 11180000,
        'population_per_px' : 1069.140,
        'vegetable_production' : 10000000,
        'obesity_rate' : 0.343,
        'importations' : [],
        'exportations' : [],
    },

    139 : {
        'name' : 'Pennsylvanie',
        'population' : 13080000,
        'population_per_px' : 1759.956,
        'vegetable_production' : 8500000,
        'obesity_rate' : 0.315,
        'importations' : [],
        'exportations' : [],
    },

    140 : {
        'name' : 'Maryland',
        'population' : 6230000,
        'population_per_px' : 3557.966,
        'vegetable_production' : 1340000,
        'obesity_rate' : 0.31,
        'importations' : [],
        'exportations' : [],
    },

    141 : {
        'name' : 'New Jersey & Delaware',
        'population' : 10020000,
        'population_per_px' : 7362.233,
        'vegetable_production' : 2400000,
        'obesity_rate' : 0.365,
        'importations' : [],
        'exportations' : [],
    },

    142 : {
        'name' : 'New York',
        'population' : 19870000,
        'population_per_px' : 2097.983,
        'vegetable_production' : 750000,
        'obesity_rate' : 0.263,
        'importations' : [],
        'exportations' : [],
    },

    143 : {
        'name' : 'Vermont',
        'population' : 650000,
        'population_per_px' : 379.229,
        'vegetable_production' : 200000,
        'obesity_rate' : 0.263,
        'importations' : [],
        'exportations' : [],
    },

    144 : {
        'name' : 'Connecticut',
        'population' : 3640000,
        'population_per_px' : 4417.475,
        'vegetable_production' : 1200000,
        'obesity_rate' : 0.292,
        'importations' : [],
        'exportations' : [],
    },

    145 : {
        'name' : 'New Hampshire',
        'population' : 1390000,
        'population_per_px' : 880.303,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.299,
        'importations' : [],
        'exportations' : [],
    },

    146 : {
        'name' : 'Massachusetts & Rhode Island',
        'population' : 7650000,
        'population_per_px' : 4757.462,
        'vegetable_production' : 2500000,
        'obesity_rate' : 0.28,
        'importations' : [],
        'exportations' : [],
    },
    
    100 : {
        'name' : None,
        'population' : 0,
        'population_per_px' : 0,
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : [],
        'exportations' : [],
    },
        
    255 : {
        'name' : None,
        'population' : 0,
        'population_per_px' : 0,
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : [],
        'exportations' : [],
    },

}

# m = 0
# n = 0
# for i in STATES :
#     m += STATES[i]["population"] + STATES[i]["population"] * STATES[i]["obesity_rate"]
#     n += STATES[i]["vegetable_production"]
# print(m)
# print(n)