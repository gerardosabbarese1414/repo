import re
import requests
import csv
import streamlit as st
import pandas as pd

def get_first_email_from_website(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
            return emails[0] if emails else None
    except:
        pass
    return None

def get_emails_from_text(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

def contains_dot(text):
    return "." in text

def create_csv(results):
    if results:
        df = pd.DataFrame(results)
        csv_data = df.to_csv(index=False)
        return csv_data
    return None

def main():
    st.title("Web Scraping di Email da Siti Web")
    st.write("Inserisci l'URL di un sito web, solo il dominio o del testo per cercare email.")

    user_input = st.text_area("Inserisci gli URL dei siti web o domini, o del testo (uno per riga)")
    items = user_input.split("\n")

    if st.button("Cerca Email"):
        st.write("Risultati:")
        results = []

        for item in items:
            item = item.strip()
            if item:
                # Search in websites or domains
                if (item.startswith("http://") or item.startswith("https://")) or contains_dot(item):
                    email = get_first_email_from_website(item)
                    if email:
                        results.append({"Sito Web o Dominio": item, "Email Trovata": email})
                # Search in plain text
                else:
                    emails = get_emails_from_text(item)
                    for email in emails:
                        results.append({"Testo": item, "Email Trovata": email})

        if results:
            st.dataframe(pd.DataFrame(results))
            csv_data = create_csv(results)
            if csv_data:
                st.download_button(
                    label="Scarica il file CSV",
                    data=csv_data,
                    file_name="results.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
