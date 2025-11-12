class KinderState :
    def __init__(self, name, population, vegetable_production, obesity_rate, importations, exportations) :
        self.name = name
        self.alive_population = population
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
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },
    
    102 : {
        'name' : 'Oregon',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    103 : {
        'name' : 'Californie',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    104 : {
        'name' : 'Idaho',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    105 : {
        'name' : 'Nevada',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    106 : {
        'name' : 'Montana',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    107 : {
        'name' : 'Wyoming',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    108 : {
        'name' : 'Utah',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    109 : {
        'name' : 'Arizona',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    110 : {
        'name' : 'Colorado',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    111 : {
        'name' : 'Nouveau-Mexique',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    112 : {
        'name' : 'Dakota du Nord',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    113 : {
        'name' : 'Dakota du Sud',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    114 : {
        'name' : 'Nebraska',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    115 : {
        'name' : 'Kansas',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    116 : {
        'name' : 'Oklahoma',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    117 : {
        'name' : 'Texas',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    118 : {
        'name' : 'Minnesota',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    119 : {
        'name' : 'Iowa',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    120 : {
        'name' : 'Missouri',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    121 : {
        'name' : 'Arkansas',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    122 : {
        'name' : 'Louisiane',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    123 : {
        'name' : 'Maine',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    124 : {
        'name' : 'Wisconsin',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    125 : {
        'name' : 'Illinois',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    126 : {
        'name' : 'Mississippi',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    127 : {
        'name' : 'Michigan',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    128 : {
        'name' : 'Indiana',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    129 : {
        'name' : 'Kentucky',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    130 : {
        'name' : 'Tennessee',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    131 : {
        'name' : 'Alabama',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    132 : {
        'name' : 'Floride',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    133 : {
        'name' : 'Ohio',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    134 : {
        'name' : 'Virginie-Occidentale',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    135 : {
        'name' : 'Virginie',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    136 : {
        'name' : 'Caroline du Nord',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    137 : {
        'name' : 'Caroline du Sud',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    138 : {
        'name' : 'Géorgie',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    139 : {
        'name' : 'Pennsylvanie',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    140 : {
        'name' : 'Maryland',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    141 : {
        'name' : 'New Jersey & Delaware',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    142 : {
        'name' : 'New York',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    143 : {
        'name' : 'Vermont',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    144 : {
        'name' : 'Connecticut',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    145 : {
        'name' : 'New Hampshire',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

    146 : {
        'name' : 'Massachusetts & Rhode Island',
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },
    
    100 : {
        'name' : None,
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },
        
    255 : {
        'name' : None,
        'population' : None,
        'vegetable_production' : None,
        'obesity_rate' : None,
        'importations' : [],
        'exportations' : [],
    },

}
