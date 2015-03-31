from ga import GA
from rubiksCube import Cube

cube = Cube()
cube.moveSequence([(3, True), (2, False), (4, True),
 (3, False), (1, False), (5, True), (1, False),
 (2, False), (2, True), (0, True), (2, True),
 (0, False), (5, True), (1, False), (1, False),
(4, False), (2, True), (0, False), (0, True), (3, True)])
#print "init entropy: ", -cube.entropy()

def getBest(list):
    best = None
    score = 0
    for g in list:
        f = entropicFitness2(g)
        if f > score:
            best = g
            score = f
        elif f == score:
            pass
    return best

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

'''
ga = GA()
ga.alphabet = [(face, dir) for face in range(6) for dir in range(2)]
ga.genomeLength = 30
ga.populationSize = 750
ga.mutationRate = .01
ga.fitnessFunction = clusterFitness
ga.elitism = .005

f = open("gaRun.txt", "w")


for gen in range(1000):
    max, avg = ga.run()
    print gen, max, avg
    f.write("%d %d %.2f \n" %(gen, max,avg))


gnomes = ga2.population
bestGnome = getBest(gnomes)
f.write("%s" %bestGnome)
f.close()

print bestGnome


'''
################################################################################
################################################################################
################################################################################
################################################################################
#                                 2x2x2 Cube


c2 = Cube(2)
c2.moveSequence([(1, False), (0, False), (1, False), (5, False),
(3, True), (0, True), (0, True), (1, False), (1, False), (3, False),
(5, False), (5, False), (4, True), (3, True), (1, True), (4, True),
(2, True), (0, False), (2, False), (0, False)])
f = open("gaRun2.txt", "w")



def clusterFitness2(genome):
    c = c2.copy()
    score = 0
    for m, d in genome:
        c.move(m, d)
        cm = c.clusterMetric()
        score = cm if cm > score else score
        if score == 48: break
    return score

def entropicFitness2(genome):
    c = cube.copy()
    e = 55
    for m, d in genome:
        c.move(m, d)
        e = min(c.entropy(), e)
        if e == 0: break
    return -e


ga2 = GA()
ga2.alphabet = [(face, dir) for face in range(6) for dir in range(2)]
ga2.genomeLength = 12
ga2.populationSize = 750
ga2.mutationRate = .01
ga2.fitnessFunction = entropicFitness2
ga2.elitism = .005

for gen in range(25):
    max, avg = ga2.run()
    print gen, max, avg
    f.write("%d %d %.2f \n" %(gen, max,avg))
    #if max == 42: break

gnomes = ga2.population


bestGnome = getBest(gnomes)


f.write("%s" %bestGnome)
f.close()
print bestGnome
print "best fitness: ", entropicFitness2(bestGnome)
print c2.moveSequence(bestGnome)
print c2
