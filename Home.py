import requests
from bs4 import BeautifulSoup

# Funzione per estrarre i dati di tutte le startup, inclusi gli indirizzi email
def extract_startup_data():
    url = 'https://startup.registroimprese.it/isin/home'

    # Effettua la richiesta HTTP alla pagina web
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Errore nella richiesta HTTP: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Estrapola i dati di tutte le pagine
    data = []
    emails = []
    while True:
        # Estrapola i dati della pagina corrente
        table = soup.find('table', class_='tab_data')
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            startup_data = [cell.text for cell in cells]
            data.append(startup_data)

            # Recupera l'indirizzo email dalla pagina di ogni startup
            link = cells[0].find('a')['href']
            email = get_email_from_startup(link)
            emails.append(email)

        # Passa alla pagina successiva, se presente
        next_button = soup.find('a', class_='next')
        if next_button is None:
            break

        next_page_url = 'https://startup.registroimprese.it' + next_button['href']
        response = requests.get(next_page_url)
        if response.status_code != 200:
            raise Exception(f"Errore nella richiesta HTTP: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

    # Crea un DataFrame con i dati estratti
    columns = ['Denominazione', 'Natura Giuridica', 'Codice Fiscale', 'Provincia', 'Comune', 'Data Iscrizione Startup', 'Data Iscrizione Registro Imprese', 'Data Inizio Attività', 'Ateco 2007', 'Settore', 'Attività', 'Sito Internet', 'Regione', 'Sezione Attività', 'Classe Addetti', 'Classe Val. Prod.', 'Alto Valore Tecnologico', 'Vocazione Sociale', 'Classe Capitale Sociale', 'Spese in Ricerca e Sviluppo', 'Forza Lavoro con Titoli', 'Possesso di Brevetti', 'Data Dichiarazione', 'Prevalenza Femminile', 'Prevalenza Giovanile', 'Prevalenza Straniera', 'Email']
    df = pd.DataFrame(data, columns=columns)
    df['Email'] = emails

    return df

# Funzione per estrarre l'email da ogni pagina di startup
def get_email_from_startup(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Errore nella richiesta HTTP: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    email_element = soup.find('a', href=lambda href: href and href.startswith('mailto:'))
    email = email_element['href'].split(':')[1]

    return email
