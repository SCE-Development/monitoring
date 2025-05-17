import wrapper

asdf = wrapper.SceGrafanalibWrapper("hello world", "testing wrapper class")

asdf.DefineRow("silly row")
asdf.AddPanelToRow("bing bong", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("outside gang", [wrapper.ExpressionAndLegendPair(expression='time()')])

dashboard = asdf.Render()
