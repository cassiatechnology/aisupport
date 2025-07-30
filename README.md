# 🤖 Projeto de Atendimento Inteligente via WhatsApp com IA e API de Tickets

Este projeto é um MVP de um sistema inteligente de atendimento ao cliente via **WhatsApp**, utilizando **OpenAI**, **Azure Functions** e uma **API de tickets em .NET**. Ele é capaz de interpretar mensagens, buscar respostas por similaridade semântica e, se necessário, abrir tickets automaticamente.

---

## 📌 Como Funciona

1. O usuário envia uma pergunta via WhatsApp
2. A Azure Function recebe o texto e gera um embedding
3. O embedding é comparado com os da base (`kb_embeddings.json`)
4. Se a similaridade for suficiente (≥ 0.6), retorna a resposta da KB
5. Caso contrário, usa o GPT-4o Mini para responder com IA generativa
6. Se a pergunta não for respondida pela KB, é aberto um ticket via API
7. A API grava o ticket em um banco de dados SQL no Azure

---

## 🧠 Visão Geral da Arquitetura

![Diagrama da Arquitetura](./DiagramaAiSupportMermaid.png)

---

## ✨ Tecnologias Utilizadas

- **🧩 Frontend e Integração**
  - 💬 **WhatsApp** (via Twilio Webhook)
  - ⚡ **Azure Functions (Python)** – backend escalável para processamento de mensagens
  - 🚀 **GitHub Actions + Azure (CI/CD)** – deploy contínuo automatizado

- **🧠 Inteligência Artificial**
  - 🤖 **OpenAI GPT-4o-mini** – geração de respostas com linguagem natural
  - 🧬 **OpenAI Embeddings** (`text-embedding-3-small`) – vetorização de textos
  - 📈 **Similaridade por cosseno** – para comparação semântica entre perguntas e respostas

- **🗄️ Persistência**
  - ☁️ **Azure Blob Storage** – armazenamento da base vetorizada (`kb_embeddings.json`)
  - 🗃️ **Azure SQL Database** – persistência dos tickets
  - 🛠️ **API de Tickets** – construída com C# e .NET 9

- **🧪 Testes e Desenvolvimento**
  - 🔬 **Postman** e `curl` – testes de API REST
  - 🧑‍💻 **VS Code** com **Azure Tools** – ambiente de desenvolvimento principal
  - 🐍 **Python 3.10+** – linguagem da Azure Function
  - ⚙️ **C# e .NET 9** – linguagem da API REST

- **🧰 Outros**
  - 🔍 **Azure Cognitive Search** – usado inicialmente com busca tradicional (etapa removida ao final)

---

## 🔧 Como rodar localmente

```bash
# Ativar ambiente
source aisupportvenv/bin/activate  # ou .\aisupportvenv\Scripts\Activate

# Rodar Azure Function local
func start
