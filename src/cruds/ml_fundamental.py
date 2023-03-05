from sqlalchemy.orm import Session

from src.models import *
from src.schemas import *

import json
import requests
from dotenv import load_dotenv
import os
from os.path import dirname, join

# from sklearn.preprocessing import StandardScaler
# import lightgbm
import pickle

def ml(data: MlFundamentalModel):
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    model = pickle.load(open(os.environ.get('TRAINED_MODEL_PATH'), 'rb'))
    standard_scaler = pickle.load(open(os.environ.get('STANDARD_SCALER_MODEL_PATH'), 'rb'))
    
    data_std = standard_scaler.transform(data.data)

    results = model.predict(data_std).tolist()

    return {
        "results": results
    }