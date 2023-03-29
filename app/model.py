import pandas as pd
import lightgbm as lgb


def convert_education(education):
    if education == 0:
        return [1,0,0,0]
    elif education == 1:
        return [0,1,0,0]
    elif education == 2:
        return [0,0,1,0]
    elif education == 3:
        return [0,0,0,1]



def create_feature(data):

    #add number of comorb.
    data["n_of_morb"] = data[["hiv", "diabetes", "other_dishx"]].sum(axis = 1)

    return data

def prediction_prob(data):

    model = lgb.Booster(model_file = 'app/binary.txt')
    #model = xgb.XGBClassifier()
    #model.load_model("app/xgb.json")

    return(model.predict(data))


