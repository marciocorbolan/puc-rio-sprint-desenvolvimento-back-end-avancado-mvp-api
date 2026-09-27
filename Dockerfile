# Usar imagem oficial e leve do Python
FROM python:3.10-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar todas as dependências diretamente no Dockerfile
RUN pip install --no-cache-dir \
    click==8.4.2 \
    flasgger==0.9.7.1 \
    Flask==3.1.3 \
    flask-cors==6.0.5 \
    flask-limiter==4.1.1 \
    Flask-SQLAlchemy==3.1.1 \
    greenlet==3.5.3 \
    importlib-metadata==9.0.0 \
    itsdangerous==2.2.0 \
    Jinja2==3.1.6 \
    MarkupSafe==3.0.3 \
    nose==1.3.7 \
    PyJWT==2.13.0 \
    PyYAML==6.0.2 \
    SQLAlchemy==2.0.51 \
    SQLAlchemy-Utils==0.42.1 \
    Werkzeug==3.1.8 \
    zipp==4.1.0 \
    requests

# Copiar todo o código do seu projeto para dentro do contêiner
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Configurar variáveis de ambiente do Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Comando para iniciar o servidor Flask
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000", "--reload"]