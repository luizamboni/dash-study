from dash import Dash, html, dcc, Input, Output, callback, State
from time import sleep
from uuid import uuid4

app = Dash()

def generate_p(idx=0):
    return html.P("another component", id=str(idx))
    
setattr(app, "items", [])


app.layout = html.Div([
    html.P("this is a static content"),
    html.P("log updates: 0", id="log"),
    html.P("always when children of panel changes", className="help"),
    dcc.Loading(
        id="loading",
        children=[
            html.Div(
                app.items, 
                id="panel", 
                className="card"
            ),
            html.P("always when button is clicked", className="help"),
        ]
    ),
    html.Button("add more", id="btn")
])

@callback(
    Output("log", "children"),
    Input("panel", "children"),
    State("log","children"),  # state not will trigger the action
)
def set_log(panel_children, log_children):
    if len(panel_children) == 0:
       print("return current value to log")
       return log_children

    return f"log updates: {uuid4()}"

@callback(
    Output("panel", "children"), # the child of dcc.Loading who will be updated
    Input("btn", "n_clicks")     # event that will trigger updates
)
def add_items(n_clicks):
    if not n_clicks:
        return app.items
    sleep(0.5)

    app.items.append(generate_p(idx=n_clicks))
    return app.items


if __name__ == '__main__':
    app.run_server(debug=True)


