import streamlit as st
import requests

st.title("Volleybuk – Beta v0.1")

team_1 = st.text_input("Drużyna 1:")
team_2 = st.text_input("Drużyna 2:")

if st.button("Analizuj"):
    if team_1 and team_2:
        # Przykład testowy
        st.subheader(f"📊 Analiza meczu: {team_1} vs {team_2}")
        st.write("🏐 Typ: " + team_1 + " -3,5")
        st.write("📈 Pewność: 82%")
        st.write("🔥 Value: Wysokie")
        st.write("Komentarz: Przewaga formy i punktów na set.")
    else:
        st.warning("Podaj obie drużyny.")
