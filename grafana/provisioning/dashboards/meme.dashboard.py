import wrapper

dashboard = wrapper.SceGrafanalibWrapper("hello world", "testing wrapper class")

dashboard.DefineRow("silly row")
dashboard.AddPanelToRow("bing bong", [wrapper.ExpressionAndLegendPair(expression="scalar(42)")])
dashboard.AddPanel("outside gang", [wrapper.ExpressionAndLegendPair(expression='scalar(42)')])

dashboard.Render()
