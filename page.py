import pandas as pd
import streamlit as st

def main():
    st.title("Elimina duplicati e esporta in CSV o Excel")

    uploaded_file = st.file_uploader("Carica il file CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Dati del file CSV:")
        st.dataframe(df)

        # Remove duplicates
        df.drop_duplicates(inplace=True)

        st.subheader("Dati senza duplicati:")
        st.dataframe(df)

        # Export options
        export_format = st.selectbox("Seleziona il formato di esportazione", ["CSV", "Excel"])

        if st.button("Esporta"):
            if export_format == "CSV":
                csv_file = "data_without_duplicates.csv"
                df.to_csv(csv_file, index=False)
                st.success(f"Dati esportati in formato CSV. Puoi scaricarlo [qui]({csv_file}).")
            elif export_format == "Excel":
                excel_file = "data_without_duplicates.xlsx"
                df.to_excel(excel_file, index=False)
                st.success(f"Dati esportati in formato Excel. Puoi scaricarlo [qui]({excel_file}).")

if __name__ == "__main__":
    main()