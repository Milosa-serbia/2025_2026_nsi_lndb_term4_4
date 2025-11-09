from random import*

deaths = 0
infected = 0
population = 340000000
trust_meter = 100


def create_virus(difficulty, name) :

    if difficulty == 10 :
        return {"name" : name,
                "propagation_rate" : 10,
                "death_rate" : 10,
                "curing_resistence" : 10,
                "survival_rate" : 10,
                "mutations" : True}
    
    if difficulty > 2 :
        return {"name" : name,
                "propagation_rate" : randint(1, difficulty),
                "death_rate" : randint(1, difficulty),
                "cure_resistance" : randint(1, difficulty),
                "survival_rate" : randint(1, difficulty),
                "mutations" : True}
    
    else :
        return {"name" : name,
                "propagation_rate" : randint(1, difficulty),
                "death_rate" : randint(1, difficulty),
                "cure_resistance" : randint(1, difficulty),
                "survival_rate" : randint(1, difficulty),
                "mutations" : False}
        
