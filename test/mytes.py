import re
from app import therapy_chat

def test_therapy_chat_output_structure():
    user_input = "I'm feeling really anxious and overwhelmed lately."
    history = []

    formatted_response, updated_history = therapy_chat(user_input, history)

    # ✅ Test if response is returned
    assert isinstance(formatted_response, str)
    assert isinstance(updated_history, list)
    assert len(updated_history) == 2

    # ✅ Check for expected keywords in AI response
    ai_response = updated_history[-1][1]
    assert "Detected Emotion:" in ai_response
    assert "THERAPEUTIC RESPONSE:" in ai_response
    assert "WELLNESS TIPS:" in ai_response

    # ✅ Check if exactly 4 tips are returned
    tips_match = re.findall(r"• ", ai_response)
    assert len(tips_match) == 4
