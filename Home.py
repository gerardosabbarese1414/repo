import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_startup_data(url, info_types):
    # Effettua la richiesta GET all'URL fornito dall'utente
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trova tutti gli elementi div che contengono i dati delle startup innovative
    startup_divs = soup.find_all('div', class_='row item clickable')

    data = []

    # Itera sugli elementi div e estrae i dati di interesse
    for div in startup_divs:
        startup_data = {}

        if "Ragione Sociale" in info_types:
            ragione_sociale = div.find('div', class_='col-12 col-md-6 name').text.strip()
            startup_data['Ragione Sociale'] = ragione_sociale

        if "PEC" in info_types:
            pec = div.find('div', class_='col-12 col-md-4 pec').text.strip()
            startup_data['PEC'] = pec

        if "Email" in info_types:
            email = div.find('div', class_='col-12 col-md-4 email').text.strip()
            startup_data['Email'] = email

        data.append(startup_data)

    df = pd.DataFrame(data)
    return df

def main():
    st.title("Scraping Dati Startup Innovative")

    # Aggiungi input utente per l'URL
    url = st.text_input("Inserisci l'URL:", "https://startup.registroimprese.it/isin/search?1#")

    # Aggiungi input utente per il tipo di informazioni
    info_types = st.multiselect("Seleziona i tipi di informazioni da scaricare:", ["Ragione Sociale", "PEC", "Email"], ["Ragione Sociale", "PEC", "Email"])

    # Esegui lo scraping dei dati al clic del pulsante
    if st.button("Esegui Scraping"):
        st.text("Estrazione dei dati in corso...")
        df = scrape_startup_data(url, info_types)
        st.write("Dati delle startup innovative:")
        st.dataframe(df)

        # Salva i dati in un file CSV al clic del pulsante
        if st.button("Salva CSV"):
            df.to_csv('startup_data.csv', index=False)
            st.success('Dati delle startup innovative salvati nel file "startup_data.csv".')

if __name__ == '__main__':
    main()





