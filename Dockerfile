from python:3.12

WORKDIR application
COPY . .

RUN pip install -r requirements.txt

WORKDIR app/ 

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]