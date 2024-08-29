from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px

app = Dash(__name__)

df = px.data.gapminder()
df = df.loc[df["pop"] > 1e8]

print(df)

app.layout = html.Div(
    [
        html.H2("Turning a Graph On and Off with BooleanSwitch"),
        html.P("graph off | graph on:", style={"textAlign": "center"}),
        daq.BooleanSwitch(id="pb", on=True),
        html.Div(id="pb-result")
    ]
)


@app.callback(
    Output("pb-result", "children"),
    Input("pb", "on"),
)
def update_output(on):
    if on:
        fig = px.line(
            df,
            x="year",
            y="lifeExp",
            color="country",
            markers=True,
            title="Life Expectancy for Countries with High Population",
        )
        fig.update(layout=dict(title=dict(x=0.5)))
        return dcc.Graph(figure=fig)
    else:
        fig = px.scatter()
        return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)