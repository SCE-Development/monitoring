from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE, BYTES_IEC

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(title='SCE CICD')

wrapper.AddPanel(
    title="Connection to smee2 (1 if connected)",
    queries=[
        ExpressionAndLegendPair(
            'is_websocket_connected',
            "{{exported_job}}",
        )
    ],
)

wrapper.AddPanel(
    title="Last Smee request timestamp",
    queries=[
        ExpressionAndLegendPair(
            'time() - last_smee_request_timestamp',
        )
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="Last github parsed from smee2",
    queries=[
        ExpressionAndLegendPair(
            'time() - last_push_timestamp',
        )
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="Docker Image Usage (bytes)",
    panel_type_enum=PanelType.STAT,
    queries=[
        ExpressionAndLegendPair(
            'docker_image_disk_usage_bytes',
            "{{exported_job}}",
        )
 ],
    unit=BYTES_IEC,
)

dashboard = wrapper.Render()
