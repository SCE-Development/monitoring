from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

from grafanalib.formatunits import SECONDS, NUMBER_FORMAT

wrapper = SceGrafanalibWrapper("SCE Transit Page")
wrapper.AddPanel(
    "Cache Update Errors",
    [ExpressionAndLegendPair("cache_update_errors_total", "__auto")],
    NUMBER_FORMAT,
)
wrapper.AddPanel(
    "HTTP Response Codes",
    [
        ExpressionAndLegendPair(
            'http_code_total{job="sceta-server", path!="/metrics"}', "{{code}} {{path}}"
        )
    ],
    NUMBER_FORMAT,
)
wrapper.AddPanel(
    "Cache Age",
    [ExpressionAndLegendPair("time() - cache_last_updated", "__auto")],
    SECONDS,
)
wrapper.AddPanel(
    "511 API Response Codes",
    [ExpressionAndLegendPair("api_response_codes_total", "__auto")],
    NUMBER_FORMAT,
)
wrapper.AddPanel(
    "511 API Latency",
    [ExpressionAndLegendPair("api_latency_sum / api_latency_count", "__auto")],
    SECONDS,
)
dashboard = wrapper.Render()