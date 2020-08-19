from django.apps import AppConfig
import joblib


class ModelpredictorConfig(AppConfig):
    name = 'modelPredictor'
    prediction_model = joblib.load('modelPredictor/machine-learnig-model/prediction_model.sav')
    point_guards_kmeans = joblib.load('modelPredictor/machine-learnig-model/kmeans_pg.sav')
    shooting_guards_kmeans = joblib.load('modelPredictor/machine-learnig-model/kmeans_sg.sav')
    small_forwards_kmeans = joblib.load('modelPredictor/machine-learnig-model/kmeans_sf.sav')
    power_forwards_kmeans = joblib.load('modelPredictor/machine-learnig-model/kmeans_pf.sav')
    centers_kmeans = joblib.load('modelPredictor/machine-learnig-model/kmeans_c.sav')
    scaler = joblib.load('modelPredictor/machine-learnig-model/scaler.bin')
    pg_scaler = joblib.load('modelPredictor/machine-learnig-model/pg_scaler.bin')
    sg_scaler = joblib.load('modelPredictor/machine-learnig-model/sg_scaler.bin')
    sf_scaler = joblib.load('modelPredictor/machine-learnig-model/sf_scaler.bin')
    pf_scaler = joblib.load('modelPredictor/machine-learnig-model/pf_scaler.bin')
    c_scaler = joblib.load('modelPredictor/machine-learnig-model/c_scaler.bin')
