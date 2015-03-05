from ga import GA
from rubiksCube import Cube

cube = Cube()
cube.scramble(20)
#print "init entropy: ", -cube.entropy()


def entropicFitness(genome):
    c = cube.copy()
    e = 55
    for m, d in genome:
        c.move(m, d)
        e = min(c.entropy(), e)
        if e == 0: break
    return -e


def clusterFitness(genome):
    c = cube.copy()
    score = 0
    for m, d in genome:
        c.move(m, d)
        cm = c.clusterMetric()
        score = cm if cm > score else score
        if score == 180: break
    return score


ga = GA()
ga.alphabet = [(face, dir) for face in range(6) for dir in range(2)]
ga.genomeLength = 30
ga.populationSize = 500
ga.mutationRate = .075
ga.fitnessFunction = clusterFitness
ga.elitism = .075

f = open("gaRun.txt", "w")


for gen in range(1000):
    max, avg = ga.run()
    print gen, max, avg
    f.write("%d %d %.2f \n" %(gen, max,avg))
f.write("%s" %ga.populationByFitness[-1])

f.close()
