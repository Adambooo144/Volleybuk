import streamlit as st
import requests
import os
import datetime

API_KEY = st.secrets["LNwMzcExgkaJ8-CUPLc_zQ"]
BASE_URL = "https://sportdevs.com/api/volleyball/matches"


def get_match_data(team_1, team_2):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=3*365)

    headers = {"Authorization": f"Bearer {API_KEY}"}

    def get_team_matches(team):
        response = requests.get(
            f"{BASE_URL}?team_name={team}&from={start_date}&to={end_date}",
            headers=headers
        )
        if response.status_code != 200:
            return []
        return response.json().get("data", [])

    matches_1 = get_team_matches(team_1)
    matches_2 = get_team_matches(team_2)

    def analyze_team(matches):
        sets_won = sets_lost = pts_scored = pts_lost = 0
        opponents = set()
        for match in matches:
            if "sets" not in match or "scores" not in match:
                continue
            team_sets = match["sets"]["team"]
            opp_sets = match["sets"]["opponent"]
            sets_won += team_sets
            sets_lost += opp_sets
            pts_scored += match["scores"]["team"]
            pts_lost += match["scores"]["opponent"]
            opponents.add(match.get("opponent_name", ""))
        return {
            "sets_won": sets_won,
            "sets_lost": sets_lost,
            "pts_scored": pts_scored,
            "pts_lost": pts_lost,
            "opponents": list(opponents)
        }

    stats_1 = analyze_team(matches_1)
    stats_2 = analyze_team(matches_2)

    # Na razie zwróćmy surowe dane
    return {
        "match": f"{team_1} vs {team_2}",
        "type": f"Typ testowy",
        "confidence": "?", 
        "value": "?",
        "analysis": f"{team_1}: {stats_1}, {team_2}: {stats_2}"
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
