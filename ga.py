import random
import math

class GA(object):

    # Constants

    SELECTION_ROULETTE = 0
    SELECTION_RANK = 1


    # Config

    alphabet = ["0", "1"]
    genomeLength = 20
    crossoverRate = 1.0
    mutationRate = 0.005
    populationSize = 100
    fitnessFunciton = lambda genome: 0
    selectionMethod = SELECTION_RANK
    elitism = 0


    # State

    _population = []
    _fitnesses = None
    _ranks = None
    _maxFitness = None
    _avgFitness = None

    _populationByFitness = None
    _elite = None



    # Helpers

    def _weightedChoice(self, elements, weights):

        randomNumber = random.uniform(0, sum(weights))

        w = 0
        for i in range(len(weights)):
            w += weights[i]

            if w > randomNumber:
                return elements[i]

        # all weights are 0
        return random.choice(elements)


    def randomGenome(self, len=0):

        if len == 0:
            len = self.genomeLength

        if len == 1:
            return [random.choice(self.alphabet)]
        else:
            return [random.choice(self.alphabet)] + self.randomGenome(len - 1)


    def crossover(self, genome1, genome2):

        crossoverPoint = random.randrange(1, len(genome1))
        return (
            genome1[:crossoverPoint] + genome2[crossoverPoint:],
            genome2[:crossoverPoint] + genome1[crossoverPoint:]
        )


    def mutate(self, genome):

        return [
            (random.choice([char for char in self.alphabet if char != cur])
                if random.uniform(0, 1) < self.mutationRate else cur)
            for cur in genome
        ]


    def selectPair(self):

        weights = None

        if self.selectionMethod == self.SELECTION_ROULETTE:
            weights = self.fitnesses

        elif self.selectionMethod == self.SELECTION_RANK:
            weights = self.ranks

        if weights != None:
            return (
                self._weightedChoice(self.population, weights),
                self._weightedChoice(self.population, weights)
            )


    # Properties

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, population):
        self._population = population
        self._fitnesses = None
        self._maxFitness = None
        self._avgFitness = None
        self._ranks = None
        self._populationByFitness = None
        self._elite = None

    @property
    def fitnesses(self):
        if self._fitnesses == None:
            self._fitnesses = [self.fitnessFunction(g) for g in self.population]
        return self._fitnesses

    @property
    def maxFitness(self):
        if self._maxFitness == None:
            self._maxFitness = max(self.fitnesses)
        return self._maxFitness

    @property
    def avgFitness(self):
        if self._avgFitness == None:
            self._avgFitness = float(sum(self.fitnesses)) / len(self.fitnesses)
        return self._avgFitness

    @property
    def ranks(self):
        if self._ranks == None:
            orderedByRank = self.populationByFitness
            self._ranks = [orderedByRank.index(g) + 1 for g in self.population]
        return self._ranks

    @property
    def populationByFitness(self):
        if self._populationByFitness == None:
            tuples = [(g, self.fitnessForGenome(g)) for g in self.population]
            tuples.sort(
                lambda a, b: 1 if a[1] > b[1] else -1 if a[1] < b[1] else 0
            )
            self._populationByFitness = [g for (g, fitnessValue) in tuples]
        return self._populationByFitness

    @property
    def elite(self):
        if self._elite == None:
            c = int(round(self.populationSize * self.elitism))
            if c % 2 == 1: c += 1
            c = min([c, self.populationSize])
            if c == 0:
                self._elite = []
            else:
                self._elite = self.populationByFitness[-c:]
        return self._elite


    def genomeForFitness(self, fitness):
        try:
            return self.population[self.fitnesses.index(fitness)]
        except ValueError:
            return None


    def fitnessForGenome(self, genome):

        try:
            return self.fitnesses[self.population.index(genome)]
        except ValueError:
            return None


    # Methods

    def useRandomPopulation(self):

        self.population = [
            self.randomGenome() for i in range(self.populationSize)
        ]


    def run(self, generations=1):

        for generation in range(generations):

            if len(self.population) == 0:

                self.useRandomPopulation()

            else:

                newPopulation = [g for g in self.elite]

                while len(newPopulation) <= self.populationSize:

                    genome1, genome2 = self.selectPair()

                    if random.uniform(0, 1) < self.crossoverRate:
                        genome1, genome2 = self.crossover(genome1, genome2)

                    newPopulation.append(self.mutate(genome1))
                    newPopulation.append(self.mutate(genome2))

                self.population = newPopulation

        return self.maxFitness, self.avgFitness
