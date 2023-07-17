import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def extract_data(url):
    # Effettua la richiesta GET alla pagina web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trova tutti gli elementi div che contengono i dati delle startup innovative
    startup_divs = soup.find_all('div', class_='row item clickable')

    data = []

    # Itera sugli elementi div e estrae i dati di interesse
    for div in startup_divs:
        ragione_sociale = div.find('div', class_='col-12 col-md-6 name').text.strip()
        pec = div.find('div', class_='col-12 col-md-4 pec').text.strip()
        email = div.find('div', class_='col-12 col-md-4 email').text.strip()

        data.append({'Ragione Sociale': ragione_sociale, 'PEC': pec, 'Email': email})

    return data

def scrape_startup_data():
    base_url = 'https://startup.registroimprese.it/isin/search?1#'
    all_data = []

    # Itera su tutte le pagine
    page = 1
    while True:
        url = f'{base_url}&page={page}'
        data = extract_data(url)

        if not data:
            break

        all_data.extend(data)
        page += 1

    # Salva i dati in un DataFrame
    df = pd.DataFrame(all_data)
    return df

def main():
    st.title("Scraping Dati Startup Innovative")

    # Esegui lo scraping dei dati al clic del pulsante
    if st.button("Esegui Scraping"):
        st.text("Estrazione dei dati in corso...")
        df = scrape_startup_data()
        st.write("Dati delle startup innovative:")
        st.dataframe(df)

        # Salva i dati in un file CSV al clic del pulsante
        if st.button("Salva CSV"):
            df.to_csv('startup_data.csv', index=False)
            st.success('Dati delle startup innovative salvati nel file "startup_data.csv".')

if __name__ == '__main__':
    main()




