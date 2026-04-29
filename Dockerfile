# NOVO CÓDIGO INSERIDO AQUI - 29/04/2026 11:50
# Usa a imagem oficial da Microsoft que já possui o Chrome instalado
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Define a pasta de trabalho dentro do servidor
WORKDIR /app

# Instala as bibliotecas de sistema exigidas pelo navegador
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copia todos os seus arquivos para o servidor
COPY . /app

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta de comunicação do Render
EXPOSE 8000

# Comando que inicializa o servidor da API
CMD ["python", "backend/main.py"]
