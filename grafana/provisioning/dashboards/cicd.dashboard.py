from grafanalib.formatunits import NUMBER_FORMAT, SECONDS

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(title="CICD")

wrapper.AddPanel(
    title="CICD Deployments",
    queries=[
        ExpressionAndLegendPair(
            'cicd_deployments_total',
            "{{repo}} {{branch}}",
        )
    ],
    dydt=True,
    unit=NUMBER_FORMAT,
)

wrapper.AddPanel(
    title="CICD Deployment Failures",
    queries=[
        ExpressionAndLegendPair(
            'cicd_deployment_failures_total',
            "{{repo}} {{branch}}",
        )
    ],
    dydt=True,
    unit=NUMBER_FORMAT,
)

wrapper.AddPanel(
    title="CICD Restarts",
    queries=[
        ExpressionAndLegendPair(
            'cicd_restarts_total',
            "{{host}}",
        )
    ],
    dydt=True,
    unit=NUMBER_FORMAT,
)

wrapper.AddPanel(
    title="CICD Deployment Duration",
    queries=[
        ExpressionAndLegendPair(
            'cicd_deployment_duration_seconds',
            "{{repo}} {{branch}}",
        )
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="CICD Server Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="sce-cicd"}',
        )
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="CICD Server Up",
    queries=[
        ExpressionAndLegendPair(
            'up{job="sce-cicd"}',
            "{{instance}}",
        )
    ],
    panel_type_enum=PanelType.STAT,
    unit=NUMBER_FORMAT,
)

dashboard = wrapper.Render()
