from dash import dcc, html
from urllib.parse import quote as urlquote
import os
from os import path 
import base64

UPLOAD_DIRECTORY = f"{os.path.dirname(os.path.realpath(__file__))}/models/"

def upload_area():
    return dcc.Upload(
        id='upload-input',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True,
    )

def create_upload_dir_if_not_exists():
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.mkdir(UPLOAD_DIRECTORY) 

def file_download_link(filename):
    location = f"{UPLOAD_DIRECTORY}/{urlquote(filename)}"
    return html.A(filename, href=location)

def save_file(filenname, content):
    create_upload_dir_if_not_exists()

    data = content.encode("utf8").split(b";base64,")[1]
    path = os.path.join(UPLOAD_DIRECTORY, filenname)
    with open(path, "wb") as fp:
        fp.write(base64.decodebytes(data))

    return path

def show_all_files():
    create_upload_dir_if_not_exists()
    
    files = []
    for file in os.listdir(UPLOAD_DIRECTORY):
        if path.isfile(path.join(UPLOAD_DIRECTORY, file)):
            files.append(file)

    return files