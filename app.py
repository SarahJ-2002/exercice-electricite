from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DOSSIER = Path(__file__).parent / "donnees"

# Configuration de la page
st.set_page_config(page_title="L'électricité dans 12 quartiers", layout="wide")

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

toutes_communes = df["commune"].unique()
communes_choisies = st.sidebar.multiselect(
    "Choisissez des communes :", 
    toutes_communes, 
    default=toutes_communes
)

annees = sorted(df["annee"].unique())
annee_choisie = st.sidebar.selectbox(
    "Choisissez une année :", 
    annees, 
    index=len(annees)-1
)

if not communes_choisies:
    st.warning("Veuillez sélectionner au moins une commune.")
    st.stop()

df_filtre = df[(df["commune"].isin(communes_choisies)) & (df["annee"] == annee_choisie)]

# --- ÉTAPE 4 : Indicateurs clés ---
st.subheader(f"Indicateurs clés pour l'année {annee_choisie}")

total_kwh = df_filtre["kwh"].sum() / 1_000_000
moyenne_abonne = df_filtre["kwh_par_abonne"].mean()
moyenne_heures = df_filtre["heures_courant"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Consommation totale", f"{total_kwh:.2f} M kWh")
col2.metric("Moyenne par abonné", f"{moyenne_abonne:.1f} kWh")
col3.metric("Heures de courant moy.", f"{moyenne_heures:.1f} h")

st.divider()

# --- ÉTAPE 5 : Onglets d'analyse ---
st.subheader("Analyse par question")
tab1, tab2, tab3 = st.tabs(["Type de quartier", "Évolution par commune", "Chaleur ou courant ?"])

with tab1:
    st.write("Consommation par type de quartier")
    df_type = df_filtre.groupby("type")["kwh_par_abonne"].mean().reset_index()
    st.bar_chart(df_type.set_index("type"))
    st.write("Le secteur Commercial consomme beaucoup plus par abonné que le Résidentiel.")

with tab2:
    st.write("Évolution de la consommation par abonné")
    df_evol = df_filtre.groupby("mois")["kwh_par_abonne"].mean().reset_index()
    st.line_chart(df_evol.set_index("mois"))
    st.write("La consommation varie selon les mois de l'année.")

with tab3:
    st.write("La consommation suit-elle la chaleur ou le courant ?")
    df_resid = df_filtre[df_filtre["type"] == "Résidentiel"]
    
    fig, ax = plt.subplots()
    ax.scatter(df_resid["heures_courant"], df_resid["kwh_par_abonne"], alpha=0.5, color="blue")
    ax.set_xlabel("Heures de courant")
    ax.set_ylabel("kWh par abonné")
    st.pyplot(fig)
    
    corr_courant = df_resid["kwh_par_abonne"].corr(df_resid["heures_courant"])
    corr_temp = df_resid["kwh_par_abonne"].corr(df_resid["temperature_c"])
    
    st.write(f"Corrélation avec les heures de courant : {corr_courant:.2f}")
    st.write(f"Corrélation avec la température : {corr_temp:.2f}")

st.divider()

# Affichage des données filtrées
st.subheader("Données filtrées")
st.dataframe(df_filtre, hide_index=True)