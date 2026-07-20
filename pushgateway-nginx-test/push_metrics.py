from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

metric = Gauge( 
    "nginx_pushgateway_test",
    "Metric sent through the Nginx proxy",
    registry=registry,
)
metric.set(50)

push_to_gateway(
    "http://nginx/pushgateway",
    job="nginx_proxy_test",
    registry=registry,
)

print("successfully pushed metric")