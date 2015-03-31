from ga import GA
import copy, random

class Genome:

    childCount = 0
    _parent = None

    def __init__(self, children=[]):
        self._children = children

        for child in children:
            child._parent = self

    def copy(self):
        return copy.deepcopy(self)

    def getChild(self, i):
        return self._children[i]

    def setChild(self, i, child):
        self._children[i] = child
        child.parent = self

    def getParent(self):
        return self._parent

    def randomSubtree(self):

        if self.childCount == 0: return None

        selected = None
        n = 1
        for node in self:
            if node is self: continue

            if random.uniform(0, 1) < 1.0 / n:
                selected = node

            n += 1

        return selected

    def replaceSubtree(self, toReplace, newSubtree):

        parent = toReplace.getParent()
        parent.setChild(parent._children.index(toReplace), newSubtree)

    def __iter__(self):
        return GenomeIterator(self)

    class GenomeIterator:

        def __init__(self, genome):

            self.stack = []
            self.genome = genome
            self.first = True

        def next(self):

            if self.first:
                self.stack.append((self.genome, 0))
                self.first = False
                return self.genome

            while len(self.stack) > 0:
                parent, index = self.stack[-1]

                if index < parent.childCount:
                    child = parent.getChild(index)
                    self.stack[-1] = (parent, index + 1)
                    self.stack.append((child, 0))
                    return child

                else:
                    self.stack.pop()

            raise StopIteration()


class GP(GA):

    @property
    def alphabet(self):
        return self._alphabet

    @alphabet.setter
    def alphabet(self, alphabet):
        self._alphabet = alphabet
        self._terminals = [node for node in alphabet if node.childCount == 0]


    def randomGenome(self, maxDepth=3, alphabet=None):

        if alphabet == none: alphabet = self.alphabet

        if maxDepth == 1:
            return random.choice(self._terminals)()

        else:
            node = random.choice(self.alphabet)
            childCount = node.childCount
            return node(
                [self.randomGenome(maxDepth - 1) for i in range(childCount)]
            )


    def crossover(self, genome1, genome2):

        genome1, genome2 = (genome1.copy(), genome2.copy())

        if genome1.childCount != 0 and genome2.childCount != 0:

            sub1 = genome1.randomSubtree()
            sub2 = genome2.randomSubtree()

            genome1.replaceSubtree(sub1, sub2)
            genome2.replaceSubtree(sub2, sub1)

        return genome1, genome2


    def mutate(self, genome):

        for node in genome:
            if random.uniform(0, 1) < self.mutationRate:
                # TODO
                pass
