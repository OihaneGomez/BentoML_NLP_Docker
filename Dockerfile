FROM python:3.10-slim

WORKDIR /app

COPY ./Scripts /app/Scripts

# 🔥 Añade esto
ENV PYTHONPATH="/app/Scripts"

ENV BENTOML_HOME=/app

RUN apt-get update && apt-get install -y git && \
    pip install --upgrade pip && \
    pip install bentoml==1.4.6 \
                pandas \
                scikit-learn \
                sentence-transformers \
                rank_bm25 \
                pydantic

EXPOSE 3000

CMD ["bentoml", "serve", "Scripts.serviceNLP:svc", "--port", "3000"]
