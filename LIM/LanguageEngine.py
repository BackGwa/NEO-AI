import re
import google.generativeai as llm

class LanguageEngine:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", system_prompt: str = "", temperature: float = 1.0):
        llm.configure(api_key=api_key)
        self.config = {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 4096,
            "response_mime_type": "text/plain",
        }
        self.model = llm.GenerativeModel(
            model_name=model,
            generation_config=self.config,
            system_instruction=system_prompt
        )
        self.session = self.model.start_chat(history=[])

    def request(self, prompt: str) -> str:
        result = self.session.send_message(prompt)
        return self.__parse_string__(result.text)

    def __parse_string__(self, input_str: str) -> tuple:
        raw_match = re.search(r'<raw>(.*?)<\/raw>', input_str, re.DOTALL)
        if raw_match:
            return ("raw", raw_match.group(1).strip())
        
        command_match = re.search(r'<command>(.*?)<\/command>', input_str, re.DOTALL)
        if command_match:
            return ("command", command_match.group(1).strip())