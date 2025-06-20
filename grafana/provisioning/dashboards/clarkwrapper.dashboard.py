from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

from grafanalib.formatunits import NUMBER_FORMAT

wrapper = SceGrafanalibWrapper("Clark w/ Wrapper")
wrapper.AddDyDtPanel("Office Access Card - 200 Responses", ExpressionAndLegendPair('endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode="200"}', ""))
wrapper.AddDyDtPanel("Office Access Card - Non 200 Responses", ExpressionAndLegendPair('endpoint_hits{route=~"/api/OfficeAccessCard/verify.*", statusCode="200"}', "{{statusCode}}"))
wrapper.AddPanel("All main-endpoints traffic", [ExpressionAndLegendPair('endpoint_hits{route!="/metrics"}', "{{route}} {{method}} {{statusCode}}")], NUMBER_FORMAT)
wrapper.AddPanel("Account access", [ExpressionAndLegendPair('endpoint_hits{route=~"/api/Auth.*"}', "{{route}} {{method}} {{statusCode}}")], NUMBER_FORMAT)
wrapper.AddPanel("Messaging", [ExpressionAndLegendPair('endpoint_hits{route=~"/api/messages/.*"}', "{{route}} {{method}} {{statusCode}}")], NUMBER_FORMAT)
dashboard = wrapper.Render()
