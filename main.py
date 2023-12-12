import numpy as np
import GeneticCurveEstimator, FitnessEvaluator
import matplotlib.pyplot as plt

def create_noisy_ADSR_curve(A, D, S, R, length):
    """
    Generates a noisy ADSR curve.

    Args:
        A (float): Attack time.
        D (float): Decay time.
        S (float): Sustain level.
        R (float): Release time.
        length (int): Length of the curve.

    Returns:
        numpy array: Noisy ADSR curve.
    """
    # Calculate the time for each segment
    total_time = A + D + R
    attack_time = int(A/total_time * length)
    decay_time = int(D/total_time * length)
    release_time = int(R/total_time * length)

    # Generate ADSR curve
    curve = np.zeros(length)
    curve[0 : attack_time] = np.linspace(0, 1, attack_time)
    curve[attack_time : attack_time+decay_time] = np.linspace(1, S, decay_time)
    curve[attack_time+decay_time : attack_time+decay_time+release_time] = np.linspace(S, 0, release_time)

    # Add noise to the curve
    noise = np.random.normal(0, 0.005, length)
    curve = curve + noise

    return curve

def main():
    # Generate target curve
    target_curve = create_noisy_ADSR_curve(np.random.random(), np.random.random(), np.random.random(), np.random.random(), 100)

    # Initialize fitness evaluator
    fitness_evaluator = FitnessEvaluator.FitnessEvaluator(
        target_curve=target_curve,
        curve_type="ADSR",
    )

    # Initialize genetic curve estimator
    genetic_curve_estimator = GeneticCurveEstimator.GeneticCurveEstimator(
        target_curve=target_curve,
        curve_type="ADSR",
        population_size=100,
        mutation_rate=0.1,
        max_generation=1000,
        fitness_evaluator=fitness_evaluator,
    )

    # Generate curve parameters
    curve_param = genetic_curve_estimator.generate(generations=1000)

    # Generate curve
    curve = fitness_evaluator.generate_ADSR(
        curve_param[0], curve_param[1], curve_param[2], curve_param[3], 100
    )

    # Plot target curve and generated curve
    plt.plot(target_curve, label="Target curve")
    plt.plot(curve, label="Generated curve")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()