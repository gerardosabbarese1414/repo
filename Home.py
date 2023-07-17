import streamlit as st
import pandas as pd

def main():
    st.title("Seleziona le colonne di interesse")

    # Aggiungi input utente per il caricamento del file CSV
    uploaded_file = st.file_uploader("Carica il file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Carica il file CSV in un DataFrame con gestione dell'errore di decodifica Unicode
            df = pd.read_csv(uploaded_file, encoding='utf-8', error_bad_lines=False)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', error_bad_lines=False)

        # Mostra l'elenco delle colonne presenti nel file CSV
        st.write("Colonne disponibili:")
        st.write(df.columns)

        # Aggiungi input utente per selezionare le colonne da mantenere
        selected_columns = st.multiselect("Seleziona le colonne da mantenere", df.columns)

        if len(selected_columns) > 0:
            # Filtra il DataFrame per mantenere solo le colonne selezionate
            df_selected = df[selected_columns]

            # Mostra il DataFrame con le sole colonne selezionate
            st.write("Dati con le colonne selezionate:")
            st.write(df_selected)

            # Salva il DataFrame con le colonne selezionate in un nuovo file CSV
            csv = df_selected.to_csv(index=False)
            st.download_button("Clicca qui per scaricare il CSV", data=csv, file_name="selected_columns_data.csv", mime="text/csv")
        else:
            st.warning("Seleziona almeno una colonna da mantenere.")
    else:
        st.warning("Carica un file CSV per iniziare.")

if __name__ == '__main__':
    main()



