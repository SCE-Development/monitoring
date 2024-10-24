FROM python:3-alpine AS builder

RUN pip install grafanalib

COPY ./provisioning/dashboards-py /dashboards

# Required for grafanalib to find the shared python files like common.py
ENV PYTHONPATH=/dashboards

RUN generate-dashboards /dashboards/*.dashboard.py

# stage 2
FROM grafana/grafana:latest

# Grafana configs
COPY ./grafana.ini /etc/grafana/grafana.ini
COPY ./provisioning/datasources/ /etc/grafana/provisioning/datasources/
COPY ./provisioning/dashboards-py/all.yml /etc/grafana/provisioning/dashboards/all.yml

# Generated dashboards
COPY --from=builder /dashboards/*.json /etc/grafana/provisioning/dashboards
