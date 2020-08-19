from django.shortcuts import render
from .apps import ModelpredictorConfig
from rest_framework import views, response, status
import pandas as pd
from sklearn.preprocessing import StandardScaler


class PredictGame(views.APIView):

    @staticmethod
    def get(request):
        """
        Predict the win probability of the local Team
        :param request: request with Game data to predict. JSON format with:
        {
            "data":{
                        "Local_TmOffRtg": 106.3268951559,
                        "Local_TmFloor%": 0.4808939695,
                        "Local_TmDefRtg": 100.8648132347,
                        "Local_Pace": 93.2749179292,
                        "Local_TS%": 0.5799537213,
                        "Local_eFG%": 0.5149127743,
                        "Local_FTARate": 0.2411367473,
                        "Local_3FGARate": 0.3162633652,
                        "Local_TmOR%": 20.6546275395,
                        "Local_TmDR%": 74.1407528642,
                        "Local_BLK%": 9.2277227723,
                        "Local_TOV%": 13.4329278498,
                        "Local_STL%": 10.0026641472,
                        "Visitor_TmOffRtg": 104.3182920583,
                        "Visitor_TmFloor%": 0.4891386826,
                        "Visitor_TmDefRtg": 107.1547410871,
                        "Visitor_Pace": 91.7010770049,
                        "Visitor_TS%": 0.5386902179,
                        "Visitor_eFG%": 0.477318694,
                        "Visitor_FTARate": 0.2964461138,
                        "Visitor_3FGARate": 0.2661080613,
                        "Visitor_TmOR%": 28.6157024793,
                        "Visitor_TmDR%": 77.1771771772,
                        "Visitor_BLK%": 5.4426983519,
                        "Visitor_TOV%": 12.0491677981,
                        "Visitor_STL%": 7.8042513187
                    }
        }
        :return: prediction, win or lose
        """
        data = request.data.get('data')
        data_to_predict = pd.DataFrame(columns=data.keys())
        data_to_predict = data_to_predict.append(data, ignore_index=True)

        X = ModelpredictorConfig.scaler.transform(data_to_predict)

        predicted_class = ModelpredictorConfig.prediction_model.predict(X=X)
        if predicted_class[0] == 1:
            prediction = 'Win'
        else:
            prediction = 'Lose'

        return response.Response(data={'prediction': prediction}, status=status.HTTP_200_OK)


class PredictPlayerCluster:

    @staticmethod
    def get(request, position):
        data = request.data.get('data')
        data_to_predict = pd.DataFrame(columns=data.keys)
        data_to_predict = data_to_predict.append(data, ignore_index=True)

        X = ModelpredictorConfig.pg_scaler.transform(data_to_predict)

        prediction = -1
        if position == 'PG':
            prediction = ModelpredictorConfig.point_guards_kmeans.predict(X=X)
        elif position == 'SG':
            prediction = ModelpredictorConfig.shooting_guards_kmeans.predict(X=X)
        elif position == 'SF':
            prediction = ModelpredictorConfig.small_forwards_kmeans.predict(X=X)
        elif position == 'PF':
            prediction = ModelpredictorConfig.power_forwards_kmeans.predict(X=X)
        elif position == 'C':
            prediction = ModelpredictorConfig.centers_kmeans.predict(X=X)

        return response.Response(data={'predicted_class': prediction}, status=status.HTTP_200_OK)

