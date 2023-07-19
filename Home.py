import re
import requests
import csv
import streamlit as st
import pandas as pd

def get_first_email_from_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
            return emails[0] if emails else None
    except:
        pass
    return None

def main():
    st.title("Web Scraping di Email da Siti Web")
    st.write("Inserisci l'URL di un sito web senza HTTPS per cercare email.")

    url_list = st.text_area("Inserisci gli URL dei siti web (uno per riga)")
    urls = url_list.split("\n")

    if st.button("Cerca Email"):
        st.write("Risultati:")
        results = []

        for url in urls:
            if url:
                email = get_first_email_from_website(f"http://{url}")
                if email:
                    results.append({"Sito Web": url, "Email Trovata": email})

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

if __name__ == "__main__":
    main()
