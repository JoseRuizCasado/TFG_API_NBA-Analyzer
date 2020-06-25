from django.apps import AppConfig
import joblib


class ModelpredictorConfig(AppConfig):
    name = 'modelPredictor'
    logistic_regression_classifier = joblib.load('modelPredictor/machine-learnig-model/lr-lbfgs.sav')
    linear_support_vector_classifier = joblib.load('modelPredictor/machine-learnig-model/linear-svc.sav')
    support_vector_classifier_linear_kernel = joblib.load('modelPredictor/machine-learnig-model/svc-linear-kernel.sav')
    voting_classifier = joblib.load('modelPredictor/machine-learnig-model/voting-classifier.sav')
