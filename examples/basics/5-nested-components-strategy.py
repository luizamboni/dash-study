# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, callback, Input, Output,ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

def generate_graph():
    btn = html.Button("hide", id="toggle-hide-show")

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    graph = dcc.Graph(
        style={'display': 'block'},
        className="card",
        id='example-graph',
        figure=fig
    )
    component = html.Div([
        btn,
        graph,
    ], id="")

    setattr(component, 'btn_id', btn.id)
    setattr(component, 'graph_id', graph.id)

    return component

graph = generate_graph()

app.layout = html.Div(children=[
    html.Div(children=[
            html.H1(children='Hello Dash'),
            html.P(children='Dash: A web application framework for your data.'),    
        ],
        className="card"
    ),
    graph,
])

@callback(
    Output(graph.graph_id, "style"),
    [
        Input(graph.btn_id, "n_clicks"),
        Input(graph.graph_id, "style"),
    ]
)
def toggle_visibility(n_clicks, style):
    if not n_clicks:
        return style
    style['display'] = 'none' if style['display'] == 'block' else 'block'
    return style

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
