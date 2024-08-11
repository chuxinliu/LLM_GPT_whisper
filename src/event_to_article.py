from src.file_manager import FileManager
from src.openai_manager import OpenAIManager

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
            # audio_file = self.file_manager.read_file(audio, 'rb')
            entire_transcript += self.openai_manager.transcribe_audio(audio)
        return entire_transcript
    
    def modify_transcript(self, transcript):
        messages = [
            {"role": "system", "content": "你是一个活动现场的笔记员，你将活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节。"},
            {"role": "user", "content": f"将接下来这段活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节，录音稿在这里：{transcript}"}
        ]
        return self.openai_manager.generate_text(messages)
    
    def generate_news(self, prompt):
        messages = [
            {"role": "system", "content": "你是一个新闻撰稿人,你的任务是将金融讲座活动的录音转成一篇2000字左右的新闻报道。你必须模仿以前的新闻报道。"},
            {"role": "user", "content": prompt}
        ]
        return self.openai_manager.generate_text(messages)
    
    def create_news_prompt(self, sample, transcript, preview):
        return f"模仿以前的新闻报道，以前的新闻稿是这样的：{sample}。接下来这段录音稿是这次活动的现场录音，内容是这样的：{transcript}。这次活动的预告内容是这样的：{preview}。将这个录音稿，结合活动预告内容，你必须模仿以前的新闻稿，在活动预告的基础上，写一份新的2000字左右的新闻报道。"
