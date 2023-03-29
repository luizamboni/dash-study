
from dash import dash_table

def render_train_table(df, id):

    records = df.to_dict('records')
    selected_rows = [ ind for ind, _ in enumerate(records) ]

    return dash_table.DataTable(
        id=id,
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=records,
        row_deletable=True,
        row_selectable="multi",
        editable=True,
        selected_rows=selected_rows,
        fixed_rows={'headers': True},
        style_cell={'textAlign': 'left', 'padding': "10px"},
        style_header={
            'backgroundColor': "#000",
            'color': '#fff',
            'fontWeight': 'bold',
        },
        style_table={'height': '300px', 'overflowY': 'auto'},
        page_size=50
    )