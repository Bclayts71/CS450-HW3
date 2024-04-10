import dash
from dash import dcc, html, Input,Output,State
import seaborn as sns
import plotly.express as px
from dash.exceptions import PreventUpdate
import io
import base64
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# Load the my_df dataset from Seaborn
my_df = sns.load_dataset("tips")

model_pipeline=None
# Get the categorical columns
categorical_columns = my_df.select_dtypes(include=['object', 'category']).columns.tolist()
# Get the numeric columns
numeric_columns = my_df.select_dtypes(include=['number']).columns.tolist()

target_dropdown=html.Div(className="dropdown2_div",children=[html.P("Select Target: "),dcc.Dropdown(id='target_dropdown_id',options=numeric_columns, value=None,style=dict(width=150,marginLeft=2))])

# radio_items=dcc.RadioItems(id='cat_radio_items_id',options=categorical_columns, value=None, inline=True)

check_list=dcc.Checklist(id="row4_checklist",options=my_df.columns,value=[],inline=True)

app = dash.Dash(__name__)

app.layout = html.Div(className="parent_container", children=[
    html.Div(id="row1", children=[dcc.Upload(id='upload-data', children='Upload File')]),
    html.Div(id="row2", children=[target_dropdown]),
    html.Div(id="row3", children=[
        html.Div(className="row3_child1", children=[
            html.Div(dcc.RadioItems(id='cat_radio_items_id',options=categorical_columns, value=None, inline=True)),  
            html.Div(dcc.Graph(id='graph1'),style=dict(width="100%"))
        ]),
        html.Div(className="row3_child2", children=[  
            html.Div(dcc.Graph(id='graph2'), style=dict(width="100%",marginTop="38px"))
        ]),
    ]),
    html.Div(id="row4", children=[
        html.Div(id="row4_child1", children=[check_list,html.Button('Train', id='train_button_id', n_clicks=0)])
    ]),
    html.Div(id="row5", children=[""]),

    html.Div(id="row6", children=[
        dcc.Input(id="row5_input_id",type="text",placeholder="input type"),
        html.Button('Predict', id='predict_button_id', n_clicks=0),
        html.P(id="predition_holder",children=[""])
    ]),
])

# Callback to handle upload
@app.callback([Output("cat_radio_items_id","options"),Output("target_dropdown_id","options"),Output("row4_checklist","options")],
              Input('upload-data', 'contents'))

def update_output(contents):
    global my_df
    if(contents is not None):
        content_string = contents.split(',')[1]
        decoded = base64.b64decode(content_string)
        my_df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))).dropna()
        # Get the categorical columns
        categorical_columns = my_df.select_dtypes(include=['object', 'category']).columns.tolist()
        # Get the numeric columns
        numeric_columns = my_df.select_dtypes(include=['number']).columns.tolist()
        return categorical_columns,numeric_columns,my_df.columns
    else:
        raise PreventUpdate

@app.callback(Output('graph1', 'figure'),[Input('cat_radio_items_id', 'value'),State('target_dropdown_id', 'value')])
def update_graph1(cat_dropdown_val, target_variable):
    if(target_variable is not None and cat_dropdown_val is not None):
        avg_y = my_df.groupby(cat_dropdown_val)[target_variable].mean().reset_index()        
        figure = px.bar(avg_y, x=cat_dropdown_val, y=target_variable,text_auto=True)
        figure.update_layout(plot_bgcolor="#f7f7f7")
        figure.update_yaxes(title_text=target_variable+' (average)')
        figure.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
        return figure
    else:
        raise PreventUpdate
    
@app.callback(Output('graph2', 'figure'),[Input('target_dropdown_id', 'value')])
def update_graph2(target_variable):
    if (target_variable is not None):
        numeric_columns = my_df.select_dtypes(include=['number']).columns.tolist()
        corr_matrix=round(my_df[numeric_columns].corr(),2)
        #fig3=px.imshow(corr_matrix)
        corr_bar_data=corr_matrix[target_variable].drop(target_variable)
        fig2=px.bar(x=corr_bar_data.index, y=corr_bar_data.values,text_auto=True)
        return fig2
    else:
        return {}

# store the features and the target
@app.callback(Output('row5', 'children'),[State('target_dropdown_id', 'value'),State("row4_checklist","value"),Input('train_button_id', 'n_clicks')])
def train_model(target,selected_features, n_clicks):
    if(target is None or len(selected_features) == 0):
        raise PreventUpdate
    global model_pipeline
    X = my_df[selected_features]
    y = my_df[target]
    selected_categorical_features = my_df[selected_features].select_dtypes(include=['object', 'category']).columns.tolist()
    selected_numerical_features =my_df[selected_features].select_dtypes(include=['number']).columns.tolist()

    numeric_transformer = Pipeline(steps=[('scaler', MinMaxScaler())]) #Define the preprocessing pipeline for numerical features
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))]) #Define the preprocessing pipeline for categorical features
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, selected_numerical_features),('cat', categorical_transformer, selected_categorical_features)]) # Combine preprocessing steps
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),('regressor', LinearRegression())]) # Create the complete pipeline

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_pipeline.fit(X_train, y_train) #Train the model
    y_pred = model_pipeline.predict(X_test) #Predict on the test set
    r2 = r2_score(y_test, y_pred) #Evaluate the model
    return "The R2 score is: "+str(round(r2,2))

@app.callback(Output('row5_input_id', 'placeholder'),[Input("row4_checklist","value")])
def change_input_placeholder(selected_features):
    if(len(selected_features) == 0):
        raise PreventUpdate
    else:
        return ",".join(selected_features)

# store the features and the target
@app.callback(Output('predition_holder', 'children'),[State("row4_checklist","value"),State("row5_input_id","value"),Input('predict_button_id', 'n_clicks')])
def predict(checklist_items,input_val,n_clicks):
    if (input_val is None):
        raise PreventUpdate

    df=pd.DataFrame([input_val.split(",")], columns=checklist_items)
    return "prediction is: " + str(round(model_pipeline.predict(df)[0],2))

if __name__ == '__main__':
    app.run_server(debug=True,port=5001)