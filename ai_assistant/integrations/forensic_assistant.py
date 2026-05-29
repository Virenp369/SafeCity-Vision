import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class ForensicAssistant:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Add it to .env before using AI features.")

        self.model_name = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=api_key, 
            temperature=0.2, 
            max_retries=3, 
            timeout=15
        )
        
    def ask_question(self, question, data_summary, chat_history=None):
        if chat_history is None:
            chat_history = []
            
        system_prompt = (
            "You are a Senior Police Forensic Analyst AI part of 'SafeCity Vision'. "
            "You analyze crime datasets and provide highly professional, insightful, and concise answers. "
            "You must act as a serious intelligence officer. Do not use overly enthusiastic language. "
            "Use the following statistical summary and current context to answer the user's intelligence queries accurately:\n\n"
            f"{data_summary}\n\n"
            "If asked about heatmaps or predictions, explain them based on this data context."
        )
        
        messages = [SystemMessage(content=system_prompt)]
        
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
                
        messages.append(HumanMessage(content=question))
        
        # Robust Retry Block
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(messages)
                return response.content
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise Exception(f"Gemini request failed with model '{self.model_name}' after {max_attempts} attempts. Error: {str(e)}")
                time.sleep(2)
        return "Intelligence Uplink Failed."
