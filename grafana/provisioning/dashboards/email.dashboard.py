from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair
from grafanalib.formatunits import NUMBER_FORMAT

wrapper = SceGrafanalibWrapper("Email Tracking")

wrapper.DefineRow("Current Time")
wrapper.AddPanel(
    title="Current Epoch Time",
    queries=[
        ExpressionAndLegendPair(
            'current_epoch_time{app="sce-core"}',
            'Current Epoch Time'
        )
    ],
)

wrapper.DefineRow("Refresh Token Expired")
wrapper.AddPanel(
    title="Refresh Token Refreshed",
    queries=[
        ExpressionAndLegendPair(
            'google_cloud_refresh_token_epoch{app="sce-core"}',
            'Refresh token expired and refreshed'
        )
    ],
)

wrapper.DefineRow("Email Sent")
wrapper.AddPanel(
    title="Total Emails Sent",
    queries=[
        ExpressionAndLegendPair(
            'email_sent{type="verification"}',
            'Total Auth Emails'
        )
    ],
    unit=NUMBER_FORMAT,
)
dashboard = wrapper.Render()
