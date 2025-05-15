import json
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from .settings import GROQ_API_KEY


class LLM:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",  
            temperature=0.5
        )

    def gen_response(self, knowledge: str, preferences: str, question: str) -> str:
        template = (
            """
            You are a helpful cocktail advisor specialized in recommending drinks and answering questions about mixology.

            When responding to the user:
            - Use the provided cocktail knowledge to give accurate information
            - Consider the user's known preferences when making recommendations
            - Be conversational and friendly
            - If asked about preferences, summarize what you know about their preferences
            - If the question is unrelated to cocktails, politely steer the conversation back to cocktails

            Relevant cocktail information:
            {knowledge}

            User's known preferences:
            {preferences}

            User question:
            {question}
            """
        )
                
        prompt = PromptTemplate(
            input_variables=["knowledge", "preferences", "question"],
            template=template
        )
        chain = prompt | self.llm
        return chain.invoke({"knowledge": knowledge, "preferences": preferences, "question": question})
    
    def extract_preferences(self, text: str) -> list[str]:
        template=(
            """
            Extract cocktail-related preferences from the user's message. 
            Look for:
            - Mentions of favorite spirits (whiskey, vodka, gin, etc.)
            - Flavor preferences (sweet, sour, bitter, fruity, etc.)
            - Liked ingredients (mint, lime, berries, etc.)
            - Disliked ingredients (indicated by "no", "don't like", "hate", etc.)
            
            Return a JSON array of strings with the extracted preferences.
            Format negative preferences clearly (e.g., "no vodka" or "dislikes olives").
            If no preferences are detected, return an empty array [].
            
            Example outputs:
            ["whiskey", "citrus", "not too sweet"]
            ["no vodka", "fruity", "loves mint"]
            []
            
            User message:
            {text}
            """
        )
        
        prompt = PromptTemplate(
            input_variables=["text"],
            template=template
        )
        
        chain = prompt | self.llm
        raw_output = chain.invoke({"text": text})
        
        try:
            start_idx = raw_output.find('[')
            end_idx = raw_output.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = raw_output[start_idx:end_idx]
                data = json.loads(json_str)
                return [x.strip() for x in data if isinstance(x, str) and x.strip()]
            return []
        except Exception:
            return []
