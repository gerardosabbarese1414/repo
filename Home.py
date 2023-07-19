import re
import requests
import csv
import streamlit as st
from io import BytesIO
import tempfile
import os

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
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                with open(temp_file.name, "w", newline="", encoding="utf-8") as csvfile:
                    fieldnames = ["Sito Web", "Email Trovata"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in results:
                        writer.writerow(result)

                st.success("Risultati generati con successo!")

                if st.button("Scarica CSV"):
                    with open(temp_file.name, "rb") as file:
                        st.download_button(
                            label="Scarica il file CSV",
                            data=file,
                            file_name="results.csv",
                            mime="text/csv"
                        )

                os.remove(temp_file.name)

if __name__ == "__main__":
    main()
