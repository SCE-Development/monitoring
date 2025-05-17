import wrapper

asdf = wrapper.SceGrafanalibWrapper("hello world", "testing wrapper class")

asdf.DefineRow("silly row")
asdf.AddPanelToRow("bing bong", [wrapper.ExpressionAndLegendPair(expression="scalar(42)")])
asdf.AddPanel("outside gang", [wrapper.ExpressionAndLegendPair(expression='scalar(42)')])

dashboard = asdf.Render()
