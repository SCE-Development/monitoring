import wrapper

asdf = wrapper.SceGrafanalibWrapper("hello world", "testing wrapper class")

asdf.AddPanel("bing bong", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("bing bong1", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("bing bong2", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("bing bong3", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("bing bong4", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("another panel", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("another panel2", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("another panel3", [wrapper.ExpressionAndLegendPair(expression="time()")])
asdf.AddPanel("another panel4", [wrapper.ExpressionAndLegendPair(expression="time()")])

dashboard = asdf.Render()
