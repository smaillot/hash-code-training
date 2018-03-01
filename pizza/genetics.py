import numpy as np
from tqdm import trange

class BRKGA_solver:

    def __init__(self, inputPb, generationSize, crossoverProba, eliteRate, mutantRate, chromosomeShape):
        self.inputPb = inputPb
        self.generationSize = generationSize
        self.crossoverProba = crossoverProba
        self.eliteSize = int(eliteRate * generationSize)
        self.mutantSize = int(mutantRate * generationSize)
        self.crossoverSize = generationSize - self.mutantSize - self.eliteSize
        self.chromosomeShape = chromosomeShape

    def decoder(self, ch):
        #TODO: Implementer le decodeur
        return ch

    def score(self, solution):
        #TODO: Implementer la fonction de score
        return np.mean(solution)

    def mate(self, ch1, ch2):
        rand = np.random.random(ch1.shape)
        result = np.copy(ch1)
        result[rand > self.crossoverProba] = ch2[rand > self.crossoverProba]
        return result

    def randomMating(self, ch, *args):
        elites = args[0]
        commons = args[1]
        ch1 = elites[np.random.randint(0, elites.shape[0])]
        ch2 = commons[np.random.randint(0, commons.shape[0])]
        return self.mate(ch1, ch2)

    def chromosomeScore(self, ch):
        solution = self.decoder(ch)
        return self.score(solution)

    def initGeneration(self):
        return np.random.random((self.generationSize, ) + self.chromosomeShape)

    def nextGen(self, gen):
        scores = np.apply_along_axis(self.chromosomeScore, 1, gen)
        indices = np.flip(np.argsort(scores), 0)
        elites = gen[indices][: self.eliteSize]
        
        commons = gen[indices][self.eliteSize :]

        crossover = np.zeros((self.crossoverSize	, ) + self.chromosomeShape)

        crossover = np.apply_along_axis(self.randomMating, 1, crossover, elites, commons)

        mutants = np.random.random((self.mutantSize, ) + self.chromosomeShape)
        newGen = np.concatenate((elites, crossover, mutants))
        return (newGen, scores[indices][0])
    
    def computeGenerations(self, N):
        gen = self.initGeneration()
        t = trange(N)
        for i in t:
            gen, score = self.nextGen(gen)
            t.set_description('GEN %i, Score: %f' % (i+1, score))
        return (gen[0], score)
    

solver = BRKGA_solver(0, 1000, 0.7, 0.1, 0.2, (100,))
if __name__ == "__main__":
    res = solver.computeGenerations(1000)
    print("Meilleur chromosome: ", res[0])
    print("Score: ", res[1])


    

    