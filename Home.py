import subprocess
subprocess.run(["pip", "install", "--no-cache-dir", "-r", "requirements.txt"])
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_emails(startup_list):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Esegui Chrome in modalità headless (senza interfaccia grafica)
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    emails = []
    for startup in startup_list:
        driver.get('https://startup.registroimprese.it/isin/home')

        # Seleziona il campo startup e clicca sul tasto ricerca avanzata
        driver.find_element_by_id('tipo_impresa').send_keys('startup')
        driver.find_element_by_id('cercaAvanzata').click()

        # Inserisci la regione nella ricerca
        driver.find_element_by_id('sigla_regione').send_keys(startup)

        # Attendi il caricamento dei risultati
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'box_segnalazioni')))

        # Estrapola le email dai risultati
        emails_elem = driver.find_elements_by_xpath('//a[@class="mailto"]')
        startup_emails = [email_elem.get_attribute('href').split(':')[1] for email_elem in emails_elem]
        emails.extend(startup_emails)

    driver.quit()
    return emails

def main():
    st.title("Bot per Estrarre Email di Startup Innovative")

    # Esempio: utilizziamo tutte le regioni italiane come elenco di ricerca
    regioni = ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Trentino-Alto Adige', 'Umbria', 'Valle d\'Aosta', 'Veneto']

    st.write("Seleziona le regioni per estrarre le email delle startup innovative:")
    selected_regions = st.multiselect("Regioni", regioni, default=regioni)

    if st.button("Estrai Email"):
        startup_emails = get_emails(selected_regions)

        st.write("Email delle startup trovate:")
        for email in startup_emails:
            st.write(email)

        # Creazione DataFrame con le email
        df = pd.DataFrame(startup_emails, columns=['Email'])

        # Download CSV
        csv_file = df.to_csv(index=False)
        st.download_button("Scarica CSV", data=csv_file, file_name='startup_emails.csv', mime='text/csv')

if __name__ == '__main__':
    main()
