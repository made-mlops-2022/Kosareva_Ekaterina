FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY model/rfc_model.sav model/rfc_model.sav
COPY src/* /
COPY data/data.csv data/data.csv

WORKDIR .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]