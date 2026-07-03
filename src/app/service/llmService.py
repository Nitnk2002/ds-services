import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from app.service.Expense import Expense
import httpx

class LLMService:
    def __init__(self):
        load_dotenv()

        # Prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                ("human", "{text}")
            ]
        )

        # API keys
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        # Primary LLM (Mistral)
        self.mistral = ChatMistralAI(
            api_key=self.mistral_key,
            model="mistral-small-latest",
            temperature=0
        )

        # Fallback LLM (OpenAI)
        self.openai = ChatOpenAI(
            api_key=self.openai_key,
            model="gpt-4o-mini",
            temperature=0
        )

        # Build pipeline
        self.runnable = self.prompt | self.mistral.with_structured_output(schema=Expense)

    def runLLM(self, message):
        try:
            # Try Mistral first
            return self.runnable.invoke({"text": message})
        except httpx.HTTPStatusError as e:
            # Handle 429 / tier exceeded
            if e.response.status_code == 429:
                print("⚠️ Mistral capacity exceeded, falling back to OpenAI...")
                fallback_runnable = self.prompt | self.openai.with_structured_output(schema=Expense)
                return fallback_runnable.invoke({"text": message})
            else:
                raise e
