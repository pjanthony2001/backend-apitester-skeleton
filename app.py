import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv', encoding="utf-8")
evenements_df = pd.read_csv(data / 'evenements_associations.csv', encoding="utf-8")

## Vous devez ajouter les routes ici : 

@app.route("/api/alive", methods=["GET"])
def alive():
    return make_response(jsonify({"message" : "Alive"}), 200)


@app.route("/api/association/", methods=["GET"])
def list_asso():
    return make_response(associations_df.to_json(orient="records", force_ascii=False), 200) 

@app.route("/api/eventments/", methods=["GET"])
def list_event():
    return make_response(evenements_df.to_json(orient="records", force_ascii=False), 200) 

@app.route("/api/association/<int:id>", methods=["GET"])
def find_asso(id: int):
    try: 
        student_info = associations_df[associations_df.id == id]
    except IndexError:
        return make_response(f"Student details for {id} not found!", 404) 
    return make_response(student_info.to_json(orient="records", force_ascii=False), 200) 


@app.route("/api/evenements/<int:id>", methods=["GET"])
def find_event(id: int):
    try: 
        event_info = evenements_df[evenements_df.id == id]
    except IndexError:
        return make_response(f"Event details for {id} not found!", 404) 
    return make_response(event_info.to_json(orient="records", force_ascii=False), 200) 


@app.route("/api/association/<int:id>/eventments", methods=["GET"])
def find_asso_event(id: int):
    try: 
        student_info = evenements_df[evenements_df.association_id == id]
    except IndexError:
        return make_response(f"Student details for {id} not found!", 404) 
    return make_response(student_info.to_json(orient="records", force_ascii=False), 200) 
    
@app.route("/api/association/type/<type>", methods=["GET"])
def find_asso_type(type: str):
    try: 
        student_info = associations_df[associations_df.type == type]
    except IndexError:
        return make_response(f"Student details for {type} not found!", 404) 

    return make_response(student_info.to_json(orient="records", force_ascii=False), 200) 

if __name__ == '__main__':
    app.run(debug=True)
