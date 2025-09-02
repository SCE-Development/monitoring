from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='sign2')

wrapper.AddPanel(
    title="Sign last updated",
    queries=[
        ExpressionAndLegendPair(
            'time() - sign_last_updated',
            unit=SECONDS
        ),
    ],
)

wrapper.AddPanel(
    title="Sign update error",
    queries=[
        ExpressionAndLegendPair(
            'sign_update_error'
        )
 ],
)

wrapper.AddPanel(
    title="LeetCode API Error",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_error'
        )
 ],
)

wrapper.AddPanel(
    title="Endpoint hits",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{endpoint!="/metrics"}',
        )
    ],
)

wrapper.AddPanel(
    title="LeetCode API Response Codes",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_response_codes',
        )
    ],
)

wrapper.AddPanel(
    title="LeetCode API latency",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_latency',
        )
    ],
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="sce-sign2"}',
            unit=SECONDS
        )
    ],
)

dashboard = wrapper.Render()
