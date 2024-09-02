from parameterized import parameterized
import unittest
import pandas as pd
from sklearn.datasets import load_breast_cancer

from flexml.classification import Classification
from flexml.logger.logger import get_logger

import warnings
warnings.filterwarnings("ignore")

class TestClassification(unittest.TestCase):
    df = load_breast_cancer(as_frame=True)['frame']
    logger = get_logger(__name__, "TEST", logging_to_file=False)
    logger.setLevel("DEBUG")
    
    @parameterized.expand(["quick", "wide"])
    def test_classification(self, exp_size: str, df: pd.DataFrame = df):
        try:
            classification_exp = Classification(
                data = df,
                target_col = "target",
                experiment_size = exp_size,
                test_size = 0.25,
                random_state = 42,
                logging_to_file = False
            )
        except Exception as e:
            error_msg = f"An error occured while setting up {exp_size} classification, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        try:
            classification_exp.start_experiment()
        except Exception as e:
            error_msg = f"An error occured while running {exp_size} classification experiment, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        top_x_models = classification_exp.get_best_models(top_n_models = 3)
        if len(top_x_models) != 3:
            error_msg = f"An error occured while retriving the best models in {exp_size} classification, expected 3, got {len(top_x_models)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
                
        try:
            classification_exp.show_model_stats()
        except Exception as e:
            error_msg = f"An error occured while showing models stats in {exp_size} classification, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        try:
            tuning_methods = ["randomized_search", "optuna"]

            for method in tuning_methods:
                classification_exp.tune_model(n_iter=3, cv = None, tuning_size=exp_size)

                if classification_exp.tuned_model is None:
                    error_msg = f"An error occured while tuning the model with {method} in {exp_size} classification, tuned model is None"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                            
                if classification_exp.tuned_model_score is None:
                    error_msg = f"An error occured while calculating the tuned model's score with {method} in {exp_size} classification, tuned model score is None"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
        
        except Exception as e:
            error_msg = f"An error occured while tuning the model in {exp_size} classification, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)