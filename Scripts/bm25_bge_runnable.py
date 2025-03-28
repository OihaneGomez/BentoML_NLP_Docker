# bm25_bge_runnable.py
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
import pickle
import torch
import torch.nn.functional as F
import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from bentoml import Runnable
from sentence_transformers import SentenceTransformer

class BM25BGERunnable(Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True
    def __init__(self):
        super().__init__()
        self.INSTRUCTION = "Represent this sentence for retrieval: "
        self.TOP_BM25 = 1500
        self.TOP_BGE = 500
        self.FINAL_RESULTS = 10
        self.BOOST_MULTIPLIER = 0.5

        # Cargar dataset - 
        # ----- CAMBIAR A VOLUMEN -----
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "bge_base_en_process_all_new_approach.pkl")
        self.df = pd.read_pickle(model_path)
        
        # Inicializar BM25
        documents = self.df["Process"].tolist()
        tokenized_corpus = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

        # Cargar modelo BGE
        self.bge_model = SentenceTransformer("BAAI/bge-base-en")

        # Normalizar embeddings
        embeddings_tensor = torch.stack([
            torch.tensor(emb, dtype=torch.float32) if not torch.is_tensor(emb) else emb.clone().detach().to(dtype=torch.float32)
            for emb in self.df["embedding"]
        ])
        self.embeddings_tensor = F.normalize(embeddings_tensor, p=2, dim=1)

    def _obtener_respuestas(self, cuestionario):
        return [q.split(":")[-1].strip() for q in cuestionario]

    def _aplicar_multiplicador(self, df_final, palabras_clave):
        for i, row in df_final.iterrows():
            proceso_text = row["Process"].lower()
            palabras_encontradas = {palabra for palabra in palabras_clave if palabra in proceso_text}
            if palabras_encontradas:
                df_final["score"] = df_final["score"].astype(np.float64)
                df_final.at[i, "score"] += self.BOOST_MULTIPLIER * len(palabras_encontradas)
        return df_final

    @Runnable.method(batchable=False)
    def buscar(self, cuestionario: list[str]) -> list[str]:
        query_tokens = " ".join(self._obtener_respuestas(cuestionario)).lower().split()
        bm25_scores = self.bm25.get_scores(query_tokens)
        top_bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:self.TOP_BM25]
        df_bm25 = self.df.iloc[top_bm25_indices].copy()

        # Embedding del cuestionario
        embedding_consulta = self.bge_model.encode(self.INSTRUCTION + " ".join(cuestionario), convert_to_tensor=True)
        embedding_consulta = F.normalize(embedding_consulta, p=2, dim=0)
        sub_embeddings = self.embeddings_tensor[top_bm25_indices]

        similitudes = torch.matmul(sub_embeddings, embedding_consulta)
        top_bge_indices = torch.topk(similitudes, self.TOP_BGE).indices.tolist()
        df_final = df_bm25.iloc[top_bge_indices].copy()
        df_final["score"] = (similitudes[top_bge_indices] - similitudes.min()) / (similitudes.max() - similitudes.min())

        palabras_clave = set(self._obtener_respuestas(cuestionario))
        df_final = self._aplicar_multiplicador(df_final, palabras_clave)
        df_final = df_final.sort_values(by="score", ascending=False).drop_duplicates(subset=["Process"], keep="first")
        df_final = df_final.head(self.FINAL_RESULTS)

        return df_final[["Process", "score"]].rename(columns={"score": "accuracy"}).to_dict(orient="records")
