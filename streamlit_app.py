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
    "cypr": "cyprus",
    "słowenia": "Slovenia",

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


def get_match_data(team_1_pl, team_2_pl):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=3*365)

    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Zmieniamy polskie nazwy na angielskie
    team_1 = TEAM_NAME_MAP.get(team_1_pl.lower())
    team_2 = TEAM_NAME_MAP.get(team_2_pl.lower())

    if not team_1 or not team_2:
        return {
            "match": f"{team_1_pl} vs {team_2_pl}",
            "type": "Nie znaleziono drużyny",
            "confidence": "❌",
            "value": "❌",
            "analysis": f"Jedna z drużyn nie została rozpoznana. Upewnij się, że wpisujesz nazwę poprawnie (np. 'polska', 'włochy')."
        }

    team_1_id = TEAM_IDS[team_1]
    team_2_id = TEAM_IDS[team_2]

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
