import dash
from dash import dcc, html
from flask import Flask, send_from_directory

from uploads import UPLOAD_DIRECTORY
from fasttext_train_model import train_fasttext
# create the Dash app

server = Flask(__name__)

app = dash.Dash(server=server, use_pages=True)


@server.route("/models/<path:path>")
def download(path):
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                ),
                className="item"
            )
            for page in dash.page_registry.values()
        ],
        className="nav-top"

    ),

	dash.page_container
],
className="layout")

# run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)