import re
import requests
import csv
import streamlit as st

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

        progress_bar = st.progress(0)
        for i, url in enumerate(urls):
            if url:
                email = get_first_email_from_website(f"http://{url}")
                if email:
                    results.append({"Sito Web": url, "Email Trovata": email})

            progress = (i + 1) / len(urls)
            progress_bar.progress(progress)

        if results:
            with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Sito Web", "Email Trovata"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
            st.success("Risultati generati con successo!")

            if st.button("Scarica CSV"):
                st.markdown(
                    f'<a href="results.csv" download>Scarica il file CSV</a>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
