# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026 17:58
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Define a pasta raiz de trabalho inicial
WORKDIR /app

# Instala as bibliotecas de sistema exigidas pelo navegador
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copia todos os seus arquivos (raiz, frontend e backend) para o servidor
COPY . /app

# Navega para dentro da pasta backend onde os arquivos Python realmente estão
WORKDIR /app/backend

# Instala as dependências do Python lendo o requirements.txt correto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta de comunicação do Render
EXPOSE 8000

# Comando que inicializa o servidor da API (agora chamando o main.py diretamente da pasta backend)
CMD ["python", "main.py"]
