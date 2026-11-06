from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"

# Configuration de la page
st.set_page_config(page_title="L'électricité dans 12 quartiers", page_icon="⚡", layout="wide")

st.title("L'électricité dans 12 quartiers")
st.caption("Relevés mensuels de janvier 2024 à décembre 2025. Données fictives.")

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

# --- ÉTAPE 4 : Indicateurs clés ---
st.subheader(f"Indicateurs clés pour l'année {annee_choisie}")

# Calcul des indicateurs
total_kwh = df_filtre["kwh"].sum() / 1_000_000 # En millions
moyenne_abonne = df_filtre["kwh_par_abonne"].mean()
moyenne_heures = df_filtre["heures_courant"].mean()

# Affichage côte à côte
col1, col2, col3 = st.columns(3)

col1.metric("Consommation totale", f"{total_kwh:.2f} M kWh")
col2.metric("Moyenne par abonné", f"{moyenne_abonne:.1f} kWh")
col3.metric("Heures de courant moy.", f"{moyenne_heures:.1f} h")

st.divider()

# Affichage des données filtrées
st.subheader("Données filtrées")
st.dataframe(df_filtre, hide_index=True)