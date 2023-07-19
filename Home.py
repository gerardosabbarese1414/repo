
import re
import requests
import csv
import streamlit as st

def get_emails_from_text(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

def main():
    st.title("Web Scraping di Email da Siti Web")
    st.write("Inserisci l'URL di un sito web, solo il dominio o del testo per cercare email.")

    user_input = st.text_area("Inserisci gli URL dei siti web o domini, o del testo (uno per riga)", height=150)
    items = user_input.split("\n")

    if st.button("Cerca Email"):
        results = []

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

        if results:
            with st.beta_expander("Risultati"):
                st.table(results)

                # Download CSV
                csv_data = "Sito Web o Dominio,Email Trovata\n"
                for result in results:
                    csv_data += f"{result.get('Sito Web o Dominio', '')},{result.get('Email Trovata', '')}\n"
                st.download_button(
                    label="Scarica il file CSV",
                    data=csv_data.encode(),
                    file_name="results.csv",
                    mime="text/csv"
                )
        else:
            st.write("Nessun risultato trovato.")


if __name__ == "__main__":
    main()
