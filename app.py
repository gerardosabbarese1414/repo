import ssl

# Disabilita la verifica del certificato SSL
ssl._create_default_https_context = ssl._create_default_https_context = ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st

            data.append([startup_name, email])

        # Passa alla pagina successiva, se presente
        next_button = driver.find_element_by_id('prossimo')
        if 'disabled' in next_button.get_attribute('class'):
            break
        else:
            next_button.click()

    driver.quit()

    # Crea un DataFrame con i dati estratti
    columns = ['Nome Startup', 'Email']
    df = pd.DataFrame(data, columns=columns)

    return df

# Funzione principale dell'app Streamlit
def main():
    st.title("Estrazione Dati Startup Innovative")

    if st.button("Estrai Dati"):
        st.text("Estrazione dei dati in corso...")
        startup_data = extract_startup_data()

        if startup_data is not None:
            st.write("Dati delle startup innovative:")
            st.dataframe(startup_data)

            # Scarica i dati in un file CSV
            csv_file = startup_data.to_csv(index=False)
            st.download_button("Scarica CSV", data=csv_file, file_name='startup_data.csv', mime='text/csv')

if __name__ == '__main__':
    main()
