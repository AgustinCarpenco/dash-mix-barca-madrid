# dash-mix-barca-madrid
# 📊 Dashboard de Estadísticas de Partidos

## 📌 Introducción
Este proyecto es un dashboard interactivo desarrollado en **Dash** (Plotly) que muestra estadísticas de partidos de fútbol, utilizando datos locales en formato CSV.

El objetivo es analizar los goles de los equipos locales y visitantes, visualizando su distribución a lo largo del tiempo y comparando su desempeño.

## 📂 Estructura del Proyecto
```
├── dash-mix-barca-madrid/
│   ├── data/
│   │   ├── Estadisticas_de_Partidos.csv  # Datos de los partidos
│   ├── app.py  # Código principal de la app
│   ├── README.md  # Documentación del proyecto
│   ├── requirements.txt  # Dependencias del proyecto
│   ├── .gitignore  # Archivos a ignorar en Git
```

## 🚀 Instalación y Ejecución
### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/dash-mix-barca-madrid.git
cd dash-mix-barca-madrid
```

### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la aplicación
```bash
python app.py
```
El dashboard estará disponible en [http://127.0.0.1:8060/](http://127.0.0.1:8060/).

## 🎨 Características del Dashboard
✅ **Gráfico de Promedio de Goles por Fecha** 📈
   - Muestra la evolución del promedio de goles por partido en el tiempo.

✅ **Comparación de Goles Locales vs Visitantes** ⚽
   - Permite visualizar cuántos goles se marcaron jugando como local y visitante.

✅ **Filtro de Equipos** 🔎
   - Se puede seleccionar un equipo específico para analizar su desempeño.

## 🖼️ Capturas de Pantalla
### 📈 Promedio de Goles por Fecha
![Promedio de Goles](ruta/a/la/captura1.png)

### ⚽ Comparación de Goles Locales vs Visitantes
![Comparación de Goles](ruta/a/la/captura2.png)

## 🔄 Actualización y Mantenimiento
Si deseas actualizar los datos, reemplaza el archivo `Estadisticas_de_Partidos.csv` en la carpeta `data/` con nuevos datos en el mismo formato.

## 📬 Contacto
Si tienes dudas o sugerencias, puedes contactarme a través de GitHub o por email.

---
📌 **¡Listo para entregar! 🚀**
