import json
import os
from openai import OpenAI

# Inicializa o cliente OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Carrega o arquivo kb_base.json
with open("kb_base.json", "r", encoding="utf-8") as f:
    base = json.load(f)

# Gera embedding para cada pergunta
enriquecido = []
for i, item in enumerate(base, 1):
    pergunta = item["pergunta"]

    response = client.embeddings.create(
        input=pergunta,
        model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding

    enriquecido.append({
        "id": str(i),
        "pergunta": pergunta,
        "resposta": item["resposta"],
        "embedding": embedding
    })

# Salva o novo arquivo enriquecido
with open("kb_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(enriquecido, f, ensure_ascii=False, indent=2)

print("✔️ Arquivo kb_embeddings.json criado com embeddings.")