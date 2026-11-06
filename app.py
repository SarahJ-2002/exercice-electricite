from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"

st.set_page_config(page_title="L'électricité dans 12 quartiers", page_icon="⚡", layout="wide")

st.title("L'électricité dans 12 quartiers")
st.caption("Relevés mensuels de janvier 2024 à décembre 2025. Données fictives.")

# --- ÉTAPE 1 : Fichier brut (on peut l'enlever pour gagner de la place) ---
# brut = pd.read_csv(DOSSIER / "consommation_brut.csv")
# st.write(f"Le fichier brut compte {len(brut)} lignes.")
# st.dataframe(brut.head(10), hide_index=True)

# --- ÉTAPE 2 : Lecture des données propres ---
@st.cache_data
def charger_donnees():
    return pd.read_csv(DOSSIER / "consommation_propre.csv")

df = charger_donnees()

st.info("Ces données ont été nettoyées et enrichies avec les informations de quartiers et la météo.")

# --- ÉTAPE 3 : Filtres dans la barre latérale ---
st.sidebar.header("Filtres")

# 1. Filtre des communes (toutes cochées par défaut)
toutes_communes = df["commune"].unique()
communes_choisies = st.sidebar.multiselect(
    "Choisissez des communes :", 
    toutes_communes, 
    default=toutes_communes
)

# 2. Filtre de l'année (2025 par défaut)
annees = sorted(df["annee"].unique())
annee_choisie = st.sidebar.selectbox(
    "Choisissez une année :", 
    annees, 
    index=len(annees)-1 # Met la dernière année (2025) par défaut
)

# Message si aucune commune n'est choisie
if not communes_choisies:
    st.warning("⚠️ Veuillez sélectionner au moins une commune.")
    st.stop() # Arrête l'exécution ici

# Application des filtres au tableau de données
df_filtre = df[(df["commune"].isin(communes_choisies)) & (df["annee"] == annee_choisie)]

# Affichage des données filtrées (on remplace le head(10) global par le tableau filtré)
st.dataframe(df_filtre, hide_index=True)