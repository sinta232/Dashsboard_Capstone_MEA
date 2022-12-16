# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# 2. Create a Dash app instance
app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY],
    name = 'Dashboard Evaluation'
)

app.title = 'BC Dash Analytics'


# Jumbotron
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Supervisory Evaluation", className="display-3"),
            html.P(
                "BC Dashboard analytics",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use this dashboard and get the insight!"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)


## --- Import Dataset GPP
dataset=pd.read_excel('validasi.xlsx')

dataset['Tanggal'] = dataset['Tanggal'].astype('datetime64')
dataset['Date'] = dataset['Tanggal'].dt.date
dataset['Day'] = dataset['Tanggal'].dt.day_name()
dataset['Hour'] = dataset['Tanggal'].dt.hour
dataset
#---- visualisasi
    ## count of validation
    ## filter nama
    ## filter objek
    ## filter tanggal
    ##-- line chart validation
G = pd.crosstab(index=dataset['Date'],
            columns='trend_validation',
            values=dataset['data'],
            aggfunc='count').reset_index()
H = px.line(
    G,
    y = 'trend_validation',
    x = 'Date',title = 'Trend of Data Deviation'
)
    ## -- bar plot rank supervisory
I = pd.crosstab(index=dataset['name'],
            columns='Count_of_supervisory',
            values=dataset['type_validation'],
            aggfunc='count').reset_index()
J = px.bar(
    I.sort_values('Count_of_supervisory').tail(10),
    x = 'Count_of_supervisory',
    y = 'name',
    title = 'Leaderboard',
    labels = {
        'Count_supervisory'
    })
    
#-- bar plot validation
# dataset1 = pd.crosstab(index=dataset['type_validation'],
#         columns='Count_Validation',
#         values=dataset['type_validation'],
#         aggfunc='count').reset_index()
        
# L = px.bar(dataset1, 
#         x='type_validation', 
#         y='Count_Validation',
#         title = 'Total of ',
#         color = 'type_validation')

    #---bar plot type object
M = pd.crosstab(index=dataset['type_object'],
            columns='Count_Object',
            values=dataset['type_object'],
            aggfunc='count').reset_index()
            
N = px.pie(M, values='Count_Object', names='type_object', hole=.3, title = 'Type of Object Deviation')

O = pd.crosstab(index=dataset['Date'],
            columns='trend_supervisory',
            values=dataset['type_validation'],
            aggfunc='count').reset_index()

            ###--

P = px.line(
    O,
    y = 'trend_supervisory',
    x = 'Date', title = 'Trend of Supervisory')


Q = pd.crosstab(index=dataset['Day'],
            columns=dataset['Hour'])
R = px.imshow(Q, title = 'Distribution of Supervisory').update_yaxes(
    categoryorder='array', 
    categoryarray= ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday', 'Saturday','Sunday'])

#---- layout
app.layout = html.Div([
    
    jumbotron,
    # row 1
    # dbc.Row([
    #     dbc.Col([
    #         dbc.Card([
    #             # dbc.CardHeader('filter name supervisory'),
    #             # dbc.CardBody(
    #             #     dcc.Dropdown(
    #             #         id='Choose_name',
    #             #         options=dataset['name'].unique(),
    #             #     ),
    #             # ),
    #         ]),
    #     ]),
    #     dbc.Col([
    #         dbc.Card([
    #         ]),
    #     ]),
    #     dbc.Col([
    #         dbc.Card([
    #             #"value 4"
    #         ]),
    #     ]),
    # ]),
    
    html.Br(),
    # row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=H),
            ]),
        ]),
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(
                    dcc.Graph(
                        figure=J),
                    label='Ranking'),
                dbc.Tab(dcc.Graph(
                        figure=P),
                        label='Trendline'),
            ]),
            ]),
        ]),
    html.Br(),

     dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=R),
            ]),
        ]),
        ]),

    html.Br(),
    # row 3
    dbc.Row([
       
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=N),
            ]),
        ]),
         dbc.Col([
            dbc.Card([
                dbc.CardHeader('Select object'),
									dbc.CardBody(
										dcc.Dropdown(
											id='list_object',
											options=dataset['type_object'].unique(),
                                            value = 'HD',
											
										),
									),
            ]),
            dcc.Graph(
                    id='plot1',
                    #figure=L,
                    ),
        ]),

    html.Br()
    ], style={
    'paddingLeft':'30px',
    'paddingRight':'30px',
    }),
    ])



## callback ranking
@app.callback(
    Output(component_id='plot1', component_property='figure'),
    Input(component_id='list_object',component_property='value'),
)

def update_plot1(object_type):
    dataset1=dataset[dataset['type_object']== object_type]
    
    dataset2 = pd.crosstab(index=dataset1['type_validation'],
            columns='Count_Validation',
            values=dataset1['type_validation'],
            aggfunc='count').reset_index()
            
    L = px.bar(dataset2, 
            x='type_validation', 
            y='Count_Validation',
            title = 'Total of True & False Each Object Deviation',
            color = 'type_validation')

    return L



# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server(debug=True)

