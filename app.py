import streamlit as st
import requests
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# =================== TITLE =====================
st.title("🌾 Generative AI for Pest Control")
st.write("Enter crop and pest info, let AI suggest eco-friendly strategies!")

# =================== USER INPUTS ===============
crop = st.text_input("🌱 Enter your crop (e.g., Wheat, Tomato, Rice)")
pest = st.text_input("🐛 Enter pest (e.g., Aphids, Locusts, Nematodes)")
climate = st.selectbox("☁️ Select climate condition", ["Dry", "Humid", "Rainy", "Hot", "Cold"])

# =================== GEMINI CALL ===============
def get_gemini_strategies(crop, pest, climate):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Suggest eco-friendly pest control strategies for {pest} affecting {crop} in {climate} conditions. Provide 3 clear strategies."
            }]
        }]
    }
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "⚠️ Could not parse Gemini response."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# =================== BUTTON ====================
if st.button("🔮 Generate Strategy"):
    if crop and pest:
        with st.spinner("✨ Thinking with Gemini... generating strategies..."):
            strategies = get_gemini_strategies(crop, pest, climate)
        st.subheader("✅ Suggested Pest Control Strategies:")
        st.write(strategies)
    else:
        st.warning("Please enter both crop and pest to generate strategies.")

