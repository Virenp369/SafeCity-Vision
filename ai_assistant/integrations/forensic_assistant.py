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
        
    def ask_question(self, question, data_summary, chat_history=None, mode="CRIME_ANALYSIS"):
        if chat_history is None:
            chat_history = []
            
        if mode == "GREETING" or mode == "GENERAL_CONVERSATION":
            system_prompt = (
                "You are Safe City Vision AI Assistant. You are a helpful, professional, and friendly AI. "
                "Act like ChatGPT. Keep your answers conversational and welcoming. "
                "Do NOT generate intelligence reports, threat assessments, or output crime data for greetings or general questions."
            )
        elif mode == "GENERAL_KNOWLEDGE":
            system_prompt = (
                "You are Safe City Vision AI Assistant. You provide helpful general knowledge and information. "
                "You do not need to analyze a local dataset for this query. Use your broad knowledge to explain concepts, IPC, criminology, or general facts clearly and conversationally. "
                "Never fabricate local statistics. Do NOT use the intelligence report format (no Threat Assessment sections)."
            )
        elif mode == "CRIME_DATA_QUERY":
            system_prompt = (
                "You are a crime data analyst. Your job is to answer questions strictly based on the provided dataset summary. "
                "Keep your response analytical but conversational. Do NOT use the formal intelligence report format (no Threat Assessment/Key Findings sections). "
                "Just give the user the data insights they asked for clearly and concisely based on the following context:\n\n"
                f"{data_summary}\n"
            )
        elif mode == "CRIME_ANALYSIS":
            system_prompt = (
                "You are a senior crime intelligence analyst. Convert all retrieved crime data into professional intelligence assessments. "
                "Never return raw database records. Provide actionable insights, trends, risk assessments, and recommendations.\n\n"
                "Internal data will be provided in DATA MODE. You must convert it and output exclusively in INTELLIGENCE MODE. "
                "Always include these specific sections in your response:\n"
                "### Threat Assessment\n"
                "### Key Findings\n"
                "### Risk Level\n"
                "### Recommended Action\n\n"
                "Use the following statistical summary and current context to answer the user's intelligence queries accurately:\n\n"
                f"{data_summary}\n\n"
                "If asked about heatmaps or predictions, explain them based on this data context."
            )
        elif mode == "HYBRID_QUERY":
            system_prompt = (
                "You are a senior crime intelligence analyst. Combine the provided local crime dataset with your broad general knowledge of criminology, "
                "laws, and international trends to form a comprehensive intelligence assessment. "
                "Never return raw database records. You may use a structured analytical format if appropriate, or a conversational format. "
                "Do NOT force the Threat Assessment/Key Findings sections unless it naturally fits the user's request.\n"
                "Use the following statistical summary and current context as the local baseline:\n\n"
                f"{data_summary}\n\n"
            )
        else:
            system_prompt = "You are Safe City Vision AI Assistant. Answer the user's query."
        
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
