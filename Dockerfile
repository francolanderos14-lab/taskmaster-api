# Imagen base: Python 3.13 en su versión "slim"
FROM python:3.13-slim

# Carpeta de trabajo dentro del contenedor. Todo lo que hagamos de aquí en
# adelante pasa "dentro" de esta carpeta, como un cd en el contenedor.
WORKDIR /app

# Copiamos PRIMERO solo requirements.txt, no todo el código todavía.
# Esto es una técnica de optimización: Docker cachea cada paso, y si el
# código cambia pero las dependencias no, no necesita reinstalar todo de nuevo.
COPY requirements.txt .

# Instalamos las dependencias dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# copiamos el resto del código (la carpeta app/)
COPY app/ ./app/

# Documentamos que este contenedor escucha en el puerto 8000
# (no abre el puerto por sí solo, solo es informativo)
EXPOSE 8000

# Comando que se ejecuta cuando el contenedor arranca
# Nota: sin --reload, eso es solo para desarrollo local, no para producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]