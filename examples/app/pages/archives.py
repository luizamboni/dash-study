import dash
from dash import html, Input, Output, callback
import pandas as pd

from panel import render_panel
from uploads import upload_area, file_download_link, save_file, show_all_files

# create the Dash app
dash.register_page(__name__, path='/archives')


def render_all_files_in_list():
    all_files = show_all_files()
    return html.Ul([
        html.Li(html.A(filename, href="/models/"+ filename)) for filename in all_files
    ], id="files-list")

upload_place = upload_area() 
all_files_list = render_all_files_in_list()

# create the layout for the app
layout = html.Div(
    [
        html.H1('archives'),
        # upload area
        render_panel("upload", "upload-area", [ upload_place ]),
        render_panel("archive", "archive-area", [
            all_files_list
        ])
    ],
    className="layout"
)

@callback(
    Output(all_files_list.id, 'children'),
    [
        Input(upload_place.id,'filename'),
        Input(upload_place.id,'contents'),
    ]
)
def display_uploaded_dataset(filename, contents):
    if filename and contents:
        save_file(filename[0], contents[0])
    return render_all_files_in_list()