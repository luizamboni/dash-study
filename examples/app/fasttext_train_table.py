
from dash import dash_table


def render_fastext_train_data(df, columns, id):

    fasttext_columns = ["text", "label"]

    return dash_table.DataTable(
        id=id,
        columns=[c for c in columns if c['name'] in fasttext_columns],
        data=df[fasttext_columns].to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'padding': "10px"},
        page_size=100
    )