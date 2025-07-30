# 🤖 Projeto de Atendimento Inteligente via WhatsApp com IA e API de Tickets

Este projeto é um MVP de um sistema inteligente de atendimento ao cliente via **WhatsApp**, utilizando **OpenAI**, **Azure Functions** e uma **API de tickets em .NET**. Ele é capaz de interpretar mensagens, buscar respostas por similaridade semântica e, se necessário, abrir tickets automaticamente.

---

## 📌 Funcionalidades

- Recebe mensagens via WhatsApp (Twilio)
- Analisa semântica da pergunta com embeddings
- Busca resposta similar na base vetorizada (`kb_embeddings.json`)
- Gera resposta com OpenAI se não encontrar similaridade suficiente
- Cria ticket automaticamente via API REST (caso aplicável)
- Registra e responde ao usuário com empatia e clareza

---

## 🧠 Visão Geral da Arquitetura

![Diagrama da Arquitetura](./A_flowchart_diagram_in_the_image_illustrates_an_in.png)

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
