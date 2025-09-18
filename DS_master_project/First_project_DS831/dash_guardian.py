# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:13:45 2021

@author: Margrethe, Esben, Benjamin & Yousef
"""

#Importing packages 
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.graph_objs as go
import random
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table as dt
import text_g

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.VAPOR])


app.layout = html.Div([
    html.H1(children = 'A Quantitative Analysis of news articles',
            style = {'textAlign':'center',                                      #Set the text to be alignmented to the center 
                     'font-family' : 'Roboto',                                  #choose what type the text could be
                     "color":"white"}),                                         #Set color the text could be
    html.Div([
        dcc.Dropdown(
            id = 'tags-number',
            options = [{'label': i, 'value': i} for i in text_g.key_values.keys()],   #label show what the user see and value is what behind the label. Here is label and value the same
            value = "Brexit",                                                         #what tag the dropdown begin with 
            style = {'width':'50%',                                                   #it only occupies 50% of the area
                   'margin':'auto',                                                   #Using margin:auto to center a block element horizontally is a well known technique.
                   "color":"black"}
        ),
    ]),
    html.Label('Articles containing your tag in a word cloud',
               style = {'font-size': '35px'}),                                  #set the size of the font
    html.Div([
            dcc.Graph(id = 'word-cloud')
    ]),
    html.Label('Frequency of tag over time', style = {'font-size': '35px'}),
    html.Div([
            dcc.Graph(id ='word-distribution-bar', figure="fig")
    ]),
    html.Label('Choose a minimum number of related tags to find similar articles', 
               style = {'font-size': '35px'}),
    html.Br(),                                                                  #it seperate the to text from each other
    html.Div([
         html.Label('Input tag'),
        dcc.Input(                                                              #input with a custom message in the box
            id = "textinput", 
            value = "'Norway'", type='text')                                      #Can only write strings in the box
    ]),
            html.Div([
         html.Label('Choose a Minimum number of tags:'),
        dcc.Input(
            id = "minimum", 
            value=2, type='text')
    ]),
    html.Div([
                    dt.DataTable(
                    id='table',
                    data = text_g.text2.to_dict('records'),
                    columns = [{'name': i, 'id': i} for i in text_g.text2.columns],
                    style_table = {'overflowX':'scroll',                          #The content is clipped and a scrolling mechanism is provided
                                 'maxHeight':'300px',"maxWidth":"1200px"},
                    style_header = {'backgroundColor':'darkslateblue'},
                    style_cell = {'text-align': 'left', 'backgroundColor':'#041f4a'},
                    sort_by=[],
                    fill_width = False
                    ),
                    ],
                style = {"display": "flex", "justifyContent": "center","marginBottom":50}),
        html.Label('Similar articles', style = {'font-size': '35px'}),
        html.Div(id = "Proposals", style = {"whiteSpace":"pre-line", 'border': '2px solid orange'}),
        html.Label('Contents of Article', style = {'font-size': '35px'}),
        html.Div(id = "output-div", style = {
                                            'line-height': '1.8',
                                            'border': '2px solid black',
                                            'outline-style': 'solid',
                                            'outline-color': 'orange'}),
])

@app.callback(
    Output(component_id = 'word-cloud', component_property ='figure'),
    Input(component_id ='tags-number', component_property = 'value'))
def display_wordcloud(choices_tag):
    liste1 = []
    for tag, articles in text_g.key_values.items():
        if tag == choices_tag:
            liste1.extend(articles)
    x = random.choices(range(100*len(liste1)), k=len(liste1))
    y = random.choices(range(100*len(liste1)), k=len(liste1))
    print(liste1,flush=True)
    data = go.Scatter(x = x,
                     y = y,
                     mode ='text',
                     text = liste1,
                     marker = {'opacity': 0.8},
                     textfont = {'size': 15 , 'color':"black"})
    layout = go.Layout({"paper_bgcolor":"rgba(0,0,0,0)",'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'height': 1000})
    return go.Figure(data = [data], layout = layout)

@app.callback(
    Output(component_id = 'word-distribution-bar', component_property = 'figure'),
    Input(component_id = "tags-number", component_property = 'value'))

def display_word_bar(choices_tag):
    #Convert from string to datetime and keeps only the year and month
    text_g.text1['Timeline'] = pd.to_datetime(text_g.text1['Timeline'])
    text_g.text1['Timeline'] = text_g.text1['Timeline'].dt.strftime('%Y-%m')
    
    dicto={}
    
    for row in text_g.text1.itertuples():
        if choices_tag in row[4]:
            if len(row[3]) == 7: #ensures only dates are taken
                if row[3]not in dicto.keys():
                    dicto[row[3]] = 1 #adds the date
                else:
                    dicto[row[3]]+=1
        else:
            if 'Denmark' not in row[4]:
                if row[3]not in dicto.keys(): 
                    dicto[row[3]] = 0
            
    df2 = pd.DataFrame(dicto.items(), columns=['Date', 'DateValue']) # convert the 'Date' column to datetime format
    df2['Date'] = pd.to_datetime(df2['Date'])
    df3 = df2.sort_values(by=['Date'], ascending=True)

    trace_1 = go.Scatter(x = df3.Date, y = df3['DateValue'],
                          name = 'Frequencies of tags',
                          line = dict(width = 2,
                                      color = 'rgb(229, 151, 50)'))
    layout = go.Layout(title = 'Time Chart',
                        hovermode = 'closest',
                        paper_bgcolor=("rgba(150, 111, 214,1)"))
    fig = go.Figure(data = [trace_1], layout = layout)
    return fig

@app.callback(
    Output(component_id ='table', component_property = 'data'),
    Input(component_id = "textinput", component_property = 'value'))
def change_table(word):
    if word!=None:
        liste = []
        liste2 = []
        for row in text_g.text1.itertuples():
            if word in row[4] or word in str(row[5]):
                liste.append(row[2])
                liste2.append(row[4])
        dic = {"name":liste, "Tags":liste2}
        df = pd.DataFrame(dic)
        return df.to_dict('records')
    else:
        return text_g.text2.to_dict('records')

@app.callback(
    Output(component_id = 'output-div', component_property = 'children'),
    Input(component_id = "table", component_property = 'active_cell'),
    Input(component_id = "table",component_property = "data"))

def get_article(active_cell, data):
    article_text = []
    if active_cell!=None:
        chosen_row = active_cell["row"]
        both = data[chosen_row]["name"]
        for row in text_g.text1.itertuples():
            if both == row[2]:
                article_text.append(row[5])
        return(article_text)
    else:
        return('no cell selected')
    
@app.callback(
    Output(component_id = 'Proposals', component_property ='children'),
    Input(component_id = "table", component_property = 'active_cell'),
    Input(component_id = "table",component_property = "data"),
    Input(component_id = "minimum",component_property = "value"))

def proposals(article_name, tags, minimum):

    list_of_proposals = []
    if article_name!=None:
        chosen_row1 = article_name["row"]
        chosen_article_tags = tags[chosen_row1]["Tags"]
        chosen_name = tags[chosen_row1]["name"]
        checkliste_tags = chosen_article_tags.replace("[","").replace("]","").split(",")
        
        for row in tags:
            if len(list_of_proposals) == 4:
                break
            else:
                counter=0
                for single_tags in checkliste_tags:
                    if single_tags in row["Tags"]:
                        counter+=1
                        if counter == int(minimum) and chosen_name != row["name"]:
                            list_of_proposals.append(row["name"])

        return([i+"\n" for i in list_of_proposals])
    else:
        return("")

if __name__ == '__main__':
    app.run_server(debug=False, port=8080)