This project contains a **Natural Language Processing (NLP)** API built with **BentoML** and deployed via **Docker**. It uses a combination of **BM25** and **semantic search (BGE embeddings)** to find the most relevant transport processes based on a questionnaire.


---


## 📦 Project Structure

  
```plaintext
BentoML_NLP/
├── Scripts/
│   ├── serviceNLP.py                             # BentoML service definition
│   ├── bm25_bge_runnable.py                      # Custom runner logic (BM25 + BGE)
│   └── bge_base_en_process_all_new_approach.pkl  # The model
├── Dockerfile
├── docker-compose.yml
└── README.md
```


  

## Quickstart

  

### 1. Clone the Repository

  

```bash

git clone https://github.com/OihaneGomez/BentoML_NLP_Docker/

cd BentoML_NLP

  ```

### 2. Build and start the container
```bash
docker-compose up  --build
  ```
  

  
# API Endpoint
Once the container is running, navigate to port 3000. For instace: http://localhost:3000 
You will see the **BentoML Swagger UI**, which documents the available endpoints:

### POST `/search_processes`

- **Input**: JSON array of questions and answers in the format `"Question : Answer"`
- **Output**: A ranked list of transport processes with their relevance scores

## Example Input

```json
[
  "In which location is this transport process taking place? : Location GLO",
  "If external road transport is used, what type of energy does the vehicle use? : Gasoline gas",
  "If you use road transport, what type of vehicle do you use? : TRUCK LORRY",
  "What is the maximum authorized weight of the vehicle? (ton) : 3.5-7.5",
  "According to the EURO classification of transport vehicles, to which group does your vehicle belong? : EURO3 EU3",
  "Do you use a container? : Container",
  "Select the type of container you use for road transport: Cooling",
  "If refrigeration equipment is used, select the refrigerant used: refrigeration R134a"
]
```
## Example Output


```json
[
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, R134a refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, R134a refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4874231219291687
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, carbon dioxide, liquid refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, carbon dioxide, liquid refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4778245091438293
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO4, R134a refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO4, R134a refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4611009359359741
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, R134a refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, R134a refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4541483521461487
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO6, R134a refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO6, R134a refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4519407153129578
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO4, carbon dioxide, liquid refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO4, carbon dioxide, liquid refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4513216614723206
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, carbon dioxide, liquid refrigerant, cooling {GLO}| market for transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO3, carbon dioxide, liquid refri(...)_1 | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4420012831687927
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, carbon dioxide, liquid refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, carbon dioxide, liquid refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4402759075164795
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO6, carbon dioxide, liquid refrigerant, cooling {GLO}| transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO6, carbon dioxide, liquid refrigerant, cooling | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4349072575569153
  },
  {
    "Process": "Transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, carbon dioxide, liquid refrigerant, cooling {GLO}| market for transport, freight, lorry with refrigeration machine, 3.5-7.5 ton, EURO5, carbon dioxide, liquid refri(...)_3 | APOS, U | {Location:GLO} | {Unit:tkm}",
    "accuracy": 1.4154694080352783
  }
]
```


> **Note**: The `.pkl` model file (`bge_base_en_process_all_new_approach.pkl`) must be located inside the `Scripts/` directory.

### References
[BentoML Documentation](https://docs.bentoml.org/)


