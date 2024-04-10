import dash
from dash import dcc, html, Input,Output
import plotly.express as px
import pandas as pd

csv_file_path = "c:\\Users\\bren5\\OneDrive\\Documents\\CS450 Apps\\ProjectApp\\Rates_of_Laboratory-Confirmed_RSV__COVID-19__and_Flu_Hospitalizations_from_the_RESP-NET_Surveillance_Systems_20240323.csv"
df = pd.read_csv(csv_file_path)
app = dash.Dash(__name__)


radio1=html.Div(className="child1_1_1",children=[dcc.RadioItems(id='radio', options=["Weekly Rate", "Cumulative Rate"], value="", inline=True)])
radio2=html.Div(className="child2_1_1",children=[dcc.RadioItems(id='radio2', options=["Weekly Rate", "Cumulative Rate"], value="", inline=True)])
radio3=html.Div(className="child3_1_1",children=[dcc.RadioItems(id='radio3', options=["Weekly Rate", "Cumulative Rate"], value="", inline=True)])
radio4=html.Div(className="child4_1_1",children=[dcc.RadioItems(id='radio4', options=["Weekly Rate", "Cumulative Rate"], value="", inline=True)])

cov = df[df[df.columns[0]] == 'FluSurv-NET']
dropDownOptions = cov[cov.columns[2]].unique()
dropdown1=html.Div(className="child1_1_2",children=[dcc.Dropdown(id='x-axis-dropdown',options=dropDownOptions[1:], value="")])

cov = df[df[df.columns[0]] == 'COVID-NET']
dropDownOptions = cov[cov.columns[2]].unique()
dropdown2=html.Div(className="child2_1_2",children=[dcc.Dropdown(id='x-axis-dropdown2',options=dropDownOptions, value="")])

cov = df[df[df.columns[0]] == 'RSV-NET']
dropDownOptions = cov[cov.columns[2]].unique()
dropdown3=html.Div(className="child3_1_2",children=[dcc.Dropdown(id='x-axis-dropdown3',options=dropDownOptions[1:], value="")])

cov = df[df[df.columns[0]] == 'COVID-NET']
dropDownOptions = cov[cov.columns[2]].unique()
dropdown4=html.Div(className="child4_1_2",children=[dcc.Dropdown(id='x-axis-dropdown4',options=dropDownOptions, value="")])

app.layout = html.Div(className="parent", children=[
    html.Div(className="child1",children=[html.Div(radio1, className="child1_1"),html.Div(dropdown1, className="child1_3"),html.Div(dcc.Graph(id='graph1'), className="child1_2")]),
    html.Div(className="child2",children=[html.Div(radio2, className="child2_1"),html.Div(dropdown2, className="child2_3"),html.Div(dcc.Graph(id='graph2'), className="child2_2")]),
    html.Div(className="child3",children=[html.Div(radio3, className="child3_1"),html.Div(dropdown3, className="child3_3"),html.Div(dcc.Graph(id='graph3'), className="child3_2")]),
    html.Div(className="child4",children=[html.Div(radio4, className="child4_1"),html.Div(dropdown4, className="child4_3"),html.Div(dcc.Graph(id='graph4'), className="child4_2")])
])


@app.callback(
    Output('graph1', 'figure'),
    [Input('radio', 'value'),Input('x-axis-dropdown', 'value')]
)
def update_graph(input_value, dropdown_value):    
    if(len(input_value)==0 or len(str(dropdown_value))==0):
       return {}
    filtered_df = df[(df[df.columns[0]] == 'FluSurv-NET') & (((df[df.columns[2]] == (dropdown_value-1)) & (df[df.columns[3]] > 39)) | ((df[df.columns[2]] == dropdown_value) & (df[df.columns[3]] < 39))) & (df[df.columns[4]] == 'Overall') & (df[df.columns[5]] == 'Overall') & (df[df.columns[6]] == 'Overall') & (df[df.columns[7]] == 'Overall')]
    figure = px.line(filtered_df, x='Week Ending Date', y=input_value, title='Flu Hospitalization Rate per 100,000')
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_xaxes(title_text='Month')
    figure.update_yaxes(title_text=input_value)
    return figure


@app.callback(
    Output('graph2', 'figure'),
    [Input('radio2', 'value'),Input('x-axis-dropdown2', 'value')]
)
def update_graph(input_value, dropdown_value):    
    if(len(input_value)==0 or len(str(dropdown_value))==0):
       return {}
    filtered_df = df[(df[df.columns[0]] == 'COVID-NET') & (((df[df.columns[2]] == (dropdown_value-1)) & (df[df.columns[3]] > 39)) | ((df[df.columns[2]] == dropdown_value) & (df[df.columns[3]] < 39))) & (df[df.columns[4]] == 'Overall') & (df[df.columns[5]] == 'Overall') & (df[df.columns[6]] == 'Overall') & (df[df.columns[7]] == 'Overall')]
    figure = px.line(filtered_df, x='Week Ending Date', y=input_value, title='Covid Hospitalization Rate per 100,000')
    figure.update_layout(
        xaxis=dict(
            showticklabels=False,
            showline=False,
            zeroline=False,
            showgrid=False
        ),
        yaxis=dict(
            showticklabels=False,
            showline=False,
            zeroline=False,
            showgrid=False
        )
    )
    return figure



@app.callback(
    Output('graph3', 'figure'),
    [Input('radio3', 'value'),Input('x-axis-dropdown3', 'value')]
)
def update_graph(input_value, dropdown_value):    
    if(len(input_value)==0 or len(str(dropdown_value))==0):
       return {}
    filtered_df = df[(df[df.columns[0]] == 'RSV-NET') & (((df[df.columns[2]] == (dropdown_value-1)) & (df[df.columns[3]] > 39)) | ((df[df.columns[2]] == dropdown_value) & (df[df.columns[3]] < 39))) & (df[df.columns[4]] == 'Overall') & (df[df.columns[5]] == 'Overall') & (df[df.columns[6]] == 'Overall') & (df[df.columns[7]] == 'Overall')]
    figure = px.line(filtered_df, x='Week Ending Date', y=input_value, title='RSV Hospitalization Rate per 100,000')
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_xaxes(title_text='Month')
    figure.update_yaxes(title_text=input_value)
    return figure

@app.callback(
    Output('graph4', 'figure'),
    [Input('radio4', 'value'),Input('x-axis-dropdown4', 'value')]
)
def update_graph(input_value, dropdown_value):    
    if(len(input_value)==0 or len(str(dropdown_value))==0):
       return {}
    filtered_df = df[(df[df.columns[0]] != 'Combined')&(((df[df.columns[2]] == (dropdown_value-1)) & (df[df.columns[3]] > 39)) | ((df[df.columns[2]] == dropdown_value) & (df[df.columns[3]] < 39))) & (df[df.columns[4]] == 'Overall') & (df[df.columns[5]] == 'Overall') & (df[df.columns[6]] == 'Overall') & (df[df.columns[7]] == 'Overall')]
    figure=px.bar(filtered_df, x='Week Ending Date', y=input_value, color='Surveillance Network', barmode='group')
    #figure=px.bar(filtered_df, x='Week Ending Date', y=input_value, color='Surveillance Network')
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_xaxes(title_text='Month')
    figure.update_yaxes(title_text=input_value)
    return figure



if __name__ == '__main__':
    app.run_server(debug=True)