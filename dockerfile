FROM python:3.7
RUN apt-get update && apt-get install -y python3.7 gunicorn
ENV VENV=/opt/venv
RUN python3.7 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"
COPY . ./app
WORKDIR app
RUN pip install -r requirements.txt
CMD ["python", "main.py", "run"]
