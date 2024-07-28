FROM python:3.8
LABEL authors="schnee"

COPY . /MemberManagement
WORKDIR /MemberManagement

# Upgrade pip to the latest version
RUN pip install --progress-bar off  --upgrade pip

RUN pip install --progress-bar off -r requirements.txt

ENV FLASK_APP="app.py" FLASK_ENV="local"

EXPOSE 5000

CMD ["python3", "-m" ,"flask", "run"]