''''
Use OPEN AI whipser and GPT-4 to convert Chuancheng event audio to news article
Created: 2024-03-11 by Chuxin Liu
'''

import openai
import os

class FileManager:
    """Handles reading and writing of files."""
    # Using static methods without creating an instance of the class
    # This is because the class doesn't need to maintain state or access instance variables
    
    @staticmethod
    def read_file(file, mode='r'):
        # 'r' for reading text files, 'rb' for reading binary files (audio files)
        with open(file, mode) as f:
            return f.read() if mode == 'r' else open(file, 'rb')
    
    @staticmethod
    def write_file(file, content):
        with open(file, 'w') as f:
            f.write(content)

class OpenAIManager:
    """Manages interactions with OpenAI's Whisper and GPT-4 models."""
    
    def __init__(self, api_key=""):
        self.client = openai.OpenAI(api_key=api_key)
    
    def transcribe_audio(self, audio_file, model="whisper-1", prompt="金融, 中英混杂"):
        transcript = self.client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text",
            prompt=prompt
        )
        return transcript
    
    def generate_text(self, model, messages):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message.content

class EventToArticle:
    """Converts event audio to a structured news article."""
    
    def __init__(self, api_key):
        self.file_manager = FileManager()
        self.openai_manager = OpenAIManager(api_key)
    
    def pipeline(self, audio_files, preview_file, sample_file):
        entire_transcript = self.combine_transcripts(audio_files)
        self.file_manager.write_file("raw_transcript.txt", entire_transcript)
        
        modified_transcript = self.modify_transcript(entire_transcript)
        self.file_manager.write_file("modified_transcript.txt", modified_transcript)
        
        preview = self.file_manager.read_file(preview_file)
        news_sample = self.file_manager.read_file(sample_file)
        prompt = self.create_news_prompt(news_sample, modified_transcript, preview)
        
        news = self.generate_news(prompt)
        self.file_manager.write_file("news.txt", news)
        
        return news
    
    def combine_transcripts(self, audio_files):
        entire_transcript = ""
        for audio in audio_files:
            audio_file = self.file_manager.read_file(audio, 'rb')
            entire_transcript += self.openai_manager.transcribe_audio(audio_file)
        return entire_transcript
    
    def modify_transcript(self, transcript):
        messages = [
            {"role": "system", "content": "你是一个活动现场的笔记员，你将活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节。"},
            {"role": "user", "content": f"将接下来这段活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节，录音稿在这里：{transcript}"}
        ]
        return self.openai_manager.generate_text('gpt-4-0125-preview', messages)
    
    def generate_news(self, prompt):
        messages = [
            {"role": "system", "content": "你是一个新闻撰稿人,你的任务是将金融讲座活动的录音转成一篇2000字左右的新闻报道。你必须模仿以前的新闻报道。"},
            {"role": "user", "content": prompt}
        ]
        return self.openai_manager.generate_text('gpt-4-0125-preview', messages)
    
    def create_news_prompt(self, sample, transcript, preview):
        return f"你需要模仿以前的新闻报道，以前的新闻稿是这样的：{sample}。接下来这段录音稿是这次活动的现场录音，内容是这样的：{transcript}。这次活动的预告内容是这样的：{preview}。将这个录音稿，结合活动预告内容，你必须模仿以前的新闻稿，在活动预告的基础上，写一份新的2000字左右的新闻报道。"

# # Example usage
api_key = ""
event_to_article = EventToArticle(api_key)
audio_files = ["Balance Arts Center 1st half.m4a", "Balance Arts Center 2nd half.m4a"]
preview_file = '0207event_description.txt'
sample_file = 'news_sample.txt'
news = event_to_article.pipeline(audio_files, preview_file, sample_file)
print(news)

# To translate the news to English, you'd use the OpenAIManager's generate_text method with appropriate translation prompts.
openai = OpenAIManager(api_key=api_key)
message_test = [
            {"role": "system", "content": "You are a bilingual journalist. You translate a chinese news article into an English one."},
            {"role": "user", "content": news}
        ]
news_en = openai.generate_text(model='gpt-4-0125-preview', messages=message_test)
FileManager.write_file("news_en.txt", news_en)
print(news_en)