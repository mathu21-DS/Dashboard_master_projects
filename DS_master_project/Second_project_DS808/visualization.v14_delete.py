# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 21:34:09 2022


"""

# %%

#Create and Activate a virtual environment 
# 1. Create the env. python -m venv <directory>
# 2. Navigate to the folder by "cd C:\Users\Margrethe\dashboard1\Scripts"
# 2.2 Add in the python interpreter by add: C:\Users\Margrethe\dashboard1\Scripts
# 3. Activate in the folder by the PowerShell ".\activate" 
# 4.1 then run this file to install the packages by running requirements.txt: pip install -r "C:\Users\Margrethe\Documents\DS_3.semester\DS808 Visualisering\DS808_group\template\Range_Slider_Jakob\requirements.txt"
# 4.2.1 or  cd "C:\Users\Margrethe\Documents\DS_3.semester\DS808 Visualisering\DS808_group\template\Range_Slider_Jakob"
# 4.2.2 pip install -r requirements.txt
#then run to check that the packages have been installet: pip list

# Imports
#import dash_core_components as dcc
#import dash_html_components as html
from dash import dcc
from dash import html


#app = dash.Dash(__name__)
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import base64
import dash
#from dash import Dash, dcc, html, Input, Output, State
from dash.dependencies import Input, Output, State
from matplotlib import pyplot as plt
import plotly.io as pio
import plotly
import json
app = dash.Dash()


# %%
# Data manegment

# Loading data

df_30 = pd.read_csv("data2/Equality_30.csv")
df1_30 = pd.read_csv("data2/Difference in equality_30.csv")

df = pd.read_csv("data2/Equality_40.csv")
df1 = pd.read_csv("data2/Difference in equality_40.csv")


# Max and minimum time for timesliders:
mintime = df['Year'].min()
maxtime = df['Year'].max()

# # image of men and women
#image_filename = 'assets/Graphite-Black-100.png'  # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
# image_filename = 'assets/woman-128.1.png'  # replace with your own image
# encoded_image2 = base64.b64encode(open(image_filename, 'rb').read())

#################################

# Dataframe preperment

#Data for earnings difference
df_d = df_30[df_30['Sector']=='All sectors']
df_d = df_d[df_d['Salary Group'] == 'All forms of pay']
df_d = df_d[df_d['Employment Group'] == 'Employees']
df_d = df_d[(df_d['Components'] == 'STANDARDIZED HOURLY EARNINGS') |( df_d['Components'] == 'STANDARDIZED MONTHLY EARNINGS')]
df_d = df_d.drop(columns=['Salary Group', 'Employment Group','Sector'])
df_d = df_d.reset_index(drop=True)

# Preparer data for sector

def sector_means(df1_30):

    df_sec = []

    for i in ['STANDARDIZED MONTHLY EARNINGS', 'STANDARDIZED MONTHLY EARNINGS']:
        df = df1_30[(df1_30['Sector'] == 'All sectors') | (df1_30['Sector'] == 'General government') | (
            df1_30['Sector'] == 'Corporations and organizations')]
        df = df[df['Salary Group'] == 'All forms of pay']
        df = df[df['Employment Group'] == 'Employees']
        df = df[df['Components'] == i]
        df = df.drop(columns=['Salary Group', 'Employment Group',
                     'Components', 'Difference', 'Contents Men', 'Contents Women'])
        df = df.reset_index(drop=True)
        df = df.replace(['All sectors', 'General government', 'Corporations and organizations'],
                        ['All Sectors', 'Public Sector', 'Private Sector'])
        df_sec.append(df)
    return df_sec


df_sec = sector_means(df1_30)


# Preparer data for scatterplot:
df_scat = df1[df1['Sector'] == "All sectors"]
df_scat = df_scat[df_scat['Salary Group'] == "All forms of pay"]
df_scat = df_scat[df_scat['Employment Group'] == "Employees"]
df_scat = df_scat.sort_values(by=['Industry'], ascending=False)
df_scat = df_scat.drop(columns=['Sector', 'Salary Group', 'Employment Group'])

# Employment barplot
df_e = df1[df1['Components'] ==
            'Number of fulltime employees in the earnings statistics']
df_e = df_e[df_e['Salary Group'] == "All forms of pay"]
df_e = df_e[df_e['Sector'] == "All sectors"]

df_e["Contents Men"].fillna(0, inplace=True)
df_e["Contents Women"].fillna(0, inplace=True)
df_e["Contents Men"]/1000
df_e["Contents Women"]/1000
df_e=df_e.drop(columns=['Sector', 'Salary Group','Components','Difference in procents',])
df_e=df_e.rename({'Contents Men':'Men', 'Contents Women':'Women',
                  'Difference':'Difference in men and women working in the industry'}, 
                 axis=1)
df_e['Procent of men in the industry']=(df_e['Men'])/(df_e['Men']+df_e['Women'])*100
df_e['Procent of women in the industry']=100
df_e['Procent of women in the industry']=df_e['Procent of women in the industry']-df_e['Procent of men in the industry']

# Difference in payment barplot

df_dif = df1[df1['Components'] != 'Lower quartile, standardized earnings']
df_dif = df_dif[df_dif['Components'] != 'Median, standardized hourly earnings']
df_dif = df_dif[df_dif['Components'] !=
            'Upper quartile, standardized hourly earnings']
df_dif = df_dif[df_dif['Components'] != 'STANDARDIZED MONTHLY EARNINGS']
df_dif = df_dif[df_dif['Components'] != 'STANDARDIZED HOURLY EARNINGS']
df_dif = df_dif[df_dif['Components'] !=
            'Number of fulltime employees in the earnings statistics']
df_dif = df_dif[df_dif['Employment Group'] == 'Employees']
df_dif = df_dif[df_dif['Salary Group'] == "All forms of pay"]
df_dif = df_dif[df_dif['Sector'] == "All sectors"]

df_dif["Contents Men"].fillna(0, inplace=True)
df_dif["Contents Women"].fillna(0, inplace=True)
df_dif=df_dif.drop(columns=['Sector', 'Salary Group','Employment Group','Difference in procents','Difference'])
df_dif=df_dif.rename({'Components':'Earnings types per standard hour','Contents Men':"Men's earning", 'Contents Women':"Women's earning",}, 
                 axis=1)
df_dif=df_dif.replace(['Basic earnings in DKK per standard hour','Fringe benefits in DKK per standard hour','Pension including ATP in DKK per standard hour'],
                      ['Basic earnings',"Fringe benefits",'Pension including ATP'])


#Colors
Background='rgba(00,00,00,0)' #makes it transparent
Background_html= "rgba(248,249,249,1.00)"#'rgba(00,00,00,0)'#'rgb(215 215 215)'#color the background
Plot_back='rgba(0,0,0,0)'
Color_women='rgba(178,0,147,1)' #'rgba(178,0,147,255)'
Color_men='rgba(1,175,175,1)'
Color_user = 'rgba(254,162,2,255)'
Color_line = 'black'
text_font= 'Arial, Helvetica, sans-serif'   # test evt med 'Courier New, monospace' det gøres meget tydeligt
text_color = "rgba(31,34,34,1.00)" # test evt med 'RebeccaPurple'
size_text = 12
size_titleheadline = 17
Background_plots = 'rgba(171, 168, 170, 0.41)'
scatter_hover_color_line = 'rgb(220,220,220)'

# %%
# Creating the HTML space
app.layout = html.Div(children=[
    
    html.H1(children='Gender pay gap between Men and Women in Denmark',
            style={'textAlign': 'center'}),
    
    html.H2(children='From year 2013 to 2020',
            style={'textAlign': 'center'}),
    

    html.Div([
        html.Div(children=[
            # html.H1(children='Time slider',
            # style={'textAlign': 'center'}),
            
            html.Div(children='''
        			Select a time period:
    					''',
               style={'margin-left':'5%'}
            ),

            html.Div(children=[
                dcc.RangeSlider(
                    id='time-slider',
                    min=mintime,
                    max=maxtime,
                    step=1,
                    value=[mintime, maxtime],
                    marks={i: str(i) for i in range(mintime, maxtime+1, 1)},
                ),
            ],
                style={'margin-left':'5%'}
            ),
            
            html.H4('',
                    style={'textAlign':'center'}
            ),
            
            html.Div(children='''
        			Select monthly or hourly pay:
    					''',
                    style={'margin-left':'5%'}
            ),
            
            html.Div([
                dcc.RadioItems(
                    options=[{"label": "Hourly wage", "value": "STANDARDIZED HOURLY EARNINGS"},
                             {"label": "Monthly wage",
                                 "value": "STANDARDIZED MONTHLY EARNINGS"}
                             ],
                    value="STANDARDIZED HOURLY EARNINGS",  # Default
                    id='components',
                    labelStyle={'display': 'block'},
                    #style={ 'textAlign':'center'}
                    # style={'display': 'inline-block',
                    #        'vertical-align': 'top', 'margin': '10%','textAlign':'left'}
                )
            ],
                style={'margin-left':'5%'}    
            ),

            # link to understand how the rangeslider work on the other callbacks. Se under title "Example 1 - Storing Data in the Browser with dcc.Store": https://dash.plotly.com/sharing-data-between-callbacks
            # the id which store the years range to be added into the other callbacks fx.
            dcc.Store(id='intermediate-value'),
            dcc.Store(id='intermediate-value2'),  # hourly or monthly
            dcc.Store(id='intermediate-value3'),  # chose of one branch
            # choose upper, median, upper, hourly or monthly component
            #dcc.Store(id='intermediate-value4'),
            # choose men or woman to the linechart
            dcc.Store(id='intermediate-value5'),
            dcc.Store(id='intermediate-value6'),  # indput the user sector
            # indput the user salary scatterplot
            dcc.Store(id='intermediate-value7'),
            # chose branch til scatterplot
            dcc.Store(id='intermediate-value8'),


            # Figures of Men and Woman
            html.H3('Overview of the average pay gap',
                    style={'textAlign':'center'}
            ),
            html.Div(id="payGapBarchart"), #jakob
            # html.Div(children=[
            #     html.Div(children=[
            #         html.Img(
            #             src='data:image/jpg;base64,{}'.format(encoded_image.decode()),),
            #         html.Div(id='output-container-range-slider-men', style={'textAlign':'center'})
            #     ],
            #                  style={ 'flex': 1,'textAlign': 'center'}
            #     ),
            #     html.Div(children=[
            #         html.Img(
            #             src='data:image/png;base64,{}'.format(encoded_image2.decode()),),
            #         html.Div(id='output-container-range-slider-women', style={'textAlign':'center'})
            #     ],
            #         style={ 'flex': 1,'textAlign': 'center'}
            #     ),
            # ],
            #          style={'display': 'flex', 'flex-direction': 'row'}
            # ),
            
            html.Div(children=[
                html.Div(children=[
                    html.H4('On average, women are earning '),
                    html.H3(
                        id='average_pay_difference',
                    ),
                    html.H4('less then men.')
                ],
                    style={'vertical-align': 'top','textAlign':'center'}
                ),
                
            ],
              # style={'textAlign':'center'}  
            ),
            # Box of inputs
            html.Div([
                html.H3('Compare your own wage to the data',
                        style={'textAlign':'center'}
                ),
                
                html.Div(children=[
                    html.Div([
                        html.Div(children='''
            			     Select gender:
        				     '''
                                 ),
                        dcc.RadioItems(
                            options=[{"label": "Woman", "value": "women"},  # chance to another value when chosing female or male
                                     {"label": "Man", "value": "men"}
                                     ],  # ["STANDARDIZED MONTHLY EARNINGS"], ["STANDARDIZED MONTHLY EARNINGS"]
                            value="women",
                            id='chose_gender',
                            labelStyle={'display': 'block'},
                            style={ 'display': 'inline-block',
                                   'vertical-align': 'top',  'margin-bottom': '2%'}
                        )
                    ],
                        style={ 'flex': 1, 'margin-left': '5%',}
                    ),
                    html.Div([
                        html.Div(children='''
             			    Select sector:
         					'''
                                 ),
    
    
                        dcc.RadioItems(
                            options=[{"label": "All sectors", "value": "All sectors"},  # chance to another value when chosing female or male
                                      {"label": "Public sector",
                                      "value": "General government"},
                                      {"label": "Private sector",
                                      "value": "Corporations and organizations"}
                                      ],
                            #  options=[
                            #      {
                            #      "label": html.Div(
                            #          [
                            #              html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), height=30),
                            #              html.Div("All sectors"),
                            #          ],
                            #          style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                            #      ),
                            #      "value": "All sectors",
                            #  },
                            #  {
                            #      "label": html.Div(
                            #          [
                            #              html.Img(src="assets/red-100.png", height=30),
                            #              html.Div("Public sector", style={'font-size': 15, 'padding-left': 10}),
                            #          ],
                            #          style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                            #      ),
                            #      "value": "General government",
                            #  },
                            #  {
                            #      "label": html.Div(
                            #          [
                            #              html.Img(src="assets/blue-100.png", height=30),
                            #              html.Div("Private sector", style={'font-size': 15, 'padding-left': 10}),
                            #          ],
                            #          style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                            #      ),
                            #      "value": "Corporations and organizations",
                            #  },
                            # ],
                            value="All sectors",
                             id='chose_sector',
                             labelStyle={'display': 'block'},
                             style={'display': 'inline-block',
                                    'vertical-align': 'top','margin-bottom': '2%'}
                        )
                    ],
                        style={ 'flex': 1,}        
                    ),
                ],
                    style={'display': 'flex', 'flex-direction': 'row'}            
                ),
                # where the salary box is added in
                html.H4('',
                        style={'textAlign':'center'}
                ),
                
                html.Div(id="container", children=[]),
                
                html.H4('',
                        style={'textAlign':'center'}
                ),
                
                html.Div([
                    html.Label(['Select your industry:'],
                    ),
                    dcc.Dropdown(
    
                        id='your_industry',
                        options=[{"label": x, "value": x}
                                 for x in sorted(list(df1["Industry"].unique()))],
                        value='Accommodation and food service activities',
                        style={'margin-top': '5%'}
                    )
                ],
                    style={'margin': '5%'},    
                ),
                html.Label(['Your input will be displayed in this orange color'],
                           style={'margin': '8%', "color": Color_user,  "font-size": 15},
                    ),
                html.H4('',
                        style={'textAlign':'center'}
                ),
            
            ],
                    style={'border': '2px black solid', 'margin': '40px 0px 40px 0px'} #margin top margin, right margin is 50px, bottom margin, left margin
            ),
            
            html.H4('',
                    style={'textAlign':'center'}
            ),
            html.H3('''
                    Explore different industries
                    ''',
                    style={'textAlign':'center'}),
            html.Div(children=['''
                Sort by:                        
                '''
            
            ],style={'margin-left':'5%'}),
            
            dcc.RadioItems(
                # options = [{"label": x, "value": x} for x in df["Components"].unique()], ######################when using all unique values in the column  Components
                options=[{"label": "Alphabetical", "value": 1},  # Or costumize the labels ourself
                         {"label": "Lowest difference", "value": 0},
                         {"label": "Highest difference", "value": 2},
                         ],  # ["STANDARDIZED MONTHLY EARNINGS"], ["STANDARDIZED MONTHLY EARNINGS"]
                value=1,  # when beginning the code to run this value will be shown in the dropdown
                # multi=False,

                id='explore_scatter',
                # inline=True
                style={'vertical-align': 'top', 'margin': '5%'},
                labelStyle={'display': 'block'}
            ),
            
            html.H4('',
                    style={'textAlign':'center'}
            ),
            
            html.Div([
                html.Label(['Insights into one industry:'],
                           #style={'font-weight': 'bold'}
                           ),
                dcc.Dropdown(

                    id='industry_raditem',
                    options=[{"label": x, "value": x}
                             for x in sorted(list(df1["Industry"].unique()))],
                    value='Accommodation and food service activities',
                    style={'margin-top':'5%'}
                ),
            ],
                style={'margin':'5%'}
            ),
            
            html.H4('',
                    style={'textAlign':'center'}
            ),

        ], 
            style={ 'flex': 1},
        ),

        # Picture of sector graphs
        html.Div(children=[
            html.Div(children=[
                html.Div([
                    dcc.Graph(
                        id='graph1', style={'width' : '100','backgroundColor':Background}
                    ),
                ]),
            ]),
            html.Div([
                dcc.Graph(
                    id='graph3', style={'width': '100', 'height': '1000px','backgroundColor':Background}
                )
            ]),
        ],
            style={'flex': 4},
        ),
    ],

        style={'display': 'flex', 'flex-direction': 'row'},
    ),

    html.Div([
        html.Div([
            dcc.Graph(
                id='emp_g_graph',
                style={'width': '33', 'height': '350px', 'backgroundColor':Background}
            )
        ],
            style={'padding': 0, 'flex': 1}
        ),
        html.Div([
            dcc.Graph(
                id='bpb_g_graph',
                style={'width': '33', 'height': '350px', 'backgroundColor':Background}
            )
        ],
            style={'padding': 0, 'flex': 1}
        )
    ],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    html.Div([
        html.Div([
            dcc.Graph(
                id='overtime_graph',
                style={'width': '33', 'height': '550px', 'backgroundColor':Background}
            )
        ]),
    ],)
], 
    #style={'backgroundColor':Background, 'title_font_family':"Times New Roman"} 
    style={'backgroundColor':Background_html, 'font-family': text_font,
           #"background-font":text_color
           } #change the texttype on the baggrund and not on the graphs
)

# App callback


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='time-slider', component_property='value')
)
def years_output(years_value):
    return years_value


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value2'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='components', component_property='value')
)
# it the one saving the choosen Component in the dropdown
def components_output(components_value):
    return components_value


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value5'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='chose_gender', component_property='value')
)
def gender_output(gender_value):  # it the one saving the choosen Component in the dropdown
    return gender_value


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value6'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='chose_sector', component_property='value')
)
def sector_output(sector_value):  # it the one saving the choosen Component in the dropdown
    return sector_value


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value7'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='chose_salary', component_property='value')
)
def salary_output(salary_value):  # it the one saving the choosen Component in the dropdown
    return salary_value


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value8'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='your_industry', component_property='value')
)
# it the one saving the choosen Component in the dropdown
def industry_output(industry_value):
    return industry_value


@app.callback(
    Output('container', 'children'),
    Input('components', 'value'),
    State('container', 'children')
)
def display_graphs(n_clicks, div_children):

    if n_clicks == "STANDARDIZED HOURLY EARNINGS":

        new_child = html.Div([
            html.Label(['Select your hourly wage:'],
                       style={'margin': '5%','margin-bottom': '2%','margin-right':'0%' }),
            html.Div(children=[
                dcc.Input(
                    placeholder='Enter your salary...',
                    type='number',
                    value=0,
                    id="chose_salary",
                    min=0,
                    max=1500,
                    style={'flex':2,'margin':'5%'}),
                html.Div('DKK', style={'flex':1,'margin':'5%','margin-left':'0%'})
            ],
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
        ]),
        return new_child
    elif n_clicks == "STANDARDIZED MONTHLY EARNINGS":
        new_child = html.Div([
            html.Label(['Select your monthly wage:'],
                       style={'margin': '5%','margin-bottom': '2%','margin-right':'0%' }),
            html.Div(children=[
                dcc.Input(
                    placeholder='Enter your salary...',
                    type='number',
                    value=0,
                    id="chose_salary",
                    min=0,
                    max=5000000,
                    style={'flex':2,'margin':'5%'}),
                html.Div('DKK', style={'flex':1,'margin':'5%','margin-left':'0%'})
            ],
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
        ]),
        return new_child


# @app.callback(
#     # it have to be written children or else the output list won't show
#     Output(component_id=('output-container-range-slider-men'),
#            component_property=('children')),
#     # the value is connected to the input which the input is is connected to the layout
#     Input(component_id='intermediate-value', component_property='data'),
#     Input(component_id='intermediate-value2', component_property='data')
# )
# def update_output_div(input_value, components1):
#     #
#     # get each value from the rangeslide list
#     dff = df_d[(df_d["Year"] >= input_value[0]) & (df_d["Year"] <= input_value[1])]

#     # it make sure to filter out all values not being MONTHLY or TIMELY
#     dff = dff[dff.Components == components1]

#     dff = dff.groupby(["Gender"])["Contents"].mean()

#     if components1 == "STANDARDIZED HOURLY EARNINGS":
#         return html.Div(children=[
#                 html.Div('{} DKK'.format(int(dff.iloc[1]))),
#                 html.Div('per hour.')
#                 ])
#     else:
#         return html.Div(children=[
#                 html.Div('{} DKK'.format(int(dff.iloc[1]))),
#                 html.Div('per month.')
#                 ])
#jakobs kode, hvor iconerne skifter størrelse
@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('payGapBarchart'),
           component_property=('children')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='intermediate-value', component_property='data'),
    Input(component_id='intermediate-value2', component_property='data')
)
def update_output_div(input_value, components1):
    #
    # get each value from the rangeslide list
    dff = df_d[(df_d["Year"] >= input_value[0]) & (df_d["Year"] <= input_value[1])]

    # it make sure to filter out all values not being MONTHLY or TIMELY
    dff = dff[dff.Components == components1]

    grouped = dff.groupby(["Gender"])["Contents"]


    meanValues = grouped.mean()
    #maxValues = grouped.max()
    #########################################################################################################
        #########################################################################################################
    #########################################################################################################
    #########################################################################################################
    if components1 == "STANDARDIZED HOURLY EARNINGS":
        value = int(meanValues.iloc[1])
        value_h = int(meanValues.iloc[1])
    else:
        value = int(meanValues.iloc[1]/160.33)
        value_h = int(meanValues.iloc[1])
    
    if components1 == "STANDARDIZED HOURLY EARNINGS":
        secondValue = int(meanValues.iloc[2])
        secondValue_m = int(meanValues.iloc[2])
    else:
        secondValue = int(meanValues.iloc[2]/160.33)#quation from dst: Standardberegnede timefortjeneste * 160,33 :)
        secondValue_m = int(meanValues.iloc[2])
    #########################################################################################################
    #########################################################################################################
    #########################################################################################################
    explanation = ""
    
    if components1 == "STANDARDIZED HOURLY EARNINGS":
        explanation = 'per hour.'
    else:
        explanation = 'per month.'
    
    return html.Div([
        html.Div([
            html.Div([html.Img(
                        src='assets/men-400x939.png', style={"height": "100%"})
                ],style={"height": '{}px'.format(int(value)), "width": "50px", "margin-right": "20px", "display": "inline-block"}),
            html.Div(children=[                    
                html.Div('{} DKK'.format(value_h), style={"margin-left": "30px"}), #ændret til v10
                    html.Div(explanation, style={"margin-left": "30px"})
                ])
            ], className="payGapGridItem"),
        html.Div([
            html.Div([html.Img(
                        src='assets/woman-367x800.png', style={"height": "100%"})
                ],style={"height": '{}px'.format(int(secondValue)), "width": "50px", "margin-right": "20px", "display": "inline-block"}),
            html.Div(children=[
                html.Div('{} DKK'.format(secondValue_m), style={"margin-left": "30px"}),##################################################################################################
                    html.Div(explanation, style={"margin-left": "30px"}) #ændret til v10
                ])
            ], className="payGapGridItem"),
        ], className="payGapGrid")


# @app.callback(
#     # it have to be written children or else the output list won't show
#     Output(component_id=('output-container-range-slider-women'),
#            component_property=('children')),
#     # the value is connected to the input which the input is is connected to the layout
#     Input(component_id='intermediate-value', component_property='data'),
#     Input(component_id='intermediate-value2', component_property='data')
# )
# def update_output_div2(input_value, components1):
#     #
#     # get each value from the rangeslide list
#     dff = df_d[(df_d["Year"] >= input_value[0]) & (df_d["Year"] <= input_value[1])]

#     # it make sure to filter out all values not being MONTHLY or TIMELY
#     dff = dff[dff.Components == components1]

#     dff = dff.groupby(["Gender"])["Contents"].mean()

#     if components1 == "STANDARDIZED HOURLY EARNINGS":
#         return html.Div(children=[
#                 html.Div('{} DKK'.format(int(dff.iloc[2]))),
#                 html.Div('per hour.')
#                 ])
#     else:
#         return html.Div(children=[
#                 html.Div('{} DKK'.format(int(dff.iloc[2]))),
#                 html.Div('per month.')
#                 ])

# Average difference:
@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('average_pay_difference'),
           component_property=('children')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='intermediate-value', component_property='data'),
    Input(component_id='intermediate-value2', component_property='data')
)
def update_output_difference(input_value, components1):
    #
    # get each value from the rangeslide list
    dff = df_d[(df_d["Year"] >= input_value[0]) & (df_d["Year"] <= input_value[1])]

    # it make sure to filter out all values not being MONTHLY or TIMELY
    dff = dff[dff.Components == components1]

    dff = dff.groupby(["Gender"])["Contents"].mean()

    if components1 == "STANDARDIZED HOURLY EARNINGS":
        return '{}%'.format(round(float((dff.iloc[1]-dff.iloc[2])/dff.iloc[1]*100),2))
    else:
        return '{}%'.format(round(float((dff.iloc[1]-dff.iloc[2])/dff.iloc[1]*100),2))


# Sector plot
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='intermediate-value', component_property='data'), #choose years
    Input(component_id='intermediate-value2', component_property='data'),#choose hourly or montly 
    Input(component_id='intermediate-value5', component_property='data'), #choose gender
    Input(component_id='intermediate-value6', component_property='data'), #choose sector
    Input(component_id='intermediate-value7', component_property='data'), #get the users salasy indput
)
def Sector_plot(years_chosen, components, n_gender, n_sector, user_salary):
        
    if user_salary=='0' or user_salary is None or user_salary=='' or user_salary=='NoneType':
        user_salary=0
        
    df_sector = df_sec[0]
    
    if components == 'STANDARDIZED HOURLY EARNINGS':
        df_sector = df_sec[0]
        
        if int(user_salary)==0 or int(user_salary) >= 1500:
            user_salary=0
            
    elif components == 'STANDARDIZED MONTHLY EARNINGS':
        df_sector = df_sec[1]
        
        if int(user_salary)<=5000 and int(user_salary) >= 5000000:
            user_salary=0
            
            
    year=[]
    text=[]

    for i in range(years_chosen[0],years_chosen[1]+1):
        year.append(i)
        text.append('')
    
    df_sector['Text']='Women earns %{y} % less then men in year %{x}'
    if years_chosen[0] != years_chosen[1]:
    

            
        if user_salary!=0:
            
                
            if n_gender == "women":
                
                salary_dif=pd.DataFrame()
                user_choosen = df1_30[(df1_30["Year"] >= years_chosen[0]) & (df1_30["Year"] <= years_chosen[1])]
                user_choosen = user_choosen[user_choosen["Sector"] == n_sector]
                user_choosen = user_choosen[user_choosen["Salary Group"] == "All forms of pay"]
                user_choosen = user_choosen[user_choosen["Components"] == components]
                user_choosen = user_choosen[user_choosen['Employment Group']=='Employees']
                
                salary_dif['Difference in procents'] = ((user_choosen['Contents Men']-float(user_salary))/user_choosen['Contents Men'])*100
                salary_dif['Year']=year
                salary_dif.insert(0,'Sector','User input',True)
                
            elif n_gender == "men":
                
                salary_dif=pd.DataFrame()
                user_choosen = df1_30[(df1_30["Year"] >= years_chosen[0]) & (df1_30["Year"] <= years_chosen[1])]
                user_choosen = user_choosen[user_choosen["Sector"] == n_sector]
                user_choosen = user_choosen[user_choosen["Salary Group"] == "All forms of pay"]
                user_choosen = user_choosen[user_choosen["Components"] == components]
                user_choosen = user_choosen[user_choosen['Employment Group']=='Employees']
                
                salary_dif['Difference in procents'] = ((float(user_salary)-user_choosen['Contents Women'])/float(user_salary))*100
                salary_dif['Year']=year
                salary_dif.insert(0,'Sector','User input',True)
            
            count=0
            for i in salary_dif['Difference in procents'].index:
                if salary_dif['Difference in procents'][i]<0:
                    if n_gender=='men':
                        text[count]='You are earning earn %{y} % less then the average women in year %{x}'
                    else: 
                        text[count]='You are earning earn %{y} % more then the average men in year %{x}'
                
                else:
                    if n_gender=='men':
                        text[count]='You are earning earn %{y} % more then the average women in year %{x}'
                    else: 
                        text[count]='You are earning earn %{y} % less then the average men in year %{x}'
                count=count+1
            
            salary_dif['Difference in procents']=abs(salary_dif['Difference in procents']) 
                
            salary_dif['Text']=text
        
        if user_salary!=0:
            df_sect = df_sector[(df_sector["Year"] >= years_chosen[0]) & (df_sector["Year"] <= years_chosen[1])]
            df_plot=pd.concat([df_sect,salary_dif])
            
            fig=px.line(df_plot,
                        x='Year',y='Difference in procents', 
                        color='Sector',
                        color_discrete_map={
                            'All Sectors':'black',
                            'Public Sector':'red',
                            'Private Sector':'blue',
                            'User input':Color_user },
                        #title="Difference in procent for "+str(years_chosen[0])+" to "+str(years_chosen[1])
                        )
            fig.update_layout(
            title={
            'text' : "Development of the gender pay gap for year "+str(years_chosen[0])+" to "+str(years_chosen[1]),
            'x':0.5,
            'xanchor': 'center',
        })
            
            fig.update_layout(
                legend=dict(
                    x=0.7,
                    y=1,
                    title_font_family=text_font,
                    font=dict(
                        family=text_font,
                        size=size_text,
                        color=text_color
                    ),
                    bgcolor='rgba(0,0,0,0)',

                ),
                paper_bgcolor=Background,
                plot_bgcolor = Background_plots
            )
            # fig.update_traces(
                
            #     hovertemplate= df_plot['Text']) #ingen grund til at bruge customdata
            fig.update_yaxes(title_text='Percentage pay gap')
            
        else:
            df_plot = df_sector[(df_sector["Year"] >= years_chosen[0]) & (df_sector["Year"] <= years_chosen[1])]
            fig=px.line(df_plot,
                        x='Year',y='Difference in procents', 
                        color='Sector',
                        color_discrete_map={
                            'All Sectors':'black',
                            'Public Sector':'red',
                            'Private Sector':'blue',
                            #'User input':Color_user 
                            },
                        #title="Difference in procent for "+str(years_chosen[0])+" to "+str(years_chosen[1])
                        )
            fig.update_layout(
            title={
            'text' : "<b> Development of the gender pay gap for year <b>"+str(years_chosen[0])+" to "+str(years_chosen[1]),
            'x':0.5,
            'xanchor': 'center',
})
            
            fig.update_layout(
                legend=dict(
                    x=0.7,
                    y=1,
                    title_font_family=text_font,
                    font=dict(
                        family=text_font,
                        size=size_text, 
                        color=text_color,
                    ),
                    bgcolor='rgba(0,0,0,0)',
            

                ),
                paper_bgcolor=Background,
                plot_bgcolor = Background_plots
            )
            fig.update_xaxes(tickvals=year)
    
        fig.update_xaxes(tickvals=year)
        fig.update_yaxes(title_text='Percentage pay gap')
        fig.update_layout(title_font_size = size_titleheadline)
        fig.update_layout(font=dict(
            family= text_font,
            size=size_text,
            color=text_color))
        

        fig.update_traces(
                hovertemplate='Women earns %{y} % less then men in year %{x}'
                )#ingen grund til at bruge customdata
        if user_salary!=0 and user_salary is not None and user_salary!='':
            fig.update_traces(
                    hovertemplate=text, selector={'name':'User input'}
                    )#ingen grund 
        
        return fig
    
    else:
        
        if user_salary!=0 and user_salary is not None and user_salary!='':
        
                
            if n_gender == "women":
                
                salary_dif=pd.DataFrame()
                user_choosen = df1_30[(df1_30["Year"] == years_chosen[0])]
                user_choosen = user_choosen[user_choosen["Sector"] == n_sector]
                user_choosen = user_choosen[user_choosen["Salary Group"] == "All forms of pay"]
                user_choosen = user_choosen[user_choosen["Components"] == components]
                user_choosen = user_choosen[user_choosen['Employment Group']=='Employees']
                
                salary_dif['Difference in procents'] = ((user_choosen['Contents Men']-float(user_salary))/user_choosen['Contents Men'])*100
                salary_dif.insert(0,'Sector','User input',True)
                
                
            elif n_gender == "men":
                
                salary_dif=pd.DataFrame()
                user_choosen = df1_30[(df1_30["Year"] == years_chosen[0])]
                user_choosen = user_choosen[user_choosen["Sector"] == n_sector]
                user_choosen = user_choosen[user_choosen["Salary Group"] == "All forms of pay"]
                user_choosen = user_choosen[user_choosen["Components"] == components]
                user_choosen = user_choosen[user_choosen['Employment Group']=='Employees']
                
                salary_dif['Difference in procents'] = ((float(user_salary)-user_choosen['Contents Women'])/float(user_salary))*100
                salary_dif.insert(0,'Sector','User input',True)
                
            count=0
            for i in salary_dif['Difference in procents'].index:
                if salary_dif['Difference in procents'][i]<0:
                    if n_gender=='men':
                        text[count]='You are earning earn %{y} % less then the average women'
                    else: 
                        text[count]='You are earning earn %{y} % more then the average men'
                
                else:
                    if n_gender=='men':
                        text[count]='You are earning earn %{y} % more then the average women'
                    else: 
                        text[count]='You are earning earn %{y} % less then the average men'
                count=count+1
            
            salary_dif['Difference in procents']=abs(salary_dif['Difference in procents']) 
                
            salary_dif['Text']=text
        
        if user_salary!=0 and user_salary is not None and user_salary!='':
            
            df_sect = df_sector[(df_sector["Year"] == years_chosen[0])]
            df_sect=df_sect.drop(columns=['Year'])
            
            
            df_plot=pd.concat([df_sect,salary_dif])
            
            barchart_two = px.bar(
                data_frame=df_plot,
                y="Difference in procents",
                x="Sector",
                opacity=0.9,            # set opacity of markers (from 0 to 1)
                orientation="v",          # 'v','h': orientation of the marks
                
                # in 'group' mode, bars are placed beside each other.
                color="Sector",
                color_discrete_map={
                    'All Sectors':'black',
                    'Public Sector':'red',
                    'Private Sector':'blue',
                    'User input':Color_user },
                                # in 'relative' mode, bars are stacked above (+) or below (-) zero.
                #title="Difference in procent for "+str(years_chosen[0]),

            )
            
            barchart_two.update_layout(
                showlegend=False,
                paper_bgcolor=Background,
                plot_bgcolor = Background_plots,
                title={
                'text' : "<b>Development of the gender pay gap for year <b>"+str(years_chosen[1]),
                'x':0.5,
                'xanchor': 'center'},
                )
            barchart_two.update_traces(hovertemplate='Women earn %{y} % less than men in year '+str(years_chosen[1]))
            barchart_two.update_yaxes(title_text='Percentage pay gap')
            barchart_two.update_layout(  #DENNE
                title_font_size=size_titleheadline,
                font=dict(
                        family=text_font,
                        size=size_text, 
                        color=text_color))
            
            fig=barchart_two
        else:
        
            df_sector = df_sector[(df_sector["Year"] == years_chosen[0])]

            barchart_two = px.bar(
                data_frame=df_sector,
                y="Difference in procents",
                x="Sector",
                opacity=0.9,            # set opacity of markers (from 0 to 1)
                orientation="v",          # 'v','h': orientation of the marks
                
                # in 'group' mode, bars are placed beside each other.
                color="Sector",
                color_discrete_map={
                    'All Sectors':'black',
                    'Public Sector':'red',
                    'Private Sector':'blue',
                    'User input':Color_user },
                                # in 'relative' mode, bars are stacked above (+) or below (-) zero.
                #title="Difference in procent for "+str(years_chosen[0]),
            )

            barchart_two.update_layout(
                showlegend=False,
                paper_bgcolor=Background,
                plot_bgcolor = Background_plots,
            title={
                'text' : "<b> Development of the gender pay gap for year <b>"+str(years_chosen[1]),
                'x':0.5,
                'xanchor': 'center'},
                )
            
            barchart_two.update_traces(hovertemplate='Women earn %{y} % less than men in year '+str(years_chosen[1]))
            barchart_two.update_yaxes(title_text='Percentage pay gap')
            # barchart_two.update_layout(title_font_size=size_titleheadline, #ændret til v10
            #            font=dict(
            #                 family=text_font,
            #                 size=size_text,
            #                 color=text_color
            #             ) )
            fig=barchart_two
            #fig.update_layout(title_font_size=size_titleheadline)
            fig.update_layout(  #DENNE
                title_font_size=size_titleheadline,
                font=dict(
                        family=text_font,
                        size=size_text, 
                        color=text_color))
        
        
        fig.update_traces(
                hovertemplate='Women earns %{y} % less then men'
                )#ingen grund til at bruge customdata
        if user_salary!=0 and user_salary is not None and user_salary!='':
            fig.update_traces(
                    hovertemplate=text, selector={'name':'User input'}
                    )#ingen grund 
        return fig



@app.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id='intermediate-value',
          component_property='data'),  # years_chosen
    Input(component_id='intermediate-value2',
          component_property='data'),  # wage
    Input(component_id='explore_scatter', component_property='value'),  # sort
    Input(component_id='intermediate-value7',
          component_property='data'),  # user_wage
    Input(component_id='intermediate-value8',
          component_property='data')  # user_industry
)
def Brance_scatter(years_chosen, wage, sort, user_wage, user_industry):

    df_scatter = df_scat

    df_scatter = df_scatter[(df_scatter["Year"] >= years_chosen[0]) & (
        df_scatter["Year"] <= years_chosen[1])]

    df_scatter = df_scatter[df_scatter['Components'] == wage]

    df_scatmen = df_scatter.groupby(['Industry'])['Contents Men'].mean()
    df_scatwomen = df_scatter.groupby(['Industry'])['Contents Women'].mean()

    industries = list(df_scatter['Industry'].unique())
    industries = list(reversed(industries))

    x_dat = round(abs((df_scatmen-df_scatwomen)), 2)
    y_dat = industries

    df_diffscat = pd.DataFrame(x_dat, y_dat)
    
    
    x_data_diff = round(100*((df_scatmen-df_scatwomen)/df_scatmen),2) 
    

    # Sort function
    if sort == 1:  # Alphabeticallt
        industries = list(df_scatter['Industry'].unique())
        industries = list(reversed(industries))
        
        y_data = industries 
        df_diffproc = pd.DataFrame(x_data_diff, y_data)

        df_scatmen = df_scatter.groupby(['Industry'])['Contents Men'].mean()
        df_scatwomen = df_scatter.groupby(
            ['Industry'])['Contents Women'].mean()

        df_scatmen = pd.DataFrame(df_scatmen, industries)
        df_scatwomen = pd.DataFrame(df_scatwomen, industries)

    elif sort == 0:  # After lowest value
        # get list to sort after
        df_diffscat = df_diffscat.sort_values(0, ascending=True)
        industries = list(df_diffscat.index.unique())
        
        y_data = industries 
        df_diffproc = pd.DataFrame(x_data_diff, y_data)

        df_scatmen = df_scatter.groupby(['Industry'])['Contents Men'].mean()
        df_scatwomen = df_scatter.groupby(
            ['Industry'])['Contents Women'].mean()

        df_scatmen = pd.DataFrame(df_scatmen, industries)
        df_scatwomen = pd.DataFrame(df_scatwomen, industries)

    else:  # highest difference
        df_diffscat = df_diffscat.sort_values(0, ascending=False)
        industries = list(df_diffscat.index.unique())
        
        y_data = industries 
        df_diffproc = pd.DataFrame(x_data_diff, y_data)

        df_scatmen = df_scatter.groupby(['Industry'])['Contents Men'].mean()
        df_scatwomen = df_scatter.groupby(
            ['Industry'])['Contents Women'].mean()

        df_scatmen = pd.DataFrame(df_scatmen, industries)
        df_scatwomen = pd.DataFrame(df_scatwomen, industries)

    if wage == "STANDARDIZED HOURLY EARNINGS":
        figa1 = px.scatter(x=df_scatwomen["Contents Women"],
                           y=industries)
        figa1.update_traces(hovertemplate='Womens hourly salary: %{x} DKK <br>Industry: %{y}', marker=dict(size=8,
                                                                                                       line=dict(width=8,
                                                                                                                 color=Color_women)),
                            selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_women)),


        figa2 = px.scatter(x=df_scatmen["Contents Men"],
                           y=industries,
                           )

        figa2.update_traces(hovertemplate='Mans hourly salary: %{x} DKK <br>Industry: %{y}', marker=dict(size=8, symbol="diamond",
                                                                                                     line=dict(width=8,
                                                                                                               color=Color_men)),
                            selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_men))

        fig_line = px.scatter(x=((df_scatmen["Contents Men"]+df_scatwomen["Contents Women"])/2),
                              y=industries, custom_data=[df_diffscat[0], df_diffproc[0]])  #tilføj
        fig_line.update_traces(hovertemplate='The difference in mean hourly wage between men and women in the %{y} industry is %{customdata[0]} DKK, which corresponds to women, on average, earning %{customdata[1]} percent less than men.', 
                               line_color='#0000ff', line_width=5,
                               marker=dict(size=0.1,
                                           line=dict(width=0.1,
                                                     color=Color_line)),
                               selector=dict(mode='markers'), hoverlabel = dict(bgcolor = scatter_hover_color_line))
        
            
        

    else:
        figa1 = px.scatter(x=df_scatwomen["Contents Women"],
                           y=industries)
        figa1.update_traces(hovertemplate='Womens monthly salary: %{x} DKK <br>Industry: %{y}', marker=dict(size=8,
                                                                                                        line=dict(width=8,
                                                                                                                  color=Color_women)),
                            selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_women))

        figa2 = px.scatter(x=df_scatmen["Contents Men"],
                           y=industries,
                           )

        figa2.update_traces(hovertemplate='Mans monthly salary: %{x} DKK <br>Industry: %{y}', marker=dict(size=8, symbol="diamond",
                                                                                                      line=dict(width=8,
                                                                                                                color=Color_men)),
                            selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_men))

        fig_line = px.scatter(x=((df_scatmen["Contents Men"]+df_scatwomen["Contents Women"])/2),
                              y=industries, custom_data=[df_diffscat[0], df_diffproc[0]])
        fig_line.update_traces(hovertemplate='The difference in mean monthly wage between men and women in the %{y} industry is %{customdata[0]} DKK, which corresponds to women, on average, earning %{customdata[1]} percent less than men.', marker=dict(size=0.1, #søg her 1
                                                                                                                                                                   line=dict(width=0.1,
                                                                                                                                                                             color=Color_line)),
                               selector=dict(mode='markers'), hoverlabel = dict(bgcolor = scatter_hover_color_line))

    # Creating the lines between men and women
    figs = []

    for i in range(19):
        x_values = [df_scatwomen["Contents Women"].iloc[i],
                    df_scatmen["Contents Men"].iloc[i]]
        y_values = [industries[i], industries[i]]

        figs.append(px.line(x=x_values, y=y_values))


    fig0 = figs[0]
    fig1 = figs[1]
    fig2 = figs[2]
    fig3 = figs[3]
    fig4 = figs[4]
    fig5 = figs[5]
    fig6 = figs[6]
    fig7 = figs[7]
    fig8 = figs[8]
    fig9 = figs[9]
    fig10 = figs[10]
    fig11 = figs[11]
    fig12 = figs[12]
    fig13 = figs[13]
    fig14 = figs[14]
    fig15 = figs[15]
    fig16 = figs[16]
    fig17 = figs[17]
    fig18 = figs[18]


    fig0.update_traces(line_color=Color_line, line_width=1)
    fig1.update_traces(line_color=Color_line, line_width=1)
    fig2.update_traces(line_color=Color_line, line_width=1)
    fig3.update_traces(line_color=Color_line, line_width=1)
    fig4.update_traces(line_color=Color_line, line_width=1)
    fig5.update_traces(line_color=Color_line, line_width=1)
    fig6.update_traces(line_color=Color_line, line_width=1)
    fig7.update_traces(line_color=Color_line, line_width=1)
    fig8.update_traces(line_color=Color_line, line_width=1)
    fig9.update_traces(line_color=Color_line, line_width=1)
    fig10.update_traces(line_color=Color_line, line_width=1)
    fig11.update_traces(line_color=Color_line, line_width=1)
    fig12.update_traces(line_color=Color_line, line_width=1)
    fig13.update_traces(line_color=Color_line, line_width=1)
    fig14.update_traces(line_color=Color_line, line_width=1)
    fig15.update_traces(line_color=Color_line, line_width=1)
    fig16.update_traces(line_color=Color_line, line_width=1)
    fig17.update_traces(line_color=Color_line, line_width=1)
    fig18.update_traces(line_color=Color_line, line_width=1)

    if user_wage=='0' or user_wage is None or user_wage =='':
        user_wage=0
        
    if user_wage != 0:
        if wage == "STANDARDIZED HOURLY EARNINGS" and int(user_wage)<=1500:
            fig_user = px.scatter(x=[user_wage], y=[user_industry]
                              )

            fig_user.update_traces(hovertemplate='Your hourly salary: %{x} DKK <br>In industry: %{y}', marker=dict(size=11, symbol="star",
                                                                                                            line=dict(width=11,
                                                                                                                      color=Color_user)),
                               selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_user))
            
            fig3 = go.Figure(data=fig_line.data + fig_user.data + fig0.data + fig1.data + fig2.data + fig3.data + fig4.data + fig5.data + fig6.data +
                             fig7.data + fig8.data + fig9.data + fig10.data + fig11.data + fig12.data + fig13.data + fig14.data + fig15.data + fig16.data + fig17.data + fig18.data+figa1.data + figa2.data)

            
        elif wage== "STANDARDIZED MONTHLY EARNINGS" and int(user_wage) >= 5000 and int(user_wage)<=5000000:
            
            fig_user = px.scatter(x=[user_wage], y=[user_industry]
                              )

            fig_user.update_traces(hovertemplate='Your monthly salary: %{x} DKK <br>In industry: %{y}', marker=dict(size=11, symbol="star",
                                                                                                            line=dict(width=11,
                                                                                                                      color=Color_user)),
                               selector=dict(mode='markers'), hoverlabel = dict(bgcolor = Color_user))

            fig3 = go.Figure(data=fig_line.data + fig_user.data + fig0.data + fig1.data + fig2.data + fig3.data + fig4.data + fig5.data + fig6.data +
                             fig7.data + fig8.data + fig9.data + fig10.data + fig11.data + fig12.data + fig13.data + fig14.data + fig15.data + fig16.data + fig17.data + fig18.data+figa1.data + figa2.data)
        
        else:
            fig3 = go.Figure(data=fig_line.data + fig0.data + fig1.data + fig2.data + fig3.data + fig4.data + fig5.data + fig6.data +
                             fig7.data + fig8.data + fig9.data + fig10.data + fig11.data + fig12.data + fig13.data + fig14.data + fig15.data + fig16.data + fig17.data + fig18.data+figa1.data + figa2.data)
        
        
    else:
        # Adding all figures together as one
        fig3 = go.Figure(data=fig_line.data + fig0.data + fig1.data + fig2.data + fig3.data + fig4.data + fig5.data + fig6.data +
                         fig7.data + fig8.data + fig9.data + fig10.data + fig11.data + fig12.data + fig13.data + fig14.data + fig15.data + fig16.data + fig17.data + fig18.data+figa1.data + figa2.data)
    
        
    if wage == "STANDARDIZED HOURLY EARNINGS":
        fig3.update_xaxes(title_text="Hourly wage in DKK")
        fig3.update_xaxes(tickvals=[160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270,
                          280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440])
        
    else:
        fig3.update_xaxes(title_text="Monthly wage in DKK")
        

    #fig3.update_layout(title_text="Industries")
    fig3.update_layout(title={
                'text' : "<b>The gender pay gap in different industries<b>",
                'x':0.5,
                'xanchor': 'center'},
                title_font_family=text_font,
                ),
    
    
    fig3.update_layout(yaxis=dict(autorange="reversed")
                       )
    fig3.update_layout(
    paper_bgcolor=Plot_back,
    plot_bgcolor = Background_plots)
    fig3.update_layout(title_font_size=size_titleheadline,
                       font=dict(
                            family=text_font,
                            size=size_text,
                            color=text_color
                        ) 
    )
    
    return fig3

###################################################################
# Employment groups


@app.callback(
    # it have to be written children or else the output list won't show
    Output(component_id=('intermediate-value3'), component_property=('data')),
    # the value is connected to the input which the input is is connected to the layout
    Input(component_id='industry_raditem', component_property='value')
)
# it the one saving the choosen Component in the dropdown
def industry_output2(industry_value):
    return industry_value


#Employment group callback
@app.callback(
    # it have to be written figure or else the output list won't show
    Output(component_id='emp_g_graph', component_property='figure'),
    # the data is connected to the input which the input is is connected to the layout
    Input(component_id='intermediate-value', component_property='data'),
    Input(component_id='intermediate-value3', component_property='data')
)
# it for the employment group
def update_bargraph1(years_chosen, components2):
    # get each value from the rangeslide list which is saved in id: intermediate-value
    dff2 = df_e[(df_e["Year"] >= years_chosen[0]) &
               (df_e["Year"] <= years_chosen[1])]

    # it add value for unique industry
    dff2 = dff2[dff2['Industry'] == str(components2)]
    dff2 = dff2.groupby(["Employment Group"], as_index=False)[
        ["Men", "Women",'Difference in men and women working in the industry',
                    'Procent of men in the industry',
                    'Procent of women in the industry']].mean()

    dff2 = round(dff2,2)
    dff2['Difference in men and women working in the industry']=abs(dff2['Difference in men and women working in the industry'])
    
# link to style and understand barchard: https://www.youtube.com/watch?v=N1GwQNatOwo&list=PLh3I780jNsiTXlWYiNWjq2rBgg3UsL1Ub&index=2

    barchart1 = px.bar(
        data_frame=dff2,  # it only show the 5 highest gap pay between men and women
        x= ["Employees in total", "Employees, non-managerial level", "General managers"],#"Employment Group",
        y=["Men", "Women"],
        opacity=0.9,            # set opacity of markers (from 0 to 1)
        orientation="v",          # 'v','h': orientation of the marks
        barmode="group",     # in 'overlay' mode, bars are top of one another.
        color_discrete_map={
        'Men': Color_men,
        'Women': Color_women
        },
        labels={'value':'Number of people'},
         hover_data={'Difference in men and women working in the industry',
                     'Procent of men in the industry','Procent of women in the industry'},
                                 # in 'group' mode, bars are placed beside each other.
                                # in 'relative' mode, bars are stacked above (+) or below (-) zero.
        #title="Distribution of employees in the " +str(components2) +' industry'
        
    )
    barchart1.update_layout(showlegend=False,paper_bgcolor=Background, plot_bgcolor = Background_plots)
    barchart1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    barchart1.update_layout(title={
                'text' : "<b>Distribution of employees in the " +str(components2) +' industry<b>',
                'x':0.5,
                'xanchor': 'center'},
                ),
    barchart1.update_traces(hovertemplate="There are %{y:.2f} in the %{x} group. </br> </br>There are a difference of %{customdata[2]} between the number of men and women in this industries </br>corresponding to men %{customdata[1]} procent and women %{customdata[0]} procent in this industry.<extra></extra>")#write customdata to get the procent of women in the industry #%{customdata[0]}, #%{customdata[2]}
    barchart1.update_xaxes(title_text='Employment groups'), #kig her
    barchart1.update_yaxes(title_text='Number of employees'),
    barchart1.update_layout(title_font_size=size_titleheadline,
                       font=dict(
                            family=text_font,
                            size=size_text,
                            color=text_color
                        ) )
    
    return barchart1



@app.callback(  
    # it have to be written figure or else the output list won't show
    Output(component_id='bpb_g_graph', component_property='figure'),
    # the data is connected to the input which the input is is connected to the layout
    Input(component_id='intermediate-value', component_property='data'),
    Input(component_id='intermediate-value2', component_property='data'),
    Input(component_id='intermediate-value3', component_property='data')
)
def update_bargraph2(years_chosen, wage,  components2):
    # get each value from the rangeslide list which is saved in id: intermediate-value
    dff2 = df_dif[(df_dif["Year"] >= years_chosen[0]) &
               (df_dif["Year"] <= years_chosen[1])]

    # it add value for unique industry
    dff2 = dff2[dff2['Industry'] == str(components2)]
    # , as_index=False) #it group together the industries and then get the mean for each group
    
    
    if wage == "STANDARDIZED HOURLY EARNINGS":
        dff2 = dff2.groupby(["Earnings types per standard hour"], as_index=False)[
            ["Men's earning", "Women's earning"]].mean()
        dff2["Women earnings compered to men's"]=100-(dff2["Men's earning"]-dff2["Women's earning"])/(dff2["Men's earning"])*100
        dff2['Basis for men']=100
    # link to style and understand barchard: https://www.youtube.com/watch?v=N1GwQNatOwo&list=PLh3I780jNsiTXlWYiNWjq2rBgg3UsL1Ub&index=2
        dff2 = round(dff2,2)
        
        barchart1 = px.bar(
            data_frame=dff2,  # it only show the 5 highest gap pay between men and women
            x= ["Basic earnings", "Benefits", "Pension including ATP"],  #"Earnings types per standard hour",
            y=["Basis for men", "Women earnings compered to men's"],
            opacity=0.9,            # set opacity of markers (from 0 to 1)
            orientation="v",          # 'v','h': orientation of the marks
            barmode="group",     # in 'overlay' mode, bars are top of one another.
            color_discrete_map={
            'Basis for men': Color_men,
            "Women earnings compered to men's": Color_women
            },
            labels={'value':'Procents'},
            hover_data=["Men's earning", "Women's earning"])
                        # in 'group' mode, bars are placed beside each other.
                                # in 'relative' mode, bars are stacked above (+) or below (-) zero.
        #title="Procents womens are getting of mens earnings in " +str(components2) +' industry'
    else:
        dff2["Men's earning"] = dff2["Men's earning"]*160.331733
        dff2["Women's earning"] = dff2["Women's earning"]*160.331733
        
        dff2 = dff2.groupby(["Earnings types per standard hour"], as_index=False)[
            ["Men's earning", "Women's earning"]].mean()
        
        
        dff2["Women earnings compered to men's"]=100-(dff2["Men's earning"]-dff2["Women's earning"])/(dff2["Men's earning"])*100
        dff2['Basis for men']=100
    # link to style and understand barchard: https://www.youtube.com/watch?v=N1GwQNatOwo&list=PLh3I780jNsiTXlWYiNWjq2rBgg3UsL1Ub&index=2
        dff2= round(dff2,2)
        
        barchart1 = px.bar(
            data_frame=dff2,  # it only show the 5 highest gap pay between men and women
            x= ["Basic earnings", "Benefits", "Pension including ATP"],  #"Earnings types per standard hour",
            y=["Basis for men", "Women earnings compered to men's"],
            opacity=0.9,            # set opacity of markers (from 0 to 1)
            orientation="v",          # 'v','h': orientation of the marks
            barmode="group",     # in 'overlay' mode, bars are top of one another.
            color_discrete_map={
            'Basis for men': Color_men,
            "Women earnings compered to men's": Color_women
            },
            labels={'value':'Procents'},
            hover_data=["Men's earning", "Women's earning"])
                        # in 'group' mode, bars are placed beside each other.
                                # in 'relative' mode, bars are stacked above (+) or below (-) zero.
        #title="Procents womens are getting of mens earnings in " +str(components2) +' industry'
        
    barchart1.update_traces(hovertemplate='Salary type: %{x} DKK <br>Procentage of mens earning: %{y} %.<br>Men earnings: %{customdata[0]} DKK <br>Women earnings: %{customdata[1]} DKK <extra></extra>') #Søg her
    barchart1.update_layout(showlegend=False,paper_bgcolor=Background, plot_bgcolor = Background_plots)
    barchart1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    barchart1.update_layout(title={
                'text' : "<b>The percentage relation between men’s and women's wages in " +str(components2) +' industry<b>',
                'x':0.5,
                'xanchor': 'center'},
                ),
    if wage == "STANDARDIZED HOURLY EARNINGS":
        barchart1.update_xaxes(title_text='Types of earnings in DKK per hour'), #kig her
        
    else:
        barchart1.update_xaxes(title_text='Types of earnings in DKK per month'), 
        
    barchart1.update_yaxes(title_text='Percentage'),
    barchart1.update_layout(title_font_size=size_titleheadline,
                       font=dict(
                            family=text_font,
                            size=size_text,
                            color=text_color
                        ) )
    
    return barchart1


# @app.callback(
#     # it have to be written children or else the output list won't show
#     Output(component_id=('intermediate-value4'), component_property=('data')),
#     # the value is connected to the input which the input is is connected to the layout
#     Input(component_id='Components_overtime', component_property='value')
# )
# def up_m_l_output(up_m_l_value):  # it the one saving the choosen Component in the dropdown
#     return up_m_l_value


@app.callback(
    Output(component_id='overtime_graph', component_property='figure'), #show the graph
    Input(component_id='intermediate-value', component_property='data'), #of the year interval #the data is connected to the input which the input is is connected to the layout
    Input(component_id='intermediate-value2', component_property='data'), #of the choosen montly or hourly
    Input(component_id='intermediate-value3', component_property='data'), #of the choosen branche
    Input(component_id='intermediate-value7', component_property='data'), #get the users salasy indput
)

def overtime_data(years_chosen, wage, industrie, user_salary):
    chose_decimals = 2

    df_box = df1
    df_box = df_box[(df_box["Year"] >= years_chosen[0]) & ( df_box["Year"] <= years_chosen[1])]
    df_box = df_box[(df_box["Industry"] == str(industrie))]
   # df_box = df_box[(df_box["Industry"] == "Manufacturing")]
    #df_box = df_box[(df_box["Year"] == 2020)]
    
    
    df_box = df_box[(df_box["Sector"] == "All sectors")] 
    df_box = df_box[(df_box["Salary Group"] == "All forms of pay")]      
    df_box=df_box.drop(columns=["Sector","Salary Group"])
    df_box.reset_index(drop = True)
    
    df_box = df_box[(df_box["Components"] != "Fringe benefits in DKK per standard hour")]
    df_box = df_box[(df_box["Components"] != "Pension including ATP in DKK per standard hour")]
    df_box = df_box[(df_box["Components"] != "Basic earnings in DKK per standard hour")]
    df_box = df_box[(df_box["Components"] != "STANDARDIZED MONTHLY EARNINGS")]
    

    
    ##MANAGERS
    general_manager_df = df_box[(df_box["Employment Group"] == "General managers")]
   
    men_general_manager_df = general_manager_df.groupby([ "Components"]) ["Contents Men"].mean()
    women_general_manager_df = general_manager_df.groupby([ "Components"]) ["Contents Women"].mean()
    
    
    
    men_general_manager_mean = round(men_general_manager_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    men_general_manager_median = round(men_general_manager_df.iloc[1],chose_decimals)
    men_general_manager_q1 = round(men_general_manager_df.iloc[0],chose_decimals) #lower quartile
    men_general_manager_q3 = round(men_general_manager_df.iloc[4],chose_decimals)
    men_general_manager_IQR = round((men_general_manager_q3 - men_general_manager_q1),chose_decimals)
    men_general_manager_lowerfence = round(men_general_manager_q1 - (1.5*men_general_manager_IQR),chose_decimals)
    men_general_manager_upperfence = round(men_general_manager_q3 + (1.5*men_general_manager_IQR),chose_decimals)
    
    
    women_general_manager_mean = round(women_general_manager_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    women_general_manager_median = round(women_general_manager_df.iloc[1],chose_decimals)
    women_general_manager_q1 = round(women_general_manager_df.iloc[0],chose_decimals) #lower quartile
    women_general_manager_q3 = round(women_general_manager_df.iloc[4],chose_decimals)
    women_general_manager_IQR = round((women_general_manager_q3 - women_general_manager_q1),chose_decimals)
    women_general_manager_lowerfence = round(women_general_manager_q1 - (1.5*women_general_manager_IQR),chose_decimals)
    women_general_manager_upperfence = round(women_general_manager_q3 + (1.5*women_general_manager_IQR),chose_decimals)
    
    
    #Employees non managers
    employees_non_managers_df = df_box[(df_box["Employment Group"] == "Employees, non-managerial level")]

    men_employees_non_managers_df = employees_non_managers_df.groupby([ "Components"]) ["Contents Men"].mean()
    women_employees_non_managers_df = employees_non_managers_df.groupby([ "Components"]) ["Contents Women"].mean()


    men_employees_non_managers_mean = round(men_employees_non_managers_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    men_employees_non_managers_median = round(men_employees_non_managers_df.iloc[1],chose_decimals)
    men_employees_non_managers_q1 = round(men_employees_non_managers_df.iloc[0],chose_decimals) #lower quartile
    men_employees_non_managers_q3 = round(men_employees_non_managers_df.iloc[4],chose_decimals)
    men_employees_non_managers_IQR = round((men_employees_non_managers_q3 - men_employees_non_managers_q1),chose_decimals)
    men_employees_non_managers_lowerfence = round(men_employees_non_managers_q1 - (1.5*men_employees_non_managers_IQR),chose_decimals)
    men_employees_non_managers_upperfence = round(men_employees_non_managers_q3 + (1.5*men_employees_non_managers_IQR),chose_decimals)


    women_employees_non_managers_mean = round(women_employees_non_managers_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    women_employees_non_managers_median = round(women_employees_non_managers_df.iloc[1],chose_decimals)
    women_employees_non_managers_q1 = round(women_employees_non_managers_df.iloc[0],chose_decimals) #lower quartile
    women_employees_non_managers_q3 = round(women_employees_non_managers_df.iloc[4],chose_decimals)
    women_employees_non_managers_IQR = round((women_employees_non_managers_q3 - women_employees_non_managers_q1),chose_decimals)
    women_employees_non_managers_lowerfence = round(women_employees_non_managers_q1 - (1.5*women_employees_non_managers_IQR),chose_decimals)
    women_employees_non_managers_upperfence = round(women_employees_non_managers_q3 + (1.5*women_employees_non_managers_IQR),chose_decimals)
  
    
    #total employees
    employees_total_df = df_box[(df_box["Employment Group"] == "Employees")]
    
    men_employees_total_df = employees_total_df.groupby([ "Components"]) ["Contents Men"].mean()
    women_employees_total_df = employees_total_df.groupby([ "Components"]) ["Contents Women"].mean()
    
    
    men_employees_total_mean = round(men_employees_total_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    men_employees_total_median = round(men_employees_total_df.iloc[1],chose_decimals)
    men_employees_total_q1 = round(men_employees_total_df.iloc[0],chose_decimals) #lower quartile
    men_employees_total_q3 = round(men_employees_total_df.iloc[4],chose_decimals)
    men_employees_total_IQR = round((men_employees_total_q3 - men_employees_total_q1),chose_decimals)
    men_employees_total_lowerfence = round(men_employees_total_q1 - (1.5*men_employees_total_IQR),chose_decimals)
    men_employees_total_upperfence = round(men_employees_total_q3 + (1.5*men_employees_total_IQR),chose_decimals)
    
    
    women_employees_total_mean = round(women_employees_total_df.iloc[3],chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
    women_employees_total_median = round(women_employees_total_df.iloc[1],chose_decimals)
    women_employees_total_q1 = round(women_employees_total_df.iloc[0],chose_decimals) #lower quartile
    women_employees_total_q3 = round(women_employees_total_df.iloc[4],chose_decimals)
    women_employees_total_IQR = round((women_employees_total_q3 - women_employees_total_q1),chose_decimals)
    women_employees_total_lowerfence = round(women_employees_total_q1 - (1.5*women_employees_total_IQR),chose_decimals)
    women_employees_total_upperfence = round(women_employees_total_q3 + (1.5*women_employees_total_IQR),chose_decimals)
    
    #her skal if statement være
    if wage == "STANDARDIZED HOURLY EARNINGS":
        fig1_gns = go.Figure() #employees men
        fig1_gns.add_trace(
        go.Box(
            x=["Total male employees"],
            #name="",
            marker_color=Color_men))
    
        fig1_gns.update_traces(q1=[men_employees_total_q1] , median=[men_employees_total_median],
                      q3=[men_employees_total_q3], lowerfence=[men_employees_total_lowerfence],
                      upperfence=[men_employees_total_upperfence], mean=[men_employees_total_mean])
    
        fig2_gns = go.Figure() #employees women
        fig2_gns.add_trace(
        go.Box(
            x=["Total female employees"],
            #name="Employees total - women",
            marker_color=Color_women))
    
        fig2_gns.update_traces(q1=[women_employees_total_q1] , median=[women_employees_total_median],
                      q3=[women_employees_total_q3], lowerfence=[women_employees_total_lowerfence],
                      upperfence=[women_employees_total_upperfence], mean=[women_employees_total_mean])
        
        
    
        fig3_gns = go.Figure() #managers men
        fig3_gns.add_trace(
        go.Box(
            x=["Male managers"],
            #name="Managers - men",
            marker_color=Color_men))
    
        fig3_gns.update_traces(q1=[men_general_manager_q1] , median=[men_general_manager_median],
                      q3=[men_general_manager_q3], lowerfence=[men_general_manager_lowerfence],
                      upperfence=[men_general_manager_upperfence], mean=[men_general_manager_mean])
        
        
        fig4_gns = go.Figure() #managers women
        fig4_gns.add_trace(
        go.Box(
            x=["Female managers"],
            #name="Managers - women",
            marker_color=Color_women))
    
        fig4_gns.update_traces(q1=[ women_general_manager_q1] , median=[ women_general_manager_median],
                      q3=[ women_general_manager_q3], lowerfence=[ women_general_manager_lowerfence],
                      upperfence=[ women_general_manager_upperfence], mean=[ women_general_manager_mean])
        
        
        fig5_gns = go.Figure() #employees - non-managers men
        fig5_gns.add_trace(
        go.Box(
            x=["Male employees, non-managerial level"],
            #name="Employees, non-managers- men",
            marker_color=Color_men))
    
        fig5_gns.update_traces(q1=[men_employees_non_managers_q1] , median=[men_employees_non_managers_median],
                      q3=[men_employees_non_managers_q3], lowerfence=[men_employees_non_managers_lowerfence],
                      upperfence=[men_employees_non_managers_upperfence], mean=[men_employees_non_managers_mean])
        
        
        fig6_gns = go.Figure() #employees - non-managers women
        fig6_gns.add_trace(
        go.Box(
            x=["Female employees, non-managerial level"],
            #name="Employees, non-managers - women",
            marker_color=Color_women))
    
        fig6_gns.update_traces(q1=[ women_employees_non_managers_q1] , median=[ women_employees_non_managers_median],
                      q3=[ women_employees_non_managers_q3], lowerfence=[ women_employees_non_managers_lowerfence],
                      upperfence=[ women_employees_non_managers_upperfence], mean=[  women_employees_non_managers_mean])
    
    else:
        recalculate = 160.331733
        ##MANAGERS
        men_general_manager_mean_2 =round(men_general_manager_mean*recalculate,chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
        men_general_manager_median_2 = round(men_general_manager_median *recalculate,chose_decimals)
        men_general_manager_q1_2 = round(men_general_manager_q1*recalculate,chose_decimals)
        men_general_manager_q3_2 = round(men_general_manager_q3*recalculate,chose_decimals)
        men_general_manager_IQR_2 = round((men_general_manager_q3_2 - men_general_manager_q1_2),chose_decimals)
        men_general_manager_lowerfence_2 = round(men_general_manager_q1_2 - (1.5*men_general_manager_IQR_2),chose_decimals)
        men_general_manager_upperfence_2 = round(men_general_manager_q3_2 + (1.5*men_general_manager_IQR_2),chose_decimals)
        
        
        women_general_manager_mean_2 = round(women_general_manager_mean*recalculate,chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
        women_general_manager_median_2 = round(women_general_manager_median*recalculate,chose_decimals)
        women_general_manager_q1_2 = round(women_general_manager_q1*recalculate,chose_decimals) #lower quartile
        women_general_manager_q3_2 = round(women_general_manager_q3*recalculate,chose_decimals)
        women_general_manager_IQR_2 = round((women_general_manager_q3_2 - women_general_manager_q1_2),chose_decimals)
        women_general_manager_lowerfence_2 = round(women_general_manager_q1_2 - (1.5*women_general_manager_IQR_2),chose_decimals)
        women_general_manager_upperfence_2 = round(women_general_manager_q3_2 + (1.5*women_general_manager_IQR_2),chose_decimals)
        
        
        #Employees non managers
        men_employees_non_managers_mean_2 = round(men_employees_non_managers_mean *recalculate,chose_decimals)#man is STANDARDIZED HOURLY EARNINGS 
        men_employees_non_managers_median_2 = round(men_employees_non_managers_median*recalculate,chose_decimals)
        men_employees_non_managers_q1_2 = round(men_employees_non_managers_q1*recalculate,chose_decimals)#lower quartile
        men_employees_non_managers_q3_2 =round(men_employees_non_managers_q3 *recalculate,chose_decimals)
        men_employees_non_managers_IQR_2 = round((men_employees_non_managers_q3_2 - men_employees_non_managers_q1_2),chose_decimals)
        men_employees_non_managers_lowerfence_2 = round(men_employees_non_managers_q1_2 - (1.5*men_employees_non_managers_IQR_2),chose_decimals)
        men_employees_non_managers_upperfence_2 = round(men_employees_non_managers_q3_2 + (1.5*men_employees_non_managers_IQR_2),chose_decimals)


        women_employees_non_managers_mean_2 = round(women_employees_non_managers_mean *recalculate,chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
        women_employees_non_managers_median_2 =  round(women_employees_non_managers_median*recalculate,chose_decimals)
        women_employees_non_managers_q1_2 =   round(women_employees_non_managers_q1*recalculate,chose_decimals)#lower quartile
        women_employees_non_managers_q3_2 =  round(women_employees_non_managers_q3*recalculate,chose_decimals)
        women_employees_non_managers_IQR_2 = round((women_employees_non_managers_q3_2 - women_employees_non_managers_q1_2),chose_decimals)
        women_employees_non_managers_lowerfence_2 = round(women_employees_non_managers_q1_2 - (1.5*women_employees_non_managers_IQR_2),chose_decimals)
        women_employees_non_managers_upperfence_2 = round(women_employees_non_managers_q3_2 + (1.5*women_employees_non_managers_IQR_2),chose_decimals)
      
        
        #total employees
        men_employees_total_mean_2 = round(men_employees_total_mean *recalculate, chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
        men_employees_total_median_2 = round(men_employees_total_median *recalculate, chose_decimals)
        men_employees_total_q1_2 =  round(men_employees_total_q1 *recalculate, chose_decimals)#lower quartile
        men_employees_total_q3_2 = round(men_employees_total_q3 *recalculate, chose_decimals)
        men_employees_total_IQR_2 = round((men_employees_total_q3_2 - men_employees_total_q1_2), chose_decimals)
        men_employees_total_lowerfence_2 = round(men_employees_total_q1_2 - (1.5*men_employees_total_IQR_2), chose_decimals)
        men_employees_total_upperfence_2 = round(men_employees_total_q3_2 + (1.5*men_employees_total_IQR_2), chose_decimals)
        
        
        women_employees_total_mean_2 = round(women_employees_total_mean *recalculate, chose_decimals) #mean is STANDARDIZED HOURLY EARNINGS 
        women_employees_total_median_2 =round(women_employees_total_median *recalculate, chose_decimals)
        women_employees_total_q1_2 =round(women_employees_total_q1*recalculate , chose_decimals)#lower quartile
        women_employees_total_q3_2 = round(women_employees_total_q3 *recalculate, chose_decimals)
        women_employees_total_IQR_2 = round((women_employees_total_q3_2 - women_employees_total_q1_2), chose_decimals)
        women_employees_total_lowerfence_2 = round(women_employees_total_q1_2 - (1.5*women_employees_total_IQR_2), chose_decimals)
        women_employees_total_upperfence_2 = round(women_employees_total_q3_2 + (1.5*women_employees_total_IQR_2), chose_decimals)
    
        fig1_gns_2 = go.Figure() #employees men
        fig1_gns_2.add_trace(
        go.Box(
            x=["Total male employees"],
            #name="",
            marker_color=Color_men))
    
        fig1_gns_2.update_traces(q1=[men_employees_total_q1_2] , median=[men_employees_total_median_2],
                      q3=[men_employees_total_q3_2], lowerfence=[men_employees_total_lowerfence_2],
                      upperfence=[men_employees_total_upperfence_2], mean=[men_employees_total_mean_2])
    
        fig2_gns_2 = go.Figure() #employees women
        fig2_gns_2.add_trace(
        go.Box(
            x=["Total female employees"],
            #name="Employees total - women",
            marker_color=Color_women))
    
        fig2_gns_2.update_traces(q1=[women_employees_total_q1_2] , median=[women_employees_total_median_2],
                      q3=[women_employees_total_q3_2], lowerfence=[women_employees_total_lowerfence_2],
                      upperfence=[women_employees_total_upperfence_2], mean=[women_employees_total_mean_2])
        
        
    
        fig3_gns_2 = go.Figure() #managers men
        fig3_gns_2.add_trace(
        go.Box(
            x=["Male managers"],
            #name="Managers - men",
            marker_color=Color_men))
    
        fig3_gns_2.update_traces(q1=[men_general_manager_q1_2] , median=[men_general_manager_median_2],
                      q3=[men_general_manager_q3_2], lowerfence=[men_general_manager_lowerfence_2],
                      upperfence=[men_general_manager_upperfence_2], mean=[men_general_manager_mean_2])
        
        
        fig4_gns_2 = go.Figure() #managers women
        fig4_gns_2.add_trace(
        go.Box(
            x=["Female managers"],
            #name="Managers - women",
            marker_color=Color_women))
    
        fig4_gns_2.update_traces(q1=[ women_general_manager_q1_2] , median=[ women_general_manager_median_2],
                      q3=[ women_general_manager_q3_2], lowerfence=[ women_general_manager_lowerfence_2],
                      upperfence=[ women_general_manager_upperfence_2], mean=[ women_general_manager_mean_2])
        
        
        fig5_gns_2 = go.Figure() #employees - non-managers men
        fig5_gns_2.add_trace(
        go.Box(
            x=["Male employees, non-managerial level"],
            #name="Employees, non-managers- men",
            marker_color=Color_men))
    
        fig5_gns_2.update_traces(q1=[men_employees_non_managers_q1_2] , median=[men_employees_non_managers_median_2],
                      q3=[men_employees_non_managers_q3_2], lowerfence=[men_employees_non_managers_lowerfence_2],
                      upperfence=[men_employees_non_managers_upperfence_2], mean=[men_employees_non_managers_mean_2])
        
        
        fig6_gns_2 = go.Figure() #employees - non-managers women
        fig6_gns_2.add_trace(
        go.Box(
            x=["Female employees, non-managerial level"],
            #name="Employees, non-managers - women",
            marker_color=Color_women))
    
        fig6_gns_2.update_traces(q1=[ women_employees_non_managers_q1_2] , median=[ women_employees_non_managers_median_2],
                      q3=[ women_employees_non_managers_q3_2], lowerfence=[ women_employees_non_managers_lowerfence_2],
                      upperfence=[ women_employees_non_managers_upperfence_2], mean=[  women_employees_non_managers_mean_2])
    

    
    if user_salary=='0' or user_salary == None or user_salary =='' or user_salary=='NoneType':
        user_salary=0
    
    if wage == "STANDARDIZED HOURLY EARNINGS":
        fig_output = go.Figure(data=fig1_gns.data + fig2_gns.data + fig5_gns.data + fig6_gns.data+ fig3_gns.data + fig4_gns.data )
        if int(user_salary)<=1500 and user_salary!=0:
            fig_output.add_hline(y=user_salary,line_color=Color_user)
        fig_output.update_layout(showlegend = False, paper_bgcolor=Background, plot_bgcolor = Background_plots)
        fig_output.update_layout(yaxis_title = 'Hourly wage in DKK', xaxis_title = 'Employment Group')
        
    elif wage=='STANDARDIZED MONTHLY EARNINGS':
        fig_output = go.Figure(data=fig1_gns_2.data + fig2_gns_2.data + fig5_gns_2.data + fig6_gns_2.data + fig3_gns_2.data + fig4_gns_2.data )
        if int(user_salary) >=5000 and int(user_salary) <=5000000:
            fig_output.add_hline(y=user_salary,line_color=Color_user)
        fig_output.update_layout(showlegend = False, paper_bgcolor=Background, plot_bgcolor = Background_plots)
        fig_output.update_layout(yaxis_title = 'Monthly wage in DKK', xaxis_title = 'Employment groups')
    
    fig_output.update_layout(title={'text':"<b> Wage distribution for employment groups based on gender for the " + str(industrie)+" industry<b>",  'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig_output.update_layout(title_font_size=size_titleheadline,
                       font=dict(
                            family=text_font,
                            size=size_text,
                            color=text_color
                        ) )
    
    
    return fig_output

if __name__ == '__main__':
    app.run(debug=False, port=8082)
