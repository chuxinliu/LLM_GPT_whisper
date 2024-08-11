import openai
client = openai.OpenAI()

class OpenAIManager:
    """Manages interactions with OpenAI's Whisper and GPT-4 models."""
    
    def __init__(self, api_key=""):
        openai.api_key = api_key
    
    def transcribe_audio(self, audio_file):
        ''' SOTA Whisper-1 Model: transcribe audio to text"""
        transcript = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file
        )
        return transcript.text
    
    def generate_text(self, messages):
        """Generate text using the standard completion mode."""
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个出色和严谨的新闻稿记者。"},
                {"role": "user", "content": f"{messages}"}
            ]
        )
        return completion.choices[0].message.content
