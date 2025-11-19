# P&L Dashboard - Ethnix Group

Sistema completo de dashboard financiero P&L (Profit & Loss) con autenticación básica HTTP, diseñado para deployment en Railway (backend) y Vercel (frontend).

## 📋 Descripción

Este proyecto proporciona una interfaz web para visualizar y analizar datos financieros P&L en tiempo real. El sistema está compuesto por:

- **Backend**: API REST desarrollada en Flask con autenticación HTTP Basic
- **Frontend**: Interfaz web responsive desarrollada en HTML/CSS/JavaScript vanilla
- **Autenticación**: Sistema de autenticación básica HTTP para proteger el acceso a los datos

## 🏗️ Arquitectura

```
┌─────────────┐         ┌─────────────┐
│   Vercel    │ ──────> │   Railway   │
│  (Frontend) │         │  (Backend)  │
└─────────────┘         └─────────────┘
     HTML/CSS/JS           Flask API
```

- **Frontend (Vercel)**: Sirve la interfaz HTML estática
- **Backend (Railway)**: Procesa requests, autentica usuarios y devuelve datos P&L
- **Comunicación**: REST API con autenticación HTTP Basic

## 📁 Estructura del Proyecto

```
pl-dashboard-ethnix/
├── backend/
│   ├── app.py                 # API Flask principal
│   ├── excel_parser.py        # Parser para archivos Excel
│   ├── requirements.txt       # Dependencias Python
│   ├── .env.example           # Template de variables de entorno
│   ├── .gitignore
│   └── data/
│       ├── excels/            # Archivos Excel fuente
│       └── json/              # Datos procesados en JSON
├── frontend/
│   ├── index.html             # Dashboard principal
│   └── vercel.json            # Configuración Vercel
├── railway.json               # Configuración Railway
├── README.md
├── DEPLOYMENT.md
└── .gitignore
```

## 🚀 Instalación Local

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes Python)
- Navegador web moderno

### Backend

1. Navegar al directorio backend:
```bash
cd backend
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Ejecutar servidor:
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend

1. Abrir `frontend/index.html` en un navegador web
2. O usar un servidor local:
```bash
cd frontend
python -m http.server 8000
# O usar cualquier servidor HTTP estático
```

## 🔐 Variables de Entorno

### Backend (.env)

```env
AUTH_USERNAME=ethnix          # Usuario para Basic Auth
AUTH_PASSWORD=tu_password     # Contraseña para Basic Auth
PORT=5000                     # Puerto del servidor (Railway lo asigna automáticamente)
```

### Frontend (index.html)

Editar la configuración en `index.html`:

```javascript
const API_CONFIG = {
    baseUrl: 'https://tu-backend.railway.app/api',  // URL de producción
    username: 'ethnix',
    password: 'tu_password'
};
```

## 📡 Endpoints de la API

### GET /api/health
Endpoint de salud (sin autenticación)
- **Respuesta**: `{"status": "ok"}`

### GET /api/pl
Obtiene datos P&L (requiere autenticación)
- **Query params**: `tipo` (opcional, default: 'general')
- **Autenticación**: HTTP Basic Auth
- **Respuesta**: JSON con estructura de datos P&L

### GET /api/files
Lista archivos disponibles (requiere autenticación)
- **Autenticación**: HTTP Basic Auth
- **Respuesta**: `{"files": []}`

## 🎨 Características del Dashboard

- **Header azul** (#1e3a5f) con título "Ethnix Group - P&L USD"
- **Controles de filtrado**: Tipo Vista, Periodo, Centro Distribución
- **Tabla P&L** con:
  - Filas totales con fondo amarillo (#ffeaa7)
  - Formato de números: 1,234,567
  - Negativos: (123,456)
  - Colores: Verde (#28a745) para positivos, Rojo (#dc3545) para negativos
  - Diseño responsive (breakpoint 768px)

## 🛠️ Tecnologías Utilizadas

### Backend
- Flask 3.0.0
- flask-cors 4.0.0
- pandas 2.1.4
- openpyxl 3.1.2
- gunicorn 21.2.0
- python-dotenv 1.0.0

### Frontend
- HTML5
- CSS3 (Vanilla)
- JavaScript (ES6+)

## 📝 Uso

1. Acceder al dashboard a través de la URL de Vercel
2. Seleccionar filtros (Tipo Vista, Periodo, Centro Distribución)
3. Los datos se cargan automáticamente desde el backend
4. Visualizar métricas P&L en la tabla

## 🔒 Seguridad

- Autenticación HTTP Basic implementada
- CORS configurado para permitir solo dominios autorizados
- Credenciales almacenadas en variables de entorno (no en código)
- Recomendado: Usar HTTPS en producción

## 📚 Documentación Adicional

Para instrucciones detalladas de deployment, consultar [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📄 Licencia

Este proyecto es propiedad de Ethnix Group.

