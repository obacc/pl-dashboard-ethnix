# Guía de Deployment - P&L Dashboard

Esta guía proporciona instrucciones paso a paso para desplegar el P&L Dashboard en Railway (backend) y Vercel (frontend).

## 📋 Prerrequisitos

- Cuenta en [Railway](https://railway.app)
- Cuenta en [Vercel](https://vercel.com)
- Repositorio Git (GitHub, GitLab, o Bitbucket)
- Código del proyecto en el repositorio

## 🚂 Paso 1: Deployment del Backend en Railway

### 1.1 Crear Proyecto en Railway

1. Iniciar sesión en [Railway](https://railway.app)
2. Click en "New Project"
3. Seleccionar "Deploy from GitHub repo" (o tu proveedor Git)
4. Seleccionar el repositorio `pl-dashboard-ethnix`

### 1.2 Configurar el Servicio

1. Railway detectará automáticamente el proyecto
2. Asegúrate de que el **Root Directory** esté configurado correctamente
3. Railway usará el archivo `railway.json` para la configuración

### 1.3 Configurar Variables de Entorno

En el dashboard de Railway, ir a la pestaña **Variables** y agregar:

```
AUTH_USERNAME=ethnix
AUTH_PASSWORD=tu_password_seguro_aqui
```

**⚠️ IMPORTANTE**: 
- Usa una contraseña segura en producción
- Railway asignará automáticamente la variable `PORT` (no necesitas configurarla)

### 1.4 Verificar Deployment

1. Railway construirá y desplegará automáticamente
2. Una vez completado, Railway proporcionará una URL (ej: `https://tu-proyecto.railway.app`)
3. Probar el endpoint de health:
   ```
   https://tu-proyecto.railway.app/api/health
   ```
   Debe responder: `{"status": "ok"}`

### 1.5 Obtener URL del Backend

1. En Railway, ir a la pestaña **Settings**
2. Copiar la **Public Domain** (ej: `tu-proyecto.railway.app`)
3. Esta URL será necesaria para configurar el frontend

## ▲ Paso 2: Deployment del Frontend en Vercel

### 2.1 Preparar el Frontend

1. Editar `frontend/index.html`
2. Actualizar la configuración de API:

```javascript
const API_CONFIG = {
    baseUrl: 'https://tu-proyecto.railway.app/api',  // URL de tu backend en Railway
    username: 'ethnix',                              // Mismo usuario configurado en Railway
    password: 'tu_password_seguro_aqui'               // Misma contraseña configurada en Railway
};
```

3. Guardar los cambios y hacer commit:
```bash
git add frontend/index.html
git commit -m "Configurar URL de API para producción"
git push
```

### 2.2 Crear Proyecto en Vercel

1. Iniciar sesión en [Vercel](https://vercel.com)
2. Click en "Add New Project"
3. Importar el repositorio `pl-dashboard-ethnix`

### 2.3 Configurar el Proyecto

1. **Root Directory**: Configurar como `frontend`
   - En Vercel, ir a Settings → General
   - En "Root Directory", escribir: `frontend`

2. **Framework Preset**: Seleccionar "Other" o dejar en blanco

3. **Build Command**: Dejar vacío (es un sitio estático)

4. **Output Directory**: Dejar vacío o poner `.`

### 2.4 Desplegar

1. Click en "Deploy"
2. Vercel construirá y desplegará el proyecto
3. Una vez completado, Vercel proporcionará una URL (ej: `https://tu-proyecto.vercel.app`)

### 2.5 Verificar Deployment

1. Abrir la URL de Vercel en el navegador
2. El dashboard debería cargarse
3. Verificar que los datos se carguen correctamente desde el backend

## 🔧 Paso 3: Configuración de CORS

Si encuentras errores de CORS, verificar que el backend permita el dominio de Vercel:

1. En `backend/app.py`, la configuración CORS ya incluye `https://*.vercel.app`
2. Si tu dominio de Vercel es diferente, actualizar:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://*.vercel.app",
            "https://tu-dominio-personalizado.com",  # Agregar si es necesario
            "http://localhost:*"
        ],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

3. Hacer commit y push (Railway redeployará automáticamente)

## 🧪 Paso 4: Testing

### 4.1 Probar Endpoint de Health

```bash
curl https://tu-proyecto.railway.app/api/health
```

Respuesta esperada:
```json
{"status": "ok"}
```

### 4.2 Probar Endpoint P&L (con autenticación)

```bash
curl -u ethnix:tu_password \
  https://tu-proyecto.railway.app/api/pl
```

Respuesta esperada: JSON con datos P&L

### 4.3 Probar desde el Frontend

1. Abrir la URL de Vercel
2. Verificar que:
   - El dashboard carga correctamente
   - Los datos se muestran en la tabla
   - Los filtros funcionan
   - Los números están formateados correctamente

## 🔐 Paso 5: Seguridad Adicional (Opcional)

### 5.1 Usar Variables de Entorno en Frontend

Para mayor seguridad, puedes usar variables de entorno de Vercel:

1. En Vercel, ir a Settings → Environment Variables
2. Agregar:
   - `NEXT_PUBLIC_API_URL` (si usas Next.js)
   - O modificar el HTML para leer desde variables

**Nota**: Como estamos usando HTML estático, las credenciales estarán visibles en el código fuente. Para mayor seguridad, considera:
- Implementar un proxy en el backend
- Usar tokens JWT en lugar de Basic Auth
- Implementar un sistema de autenticación más robusto

### 5.2 Configurar Dominio Personalizado

**Railway**:
1. En Settings → Domains
2. Agregar dominio personalizado
3. Configurar DNS según instrucciones

**Vercel**:
1. En Settings → Domains
2. Agregar dominio personalizado
3. Configurar DNS según instrucciones

## 🐛 Troubleshooting

### Error: CORS bloqueado

**Solución**: Verificar que el dominio de Vercel esté en la lista de orígenes permitidos en `backend/app.py`

### Error: 401 Unauthorized

**Solución**: 
- Verificar que las credenciales en `frontend/index.html` coincidan con las de Railway
- Verificar que las variables de entorno en Railway estén configuradas correctamente

### Error: Backend no responde

**Solución**:
- Verificar logs en Railway
- Verificar que el servicio esté activo
- Verificar que el puerto esté configurado correctamente

### Error: Frontend no carga datos

**Solución**:
- Abrir consola del navegador (F12) y revisar errores
- Verificar que la URL del backend en `index.html` sea correcta
- Verificar que el backend esté accesible públicamente

## 📊 Monitoreo

### Railway

- Ver logs en tiempo real en el dashboard de Railway
- Configurar alertas en Settings → Notifications

### Vercel

- Ver analytics en el dashboard de Vercel
- Configurar webhooks para notificaciones

## 🔄 Actualizaciones

### Actualizar Backend

1. Hacer cambios en el código
2. Commit y push al repositorio
3. Railway detectará cambios y redeployará automáticamente

### Actualizar Frontend

1. Hacer cambios en `frontend/index.html`
2. Commit y push al repositorio
3. Vercel detectará cambios y redeployará automáticamente

## 📝 Checklist de Deployment

- [ ] Backend desplegado en Railway
- [ ] Variables de entorno configuradas en Railway
- [ ] Endpoint `/api/health` responde correctamente
- [ ] Frontend actualizado con URL del backend
- [ ] Frontend desplegado en Vercel
- [ ] CORS configurado correctamente
- [ ] Autenticación funcionando
- [ ] Dashboard carga datos correctamente
- [ ] Filtros funcionan
- [ ] Diseño responsive funciona en móviles

## 🎉 ¡Listo!

Tu P&L Dashboard está ahora desplegado y funcionando en producción. Puedes acceder al dashboard a través de la URL de Vercel y los datos se cargarán desde el backend en Railway.

