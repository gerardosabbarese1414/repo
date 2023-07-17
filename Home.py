import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_startup_data(url):
    # Effettua la richiesta GET all'URL fornito dall'utente
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trova la tabella contenente i risultati della ricerca
    table = soup.find('table', class_='tab_data')

    # Estrai le intestazioni delle colonne dalla prima riga della tabella
    header_row = table.find('tr')
    headers = [header.text.strip() for header in header_row.find_all('th')]

    # Crea una lista per memorizzare i dati delle startup
    data = []

    # Itera sulle righe della tabella (escludendo la prima riga delle intestazioni)
    for row in table.find_all('tr')[1:]:
        # Estrai i dati da ogni cella della riga
        cell_data = [cell.text.strip() for cell in row.find_all('td')]
        data.append(cell_data)

    # Crea un DataFrame utilizzando i dati estratti e le intestazioni delle colonne
    df = pd.DataFrame(data, columns=headers)
    return df

def main():
    st.title("Scraping Dati Startup Innovative")

    # Aggiungi input utente per l'URL
    url = st.text_input("Inserisci l'URL:", "https://startup.registroimprese.it/isin/search?0#")

    # Esegui lo scraping dei dati al clic del pulsante
    if st.button("Esegui Scraping"):
        st.text("Estrazione dei dati in corso...")
        df = scrape_startup_data(url)
        st.write("Dati delle startup innovative:")
        st.dataframe(df)

        # Salva il DataFrame in un file CSV al clic del pulsante "Download CSV"
        if st.button("Download CSV"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Codifica in base64
            href = f'<a href="data:file/csv;base64,{b64}" download="startup_data.csv">Clicca qui per scaricare il CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()





