import random
import math

class GA:

    # Constants

    SELECTION_ROULETTE = 0

    # Config

    alphabet = ["0", "1"]
    genomeLength = 20
    crossoverRate = 1.0
    mutationRate = 0.005
    populationSize = 100
    selectionMethod = SELECTION_ROULETTE
    fitnessFunciton = lambda genome: 0


    # State

    population = []
    fitnesses = []
    maxFitness = 0
    avgFitness = 0


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


    def randomGenome(self, length=0):

        if length == 0:
            length = self.genomeLength

        if length == 1:
            return random.choice(self.alphabet)
        else:
            return random.choice(self.alphabet) + self.randomGenome(length - 1)


    def crossover(self, genome1, genome2):

        crossoverPoint = random.randrange(1, len(genome1))
        return (
            genome1[:crossoverPoint] + genome2[crossoverPoint:],
            genome2[:crossoverPoint] + genome1[crossoverPoint:]
        )


    def mutate(self, genome):

        return ''.join([
            (random.choice([char for char in self.alphabet if char != cur])
                if random.uniform(0, 1) < self.mutationRate else cur)
            for cur in genome
        ])


    def selectPair(self):

        if self.selectionMethod == self.SELECTION_ROULETTE:

            return (
                self._weightedChoice(self.population, self.fitnesses),
                self._weightedChoice(self.population, self.fitnesses)
            )


    # Methods

    def setPopulation(self, population):

        self.population = population
        self.fitnesses = [self.fitnessFunction(genome) for genome in population]
        self.maxFitness = max(self.fitnesses)
        self.avgFitness = float(sum(self.fitnesses)) / len(self.fitnesses)


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


    def useRandomPopulation(self):

        self.setPopulation([self.randomGenome() for i in range(self.populationSize)])


    def run(self, generations=1):

        for generation in range(generations):

            if len(self.population) is 0:

                self.useRandomPopulation()

            else:

                newPopulation = []

                for i in range(int(math.ceil(self.populationSize/2.0))):

                    genome1, genome2 = self.selectPair()

                    if random.uniform(0, 1) < self.crossoverRate:
                        genome1, genome2 = self.crossover(genome1, genome2)

                    newPopulation.append(self.mutate(genome1))
                    newPopulation.append(self.mutate(genome2))

                self.setPopulation(newPopulation)

        return self.maxFitness, self.avgFitness
