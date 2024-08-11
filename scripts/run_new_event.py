''''
Use OPEN AI whipser and GPT-4 to convert Chuancheng event audio to news article
'''
import os

# change path to the repo root
import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

from src.event_to_article import EventToArticle

def main():
    # Set up API key from environment variable or hard-code for testing purposes
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Initialize the EventToArticle class
    event_to_article = EventToArticle(api_key)

    # Set up the path to the event directory
    event_dir = repo_root / "data" / "event0807"                            # Just change this every new event before running the script!
    # Specify the paths to your input files
    audio_files = list(event_dir.glob("*.m4a"))
    preview_file = list(event_dir.glob("*.txt"))[0]
    sample_file = repo_root / 'data' / 'samples' / 'news_sample.txt'
    
    # Run the pipeline
    news = event_to_article.pipeline(audio_files, preview_file, sample_file)
    
    # Print or log the output
    print("News article generated successfully!")
    print(news)

if __name__ == "__main__":
    main()
