# Use a imagem base do Python para Django
FROM python:3.10
# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY ../. .
# Coleta arquivos estáticos para produção
RUN python manage.py collectstatic
# Copia o resto do código para o diretório de trabalho
# Configuração para o servidor Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.wsgi:application"]