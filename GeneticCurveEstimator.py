import random

class GeneticCurveEstimator:
    """
    Estimates the curve parameter using genetic algorithm.

    Attributes:

        target_curve (numpy array): List of points that the curve should match.
        curve_type (string): Type of curve to be used for fitness evaluation.
        population_size (int): Number of curves in the population.
        mutation_rate (float): Probability of mutation.
        max_generation (int): Maximum number of generations.
        fitness_evaluator (FitnessEvaluator): Fitness evaluator.
    """

    def __init__(self, target_curve, curve_type, population_size, mutation_rate, max_generation, fitness_evaluator):
        """
        Initializes the genetic curve estimator.

        Args:
            target_curve (numpy array): List of points that the curve should match.
            curve_type (string): Type of curve to be used for fitness evaluation.
            population_size (int): Number of curves in the population.
            mutation_rate (float): Probability of mutation.
            max_generation (int): Maximum number of generations.
            fitness_evaluator (FitnessEvaluator): Fitness evaluator.
        """
        self.target_curve = target_curve
        self.curve_type = curve_type
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generation = max_generation
        self.fitness_evaluator = fitness_evaluator
        self._population = []

    def generate(self, generations=1000):
        """
        Generates curve parameters for fitting a signal using genetic algorithm.

        Parameters:
            generations (int): Number of generations for evolution.

        Returns:
            best_chord_sequence (list): Curve parameters with the highest fitness.
        """

        self._initialise_population()
        for _ in range(generations):
            parents = self._select_parents()
            new_population = self._create_new_population(parents)
            self._population = new_population
        best_curve_param = (
            self.fitness_evaluator.get_curve_param_with_highest_fitness(
                self._population
            )
        )
        return best_curve_param
    
    def _initialise_population(self):
        """
        Initializes the population with random curve parameters.
        """
        for i in range(self.population_size):
            self._population.append(self._get_random_curve_param())

    def _get_random_curve_param(self):
        """
        Returns a random curve parameter based on the curve type.

        Returns:
            numpy array: Curve parameter.
        """
        if self.curve_type == "ADSR":
            return self._get_random_ADSR_curve_param()
        else:
            raise ValueError("Invalid curve type.")
        
    def _get_random_ADSR_curve_param(self):
        """
        Returns random curve parameter for ADSR curve.

        Returns:
            numpy array: Curve parameter.
        """
        return [
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        ]

    def _select_parents(self):
        """
        Selects parent sequences for breeding based on fitness.

        Returns:
            list: Selected parent chord sequences.
        """

        fitness_values = [
            self.fitness_evaluator.evaluate(seq) for seq in self._population
        ]
        return random.choices(
            self._population, weights=fitness_values, k=self.population_size
        )
    
    def _create_new_population(self, parents):
        """
        Creates a new population from the selected parents.

        Args:
            parents (list): Selected parent chord sequences.
        """
        new_population = []
        for i in range(0, self.population_size, 2):
            child1, child2 = self._crossover(
                parents[i], parents[i + 1]
            ), self._crossover(parents[i + 1], parents[i])
            child1 = self._mutate(child1)
            child2 = self._mutate(child2)
            new_population.extend([child1, child2])
        return new_population
    
    def _crossover(self, parent1, parent2):
        """
        Combines two parent sequences into a new child sequence using one-point
        crossover.

        Parameters:
            parent1 (list): First parent sequence.
            parent2 (list): Second parent sequence.

        Returns:
            list: Resulting child chord sequence.
        """
        cut_index = random.randint(1, len(parent1) - 1)
        return parent1[:cut_index] + parent2[cut_index:]

    def _mutate(self, curve_param):
        """
        Mutates curve parameters in the sequence based on mutation rate.

        Parameters:
            curve_param (list): Curve parameters to mutate.

        Returns:
            list: Mutated curve parameters
        """
        if random.random() < self.mutation_rate:
            mutation_index = random.randint(0, len(curve_param) - 1)
            curve_param[mutation_index] = random.uniform(0, 1)
        return curve_param
    

