from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair
from grafanalib.formatunits import NUMBER_FORMAT

wrapper = SceGrafanalibWrapper("Email Tracking")

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
