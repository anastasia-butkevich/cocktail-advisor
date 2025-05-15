# Cocktail Advisor Chat - Anastasia Butkevych

To start this project, I first carefully analyzed the task requirements and selected the appropriate technologies. My approach was to build a minimal viable product quickly, focusing on core functionality before adding any advanced features. 

### My main goals:
- Implement a FastAPI endpoint `/chat` to handle user interactions (currently only one endpoint).
- Use FAISS vector store combined with HuggingFace embeddings for efficient similarity search.
- Detect and track user preferences related to cocktail choices.
- Retrieve relevant documents based on user queries using similarity search.
- Implement simple Streamlit UI.

Because I'm short on time, I used a technology stack similar to one I used successfully in a previous project (Concert ChatApp), since the requirements are quite similar. For the LLM interface, I integrated the Groq API.

## Project structure
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

## Build instructions
1. Clone the repository (if not already done).
```
git clone https://github.com/anastasia-butkevich/cocktail-advisor.git
cd cocktail-advisor
```
2. Set the environment variable `GROQ_API_KEY` with your API key.
```
export GROQ_API_KEY=your_actual_api_key_here
```
3. Build and start the Docker container using Docker Compose.
```
docker-compose up --build
```
4. Access the application at the following URLs:
- Cocktail app API: `http://localhost:8000`
- Streamlit UI: `http://localhost:8501`