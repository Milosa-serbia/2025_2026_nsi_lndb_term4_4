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
        self.exportations = exportations
        
        

STATES = {
    
}