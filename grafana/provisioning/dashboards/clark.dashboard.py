from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

from grafanalib.formatunits import NUMBER_FORMAT

wrapper = SceGrafanalibWrapper("Clark")
wrapper.DefineRow("Office Access Card")
wrapper.AddPanel(
    title="Office Access Card - 200 Responses",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode="200"}',
            "",
        )
    ],
    dydt=True,
)
wrapper.AddPanel(
    title="Office Access Card - Non 200 Responses",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode!="200"}',
            "{{statusCode}}",
        )
    ],
    dydt=True,
)
wrapper.DefineRow("Endpoint Requests")
wrapper.AddPanel(
    title="All main-endpoints traffic",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{route!="/metrics"}', "{{route}} {{method}} {{statusCode}}"
        )
    ],
    unit=NUMBER_FORMAT,
)
wrapper.AddPanel(
    title="Account access",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{route=~"/api/Auth.*"}', "{{route}} {{method}} {{statusCode}}"
        )
    ],
    unit=NUMBER_FORMAT,
)
wrapper.AddPanel(
    title="Messaging",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{route=~"/api/messages/.*"}',
            "{{route}} {{method}} {{statusCode}}",
        )
    ],
    unit=NUMBER_FORMAT,
)
dashboard = wrapper.Render()
