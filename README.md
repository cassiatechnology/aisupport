# MVP - Suporte Inteligente via WhatsApp com IA

Este projeto implementa um sistema de atendimento automático via WhatsApp, utilizando IA para responder perguntas, com fallback para criação de tickets quando a similaridade for baixa.

## ✨ Tecnologias Utilizadas

- **Frontend e Integração**
  - WhatsApp (via Twilio Webhook)
  - Azure Functions (Python)

- **Inteligência Artificial**
  - OpenAI GPT-4o-mini (chat)
  - OpenAI Embeddings (`text-embedding-3-small`)
  - Similaridade por cosseno

- **Persistência**
  - Azure Blob Storage (`kb_embeddings.json`)
  - API de Tickets (C#, .NET 9)
  - Azure SQL Database

- **Outros**
  - Azure Cognitive Search (opcional)
  - CI/CD via GitHub + Azure

## 🧠 Como funciona

1. O usuário envia uma pergunta via WhatsApp
2. A Azure Function recebe o texto e gera um embedding
3. O embedding é comparado com os da base (`kb_embeddings.json`)
4. Se a similaridade for suficiente (≥ 0.6), retorna a resposta da KB
5. Caso contrário, usa o GPT-4o Mini para responder com IA generativa
6. Se a pergunta não for respondida pela KB, é aberto um ticket via API
7. A API grava o ticket em um banco de dados SQL no Azure

## 🔧 Como rodar localmente

```bash
# Ativar ambiente
source aisupportvenv/bin/activate  # ou .\aisupportvenv\Scripts\Activate

# Rodar Azure Function local
func start
