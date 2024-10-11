FROM python:3.9-slim-buster as builder

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./provisioning/dashboards-py/* ./

RUN ls

RUN ./generate.sh

# stage 2
FROM grafana/grafana:latest

COPY --from=builder /app/silly /etc/grafana/provisioning/dashboards

COPY ./grafana.ini /etc/grafana/grafana.ini

COPY ./provisioning/dashboards-py/all.yml /etc/grafana/provisioning/dashboards/all.yml

COPY ./provisioning/datasources/ /etc/grafana/provisioning/datasources/

RUN ls /etc/grafana/provisioning/dashboards

EXPOSE 3000

ENTRYPOINT [ "/run.sh" ]
