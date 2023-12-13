import numpy as np

class FitnessEvaluator:
    """
    Evaluates the fitness of a curve based on how close it is to the target curve.

    Attributes:
        target_curve (numpy array): List of points that the curve should match.
        curve_type (string): Type of curve to be used for fitness evaluation.
    """

    def __init__(self, target_curve, curve_type):
        """
        Initializes the fitness evaluator.

        Args:
            target_curve (numpy array): List of points that the curve should match.
            curve_type (string): Type of curve to be used for fitness evaluation.
        """
        self.target_curve = target_curve
        self.curve_type = curve_type
        self.length = np.size(target_curve)
    
    def get_curve_param_with_highest_fitness(self, curve_param_list):
        """
        Returns the curve parameter with the highest fitness.

        Args:
            curve_param_list (list): List of curve parameters.

        Returns:
            numpy array: Curve parameter with the highest fitness.
        """
        return max(curve_param_list, key=self.evaluate)
    
    def evaluate(self, curve_param):
        """
        Evaluates the fitness of a curve based on the curve type.

        Args:
            curve_param (numpy array): Curve parameter.

        Returns:
            float: Fitness of the curve.

        """
        if self.curve_type == "ADSR":
            return self.evaluate_ADSR_curve(curve_param)
        elif self.curve_type == "exp":
            return self.evaluate_exp_curve(curve_param)
        else:
            raise ValueError("Invalid curve type.")
        
    def evaluate_exp_curve(self, curve_param): 
        """
            Evaluates the fitness of exp curve fit to the target curve.
            Args:
                curve_param (numpy array): Curve parameter.
            
            Returns:
                float: Fitness of the curve.
        """

        curve = self.generate_exp(curve_param[0], curve_param[1], self.length)
        fitness = -np.square(curve - self.target_curve).mean()

        return fitness
    
    def generate_exp(self, A, B, length):
        """
            Generates an exp curve given A, B, and the length of the curve.

            Args:
                A (float): Attack time.
                B (float): Decay time.
                length (int): Length of the curve.

            Returns:
                numpy array: exp curve.
        """
        curve = np.zeros(length)
        t = np.linspace(0, 1, length)
        curve[0: length] = np.exp(-A*t) * (1 - np.exp(-B * t))
        return curve

    def evaluate_ADSR_curve(self, curve_param):
        """
        Evaluates the fitness of ADSR curve fit to the target curve.
        Args:
            curve_param (numpy array): Curve parameter.

        Returns:
            float: Fitness of the curve.
        """
        # Calculate the fitness of the curve
        curve = self.generate_ADSR(curve_param[0], curve_param[1], curve_param[2], curve_param[3], self.length)
        fitness = -np.square(curve - self.target_curve).mean()

        return fitness
    
    # Generate ADSR curve given A, D, S, R, and the length of the curve
    def generate_ADSR(self, A, D, S, R, length):
        """
        Generates an ADSR curve given A, D, S, R, and the length of the curve.

        Args:
            A (float): Attack time.
            D (float): Decay time.
            S (float): Sustain level.
            R (float): Release time.
            length (int): Length of the curve.

        Returns:
            numpy array: ADSR curve.
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

        return curve