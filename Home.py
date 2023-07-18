import streamlit as st
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Funzione per estrarre i dati di tutte le startup, inclusi gli indirizzi email
def extract_startup_data():
    # Installa automaticamente il driver di Chrome
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Esegui Chrome in modalità headless (senza interfaccia grafica)
    driver = webdriver.Chrome(options=options)

    url = 'https://startup.registroimprese.it/isin/home'
    driver.get(url)

    # Seleziona il campo "Startup" e clicca sul tasto "Ricerca Avanzata"
    driver.find_element_by_id('tipo_impresa').send_keys('startup')
    driver.find_element_by_id('cercaAvanzata').click()

    # Estrapola i dati di tutte le pagine
    data = []
    emails = []
    while True:
        # Attendi il caricamento dei risultati
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'box_segnalazioni')))

        # Estrapola i dati della pagina corrente
        table = driver.find_element_by_class_name('tab_data')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows[1:]:
            cells = row.find_elements_by_tag_name('td')
            startup_data = [cell.text for cell in cells]
            data.append(startup_data)

            # Recupera l'indirizzo email dalla pagina di ogni startup
            link = cells[0].find_element_by_tag_name('a').get_attribute('href')
            email = get_email_from_startup(link)
            emails.append(email)

        # Passa alla pagina successiva, se presente
        next_button = driver.find_element_by_id('prossimo')
        if next_button.get_attribute('class') == 'next disabled':
            break
        else:
            next_button.click()

    driver.quit()

    # Crea un DataFrame con i dati estratti
    columns = ['Denominazione', 'Natura Giuridica', 'Codice Fiscale', 'Provincia', 'Comune', 'Data Iscrizione Startup', 'Data Iscrizione Registro Imprese', 'Data Inizio Attività', 'Ateco 2007', 'Settore', 'Attività', 'Sito Internet', 'Regione', 'Sezione Attività', 'Classe Addetti', 'Classe Val. Prod.', 'Alto Valore Tecnologico', 'Vocazione Sociale', 'Classe Capitale Sociale', 'Spese in Ricerca e Sviluppo', 'Forza Lavoro con Titoli', 'Possesso di Brevetti', 'Data Dichiarazione', 'Prevalenza Femminile', 'Prevalenza Giovanile', 'Prevalenza Straniera', 'Email']
    df = pd.DataFrame(data, columns=columns)
    df['Email'] = emails

    return df

# Funzione per estrarre l'email da ogni pagina di startup
def get_email_from_startup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Esegui Chrome in modalità headless (senza interfaccia grafica)
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Trova l'elemento che contiene l'email
    email_element = driver.find_element_by_xpath('//a[contains(@href, "mailto:")]')
    email = email_element.get_attribute('href').split(':')[1]

    driver.quit()
    return email

# Funzione principale dell'app Streamlit
def main():
    st.title("Estrazione Dati Startup Innovative")

    if st.button("Estrai Dati"):
        st.text("Estrazione dei dati in corso...")
        startup_data = extract_startup_data()

        st.write("Dati delle startup innovative:")
        st.dataframe(startup_data)

        # Scarica i dati in un file CSV
        csv_file = startup_data.to_csv(index=False)
        st.download_button("Scarica CSV", data=csv_file, file_name='startup_data.csv', mime='text/csv')

if __name__ == '__main__':
    main()

