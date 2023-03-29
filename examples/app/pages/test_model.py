import dash
from dash import html, Input, Output, callback, dcc

from panel import render_panel
from fasttext_train_model import load_model
from uploads import UPLOAD_DIRECTORY
# create the Dash app
dash.register_page(__name__, path_template='/test-model/<model_filename>')

model = None
# create the layout for the app
def layout(model_filename=None):
    global model
    if model_filename:
        model = load_model(f'{UPLOAD_DIRECTORY}/{model_filename}')

    return html.Div(
        [
            html.H1('model test'),
            html.Div([
                "Input: ",
                dcc.Input(id='text-input', value='initial value', type='text')
            ]),
            html.Br(),
            html.Div(id='class-output'),
        ],
        className="layout"
    )

@callback(
    Output('class-output', 'children'),
    Input('text-input', 'value'),
)
def test_against(value):
    labels, confidence = model.predict(value)
    first_label = labels[0]
    return f"{first_label}  with confidence of {confidence[0]}"

