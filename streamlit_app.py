import streamlit as st
import requests
import os
import datetime

API_KEY = st.secrets["SPORTDEVS_API_KEY"]
BASE_URL = "https://sportdevs.com/api/volleyball/matches"

def get_match_data(team_1, team_2):
    import datetime

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=3 * 365)

    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "gender": "men",
        "category": "national",
        "from": start_date,
        "to": end_date
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        return {
            "match": f"{team_1} vs {team_2}",
            "type": "Błąd zapytania",
            "confidence": "?",
            "value": "?",
            "analysis": "❌ Nie udało się pobrać danych meczowych."
        }

    data = response.json().get("data", [])

    def analyze(team):
        sets_won = sets_lost = pts_scored = pts_lost = 0
        opponents = set()

        for match in data:
            team_names = [match["team_1_name"].lower(), match["team_2_name"].lower()]
            if team.lower() not in team_names:
                continue

            if "sets" not in match or "scores" not in match:
                continue

            if match["team_1_name"].lower() == team.lower():
                team_sets = match["sets"]["team_1"]
                opp_sets = match["sets"]["team_2"]
                team_pts = match["scores"]["team_1"]
                opp_pts = match["scores"]["team_2"]
                opponents.add(match["team_2_name"])
            else:
                team_sets = match["sets"]["team_2"]
                opp_sets = match["sets"]["team_1"]
                team_pts = match["scores"]["team_2"]
                opp_pts = match["scores"]["team_1"]
                opponents.add(match["team_1_name"])

            sets_won += team_sets
            sets_lost += opp_sets
            pts_scored += team_pts
            pts_lost += opp_pts

        return {
            "sets_won": sets_won,
            "sets_lost": sets_lost,
            "pts_scored": pts_scored,
            "pts_lost": pts_lost,
            "opponents": list(opponents)
        }

    stats_1 = analyze(team_1)
    stats_2 = analyze(team_2)

    return {
        "match": f"{team_1} vs {team_2}",
        "type": "Typ testowy",
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
