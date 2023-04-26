from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import app.model as app_functions
import pandas as pd


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
        print(result)
        
        result.rename(columns = {"imc": "imc", "cec":"tempo_cec_min", "mv":"tempo_vm_horas", 
                                 "ec": "eco_feve", "creatinine":"cr_pos_op",
                                 "troponin":"pico_tropo", "lactate":"pico_lactato_24h" }, inplace = True)
        result = result[['imc', 'tempo_cec_min', 'cr_pos_op', 'tempo_vm_horas', 
                         'pico_tropo', 'pico_lactato_24h', 'eco_feve']]
        print(result)




        prob = app_functions.prediction_prob(result)[0][0]
        labels = ["Non Death", "Death"]
        values = [prob,1-prob]

        

      
        return render_template("graph.html", labels = labels, values = values)

    return render_template("index.html")