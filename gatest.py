from ga import GA

def fitness(genome):
    f = 0
    for bit in genome:
        if bit == "1": f += 1
    return f

ga = GA()
ga.fitnessFunction = fitness

gens = 0
while ga.maxFitness < 20:
    ga.run()
    gens += 1

print gens
