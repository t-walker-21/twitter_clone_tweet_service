from python:3.12

WORKDIR app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0"]