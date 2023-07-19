import os
import re
import csv
import requests
from tqdm import tqdm


def get_emails_from_text(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails


def main():
    print("Web Scraping di Email da Siti Web")
    print("Inserisci l'URL di un sito web, solo il dominio o del testo per cercare email.")

    user_input = input(
        "Inserisci gli URL dei siti web o domini, o del testo (uno per riga). Digita 'FINE' per terminare l'inserimento.\n")
    items = []

    while user_input.strip().lower() != 'fine':
        items.append(user_input.strip())
        user_input = input()

    results = []

    with tqdm(total=len(items)) as pbar:
        for item in items:
            item = item.strip()
            if item:
                # Search in websites or domains
                if (item.startswith("http://") or item.startswith("https://")):
                    try:
                        response = requests.get(item, timeout=10)
                        if response.status_code == 200:
                            emails = get_emails_from_text(response.text)
                            for email in emails:
                                results.append({"Sito Web o Dominio": item, "Email Trovata": email})
                    except:
                        pass
                # Search in plain text
                else:
                    emails = get_emails_from_text(item)
                    for email in emails:
                        results.append({"Testo": item, "Email Trovata": email})
            pbar.update(1)

    if results:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        csv_file = os.path.join(desktop_path, "MANNAGGIA LA MADONNA.csv")

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Sito Web o Dominio", "Testo", "Email Trovata"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        print(f"Risultati salvati correttamente nel file '{csv_file}'")
    else:
        print("Nessun risultato trovato.")


if __name__ == "__main__":
    main()
