from dash import Dash, dcc, html, Input, Output # type: ignore
import dash_daq as daq # type: ignore
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv('output.csv')


def convert_units(value):
    if value >= 1_000_000:
        return value / 1_000_000, 'TB'
    elif value >= 1_000:
        return value / 1_000, 'GB'
    else:
        return value, 'MB'

def convert_avg_case_units(value):
    if value >= 1_000_000_000_000:
        return f"{int (value / 1_000_000_000_000) } TB"
    elif value >= 1_000_000_000:
        return f"{ int(value / 1_000_000_000) } GB"
    elif value >= 1_000_000:
        return f"{ int(value / 1_000_000) } MB"
    elif value >= 1_000:
        return f"{ int(value / 1_000) } KB"
    else:
        return f"{ int(value)} bytes"    
    
# Convert 'additional_field_1' to another unit, e.g., from meters to kilometers
df['total_datasize'] = (df['total_data'] ).apply(convert_avg_case_units)
df['avg_case_length'] = df['total_avg_case_length'].apply(convert_avg_case_units)

    
# Get the minimum and maximum values of pr_avg_row for the slider
min_pr_avg_row = df['total_avg_case_length'].min()
max_pr_avg_row = df['total_avg_case_length'].max()

marks={int(i): convert_avg_case_units(int(i)) for i in range(int(min_pr_avg_row), int(max_pr_avg_row)+1, int((max_pr_avg_row-min_pr_avg_row)/16))}
print(marks)
app.layout = html.Div(
    [
        html.H2("Filter Graph by average case size"),
        html.P("Select average case size :", style={"textAlign": "center"}),
        dcc.RangeSlider(
            id='pr-avg-row-slider',
            min=min_pr_avg_row,
            max=max_pr_avg_row,
            step=1,
            value=[min_pr_avg_row, max_pr_avg_row],
            marks=marks
        ),
        html.Div(id="slider-result")
    ]
)


@app.callback(
    Output("slider-result", "children"),
    Input("pr-avg-row-slider", "value"),
)
def update_output(value): 
    min_val, max_val = value
    filtered_df = df[(df['total_avg_case_length'] >= min_val) & (df['total_avg_case_length'] <= max_val)]
    
    if not filtered_df.empty:

        fig = px.line(
            filtered_df,
            x="pr_rows",
            y="total_data",
            color="schema",
            markers=True,
            title="Correlation Between Number of Cases and Database Size",
            hover_data={
                'pr_rows': True,
                'total_data': False,
                'total_datasize': True,
                'avg_case_length': True
            }
        )
        
        fig.update_yaxes(title_text=f"Total Data size")
        fig.update_xaxes(title_text=f"Cases", tickformat=',')        
                
        fig.update(layout=dict(
            title=dict(x=0.1),
            height=750
            ))
        return dcc.Graph(figure=fig)
    else:
        return html.P("No data available for the selected range.")

if __name__ == "__main__":
    app.run_server(debug=True)