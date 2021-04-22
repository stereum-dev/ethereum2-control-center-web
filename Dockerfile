FROM node as frontend-builder
WORKDIR /tmp/build
COPY frontend/package.json frontend/vue.config.js frontend/package-lock.json /tmp/build/
COPY frontend/src src
COPY frontend/public public
RUN npm i
RUN npm run build

FROM python:3.9-slim-buster
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py inventory.yaml playbook.yaml /opt/app/
WORKDIR /opt/app/public
COPY --from=frontend-builder /tmp/build/dist .
WORKDIR /opt/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "3" ]
