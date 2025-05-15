import pandas as pd
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from app.rag.llm import LLM


class RAGSystem:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.cocktail_store = self._load_knowledge_base()
        self.preference_store = self._load_or_create_preference_store()
        self.llm = LLM()

    def _load_knowledge_base(self):
        df = pd.read_csv("data/final_cocktails.csv")

        docs = [
            Document(
                page_content=(
                    f"Name: {row['name']}\n"
                    f"Alcoholic: {row['alcoholic']}\n"
                    f"Category: {row['category']}\n"
                    f"Glass Type: {row['glassType']}\n"
                    f"Ingredients: {row['ingredients']}\n"
                    f"Measures: {row['ingredientMeasures']}\n"
                    f"Instructions: {row['instructions']}"
                ),
                metadata={
                    "type": "cocktail",
                    "name": row['name'],
                    "ingredients": row['ingredients'] 
                }
            )
            for _, row in df.iterrows()
        ]

        return FAISS.from_documents(docs, self.embeddings)

    def _load_or_create_preference_store(self):
        preference_index_path = "data/preference_store"
        if os.path.exists(preference_index_path):
            return FAISS.load_local(preference_index_path, self.embeddings)
        else:
            return None

    def _save_preference_store(self):
        preference_index_path = "data/preference_store"
        os.makedirs(os.path.dirname(preference_index_path), exist_ok=True)
        self.preference_store.save_local(preference_index_path)

    def _get_user_preferences(self):
        if self.preference_store is None or len(self.preference_store.docstore._dict) == 0:
            return set()
        preferences = set()
        for doc_id in self.preference_store.docstore._dict:
            doc = self.preference_store.docstore._dict[doc_id]
            if doc.metadata.get("type") == "preference":
                preferences.add(doc.page_content)
        return preferences

    def response(self, user_input: str):
        new_preferences = self.llm.extract_preferences(user_input)
        if new_preferences:
            current_preferences = self._get_user_preferences()
            new_docs = []
            for pref in new_preferences:
                if pref not in current_preferences:
                    pref_doc = Document(
                        page_content=pref,
                        metadata={"type": "preference"}
                    )
                    new_docs.append(pref_doc)

            if new_docs:
                if self.preference_store is None:
                    self.preference_store = FAISS.from_documents(new_docs, self.embeddings)
                else:
                    self.preference_store.add_documents(new_docs)
                self._save_preference_store()

        cocktail_docs = self.cocktail_store.similarity_search(user_input, k=6)
        knowledge = "\n---\n".join(doc.page_content for doc in cocktail_docs)
        all_preferences = self._get_user_preferences()
        preference_summary = ", ".join(all_preferences) if all_preferences else "None"
        return self.llm.gen_response(knowledge, preference_summary, user_input)
