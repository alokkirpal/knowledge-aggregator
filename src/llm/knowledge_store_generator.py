import json
from pathlib import Path

from google import genai


class KnowledgeStoreGenerator:

    def __init__(self, api_key):

        self.client = genai.Client(
            api_key=api_key
        )

        self.prompt = Path(
            "prompts/knowledge_store_prompt.txt"
        ).read_text()

    def generate(self, chunks):

        prompt = self.prompt.replace(

            "{{CHUNKS}}",

            json.dumps(
                chunks,
                indent=2
            )

        )

        response = self.client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return response.text