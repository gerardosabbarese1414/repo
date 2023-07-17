import streamlit as st
import pandas as pd

def main():
    st.title("Seleziona le colonne di interesse")

    # Aggiungi input utente per il caricamento del file CSV
    uploaded_file = st.file_uploader("Carica il file CSV", type=["csv"])

    if uploaded_file is not None:
        # Carica il file CSV in un DataFrame
        df = pd.read_csv(uploaded_file)

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
            b64 = base64.b64encode(csv.encode()).decode()  # Codifica in base64
            href = f'<a href="data:file/csv;base64,{b64}" download="selected_columns_data.csv">Clicca qui per scaricare il CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("Seleziona almeno una colonna da mantenere.")
    else:
        st.warning("Carica un file CSV per iniziare.")

if __name__ == '__main__':
    main()




