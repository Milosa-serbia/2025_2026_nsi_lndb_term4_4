class KinderState :
    def __init__(self, name, population, population_per_px, vegetable_production, obesity_rate, importations, exportations) :
        self.name = name
        self.population = population
        self.alive_population = population
        self.population_per_px = population_per_px
        self.open_border = True
        self.lockdown = False
        self.initial_vegetable_production = vegetable_production
        self.vegetable_production = vegetable_production
        self.food_ressources = 0
        self.obesity_rate = obesity_rate
        self.importations = importations
        self.exportations = exportations
        


STATES = {
    101 : {
        'name' : 'Washington',
        'population' : 8115100,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.28,
        'importations' : {},
        'exportations' : {},
    },
    
    102 : {
        'name' : 'Oregon',
        'population' : 4291090,
        'vegetable_production' : 1230000,
        'obesity_rate' : 0.281,
        'importations' : {},
        'exportations' : {},
    },

    103 : {
        'name' : 'Californie',
        'population' : 39431000,
        'vegetable_production' : 35000000,
        'obesity_rate' : 0.303,
        'importations' : {},
        'exportations' : {},
    },

    104 : {
        'name' : 'Idaho',
        'population' : 1967000,
        'vegetable_production' : 3500000,
        'obesity_rate' : 0.311,
        'importations' : {},
        'exportations' : {},
    },

    105 : {
        'name' : 'Nevada',
        'population' : 3265000,
        'vegetable_production' : 900000,
        'obesity_rate' : 0.287,
        'importations' : {},
        'exportations' : {},
    },

    106 : {
        'name' : 'Montana',
        'population' : 1153000,
        'vegetable_production' : 670500,
        'obesity_rate' : 0.285,
        'importations' : {},
        'exportations' : {},
    },

    107 : {
        'name' : 'Wyoming',
        'population' : 584000,
        'vegetable_production' : 400000,
        'obesity_rate' : 0.307,
        'importations' : {},
        'exportations' : {},
    },

    108 : {
        'name' : 'Utah',
        'population' : 3427000,
        'vegetable_production' : 800000,
        'obesity_rate' : 0.286,
        'importations' : {},
        'exportations' : {},
    },

    109 : {
        'name' : 'Arizona',
        'population' : 7600000,
        'vegetable_production' : 1400000,
        'obesity_rate' : 0.309,
        'importations' : {},
        'exportations' : {},
    },

    110 : {
        'name' : 'Colorado',
        'population' : 6023000,
        'vegetable_production' : 5500000,
        'obesity_rate' : 0.242,
        'importations' : {},
        'exportations' : {},
    },

    111 : {
        'name' : 'Nouveau-Mexique',
        'population' : 2110000,
        'vegetable_production' : 1750000,
        'obesity_rate' : 0.309,
        'importations' : {},
        'exportations' : {},
    },

    112 : {
        'name' : 'Dakota du Nord',
        'population' : 783000,
        'vegetable_production' : 1500000,
        'obesity_rate' : 0.331,
        'importations' : {},
        'exportations' : {},
    },

    113 : {
        'name' : 'Dakota du Sud',
        'population' : 919000,
        'vegetable_production' : 1700000,
        'obesity_rate' : 0.332,
        'importations' : {},
        'exportations' : {},
    },

    114 : {
        'name' : 'Nebraska',
        'population' : 1973000,
        'vegetable_production' : 29000000,
        'obesity_rate' : 0.34,
        'importations' : {},
        'exportations' : {'Californie' : 10000000},
    },

    115 : {
        'name' : 'Kansas',
        'population' : 2943000,
        'vegetable_production' : 63000000,
        'obesity_rate' : 0.353,
        'importations' : {},
        'exportations' : {'Oklahoma' : 2100000},
    },

    116 : {
        'name' : 'Oklahoma',
        'population' : 4060000,
        'vegetable_production' : 4500000,
        'obesity_rate' : 0.364,
        'importations' : {},
        'exportations' : {},
    },

    117 : {
        'name' : 'Texas',
        'population' : 31290000,
        'vegetable_production' : 60000000,
        'obesity_rate' : 0.358,
        'importations' : {},
        'exportations' : {'Californie' : 7000000, 'Nevada' : 3500000},
    },

    118 : {
        'name' : 'Minnesota',
        'population' : 5787000,
        'vegetable_production' : 35000000,
        'obesity_rate' : 0.307,
        'importations' : {},
        'exportations' : {'Missouri' : 4000000, 'Arkansas' : 1500000},
    },

    119 : {
        'name' : 'Iowa',
        'population' : 3200000,
        'vegetable_production' : 33470000,
        'obesity_rate' : 0.365,
        'importations' : {},
        'exportations' : {'Washington' : 2500000, 'Oregon' : 4400000, 'Louisiane' : 4500000},
    },

    120 : {
        'name' : 'Missouri',
        'population' : 6217000,
        'vegetable_production' : 5000000,
        'obesity_rate' : 0.34,
        'importations' : {},
        'exportations' : {},
    },

    121 : {
        'name' : 'Arkansas',
        'population' : 3080000,
        'vegetable_production' : 3000000,
        'obesity_rate' : 0.364,
        'importations' : {},
        'exportations' : {},
    },

    122 : {
        'name' : 'Louisiane',
        'population' : 4540000,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.381,
        'importations' : {},
        'exportations' : {},
    },

    123 : {
        'name' : 'Maine',
        'population' : 1380000,
        'vegetable_production' : 600000,
        'obesity_rate' : 0.31,
        'importations' : {},
        'exportations' : {},
    },

    124 : {
        'name' : 'Wisconsin',
        'population' : 5890000,
        'vegetable_production' : 30000000,
        'obesity_rate' : 0.323,
        'importations' : {},
        'exportations' : {'Michigan' : 6000000, 'Montana' : 1000000, 'Maine' : 1500000, 'Mississippi' : 3000000},
    },

    125 : {
        'name' : 'Illinois',
        'population' : 12710000,
        'vegetable_production' : 50000000,
        'obesity_rate' : 0.324,
        'importations' : {},
        'exportations' : {},
    },

    126 : {
        'name' : 'Mississippi',
        'population' : 2940000,
        'vegetable_production' : 1500000,
        'obesity_rate' : 0.397,
        'importations' : {},
        'exportations' : {},
    },

    127 : {
        'name' : 'Michigan',
        'population' : 10077000,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.352,
        'importations' : {},
        'exportations' : {},
    },

    128 : {
        'name' : 'Indiana',
        'population' : 6890000,
        'vegetable_production' : 36000000,
        'obesity_rate' : 0.368,
        'importations' : {},
        'exportations' : {'Arizona' : 9000000, 'Colorado' : 2000000, 'Nouveau-Mexique' : 1300000},
    },

    129 : {
        'name' : 'Kentucky',
        'population' : 4530000,
        'vegetable_production' : 10000000,
        'obesity_rate' : 0.366,
        'importations' : {},
        'exportations' : {'Tennessee' : 2000000},
    },

    130 : { 
        'name' : 'Tennessee',
        'population' : 7190000,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.356,
        'importations' : {},
        'exportations' : {},
    },

    131 : {
        'name' : 'Alabama',
        'population' : 5080000,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.39,
        'importations' : {},
        'exportations' : {},
    },
# Reprendre le travail à partir d'ici.
    132 : {
        'name' : 'Floride',
        'population' : 23370000,
        'vegetable_production' : 9000000,
        'obesity_rate' : 0.284,
        'importations' : {},
        'exportations' : {},
    },

    133 : {
        'name' : 'Ohio',
        'population' : 11880000,
        'vegetable_production' : 8000000,
        'obesity_rate' : 0.355,
        'importations' : {},
        'exportations' : {},
    },

    134 : {
        'name' : 'Virginie-Occidentale',
        'population' : 1760000,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.391,
        'importations' : {},
        'exportations' : {},
    },

    135 : {
        'name' : 'Virginie',
        'population' : 8870000,
        'vegetable_production' : 2000000,
        'obesity_rate' : 0.322,
        'importations' : {},
        'exportations' : {},
    },

    136 : {
        'name' : 'Caroline du Nord',
        'population' : 11046000,
        'vegetable_production' : 23760000,
        'obesity_rate' : 0.336,
        'importations' : {},
        'exportations' : {'Wyoming' : 500000, 'Utah' : 4000000},
    },

    137 : {
        'name' : 'Caroline du Sud',
        'population' : 5420000,
        'vegetable_production' : 1500000,
        'obesity_rate' : 0.362,
        'importations' : {},
        'exportations' : {},
    },

    138 : {
        'name' : 'Géorgie',
        'population' : 11180000,
        'vegetable_production' : 10000000,
        'obesity_rate' : 0.343,
        'importations' : {},
        'exportations' : {},
    },

    139 : {
        'name' : 'Pennsylvanie',
        'population' : 13080000,
        'vegetable_production' : 8500000,
        'obesity_rate' : 0.315,
        'importations' : {},
        'exportations' : {},
    },

    140 : {
        'name' : 'Maryland',
        'population' : 6230000,
        'vegetable_production' : 1340000,
        'obesity_rate' : 0.31,
        'importations' : {},
        'exportations' : {},
    },

    141 : {
        'name' : 'New Jersey & Delaware',
        'population' : 10020000,
        'vegetable_production' : 2400000,
        'obesity_rate' : 0.365,
        'importations' : {},
        'exportations' : {},
    },

    142 : {
        'name' : 'New York',
        'population' : 19870000,
        'vegetable_production' : 750000,
        'obesity_rate' : 0.263,
        'importations' : {},
        'exportations' : {},
    },

    143 : {
        'name' : 'Vermont',
        'population' : 650000,
        'vegetable_production' : 200000,
        'obesity_rate' : 0.263,
        'importations' : {},
        'exportations' : {},
    },

    144 : {
        'name' : 'Connecticut',
        'population' : 3640000,
        'vegetable_production' : 1200000,
        'obesity_rate' : 0.292,
        'importations' : {},
        'exportations' : {},
    },

    145 : {
        'name' : 'New Hampshire',
        'population' : 1390000,
        'vegetable_production' : 1000000,
        'obesity_rate' : 0.299,
        'importations' : {},
        'exportations' : {},
    },

    146 : {
        'name' : 'Massachusetts & Rhode Island',
        'population' : 7650000,
        'vegetable_production' : 2500000,
        'obesity_rate' : 0.28,
        'importations' : {},
        'exportations' : {},
    },
    
    100 : {
        'name' : None,
        'population' : 1,    
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : {},
        'exportations' : {},
    },
        
    255 : {
        'name' : None,
        'population' : 1,    
        'vegetable_production' : 0,
        'obesity_rate' : 0,
        'importations' : {},
        'exportations' : {},
    },

}

# m = 0
# n = 0
# for i in STATES :
#     m += STATES[i]["population"] + STATES[i]["population"] * STATES[i]["obesity_rate"]
#     n += STATES[i]["vegetable_production"]
# print(m)
# print(n)