from attrs import define
from grafanalib.core import Template, TimeSeries, Dashboard, HIDE_VARIABLE, Target

PROMETHEUS_DATASOURCE_NAME = 'Prometheus'


@define
class MyDashboard(Dashboard):
    """Wrapper class for Dashboard with some default values"""
    timezone: str = 'browser'
    sharedCrosshair: bool = True


@define
class MyTimeSeries(TimeSeries):
    """Wrapper class for TimeSeries with some default values and custom fields"""
    fillOpacity: int = 10
    lineWidth: int = 1
    showPoints: str = 'never'
    tooltipMode: str = 'multi'
    maxDataPoints: int = None

    # new fields
    axisCenteredZero: bool = False

    def to_json_data(self):
        data = super().to_json_data()
        data['fieldConfig']['defaults']['custom']['axisCenteredZero'] = self.axisCenteredZero
        return data


@define
class PromTarget(Target):
    """Wrapper class for Target with default prometheus datasource"""
    datasource: str = PROMETHEUS_DATASOURCE_NAME
