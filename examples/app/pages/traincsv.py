import dash
from dash import dcc, html, Input, Output, dash_table, callback
import pandas as pd

from train_table import render_train_table
from fasttext_train_table import render_fastext_train_data
from panel import render_panel
from uploads import upload_area, file_download_link, save_file
from fasttext_train_model import train_fasttext
# create the Dash app

dash.register_page(__name__, path='/')


upload_place = upload_area() 
table_to_select_examples = dash_table.DataTable(id="table-to-select-examples")
table_of_selected_examples = dash_table.DataTable(id="table-of-selected-examples")
train_btn = html.Button("treinar Modelo", className="btn", id="train-btn", n_clicks=0)
model_output_panel = render_panel("modelo", "model-output-panel", [])

# create the layout for the app
layout = html.Div(
    [
        html.H1('Model Training'),
        # upload area
        render_panel(
            "upload", 
            "upload-area", 
            [ upload_place ]
        ),
        # result of uploaded csv
        render_panel(
            "exemplos a validar", 
            "examples-to-select-panel", 
            [ table_to_select_examples ]
        ),
        # result of selected rows
        render_panel(
            "exemplos", 
            "selected-examples-panel", 
            [ table_of_selected_examples ]
        ),
        # train model btn
        train_btn,
        # model statistcs output
        model_output_panel,
    ],
    className="layout"
)

@callback(
    Output("examples-to-select-panel-content", 'children'),
    [
        Input(upload_place.id,'filename'),
        Input(upload_place.id,'contents'),
    ]
)
def display_uploaded_dataset(filename, contents):
    if not filename or not contents:
        return None

    path = save_file(filename[0], contents[0])
    df = pd.read_csv(path)
    return render_train_table(df, table_to_select_examples.id)

@callback(
    Output("selected-examples-panel-content", 'children'),
    [
        Input(table_to_select_examples.id, 'data'),
        Input(table_to_select_examples.id, 'columns'),
        Input(table_to_select_examples.id, 'selected_rows'),
    ]
)
def display_selected_examples(rows, columns, selected_rows):
    if not rows or not columns or not selected_rows:
        return None

    df = pd.DataFrame(
        rows, 
        columns=[c['name'] for c in columns],
        index=[ ind for ind, _ in enumerate(rows) ]
    ).iloc[selected_rows]

    return render_fastext_train_data(df, columns, table_of_selected_examples.id) 

@callback(
    Output("model-output-panel-content", 'children'),
    [
        Input(train_btn.id, 'n_clicks'),
        Input(table_of_selected_examples.id, 'data'),
        Input(table_of_selected_examples.id, 'columns'),
    ],
)
def train_model(n_clicks, rows, columns):
    if n_clicks == 0:
        return None

    train_data_df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

    model, model_filename, precision, recall, f1_score = train_fasttext(train_data_df)


    return html.Div([
        html.P(f'Precision: {precision}'),
        html.P(f'Recall: {recall}'),
        html.P(f'F1-Score: {f1_score}'),
        file_download_link(model_filename),
        dcc.Input(
            id="test-value",
            type="text",
            placeholder="teste aqui...",
        ),
        html.Button("Testar", id="test-model-btn"),
        html.P(f'class: ...'),
    ])
