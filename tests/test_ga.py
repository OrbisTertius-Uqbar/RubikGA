import unittest, copy
from ga import GA

class TestGA(unittest.TestCase):

    def setUp(self):
        ga = GA()
        ga.alphabet = ['0', '1']
        ga.genomeLength = 20
        ga.crossoverRate = 1.0
        ga.mutationRate = 0.005
        ga.populationSize = 100
        ga.fitnessFunction = lambda g: len([bit for bit in g if bit == '1'])
        ga.selectionMethod = GA.SELECTION_ROULETTE
        ga.elitism = 0
        self.ga = ga

    def test_weightedChoice(self):
        els     = [1,  2,  3,  4, 5, 6, 7, 8,  9, 10]
        weights = [10, 20, 30, 5, 5, 1, 4, 25, 0, 0 ]
        choices = []
        for i in range(1000):
            choices.append(self.ga._weightedChoice(els, weights))

        passed = True
        totalWeight = float(sum(weights))
        choicesLen = float(len(choices))
        for el in els:
            expectedProb = weights[els.index(el)] / totalWeight
            errorMargin = .03 if expectedProb > 0 else 0
            testedProb = len([c for c in choices if c == el]) / choicesLen
            self.assertLessEqual(abs(expectedProb - testedProb), errorMargin,
                'weightedChoice resulted in probablity %.4f, expected %.4f'
                % (testedProb, expectedProb))

    def test_randomGenome(self):
        for i in range(100):
            rg = self.ga.randomGenome()
            self.assertEqual(len(rg), self.ga.genomeLength,
                'randomGenome producing genome of incorrect length')
            for char in rg:
                self.assertIn(char, self.ga.alphabet)

    def test_randomPopulation(self):
        self.ga.useRandomPopulation()
        self.assertEqual(len(self.ga.population), self.ga.populationSize)

    def test_fitnesses(self):
        self.ga.elitism = 0.10
        self.ga.population = pop = [
            (['1'] * l) + (['0'] * (20 - l)) for l in range(0, 20)
        ]
        self.assertEqual(self.ga.fitnesses, [i for i in range(0, 20)],
            'ga.fitness not returning expected value')
        self.assertEqual(self.ga.maxFitness, 19,
            'ga.maxFitness not returning expected value')
        self.assertEqual(self.ga.avgFitness, sum(range(0, 20)) / 20.0,
            'ga.avgFitness not returning expected value')
        self.assertEqual(self.ga.genomeForFitness(10), pop[10],
            'ga.genomeForFitness not returning expected value')
        self.assertEqual(self.ga.fitnessForGenome(pop[10]), 10,
            'ga.fitnessForGenome not returning expected value')
        self.assertEqual(self.ga.ranks, range(1, 21),
            'ga.ranks not returning expected value')
        self.assertEqual(self.ga.populationByFitness, pop,
            'ga.populationByFitness not returning expected value')
        self.assertEqual(self.ga.elite, pop[-10:], # 10% of ga.populationSize
            'ga.elite not returning expected value')

        self.ga.elitism = 0

    def test_selection(self):
        self.ga.population = pop = [
            (['1'] * l) + (['0'] * (20 - l)) for l in range(0, 21)
        ]

        self.ga.selectionMethod = GA.SELECTION_RANK
        choices = []
        for i in range(1000):
            a, b = self.ga.selectPair()
            choices.append(a)
            choices.append(b)
        rank = 1
        totalRank = float(sum(range(1, 22)))
        choicesLen = float(len(choices))
        for el in pop:
            expectedProb = rank / totalRank
            errorMargin = .02
            testedProb = len([c for c in choices if c == el]) / choicesLen
            self.assertLessEqual(abs(expectedProb - testedProb), errorMargin,
                'rank selection picked genome with prob. %.4f, expected %.4f'
                % (testedProb, expectedProb))
            rank += 1

        self.ga.selectionMethod = GA.SELECTION_ROULETTE
        choices = []
        for i in range(1000):
            a, b = self.ga.selectPair()
            choices.append(a)
            choices.append(b)
        totalFitness = float(sum(self.ga.fitnesses))
        choicesLen = float(len(choices))
        for el in pop:
            expectedProb = self.ga.fitnessForGenome(el) / totalFitness
            errorMargin = .02
            testedProb = len([c for c in choices if c == el]) / choicesLen
            self.assertLessEqual(abs(expectedProb - testedProb), errorMargin,
                'roulette selection picked genome with prob %.4f, expected %.4f'
                % (testedProb, expectedProb))

        self.ga.selectionMethod = GA.SELECTION_ROULETTE

    def test_crossover(self):
        self.ga.useRandomPopulation()

        for trial in range(100):
            a , b  = self.ga.selectPair()
            a1, b1 = self.ga.crossover(a, b)
            success = False
            for i in range(1, len(a)):
                if a1 == a[:i] + b[i:] and b1 == b[:i] + a[i:] \
                or a1 == b[:i] + a[i:] and b1 == a[:i] + b[i:]:
                    success = True
            self.assertTrue(success, 'crossover not working as expected')

    def test_mutation(self):
        for mRate in [0, 0.001, 0.01, 0.1, 0.005, 0.25, 1]:
            self.ga.mutationRate = mRate
            trials = 2000
            totalChars = float(self.ga.genomeLength * trials)
            mutatedChars = 0
            for trial in range(trials):
                g = self.ga.randomGenome()
                m = self.ga.mutate(g)
                for i in range(len(g)):
                    if g[i] != m[i]: mutatedChars += 1

            errorMargin = .005 if mRate > 0 else 1 if mRate == 1 else 0
            testedProb = mutatedChars / totalChars
            self.assertLessEqual(abs(mRate - testedProb), errorMargin,
                'mutated with probablity of %.4f, expected %.4f'
                % (testedProb, mRate))

        self.ga.mutationRate = 0.005

    def test_run(self):
        for elitism in [True, False]:
            self.ga.elitism = .70 if elitism else 0
            self.ga.population = []
            self.ga.run()
            prev = copy.deepcopy(self.ga.populationByFitness)

            for gen in range(100):
                self.ga.run()
                self.assertEqual(len(prev), len(self.ga.population),
                    'population size not constant')
                if elitism:
                    for g in prev[-70:]:
                        self.assertIn(g, self.ga.population,
                            'elitism not working as expected')
                prev = copy.deepcopy(self.ga.populationByFitness)

        self.ga.elitisim = 0

        self.ga.population = []
        maxFitness, __ = self.ga.run(1000)
        self.assertEqual(maxFitness, 20,
            'did not evolve all-ones genome')
        self.assertEqual(self.ga.genomeForFitness(maxFitness), ['1'] * 20,
            'did not evolve expected genome')
