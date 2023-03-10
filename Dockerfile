FROM python:3.8.10

RUN pip install Flask==2.2.2

RUN pip install requests

RUN pip install xmltodict

RUN pip install geopy

COPY iss_tracker.py /iss_tracker.py

CMD ["python", "iss_tracker.py"]
