import streamlit as st
import requests
import os
import datetime

API_KEY = st.secrets["SPORTDEVS_API_KEY"]
BASE_URL = "https://sportdevs.com/api/volleyball/matches"

# Mapa polskich nazw na angielskie
TEAM_NAME_MAP = {
    "kanada": "canada",
    "usa": "usa",
    "niemcy": "germany",
    "anglia": "england",
    "san marino": "san marino",
    "oman": "oman",
    "maroko": "morocco",
    "norwegia": "norway",
    "kostaryka": "costa rica",
    "armenia": "armenia",
    "irlandia północna": "northern ireland",
    "tunezja": "tunisia",
    "irlandia": "ireland",
    "rosja": "russia",
    "egipt": "egypt",
    "brazylia": "brazil",
    "holandia": "netherlands",
    "hiszpania": "spain",
    "szkocja": "scotland",
    "szwajcaria": "switzerland",
    "włochy": "italy",
    "walia": "wales",
    "korea południowa": "south korea",
    "rumunia": "romania",
    "japonia": "japan",
    "australia": "australia",
    "andora": "andorra",
    "malta": "malta",
    "algieria": "algeria",
    "hongkong": "hong kong",
    "meksyk": "mexico",
    "urugwaj": "uruguay",
    "francja": "france",
    "katar": "qatar",
    "argentyna": "argentina",
    "arabia saudyjska": "saudi arabia",
    "portugalia": "portugal",
    "grecja": "greece",
    "czechy": "czech republic",
    "dania": "denmark",
    "belgia": "belgium",
    "ekwador": "ecuador",
    "kolumbia": "colombia",
    "irak": "iraq",
    "polska": "poland",
    "serbia": "serbia",
    "kuwejt": "kuwait",
    "peru": "peru",
    "cypr": "cyprus"
}

# Mapowanie angielskich nazw na ID z API
TEAM_IDS = {
    "canada": 1,
    "usa": 2,
    "germany": 3,
    "england": 4,
    "san marino": 5,
    "oman": 6,
    "morocco": 7,
    "norway": 8,
    "costa rica": 9,
    "armenia": 10,
    "northern ireland": 11,
    "tunisia": 12,
    "ireland": 13,
    "russia": 14,
    "egypt": 15,
    "brazil": 16,
    "netherlands": 17,
    "spain": 18,
    "scotland": 19,
    "switzerland": 20,
    "italy": 21,
    "wales": 22,
    "south korea": 23,
    "romania": 24,
    "japan": 25,
    "australia": 26,
    "andorra": 27,
    "malta": 28,
    "algeria": 30,
    "hong kong": 31,
    "mexico": 32,
    "uruguay": 33,
    "france": 34,
    "qatar": 35,
    "argentina": 36,
    "saudi arabia": 37,
    "portugal": 38,
    "greece": 39,
    "czech republic": 40,
    "denmark": 41,
    "belgium": 42,
    "ecuador": 43,
    "colombia": 44,
    "iraq": 45,
    "poland": 46,
    "serbia": 47,
    "kuwait": 48,
    "peru": 49,
    "cyprus": 50
}


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
