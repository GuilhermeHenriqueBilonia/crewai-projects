# Use uma imagem base oficial do Python
FROM python:3.11.5

# Defina o diretório de trabalho no contêiner
WORKDIR /

# Instale as dependências do sistema que podem ser necessárias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https

# Copie o requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo do projeto para o diretório de trabalho
COPY . .

# Exponha a porta em que o Uvicorn está rodando
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]