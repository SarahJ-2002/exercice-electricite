from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"

st.set_page_config(page_title="L'électricité dans 12 quartiers", page_icon="⚡", layout="wide")

st.title("L'électricité dans 12 quartiers")
st.caption("Relevés mensuels de janvier 2024 à décembre 2025. Données fictives.")

# --- ÉTAPE 1 : Fichier brut (on le garde pour comparaison ou on l'enlève plus tard) ---
brut = pd.read_csv(DOSSIER / "consommation_brut.csv")
st.write(f"Le fichier brut compte {len(brut)} lignes.")
st.dataframe(brut.head(10), hide_index=True)

# --- ÉTAPE 2 : Lecture des données propres ---
@st.cache_data
def charger_donnees():
    # On lit le fichier propre généré par le notebook
    return pd.read_csv(DOSSIER / "consommation_propre.csv")

df = charger_donnees()

# Deux phrases de contexte
st.info("Ces données ont été nettoyées et enrichies avec les informations de quartiers et la météo.")
st.write(f"Le fichier propre contient {len(df)} lignes prêtes pour l'analyse.")

# Affichage d'un aperçu des données propres
st.dataframe(df.head(10), hide_index=True)