''''
Use OPEN AI whipser and GPT-4 to convert Chuancheng event audio to news article
Created: 2024-03-10 by Chuxin Liu
'''

import openai
import os

OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# read txt file
def read_txt(file):
    with open(file, 'r') as file:
        file_contents = file.read()
    return file_contents

# write txt file
def write_txt(file, content):
    with open(file, 'w') as file:
        file.write(content)

# read audio file
def read_m4a(file):
    return open(file, 'rb')

# audio to text
def retrive_transcript(audio_file):
    transcipt = client.audio.transcriptions.create(
       model="whisper-1",
       file=audio_file,
       response_format="text",
       prompt="金融, 中英混杂"
       )
    return transcipt
def combine_transcript(audio_files):
    entire_transcript = ""
    for audio in audio_files: 
        entire_transcript += retrive_transcript(read_m4a(audio))
    return entire_transcript
def write_raw_transcript(transcript):
    write_txt("raw_transcript.txt", transcript)

# raw text to structured text
def modify_transcript(prompt):
    completion = client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=[
            {"role": "system", "content": "你是一个活动现场的笔记员，你将活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节。"},
            {"role": "user", "content": f"将接下来这段活动录音重写，并写成有问有答的，有逻辑的，有结构的录音稿。并尽可能保留原文的内容和细节，录音稿在这里：{prompt}"}
            ]
            )
    return completion.choices[0].message.content
def write_modified_transcript(transcript):
    write_txt("modified_transcript.txt", transcript)

# news article generation
def generate_news(prompt):
    completion = client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=[
            {"role": "system", "content": "你是一个新闻撰稿人,你的任务是将金融讲座活动的录音转成一篇2000字左右的新闻报道。你必须模仿以前的新闻报道。"},
            {"role": "user", "content": prompt}
            ]
            )
    return completion.choices[0].message.content
def write_news(news):
    write_txt("news.txt", news)

# final pipeline
def pipeline(audio_files, preview_file, sample_file):
    
    entire_transcript = combine_transcript(audio_files)
    write_raw_transcript(entire_transcript)

    modified_transcript = modify_transcript(entire_transcript)
    write_modified_transcript(modified_transcript)

    preview = read_txt(preview_file) 
    news_sample = read_txt(sample_file)
    prompt = f"你需要模仿以前的新闻报道，以前的新闻稿是这样的：{news_sample}。接下来这段录音稿是这次活动的现场录音，内容是这样的：{modified_transcript}。这次活动的预告内容是这样的：{preview}。将这个录音稿，结合活动预告内容，你必须模仿以前的新闻稿，在活动预告的基础上，写一份新的2000字左右的新闻报道。"
    
    news = generate_news(prompt)
    write_news(news)
    return news


# --------------------------------------------------------------------------------------------------------

# Inputs
audio_files = ["Balance Arts Center 1st half.m4a", "Balance Arts Center 2nd half.m4a"]
preview_file = '0207event_description.txt'
sample_file = 'news_sample.txt'

# Output
news = pipeline(audio_files, preview_file, sample_file)
print(news)

# Translate to English
news_en = client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=[{"role": "system", "content": "translate to english"},
                  {"role": "user", "content": news}])
write_txt("news_en.txt", news_en.choices[0].message.content)



