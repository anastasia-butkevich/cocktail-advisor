# Cocktail Advisor Chat

## Overview

**Cocktail Advisor Chat** is an intelligent assistant designed to provide cocktail recommendations based on user preferences. Built with **FastAPI** and **Streamlit**, the app uses **Retrieval-Augmented Generation (RAG)** techniques powered by **FAISS**, **HuggingFace embeddings**, and **Groq-hosted LLMs** to retrieve relevant cocktail data and respond to user queries.

## Main Features

**1. Chat Endpoint:** Responds to user queries via a `/chat` endpoint, powered by an LLM with cocktail-specific context.

**2. Preference Tracking:** Tracks user preferences (e.g., ingredients, type, flavor profile) during interaction to tailor recommendations.

**3. Similarity Search:** Retrieves cocktail entries relevant to user input using FAISS vector store with HuggingFace embeddings.

**4. Streamlit UI:** Provides a clean, interactive interface for chatting with the assistant.

## Routes

The backend exposes the following main route:

* `POST /chat:` Accepts a user message and returns a cocktail-related response based on relevant documents.

## Cocktail Retrieval (RAG)

The system implements a basic RAG pipeline:

* **Embedding:** Cocktail descriptions from a CSV file are embedded using a HuggingFace model.

* **Storage:** Embeddings are indexed using FAISS for efficient vector similarity search.

* **Retrieval & Response:** Relevant cocktail entries are retrieved and passed to a Groq-hosted LLM to generate a contextual response.

## Project Structure

```
cocktail-advisor/
├── Dockerfile
├── README.md
├── app
│   ├── api
│   │   ├── models.py
│   │   └── routes.py
│   ├── rag
│   │   ├── llm.py
│   │   ├── rag.py
│   │   └── settings.py
│   └── ui
│       └── streamlit_ui.py
├── data
│   └── final_cocktails.csv
├── docker_compose.yml
├── requirements.txt
└── run.sh
```

## Setup Instructions

**IMPORTANT:** Make sure your Groq API key is available as an environment variable.

### Run with Docker Compose

**1. Clone the Repository**

```
git clone https://github.com/anastasia-butkevich/cocktail-advisor.git
cd cocktail-advisor
```

**2. Set Your Environment Variable**

```
export GROQ_API_KEY=your_actual_api_key_here
```

**3. Build and Run the Application**

```
docker-compose up --build
```

**4. Access the Application:**

* API: `http://localhost:8000`
* Streamlit UI: `http://localhost:8501`

**5. Stopping the Application:**
Stop the services with:

```
docker-compose down
```
