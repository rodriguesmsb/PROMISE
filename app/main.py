from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import app.model as app_functions
import pandas as pd
import numpy as np



app = Flask(__name__)


@app.route("/", methods = ['GET','POST'])
def make_pred():

    #get user response
    if request.method == "POST":
        #foo

        result = request.form.to_dict(flat = False) #convert form to a dict

        #convert dict to a data frame
        result = pd.DataFrame.from_dict(result)
        for col in result.columns:
            result[col] = result[col].astype(float)
       

        result.rename(columns = {"age":"idade", "imc": "imc", "creatinine":"cr_pre_op",
                                 "troponin":"pico_tropo", "lactate":"pico_lactato_24h",  
                                 "ec": "eco_feve"}, inplace = True)

        features_names = ['idade', 'imc', 'cr_pre_op', "tempo_vm_horas", 'pico_tropo', 'pico_lactato_24h', 'eco_feve']

        #mean values
        dict_mean = {"idade":54.301075, "imc":92.402650, "cr_pre_op":2.623152,
                     "tempo_vm_horas":244.365319, "pico_tropo":568.696721,
                     "pico_lactato_24h":7.602228, "eco_feve":336.747544}

        #std values
        dict_std = {"idade":14.642141, "imc":1261.989164, "cr_pre_op":51.290603,
                     "tempo_vm_horas":2718.449842, "pico_tropo":2988.646148,
                     "pico_lactato_24h":132.060516, "eco_feve":4104.512829}

        
       
   

        for col in result.columns:
            result[col] = (result[col] - dict_mean[col])/dict_std[col]

        #create a series hourly
        result = pd.DataFrame.from_dict({"idade": result["idade"].repeat(72).tolist(),
                                         "imc": result["imc"].repeat(72).tolist(),
                                         "cr_pre_op": result["cr_pre_op"].repeat(72).tolist(),
                                         "pico_tropo": result["pico_tropo"].repeat(72).tolist(),
                                         "pico_lactato_24h": result["pico_lactato_24h"].repeat(72).tolist(),
                                         "eco_feve": result["eco_feve"].repeat(72).tolist(),
                                         "tempo_vm_horas": (pd.Series(range(1,73)) - dict_mean["tempo_vm_horas"])/dict_std["tempo_vm_horas"]})
        


        prob = app_functions.prediction_prob(result[features_names])
        

        labels = np.arange(0,72).tolist()
        values = [prob[i][1] for i in np.arange(0,72)]

      
        return render_template("graph.html", labels = labels, values = values)

    return render_template("index.html")