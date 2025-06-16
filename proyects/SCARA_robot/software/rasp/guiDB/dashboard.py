import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# Configuración de la página
st.set_page_config(
    page_title="PLC Monitoring Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para inicializar Firebase
@st.cache_resource
def init_firebase():
    """Inicializa la conexión con Firebase"""
    try:
        # Si ya está inicializado, usar la app existente
        app = firebase_admin.get_app()
    except ValueError:
        # Configurar credenciales de Firebase
        # Reemplaza con tu archivo de credenciales o configuración
        cred = credentials.Certificate({
            # Aquí debes poner tu configuración de Firebase
            # Ejemplo:
            "type": "service_account",
            "project_id": "desfy-76d75",
            "private_key_id": "8244110d7bd84b5cd1bc71e3774d00b91253f669",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDWcuCC0BdgpUgO\nqkZRTtt+mFcksF9Pd3zvpr4xGAVL6qX5ZoG9ss0ISal2lF6t94QF9x3AYNxIjCaw\nqhwKkwyr3aG0xboUOENfMYKVBCEeQ6WZAWv/dfcHeCKRguHxOuMSjGC9ioAxiUeK\ngYcSDsptvmSajkwWdejd0zARv3yaX8YOrnnSqPOSCr+p5pUCQdV+JVAeJnvgnxsr\nYEcnOXPmCtScmtEFTmHpvFxnJzMYrEaxgV/I0gzP5TVVtTP4vU4ANtud5XnA3Fr6\n3o2Z77yCFwMsNKU4/SS4lJiFSteI9ri73QsKxcsVhVCG7g3l3BhBMqp+/uRkSa7i\nK2wOfRGjAgMBAAECggEAH6y4HJo/2baP/hqIaFoNcZVuyayDZ2luurcWQIobvira\neQv6/dn7Ds5SiYFAutFkXr0xV8j2wIBy9oUpvyYZKQmDaQALjBEDYnwdnYUOnzm+\nq+rZ2NHDuwazlGqQlODtyT+Symw6oxZzyrF3EeO9YphMo8eA1ZB05M7cusJd1S8r\nAHj4Kra0AYKO8J+iMyVADHKIYjWNet5E1TvByi2wi3Bmvamk+hgLzSDyxLtjdHfG\nrklaz0T5llE/QOTu6v/SExuY86PjdzKrz3a5cofzQCbyq+gLaEK29M0kRROo21VG\nAyOtTVwep4OSUdA94AwTh7fgUnhsf8iL4GPu2/E+gQKBgQDiiK/4+6i5Y0PALe2H\ns1j8jSnl8+JVROpI24AmWn5R8q89qgVMNvn/RyBs153S+tNBEWjq6scWW/SR0T9m\nlRYMNphR5r4eebimQ/b5zwwFYZ7cpiR/C61MhaGvOuajXK5AUfTej6byMClahf7d\n8Vxeiqrkg92OVThiSpK+4DvXvQKBgQDyV8RN9zB/yKB69QddNVL4oclbOtLB48Ct\nZ/qZqTNxrsizxbiR0xAakIAC3/toKPm7alsSeH6rQiViTBJehzsCqYWtR4c4tdcJ\ntZFxsk92mF8cSvaROTWhakWbX8MKu1qhPF/pLJcf4y9FaWHd27GPuMR+MlSQPDXN\n1jnpsWz03wKBgC1Lh2QRbbsjzfgvNr9bbP+Sej4wdaD3FqFawlTo4zkffUqnJEgI\n9hPE9QbOVhBJdtQb1w6hww0FdfFyFWs9hBsND4fQy1Lso68bB9cLPywUSN91mPaO\nLyiNz7Zp4JPphC34NS4LKyZh2uLux/c4u29r6p+mfjZnc86zeoQP8edBAoGAfJJQ\n/iLKc2UV2R6LIoZ+l//SGWsrWy9Po9OHJeWr5AwMbxx7u7na1UziAJhSC0DE3mnV\nVrFJq47c2KJx7tVkqAGsDV5vS99tIjiLAv69iiDZAxollJDr2IVgMnYPND0KYUc/\npgSdym5lpjB9diWwKEi5+IS2o03P+nbcXhwt/dECgYAQE/UeKLQHbV8gOPbP0Fp6\nKL10xkmjZreMVCBOMVp8EEd86N7uTFDlzcOYZc5UG6xezpiqTKP26Zjt2JdkXaXR\nf9vXrNcTQ9oI8jaekABjHwCv7Dpzklv3uSavTrmmGJl/fGgvEAjYVVMakk70e+G4\nrGJ4RMtQKV0WcbPJXYlOew==\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-4ai3w@desfy-76d75.iam.gserviceaccount.com",
            "client_id": "110405238934402612828",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4ai3w%40desfy-76d75.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        })
        app = firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Función para obtener datos en tiempo real
@st.cache_data(ttl=30)  # Cache por 5 segundos
def get_realtime_data(_db):
    """Obtiene los datos en tiempo real del PLC desde Firebase"""
    try:
        # Obtener el documento más reciente
        doc_ref = _db.collection('plc_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        docs = doc_ref.stream()
        
        for doc in docs:
            data = doc.to_dict()
            return {
                'box_count': data.get('box_count', 0),
                'machine_speed': data.get('machine_speed', 0),
                'system_status': data.get('system_status', 'OK'),
                'error_message': data.get('error_message', ''),
                'production_time': data.get('production_time', 0),
                'remaining_time': data.get('remaining_time', 0),
                'cycles': data.get('cycles', 0),
                'timestamp': data.get('timestamp', datetime.now())
            }
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return None

# Función para obtener datos históricos
@st.cache_data(ttl=30)  # Cache por 30 segundos
def get_historical_data(_db, limit=50):
    """Obtiene los datos históricos del PLC"""
    try:
        docs = _db.collection('plc_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        data_list = []
        for doc in docs:
            data = doc.to_dict()
            data_list.append(data)
        
        if data_list:
            df = pd.DataFrame(data_list)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df.sort_values('timestamp')
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al obtener datos históricos: {e}")
        return pd.DataFrame()

# Función para crear tarjetas de métricas
def create_metric_card(title, value, subtitle, icon="", status="normal"):
    """Crea una tarjeta de métrica personalizada"""
    if status == "error":
        color = "#ff4b4b"
        bg_color = "#ffe6e6"
    elif status == "warning":
        color = "#ff8c00"
        bg_color = "#fff4e6"
    else:
        color = "#0068c9"
        bg_color = "#e6f3ff"
    
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {color};
        margin: 0.5rem 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; color: #333; font-size: 1rem;">{title} {icon}</h3>
                <h1 style="margin: 0.2rem 0; color: {color}; font-size: 2rem;">{value}</h1>
                <p style="margin: 0; color: #666; font-size: 0.8rem;">{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Título principal
    st.title("🏭 PLC Monitoring Dashboard")
    
    # Sidebar para navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página", ["Dashboard Principal", "Gráficos Históricos", "Configuración"])
    
    # Inicializar Firebase
    try:
        db = init_firebase()
    except Exception as e:
        st.error("Error al conectar con Firebase. Verifica tu configuración.")
        st.error(f"Detalles: {e}")
        return
    
    if page == "Dashboard Principal":
        # Auto-refresh cada 5 segundos
        placeholder = st.empty()
        
        # Botón para refrescar manualmente
        if st.button("🔄 Actualizar Datos"):
            st.cache_data.clear()
        
        # Obtener datos en tiempo real
        data = get_realtime_data(db)
        
        if data:
            # Mostrar timestamp de última actualización
            st.caption(f"Última actualización: {data['timestamp'].strftime('%H:%M:%S')}")
            
            # Primera fila de métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card(
                    "Box Count", 
                    str(data['box_count']), 
                    "Total boxes processed",
                    "📦"
                )
            
            with col2:
                create_metric_card(
                    "Machine Speed", 
                    f"{data['machine_speed']} units/min", 
                    "Current operational speed",
                    "⚡"
                )
            
            with col3:
                status = "error" if data['system_status'] == "Error" else "normal"
                create_metric_card(
                    "System Status", 
                    data['system_status'], 
                    data['error_message'] if data['error_message'] else "Sistema funcionando correctamente",
                    "⚠️" if status == "error" else "✅",
                    status
                )
            
            # Segunda fila de métricas
            col4, col5, col6 = st.columns(3)
            
            with col4:
                create_metric_card(
                    "Tiempo de Producción", 
                    f"{data['production_time']}s", 
                    "Total time machine was productive",
                    "⏱️"
                )
            
            with col5:
                create_metric_card(
                    "Tiempo Restante de Emplayé", 
                    f"{data['remaining_time']}s", 
                    "Estimated time for current wrap cycle",
                    "⏳"
                )
            
            with col6:
                create_metric_card(
                    "Ciclos", 
                    str(data['cycles']), 
                    "Completed operational cycles",
                    "🔄"
                )
            
            # Auto-refresh
            time.sleep(5)
            st.rerun()
        else:
            st.warning("No se pudieron obtener los datos del PLC")
    
    elif page == "Gráficos Históricos":
        st.header("📊 Análisis Histórico")
        
        # Controles
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Últimas 50 muestras")
        with col2:
            if st.button("🔄 Actualizar Gráficos"):
                st.cache_data.clear()
        
        # Obtener datos históricos
        df = get_historical_data(db)
        
        if not df.empty:
            # Selectbox para elegir qué variable graficar
            variable = st.selectbox(
                "Selecciona la variable a graficar:",
                ["box_count", "machine_speed", "production_time", "remaining_time", "cycles"]
            )
            
            # Configurar títulos y unidades
            titles = {
                "box_count": "Conteo de Cajas",
                "machine_speed": "Velocidad de Máquina (units/min)",
                "production_time": "Tiempo de Producción (s)",
                "remaining_time": "Tiempo Restante (s)",
                "cycles": "Ciclos Completados"
            }
            
            # Crear gráfico de línea
            fig = px.line(
                df, 
                x='timestamp', 
                y=variable,
                title=f'Histórico: {titles[variable]}',
                labels={'timestamp': 'Tiempo', variable: titles[variable]}
            )
            
            fig.update_layout(
                xaxis_title="Tiempo",
                yaxis_title=titles[variable],
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de barras para ciclos si está seleccionado
            if variable == "cycles":
                fig_bar = px.bar(
                    df.tail(20), 
                    x='timestamp', 
                    y='cycles',
                    title='Ciclos Completados (Últimas 20 muestras)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Mostrar estadísticas
            st.subheader("📈 Estadísticas")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Promedio", f"{df[variable].mean():.2f}")
            with col2:
                st.metric("Máximo", f"{df[variable].max():.2f}")
            with col3:
                st.metric("Mínimo", f"{df[variable].min():.2f}")
            with col4:
                st.metric("Std Dev", f"{df[variable].std():.2f}")
            
            # Tabla de datos recientes
            st.subheader("📋 Datos Recientes")
            st.dataframe(df.tail(10)[['timestamp', 'box_count', 'machine_speed', 'system_status', 'cycles']])
        else:
            st.warning("No hay datos históricos disponibles")
    
    elif page == "Configuración":
        st.header("⚙️ Configuración")
        
        st.subheader("Configuración de Firebase")
        st.info("Para configurar Firebase, debes:")
        st.markdown("""
        1. Crear un proyecto en Firebase Console
        2. Generar una clave de servicio (Service Account Key)
        3. Reemplazar la configuración en el código con tus credenciales
        4. Asegurarte de que Firestore esté habilitado
        """)
        
        st.subheader("Estructura de Datos Esperada")
        st.code("""
        Colección: plc_data
        Documento: {
            "box_count": 43,
            "machine_speed": 103,
            "system_status": "Error",
            "error_message": "Error código 373: Falla de sensor",
            "production_time": 28,
            "remaining_time": 55,
            "cycles": 8,
            "timestamp": timestamp
        }
        """)
        
        st.subheader("Configuración de Auto-refresh")
        refresh_interval = st.slider("Intervalo de actualización (segundos)", 1, 30, 5)
        st.info(f"Los datos se actualizarán cada {refresh_interval} segundos")

if __name__ == "__main__":
    main()