import azure.functions as func
import urllib.parse
import logging
import json
import os
import math
import requests
from openai import OpenAI

# Configurações
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_CHAT = "gpt-4o-mini"
MODEL_EMBEDDING = "text-embedding-3-small"
EMBEDDINGS_PATH = "kb_embeddings.json"
SCORE_SIMILARITY = 0.6
TICKET_API_URL = "https://aisupportapi-f0frfeh8abc9g2ey.brazilsouth-01.azurewebsites.net/api/ticket"

# Inicializa o cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Carrega os dados de embeddings
with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
    kb_data = json.load(f)

def gerar_embedding(texto: str):
    response = client.embeddings.create(
        model=MODEL_EMBEDDING,
        input=texto.replace("\n", " ")
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def criar_ticket(pergunta: str):
    payload = {
        "category": "Dúvida",
        "description": pergunta,
        "status": 1
    }
    try:
        response = requests.post(TICKET_API_URL, json=payload)

        mensagem = ""

        if response.status_code == 201:
            ticket = response.json()
            ticket_id = ticket.get("id")
            mensagem = f"Ticket criado com ID: {ticket_id}"
        else:
            mensagem = f"Erro ao criar ticket: {response.status_code} - {response.text}"

        return mensagem
    except Exception as e:
        logging.error(f"Erro ao criar ticket: {str(e)}")

# Azure Function principal
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="responder_mensagem", methods=["POST"])
def responder_mensagem(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = urllib.parse.parse_qs(req.get_body().decode())
        user_msg = req_body.get("Body", [""])[0].strip()
        logging.info(f"Pergunta: {user_msg}")

        if not OPENAI_API_KEY:
            return func.HttpResponse("API Key não configurada.", status_code=500)

        embedding_usuario = gerar_embedding(user_msg)

        melhor_score = 0
        melhor_resposta = None

        for item in kb_data:
            score = cosine_similarity(embedding_usuario, item["embedding"])
            if score > melhor_score:
                melhor_score = score
                melhor_resposta = item["resposta"]

        logging.info(f"Melhor similaridade: {melhor_score:.4f}")

        if melhor_score >= SCORE_SIMILARITY:
            logging.info("Fonte da resposta: Knowledge Base (KB)")
            resposta = melhor_resposta
        else:
            logging.info("Fonte da resposta: OpenAI")
            ticket_info = criar_ticket(user_msg)
            prompt = (
                f"Um usuário perguntou: '{user_msg}'.\n"
                "Não encontramos uma resposta exata na base de conhecimento.\n"
                "Responda de forma clara, objetiva e empática, como um atendente humano faria.\n"
                "Informe ao usuário que você abrirá um chamado para esclarecer a dúvida dele."
            )
            response = client.chat.completions.create(
                model=MODEL_CHAT,
                messages=[
                    {"role": "system", "content": "Você é um assistente de suporte inteligente."},
                    {"role": "user", "content": prompt}
                ]
            )
            resposta = f"{response.choices[0].message.content.strip()}\n{ticket_info}"

        logging.info(f"Resposta final: {resposta}")
        return func.HttpResponse(resposta, status_code=200, mimetype="text/plain")

    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        return func.HttpResponse(f"Erro: {str(e)}", status_code=500)