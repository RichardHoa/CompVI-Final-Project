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
Bạn là một chuyên gia nhân tướng học (physiognomy expert). Dựa trên các đặc điểm diện mạo sau đây của một người:

{os.linesep.join(features_summary)}

Hãy đưa ra đúng 3 câu nhận xét về tính cách của người này. 
Yêu cầu:
1. Chỉ tập trung vào những điểm mạnh, điểm tốt và tiềm năng tích cực trong tính cách.
2. Tuyệt đối không nhắc đến bất kỳ điểm yếu, điểm xấu hay khía cạnh tiêu cực nào.
3. Văn phong trang trọng, tinh tế và mang tính khích lệ.
4. Trình bày dưới dạng 3 câu văn liên tiếp, không đánh số.
"""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Không thể tạo phân tích tính cách lúc này."
            
    except Exception as e:
        print(f"[Stage 7] Error calling Gemini API: {str(e)}")
        return f"Phân tích tính cách tạm thời không khả dụng."
