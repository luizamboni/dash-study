from dash import Dash, html, dcc, dash_table
import pandas as pd
import numpy as np

app = Dash()

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

seattle = "[![Seattle](https://upload.wikimedia.org/wikipedia/commons/8/80/SeattleQueenAnne2021-2.png#thumbnail)](https://en.wikipedia.org/wiki/Seattle)"
montreal = "[![Montreal](https://upload.wikimedia.org/wikipedia/commons/d/d0/Montreal_August_2017_05.jpg#thumbnail)](https://en.wikipedia.org/wiki/Montreal)"
nyc = "[![New York City](https://upload.wikimedia.org/wikipedia/commons/f/f7/Lower_Manhattan_skyline_-_June_2017.jpg#thumbnail)](https://en.wikipedia.org/wiki/New_York_City)"

df = pd.DataFrame()
df["id"] = range(1, 10)
df["country"] =  np.random.choice(["USA", "Canada"], df.shape[0])
df["image"] =  np.random.choice([seattle, montreal, nyc], df.shape[0])

def generate_data_table(dataframe, allowed_columns=[]):
    columns_config = []
    for column in allowed_columns:

        if column in dataframe.columns:
                if column == "image":
                    columns_config.append({"name": column, "id": column,  "deletable": 'first', 'editable': True, "presentation": "markdown"  })
                else:
                    columns_config.append({"name": column, "id": column,  "deletable": 'first', 'editable': True})
        else:
            columns_config.append({"name": column, "id": column,  "deletable": 'first', 'clearable': True, 'editable': True})

    return dash_table.DataTable(
        list(map(lambda v: { **v}, dataframe.to_dict('records'))),
        columns = columns_config,
        column_selectable="multi",
        row_deletable=True,
        row_selectable="multi",
        editable=True,
        style_cell={'textAlign': 'left', 'padding': "20px"},
        style_cell_conditional=[
            {"if": {"column_id": "image"}, "width": "200px", 'padding': '5px'}
        ],
 
    )

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''


app.layout = html.Div([
    # dcc.Markdown(children=markdown_text, className="card"),
    # html.Div([
    #         html.Form(
    #         [
    #             html.P("state	total exports	beef	pork	poultry	dairy	fruits fresh	fruits proc	total fruits	veggies fresh	veggies proc	total veggies	corn	wheat	cotton"),
    #             # html.Input()
    #             html.Button("Adicionar")
    #         ])
    #     ],
    #     className="card"    
    # ),
    html.Div(
        [
            html.H1("Cities and Contries"),
            generate_data_table(df, [ "id", "image", "country"]),
            html.Form(
            [
                html.Button("Treinar Modelo", className="btn")
            ])
        ],
        className="card"
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)


