import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_personality_analysis(interpretation):
    """
    Stage 7: Gemini-powered Personality Analysis
    Takes the rule-based interpretation and generates a 3-sentence personality summary.
    """
    if not api_key:
        print("[Stage 7] GEMINI_API_KEY not found in environment.")
        return "Gemini API key not found. Please check your .env file."
    
    print("[Stage 7] Requesting personality analysis from AI")
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Format the interpretation into a descriptive string for the prompt
        features_summary = []
        for category, traits in interpretation.items():
            if traits:
                features_summary.append(f"- {category.capitalize()}: {', '.join(traits)}")
        
        prompt = f"""
You are a physiognomy expert. Based on the following facial features of a person:

{os.linesep.join(features_summary)}

Please provide exactly 3 sentences describing this person's personality.
Requirements:
1. Focus only on the strengths, positive traits, and encouraging potential in their personality.
2. Absolutely do not mention any weaknesses, flaws, or negative aspects.
3. The tone should be formal, refined, and encouraging.
4. Present the analysis as exactly 3 consecutive sentences, without numbering.
"""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Could not generate personality analysis at this moment."
            
    except Exception as e:
        print(f"[Stage 7] Error calling Gemini API: {str(e)}")
        return f"Personality analysis is temporarily unavailable."
