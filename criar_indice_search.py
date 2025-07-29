from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.search.documents import SearchClient
import requests
import os

# Chave admin do Azure Cognitive Search (Variável de ambiente)
admin_key = os.environ.get("SEARCH_KEY")
service_name = "aisupportkb"
index_name = "kb-index"

if not admin_key:
    raise ValueError("Variável de ambiente SEARCH_KEY não foi definida.")

# 1. Criar índice
endpoint = f"https://{service_name}.search.windows.net"
credential = AzureKeyCredential(admin_key)
index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=credential,
    api_version="2023-11-01"
)

# Excluir índice antigo, se existir
try:
    index_client.delete_index(index_name)
except ResourceNotFoundError:
    pass

fields = [
    SimpleField(name="id", type="Edm.String", key=True),
    SearchableField(name="pergunta", type="Edm.String", language="pt-br"),
    SimpleField(name="resposta", type="Edm.String")
]

index = SearchIndex(name=index_name, fields=fields)
index_client.create_index(index)
print(f"✔️ Índice '{index_name}' criado.")

# 2. Carregar dados do JSON do blob
response = requests.get("https://aisupportstorage01.blob.core.windows.net/aisupportcontainer/kb_base.json")
dados = response.json()

# Adicionar campo 'id' para cada item
for i, item in enumerate(dados):
    item["id"] = str(i + 1)

# 3. Inserir documentos no índice
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
result = search_client.upload_documents(documents=dados)
print(f"✔️ Documentos enviados: {result}")

# 4. Consulta de teste
print("\n🔍 Consulta de exemplo: 'Como redefinir minha senha?'")
results = search_client.search("Como redefinir minha senha?")
for r in results:
    print(f"- {r['resposta']}")