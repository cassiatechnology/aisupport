import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import urllib.parse
import os
import logging
from openai import OpenAI

# Configurações do Azure Search
SEARCH_ENDPOINT = "https://aisupportkb.search.windows.net"
INDEX_NAME = "kb-index"
MODEL_NAME = "gpt-4o-mini"
SEARCH_KEY = os.environ.get("SEARCH_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Função principal da Azure Function
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="responder_mensagem", methods=["POST"])
def responder_mensagem(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = urllib.parse.parse_qs(req.get_body().decode())
        user_msg = req_body.get("Body", [""])[0]

        logging.info(f"Pergunta: {user_msg}")

        if not SEARCH_KEY or not OPENAI_API_KEY:
            return func.HttpResponse(
                "Chaves de API não configuradas corretamente.",
                status_code=500
            )

        # Azure Search
        credential = AzureKeyCredential(SEARCH_KEY)
        search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=credential)
        results = search_client.search(user_msg, top=1)

        logging.info("Verificando resultado...")
        logging.info(f"Resultado Search Client: {len(list(results))}")

        resposta = None
        for r in results:
            logging.info(f"Document keys: {r.keys()}")
            
            score = r.get('@search.score')
            
            if score is not None:
                logging.info(f"Score: {score}")
            else:
                logging.warning("⚠️ Score não encontrado no documento retornado.")
            
            if score and score >= 1.2:
                resposta = r.get("resposta")
            break

        # Se não achou uma resposta relevante, usa a OpenAI
        if not resposta:
            prompt = (
                f"Um usuário perguntou: '{user_msg}'. "
                "Não encontramos uma resposta exata na base de conhecimento. "
                "Responda de forma clara, objetiva e empática, como um assistente de suporte humano faria, "
                "utilizando seu conhecimento geral para ajudar o usuário da melhor forma possível."
                )
            
            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Você é um assistente de suporte inteligente."},
                    {"role": "user", "content": prompt}
                ]
            )

            resposta = response.choices[0].message.content.strip()

        logging.info(f"Resposta: {resposta}")
        return func.HttpResponse(resposta, status_code=200, mimetype="text/plain")

    except Exception as e:
        return func.HttpResponse(f"Erro: {str(e)}", status_code=500)