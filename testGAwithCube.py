from ga import GA
from rubiksCube import Cube

cube = Cube()
cube.scramble(20)
print "init entropy: ", -cube.entropy()

def fitness(genome):
    c = cube.copy()
    e = 55
    for m, d in genome:
        c.move(m, d)
        e = min(c.entropy(), e)
        if e == 0: break
    return -e

ga = GA()
ga.alphabet = [(face, dir) for face in range(6) for dir in range(2)]
ga.genomeLength = 50
ga.populationSize = 500
ga.mutationRate = .075
ga.fitnessFunction = fitness
ga.elitism = .075

f = open("garun.txt", "w")


for gen in range(10000):
    max, avg = ga.run()
    print gen, max, avg
    f.write("%d %d %.2f \n" %(gen, max,avg))

f.close()
