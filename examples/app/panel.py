from dash import html


def render_panel(title, id,  childs=[]):
    return html.Div([
            html.P(title, className="label"), html.Div(childs, id=f"{id}-content")
        ],
        id=id,
        className="panel"
    )
