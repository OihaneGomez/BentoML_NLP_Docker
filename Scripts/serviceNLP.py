import numpy as np
import bentoml
import pickle
import os
from bentoml.io import NumpyNdarray, JSON
from typing import List
from Scripts.bm25_bge_runnable import BM25BGERunnable
from pydantic import RootModel
from typing import List, Dict


#NLP runner
nlp_runner = bentoml.Runner(BM25BGERunnable, name="bm25_bge_runner")
#Both Services
svc = bentoml.Service("nlp_model_service", runners=[nlp_runner])



## NLP Model
class Questionnaire(RootModel):
    root: List[str]

sample_questionnaire = Questionnaire(
    root=[
        "In which location is this transport process taking place? : Location GLO",
        "If external road transport is used, what type of energy does the vehicle use? : Gasoline gas",
        "If you use road transport, what type of vehicle do you use? : TRUCK LORRY",
        "What is the maximum authorized weight of the vehicle? (ton) : 3.5-7.5",
        "According to the EURO classification of transport vehicles, to which group does your vehicle belong? : EURO3 EU3",
        "Do you use a container? : Container",
        "Select the type of container you use for road transport: Cooling",
        "If refrigeration equipment is used, select the refrigerant used: refrigeration R134a"
    ]
)


@svc.api(input=JSON.from_sample(sample_questionnaire), output=JSON())
async def search_processes(cuestionario: Questionnaire) -> List[Dict[str, float]]:
    return await nlp_runner.buscar.async_run(cuestionario.root)