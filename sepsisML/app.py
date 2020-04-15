from flask import Flask, jsonify, request
import pickle

from sepsisML import settings
from sepsisML import logger
from sepsisML.errors import PatientNotFound, InvalidVersion, NotEnoughData
from sepsisML.parser import parser
from sepsisML.ml import preprocessor, model

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(status="sepsisML is running")

# 1f444f0c-a2a0-42aa-8705-3a293d74abf9
@app.route("/api/v1/predict", methods=["GET", "POST"])
def predict():
    logger.info("Predict endpoint triggered")
    
    patient_id = request.args.get("patient", "")
    patient_id = patient_id.split(",")

    logger.info("Patient id: {}".format(patient_id))

    endpoint = request.args.get("endpoint", "default")

    if endpoint not in settings.MAP_ENDPOINT.keys():
        return jsonify(result="ERROR", 
                message= "Accepted endpoints: {}".format([endp for endp in settings.MAP_ENDPOINT.keys()]))
    logger.info("FHIR server: {}".format(endpoint))

    version = request.args.get("version", "default")
    logger.info("FHIR version: {}".format(version))

    logger.info("Getting FHIR data...")
    try:
        data = parser.get_fhir_data(patient_id, endpoint, version)
    except PatientNotFound as patientnotfound:
        return jsonify(result="ERROR", 
                    message=patientnotfound.message)
    except InvalidVersion as invalidversion:
        return jsonify(result="ERROR",
                    message=invalidversion.message)
    except NotEnoughData as notenoughdata:
        return jsonify(result="ERROR",
                    message=notenoughdata.message)
    # return data.to_json()

    pre_data = preprocessor.preprocess(data)
    prediction = model.predict(pre_data)
    explanation = model.explain(pre_data)

    new_explain = []
    
    for explain, preds in zip(explanation, prediction.values):
        explain['prediction'] = preds
        new_explain.append(explain)

    for sign in ['pos', 'neg']:
        temp_explain = []
        for i, exp in enumerate(new_explain[0]['feature_weights'][sign]):
            if exp['feature'] == '<BIAS>' \
                or exp['value'] == 0:
                pass
            else:
                temp_explain.append(new_explain[0]['feature_weights'][sign][i])            
        new_explain[0]['feature_weights'][sign] = temp_explain

    return jsonify(new_explain)

