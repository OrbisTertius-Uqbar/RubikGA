from gp import GP, Genome

class One(Genome):
    childCount = 1

class Zero(Genome):
    childCount = 1

class Halt(Genome):
    childCount = 0

def fitness(genome):
    if genome.__class__ is One:
        return 1 + fitness(genome.children[0])
    elif genome.__class__ is Zero:
        return 0 + fitness(genome.children[0])
    elif genome.__class__ is Halt:
        return 0

gp = GP()
gp.alphabet = [One, Zero, Halt]

gens = 0
while gp.maxFitness < 20:
    run()
    gens += 1
print gens
