import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    API_KEY = os.getenv('API_KEY')
    try:
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        token_response.raise_for_status()
        mltoken = token_response.json()["access_token"]
        return mltoken
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener el token de acceso: {e}")
        return None

def predict_daniado(DOY_llenado, hum_grano_llenado, temp_grano_llenado, 
                    hum_amb_llenado, temp_amb_muestra, cuerpo_extranio_llenado):
    mltoken = get_access_token()
    if mltoken is None:
        return None
    json_data = {
        "input_data": [
            {
                "fields": [
                    "ID", "pista", "fecha_llenado", "DOY_llenado", 
                    "hum_grano_llenado", "temp_grano_llenado", "hum_amb_llenado", 
                    "temp_amb_muestra", "cuerpo_extranio_llenado"
                ],
                "values": [[1.1, 1, "13/04/2019", DOY_llenado, hum_grano_llenado, 
                            temp_grano_llenado, hum_amb_llenado, temp_amb_muestra, 
                            cuerpo_extranio_llenado]]
            }
        ]
    }
    try:
        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/granodaniado/predictions?version=2021-05-01',
            json=json_data, headers={'Authorization': 'Bearer ' + mltoken}
        )
        response_scoring.raise_for_status()
        prediction = response_scoring.json()['predictions'][0]['values'][0][0]
        return prediction
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener la predicción: {e}")
        return None

st.write('#### Predicción de Grano Dañado')

def update_slider():
    st.session_state.slider_doy = st.session_state.numeric_doy
    st.session_state.slider_hum_grano = st.session_state.numeric_hum_grano
    st.session_state.slider_temp_grano = st.session_state.numeric_temp_grano
    st.session_state.slider_hum_amb = st.session_state.numeric_hum_amb
    st.session_state.slider_temp_amb = st.session_state.numeric_temp_amb
    st.session_state.slider_cuerpo_extranio = st.session_state.numeric_cuerpo_extranio

def update_numin():
    st.session_state.numeric_doy = st.session_state.slider_doy
    st.session_state.numeric_hum_grano = st.session_state.slider_hum_grano
    st.session_state.numeric_temp_grano = st.session_state.slider_temp_grano
    st.session_state.numeric_hum_amb = st.session_state.slider_hum_amb
    st.session_state.numeric_temp_amb = st.session_state.slider_temp_amb
    st.session_state.numeric_cuerpo_extranio = st.session_state.slider_cuerpo_extranio

if st.button('Predecir'):
    prediction = predict_daniado(
        st.session_state.numeric_doy, st.session_state.numeric_hum_grano, st.session_state.numeric_temp_grano,
        st.session_state.numeric_hum_amb, st.session_state.numeric_temp_amb, st.session_state.numeric_cuerpo_extranio
    )
    if prediction is not None:
        st.write(f'Grano Dañado: {prediction:.2f}')
    else:
        st.write("No se pudo obtener la predicción. Verifique los datos y vuelva a intentarlo.")

col1, col2, col3 = st.columns(3)

with col1:
    DOY_llenado = st.number_input('DOY Llenado', min_value=0, max_value=365, value=0, key='numeric_doy', on_change=update_slider)
    hum_grano_llenado = st.number_input('Humedad Grano Llenado', min_value=0.0, max_value=100.0, value=0.0, key='numeric_hum_grano', on_change=update_slider)
    
with col2:
    temp_grano_llenado = st.number_input('Temperatura Grano Llenado', min_value=-20.0, max_value=50.0, value=0.0, key='numeric_temp_grano', on_change=update_slider)
    hum_amb_llenado = st.number_input('Humedad Ambiente Llenado', min_value=0.0, max_value=100.0, value=0.0, key='numeric_hum_amb', on_change=update_slider)
    
with col3:
    temp_amb_muestra = st.number_input('Temperatura Ambiente Muestra', min_value=-20.0, max_value=50.0, value=0.0, key='numeric_temp_amb', on_change=update_slider)
    cuerpo_extranio_llenado = st.number_input('Cuerpo Extraño Llenado', min_value=0.0, max_value=5.0, value=0.0, key='numeric_cuerpo_extranio', on_change=update_slider)
    
DOY_llenado_slider = st.slider('DOY Llenado', min_value=0, max_value=365, value=DOY_llenado, key='slider_doy', on_change=update_numin)
hum_grano_llenado_slider = st.slider('Humedad Grano Llenado', min_value=0.0, max_value=100.0, value=hum_grano_llenado, key='slider_hum_grano', on_change=update_numin)
temp_grano_llenado_slider = st.slider('Temperatura Grano Llenado', min_value=-20.0, max_value=50.0, value=temp_grano_llenado, key='slider_temp_grano', on_change=update_numin)
hum_amb_llenado_slider = st.slider('Humedad Ambiente Llenado', min_value=0.0, max_value=100.0, value=hum_amb_llenado, key='slider_hum_amb', on_change=update_numin)
temp_amb_muestra_slider = st.slider('Temperatura Ambiente Muestra', min_value=-20.0, max_value=50.0, value=temp_amb_muestra, key='slider_temp_amb', on_change=update_numin)
cuerpo_extranio_llenado_slider = st.slider('Cuerpo Extraño Llenado', min_value=0.0, max_value=5.0, value=cuerpo_extranio_llenado, key='slider_cuerpo_extranio', on_change=update_numin)
