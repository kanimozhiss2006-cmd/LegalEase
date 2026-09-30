import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add it to the .env file."
            )

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            self.model_name
        )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
You are an AI legal document drafting assistant.

Create a professional draft legal document.

DOCUMENT TYPE:
{document_type}

PARTIES INVOLVED:
{parties}

EFFECTIVE DATE:
{dates}

TERMS AND CONDITIONS:
{terms}

Instructions:

1. Create a professional legal document.
2. Include a clear title.
3. Include the parties involved.
4. Include the effective date.
5. Convert the supplied terms into proper clauses.
6. Organize the document using numbered sections.
7. Use formal and easy-to-understand language.
8. Include signature sections at the end.
9. Do not invent personal information.
10. Do not invent facts that were not provided.
11. Do not claim that the generated document is legal advice.
12. Return only the document text.
"""

        response = self.model.generate_content(prompt)

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()