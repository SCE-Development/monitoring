import wrapper

asdf = wrapper.SceGrafanalibWrapper("hello world", "testing wrapper class")

asdf.DefineRow("first row")
asdf.AddPanelToRow("bing bong", [
    wrapper.ExpressionAndLegendPair(expression="time()"),
    wrapper.ExpressionAndLegendPair(expression="time()"),
])
asdf.AddPanelToRow("bing bong1", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("bing bong2", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("bing bong3", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("bing bong4", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.DefineRow("i added another")
asdf.AddPanelToRow("another panel", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("another panel2", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("another panel3", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanelToRow("another panel4", [wrapper.ExpressionAndLegendPair(expression="time()")])

dashboard = asdf.Render()
