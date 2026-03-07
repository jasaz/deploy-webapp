#################################### build-stage ########################################

FROM docker.io/jasaz/wolfi-python:wolfi-python3-14-pip as build-stage

WORKDIR /app
COPY *.py .
COPY requirements.txt .
COPY wizexercise.txt .

RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

#################################### final-stage ########################################

FROM docker.io/jasaz/wolfi-python:wolfi-python3-14 as final-stage

WORKDIR /app

COPY --from=build-stage /home/nonroot/.local /home/nonroot/.local 
COPY --from=build-stage /app /app

ENV PATH=/bin:/usr/bin:/home/nonroot/.local/bin

ENTRYPOINT ["python", "flask-demo.py"]
