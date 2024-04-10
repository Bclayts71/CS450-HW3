import dash
from dash import dcc, html, Input,Output, dash_table
import plotly.express as px
import pandas as pd

csv_file_path = "c:\\Users\\bren5\\OneDrive\\Documents\\CS450 Apps\\src\\ProcessedTweets.csv"
df = pd.read_csv(csv_file_path)
app = dash.Dash(__name__)
server = app.server


dropDownOptions = df['Month'].unique()

slider1Min = df['Sentiment'].min()
slider1Max = df['Sentiment'].max()

slider2Min = df['Subjectivity'].min()
slider2Max = df['Subjectivity'].max()

dropdown1=html.Div(className="child1_1_1",children=[html.Div("Month", style={'margin-right': '.5vw', 'margin-top': '1.5vh'}),dcc.Dropdown(id='month-dropdown',options=dropDownOptions, value=dropDownOptions[0], style={'margin-right': '2vw', 'margin-top': '1%'})])
slider1=html.Div(className="child1_1_2",children=[html.Div("Sentiment Score", style={'margin-right': '.5vw', 'margin-top': '3%'}),html.Div(dcc.RangeSlider(slider1Min, slider1Max, value=[slider1Min,slider1Max], marks={int(slider1Min):str(slider1Min), int(slider1Max):str(slider1Max)}, id='slider'), style={'margin-top': '1VH', 'margin-right': '1vw', 'width': '10VW'})])
slider2=html.Div(className="child1_1_3",children=[html.Div("Subjectivity Score", style={'margin-right': '.5vw', 'margin-top': '3%'}),html.Div(dcc.RangeSlider(slider2Min, slider2Max, value=[slider2Min,slider2Max], marks={int(slider2Min):str(slider2Min), int(slider2Max):str(slider2Max)}, id='slider2') , style={'margin-top': '1VH', 'margin-right': '1vw', 'width': '10VW'})])
app.layout = html.Div(className="parent", children=[
    html.Div(className="child1",children=[html.Div(dropdown1, className="child1_1"),html.Div(slider1, className="child1_2"),html.Div(slider2, className="child1_3")]),
    html.Div(className="child2",children=[html.Div(dcc.Graph(id='graph1'), className="child1_4")]),
    html.Div(className="child3",children=[html.Div(id='table-container', style={'width': '98vw'})])
])
@app.callback(
    Output('graph1', 'figure'),
    [Input('slider', 'value'),Input('slider2', 'value'), Input('month-dropdown', 'value')]
)
def update_output(sentiment, subjectivity, month):
    filtered_df = df[(df['Month'] == month) & (df['Sentiment'] > sentiment[0]) & (df['Subjectivity'] > subjectivity[0]) & (df['Sentiment'] < sentiment[1]) & (df['Subjectivity'] < subjectivity[1])]
    figure = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', color_discrete_sequence=['grey'])
    figure.update_layout(
        modebar=dict(orientation='v'),
        xaxis=dict(
            showticklabels=False,
            title='',
            showgrid=False
        ),
        yaxis=dict(
            showticklabels=False,
            title='',
            showgrid=False
        )
    )
    return figure

@app.callback(
    Output('table-container', 'children'),
    [Input('graph1', 'selectedData'),Input('slider', 'value'),Input('slider2', 'value'), Input('month-dropdown', 'value')]
)
def update_table(selected_data, sentiment, subjectivity, month):
    if selected_data is None:
        return dash_table.DataTable(
        style_header={'textAlign': 'center'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'center'
        },
        columns=[{"name": "RawTweet", "id": "RawTweet"}],
        )
    filtered_df = df[(df['Month'] == month) & (df['Sentiment'] > sentiment[0]) & (df['Subjectivity'] > subjectivity[0]) & (df['Sentiment'] < sentiment[1]) & (df['Subjectivity'] < subjectivity[1])]
    selected_indices = [point['pointIndex'] for point in selected_data['points']]
    selected_df = filtered_df.iloc[selected_indices]
    return dash_table.DataTable(
        style_header={'textAlign': 'center'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'center'
        },
        data=selected_df.to_dict('records'),
        columns=[{"name": "RawTweet", "id": "RawTweet"}],
        page_size=6
    )

    

if __name__ == '__main__':
    app.run_server(debug=True)
