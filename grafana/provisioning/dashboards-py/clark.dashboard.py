from grafanalib.core import (
    Dashboard,
    Templating,
    Template,
    TimeSeries,
    Target,
    GridPos,
    Row,
)
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import PROMETHEUS_DATASOURCE_NAME


def get_office_card_row():
    return Row(
        title="Office Access Card",
        panels=[
            TimeSeries(
                title="Office Access Card - 200 Responses",
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='sum(endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode="200"})',
                        legendFormat="total",
                        refId="A",
                    ),
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='sum(rate(endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode="200"}[1h])) * 3600',
                        legendFormat="dY/dt [hourly]",
                        refId="B",
                    ),
                ],
            ),
            TimeSeries(
                title="Office Access Card - Non 200 Responses",
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='sum(endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode!="200"}) by (statusCode)',
                        legendFormat="{{statusCode}} total",
                        refId="A",
                    ),
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='sum(rate(endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode!="200"}[1h])) by (statusCode) * 3600',
                        legendFormat="{{statusCode}} dY/dt [hourly]",
                        refId="B",
                    ),
                ],
            ),
        ],
    )


def get_other_row():
    return Row(
        title="Endpoint Requests",
        panels=[
            TimeSeries(
                title="All main-endpoints traffic",
                unit=NUMBER_FORMAT,
                gridPos=GridPos(h=8, w=12, x=0, y=0),
                lineWidth=2,
                stacking={"group": "A", "mode": "none"},
                tooltipMode="all",
                tooltipSort="desc",
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='endpoint_hits{route!="/metrics"}',
                        legendFormat="{{route}} {{method}} {{statusCode}}",
                        refId="A",
                    ),
                ],
            ),
            TimeSeries(
                title="Account access",
                unit=NUMBER_FORMAT,
                gridPos=GridPos(h=8, w=12, x=12, y=0),
                lineWidth=2,
                stacking={"group": "A", "mode": "none"},
                tooltipMode="all",
                tooltipSort="desc",
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='endpoint_hits{route=~"/api/Auth.*"}',
                        legendFormat="{{route}} {{method}} {{statusCode}}",
                        refId="A",
                    ),
                ],
            ),
            TimeSeries(
                title="Messaging",
                unit=NUMBER_FORMAT,
                gridPos=GridPos(h=8, w=12, x=12, y=8),
                lineWidth=2,
                stacking={"group": "A", "mode": "none"},
                tooltipMode="all",
                tooltipSort="desc",
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr='endpoint_hits{route=~"/api/messages/.*"}',
                        legendFormat="{{route}} {{method}} {{statusCode}}",
                        refId="A",
                    ),
                ],
            ),
        ],
    )


dashboard = Dashboard(
    title="Clark",
    uid="clark",
    description="sce club website",
    timezone="browser",
    rows=[get_office_card_row(), get_other_row()],
).auto_panel_ids()
