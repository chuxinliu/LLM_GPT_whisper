import openai
from langchain.llms import OpenAI 

class OpenAIManager:
    """Manages interactions with OpenAI's Whisper and GPT-4 models."""
    
    def __init__(self, api_key=""):
        openai.api_key = api_key
        self.llm = OpenAI(temperature=0.2)
    
    def transcribe_audio(self, audio_file, model="whisper-1", prompt="金融, 中英混杂"):
        transcript = openai.Audio.transcribe(
            model=model,
            file=audio_file,
            response_format="text",
            prompt=prompt
        )
        return transcript
    
    def generate_text(self, messages):
        completion = self.llm.generate(messages)
        return completion['choices'][0]['message']['content']
