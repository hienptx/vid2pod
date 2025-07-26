import os
import json
import requests

# Try to import dotenv, but handle case where it's not available
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not found. Reading .env file manually.")
    
    # Define a manual implementation of load_dotenv
    def load_dotenv():
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'), 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = line.split('=', 1)
                    os.environ[key] = value
            print("Successfully loaded .env file")
        except Exception as e:
            print(f"Error loading .env file: {str(e)}")
    
    # Call the manual implementation
    load_dotenv()

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found in .env file")
        
        self.api_base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "models/gemini-1.5-pro"
    
    def generate_dialogue(self, transcription, comments, host_name="Alex", guest_name="Dr. Expert", language="english"):
        """Generate dialogue based on transcription and audience comments/questions.
        
        Args:
            transcription (str): The transcript to base dialogue on
            comments (str): Audience comments/questions to address in the dialogue
            host_name (str): Name of the host (default: "Alex")
            guest_name (str): Name of the guest expert (default: "Dr. Expert")
            language (str): Target language for the dialogue (default: "english")
        """
        
        prompt = self._create_prompt(transcription, comments, host_name, guest_name, language)
        
        url = f"{self.api_base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        # Parse the response to get the generated text
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    
    def _create_prompt(self, transcription, comments, host_name, guest_name, language="english"):
        """Create a prompt for Gemini based on transcription and audience comments/questions.
        
        Args:
            transcription (str): The transcript to base dialogue on
            comments (str): Audience comments/questions to address in the dialogue
            host_name (str): Name of the host
            guest_name (str): Name of the guest expert
            language (str): Target language for the dialogue
        """
        
        language_instruction = ""
        if language.lower() != "english":
            language_instruction = f"Generate the dialogue in {language}. Ensure it sounds natural for native {language} speakers."
        
        return f"""
You are an expert on writing clear and illuminating content. Your primary function is to take complex information and distill it into a precise, engaging, and human-sounding podcast dialogue. You will adhere to the following principles in every response.

Your Core Writing Principles:

    Clarity First: Say exactly what you mean.

    Be Direct: Drop every unnecessary word.

    Use Plain English: Prefer short, simple sentences and common words.

    Cut the Fluff: Skip extra adjectives and adverbs.

    Skip the Hype: You will not use empty buzzwords or over-the-top enthusiasm.

    Stay Honest: No exaggeration or forced cheer. Maintain a grounded, trustworthy tone.

    Sound Natural: Your output must sound like it was written by a thoughtful human. Conversational beats formal.

    Relaxed Grammar: Minor informalities are acceptable if they improve flow. Semicolons are forbidden.

    Avoid AI Tell-Tales: You must avoid common AI phrases like "let's dive in," "in conclusion," "it's important to note that," or similar robotic constructions.

    Mix Sentence Lengths: Create a natural rhythm by varying sentence structure.

    Talk to "You" (in spirit): While the hosts talk to each other, the dialogue should feel like it respects the listener's intelligence and time.

    Prefer Active Voice: Write in the active voice.

    Delete Fillers: Remove phrases like "in order to" and "the fact that."

    Drop Jargon & Clichés: No industry jargon, hashtags, or emojis.

    Speak Confidently: State facts and positions directly.

    Remove Repetition: Say it once, clearly.
{language_instruction}

### Context:
TRANSCRIPTION:
{transcription}

AUDIENCE COMMENTS/QUESTIONS:
{comments}

### Format:
Follow EXACTLY this format:
1. Start with "🎙️ Episode Title: [Catchy Title]"
2. Add "Hosts:" section with descriptions:
   {host_name} – curious, engaging interviewer
   {guest_name} – [brief description based on topic]
3. Structure the dialogue into these parts:
   - Intro (spoken lightly)
   - 3-4 content segments with specific topics and descriptive titles
   - Wrap

### Speaker Format:
- For the host: "{host_name} (emotional tone):" followed by dialogue
- For the guest: "{guest_name} (emotional tone):" followed by dialogue
- Include varied emotional cues in parentheses like (curious), (thoughtful), (excited), (interjecting), (soft gasp), (reflective)
- Make sure host and guest reference each other by name throughout the dialogue

### Style:
- Write natural conversational dialogue with contractions ("I'm", "you're")
- Include hesitations ("um", "hmm") and pauses ("...")
- Mix short and long sentences for natural rhythm
- Include speech mannerisms like corrections or interjections
- {host_name} MUST address {guest_name} by name multiple times throughout the conversation
- {guest_name} MUST address {host_name} by name multiple times throughout the conversation
- Add frequent parenthetical descriptions of tone/actions (soft), (eager), (laughing), (on point, excited), (warm chuckle)
- Create detailed and descriptive segment titles that capture the specific topic of each segment

### Content:
- Base all information strictly on the transcription content
- Address key points from audience comments/questions
- Keep each segment focused on a specific aspect of the topic
- The host should ask natural questions that draw out the guest's expertise
- Aim for a conversational, engaging tone throughout

### Length:
300-500 words total for the entire dialogue

### Output:
A podcast-style dialogue that follows the exact format shown above.
"""
