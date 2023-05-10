FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run", "./app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]