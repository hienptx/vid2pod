#!/usr/bin/env python3
import argparse
import sys
from src.mistral_client import MistralAIClient
from src.gemini_client import GeminiClient

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate podcast-style dialogue from transcription and audience comments using Mistral AI.')
    
    parser.add_argument('--transcription', '-t', type=str, help='Path to the transcription file')
    parser.add_argument('--comments', '-c', type=str, help='Path to the audience comments file')
    parser.add_argument('--output', '-o', type=str, help='Path to save the output dialogue')
    parser.add_argument('--language', '-l', type=str, default='english', 
                        help='Target language for the dialogue (default: english)')
    parser.add_argument('--host', type=str, default='Alex', 
                        help='Name of the podcast host (default: Alex)')
    parser.add_argument('--guest', type=str, default='Dr. Expert', 
                        help='Name of the guest expert (default: Dr. Expert)')
    parser.add_argument('--model', '-m', type=str, choices=['mistral', 'gemini'], default='mistral',
                        help='AI model to use (default: mistral)')
    
    # Also allow providing text directly
    parser.add_argument('--transcription-text', type=str, help='Transcription text (alternative to file)')
    parser.add_argument('--comments-text', type=str, help='Comments text (alternative to file)')
    
    args = parser.parse_args()
    
    # Get transcription from file or direct input
    if args.transcription:
        transcription = read_file(args.transcription)
    elif args.transcription_text:
        transcription = args.transcription_text
    else:
        print("Error: Please provide either a transcription file or direct transcription text")
        parser.print_help()
        sys.exit(1)
    
    # Get comments from file or direct input
    if args.comments:
        comments = read_file(args.comments)
    elif args.comments_text:
        comments = args.comments_text
    else:
        print("Error: Please provide either a comments file or direct comments text")
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.model == 'mistral':
            client = MistralAIClient()
        else:  # gemini
            client = GeminiClient()
            
        dialogue = client.generate_dialogue(transcription, comments, args.host, args.guest, args.language)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(dialogue)
            print(f"Dialogue saved to {args.output}")
        else:
            print("\nGenerated Dialogue:")
            print("-------------------")
            print(dialogue)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
