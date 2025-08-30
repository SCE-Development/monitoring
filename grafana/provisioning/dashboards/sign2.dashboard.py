from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='sign2')

wrapper.AddPanel(
    title="Sign last updated",
    queries=[
        ExpressionAndLegendPair(
            'time() - sign_last_updated',
        )
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
            'endpoint_hits',
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

dashboard = wrapper.Render()
