import streamlit as st
import requests
import os

st.set_page_config(page_title="Volleybuk v0.2", layout="centered")
st.title("🏐 Volleybuk – typy siatkarskie na żywo")

API_KEY = st.secrets["SPORTDEVS_API_KEY"]
BASE_URL = "https://sportdevs.com/api/volleyball/matches"

def get_match_data(team_1, team_2):
    # Placeholder na analizę drużyn
    return {
        "match": f"{team_1} vs {team_2}",
        "type": f"{team_1} -1.5 seta",
        "confidence": "81%",
        "value": "Wysokie",
        "analysis": f"{team_1} wygrało 4 z 5 ostatnich meczów, średnia różnica punktów: +6.3"
    }

team_1 = st.text_input("Drużyna 1", "")
team_2 = st.text_input("Drużyna 2", "")

if st.button("Analizuj"):
    if team_1 and team_2:
        with st.spinner("Analizuję dane..."):
            result = get_match_data(team_1, team_2)
        st.subheader(f"📊 {result['match']}")
        st.write(f"🏐 **Typ:** {result['type']}")
        st.write(f"📈 **Pewność:** {result['confidence']}")
        st.write(f"🔥 **Value:** {result['value']}")
        st.info(f"🧠 {result['analysis']}")
    else:
        st.warning("Wpisz poprawnie obie drużyny.")
