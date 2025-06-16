# 🏭 Dashboard PLC con Streamlit y Firebase - Guía de Instalación

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Firebase con Firestore habilitado
- PLC compatible con protocolo S7 (Siemens)
- Snap7 instalado en el sistema

## 🚀 Instalación

### 1. Preparar el Entorno

```bash
# Clonar o descargar los archivos
mkdir plc-dashboard
cd plc-dashboard

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Instalar paquetes de Python
pip install -r requirements.txt

# Instalar Snap7 (para comunicación con PLC)
# Windows: Descargar desde https://snap7.sourceforge.net/
# Linux:
sudo apt-get install libsnap7-dev
pip install python-snap7

# Mac:
brew install snap7
pip install python-snap7
```

### 3. Configurar Firebase

#### 3.1 Crear Proyecto Firebase
1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. Habilita Firestore Database
4. Ve a "Project Settings" > "Service Accounts"
5. Genera una nueva clave privada (archivo JSON)

#### 3.2 Configurar Credenciales
Opción A - Archivo de credenciales (más fácil):
```bash
# Guarda el archivo JSON como "firebase-credentials.json" en la carpeta del proyecto
```

Opción B - Variables de entorno (más seguro):
```bash
export FIREBASE_PROJECT_ID="tu-proyecto-id"
export FIREBASE_PRIVATE_KEY_ID="tu-private-key-id"
export FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nTU_KEY\n-----END PRIVATE KEY-----"
export FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxx@tu-proyecto.iam.gserviceaccount.com"
export FIREBASE_CLIENT_ID="tu-client-id"
export FIREBASE_CLIENT_CERT_URL="tu-cert-url"
```

### 4. Configurar PLC

#### 4.1 Editar configuración en `plc_connector.py`:
```python
# Cambiar la IP del PLC
PLC_IP = "192.168.1.100"  # Tu IP del PLC

# Configurar los tags según tu PLC
self.tags_config = {
    "box_count": {"db": 1, "start": 0, "size": 4, "type": "int"},
    "machine_speed": {"db": 1, "start": 4, "size": 4, "type": "int"},
    # ... ajustar según tu configuración
}
```

#### 4.2 Estructura de datos en el PLC:
```
DB1 (Data Block 1):
- DBD0: Box Count (Double Word - 32 bits)
- DBD4: Machine Speed (Double Word - 32 bits)
- DBD8: System Status (Double Word - 32 bits)
- DBD12: Production Time (Double Word - 32 bits)
- DBD16: Remaining Time (Double Word - 32 bits)
- DBD20: Cycles (Double Word - 32 bits)
- DBD24: Error Code (Double Word - 32 bits)
```

## 🏃‍♂️ Ejecución

### Método 1: Script Automático
```bash
python run.py
```

### Método 2: Manual

#### Solo Dashboard:
```bash
streamlit run dashboard.py
```

#### Solo Conector PLC:
```bash
python plc_connector.py
```

#### Ambos (en terminales separadas):
```bash
# Terminal 1:
python plc_connector.py

# Terminal 2:
streamlit run dashboard.py
```

## 📊 Uso del Dashboard

### Dashboard Principal
- **Métricas en tiempo real**: Box Count, Machine Speed, System Status
- **Auto-refresh**: Actualización automática cada 5 segundos
- **Estado del sistema**: Indicadores visuales de errores

### Gráficos Históricos
- **Análisis temporal**: Últimas 50 muestras
- **Variables seleccionables**: Todas las métricas disponibles
- **Estadísticas**: Promedio, máximo, mínimo, desviación estándar

## 🛠️ Personalización

### Cambiar Intervalo de Actualización
En `plc_connector.py`:
```python
MONITORING_INTERVAL = 10  # Cambiar a 10 segundos
```

En `dashboard.py`:
```python
@st.cache_data(ttl=10)  # Cambiar cache a 10 segundos
```

### Agregar Nuevas Variables
1. En `plc_connector.py`, agregar al `tags_config`:
```python
"nueva_variable": {"db": 1, "start": 28, "size": 4, "type": "int"}
```

2. En `dashboard.py`, agregar a las métricas o gráficos

### Personalizar Códigos de Error
En `plc_connector.py`:
```python
self.error_codes = {
    0: "OK",
    373: "Error código 373: Falla de sensor",
    400: "Tu nuevo código de error",
    # Agregar más códigos
}
```

## 🔧 Solución de Problemas

### Error de Conexión Firebase
- Verificar credenciales en `config.py`
- Comprobar que Firestore esté habilitado
- Revisar permisos de la cuenta de servicio

### Error de Conexión PLC
- Verificar IP del PLC
- Comprobar que el PLC esté en RUN
- Revisar configuración de rack/slot
- Verificar que Snap7 esté instalado correctamente

### Dashboard no muestra datos
- Verificar que el conector PLC esté ejecutándose
- Comprobar que haya datos en Firebase
- Revisar logs en la consola

### Rendimiento lento
- Aumentar intervalos de cache
- Reducir número de muestras históricas
- Optimizar configuración de Firebase

## 📁 Estructura del Proyecto

```
plc-dashboard/
├── dashboard.py              # Dashboard principal de Streamlit
├── plc_connector.py         # Conector para leer datos del PLC
├── config.py                # Configuración de Firebase
├── run.py                   # Script de inicio
├── requirements.txt         # Dependencias de Python
├── firebase-credentials.json # Credenciales de Firebase (no incluir en git)
└── README.md               # Esta guía
```

## 🔒 Seguridad

### Variables de Entorno
Para producción, usar variables de entorno:
```bash
# .env
FIREBASE_PROJECT_ID=tu-proyecto
FIREBASE_PRIVATE_KEY=tu-clave-privada
# ... otras variables
```

### Firestore Rules
Configurar reglas de seguridad en Firebase:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /plc_data/{document} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 📈 Escalabilidad

### Para Múltiples PLCs
1. Modificar `plc_connector.py` para manejar múltiples conexiones
2. Usar diferentes colecciones en Firebase por PLC
3. Agregar filtros en el dashboard por PLC

### Para Más Datos
1. Implementar particionamiento por fecha en Firebase
2. Usar Firebase Functions para procesamiento
3. Considerar bases de datos de series temporales (InfluxDB)

## 🆘 Soporte

Para problemas específicos:
1. Revisar logs en la consola
2. Verificar configuración de red PLC
3. Comprobar estado de Firebase
4. Consultar documentación de Snap7

---

## 📝 Notas Importantes

- El sistema guarda datos cada 5 segundos por defecto
- Firebase tiene límites de lectura/escritura en el plan gratuito
- Se recomienda usar variables de entorno en producción
- Los datos históricos se mantienen automáticamente (configurable)