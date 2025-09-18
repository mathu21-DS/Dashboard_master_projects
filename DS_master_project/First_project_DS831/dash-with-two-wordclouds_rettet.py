# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:28:29 2022

@author: Margrethe, Esben, Benjamin & Yousef
"""

#Importing packages 
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import dash.dependencies as dd
import plotly.graph_objs as go
import random
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table as dt
import text_g
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import base64
from io import BytesIO

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
    html.Label('Wordcloud of all articles with selected tag',
               style = {'font-size': '35px'}),                                  #set the size of the font
    html.Div([    
        html.Img(id="image_wc")
        
    ]),
    html.Label('Frequency of tag over time', style = {'font-size': '35px'}),
    html.Div([
            dcc.Graph(id ='word-distribution-bar', figure="fig")
    ]),
    html.Label('Choose a minimum number of related tags to find similar articles', 
               style = {'font-size': '35px'}),
    html.Br(),                                                                  #it seperate the to text from each other
    html.Div([
         html.Label('Text Input'),
        dcc.Input(
            id="tekstinput", 
            value="'Norway'", type='text')
    ]),
            html.Div([
         html.Label('Choose a Minimum number of tags:'),
        dcc.Input(
            id="minimum", 
            value=2, type='text')
    ]),
    html.Div([
                    dt.DataTable(
                    id='table',
                    data=text_g.text2.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in text_g.text2.columns],
                    style_table={'overflowX':'scroll',
                                 'maxHeight':'300px',"maxWidth":"1200px"},
                    style_header={'backgroundColor':'darkslateblue'},
                    style_cell={'text-align': 'left', 'backgroundColor':'#041f4a'},
                    sort_by=[],
                    fill_width=False
                    ),
                    ],
                style={"display": "flex", "justifyContent": "center","marginBottom":50}),
        html.Label('Similar articles', style = {'font-size': '35px'}),
        html.Div([
            dt.DataTable(
                    id='table2',
                    data=text_g.text3.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in text_g.text3.columns],
                    style_table={'overflowX':'scroll',
                                 'maxHeight':'300px',"maxWidth":"1200px"},
                    style_header={'backgroundColor':'darkslateblue'},
                    style_cell={'text-align': 'left', 'backgroundColor':'#041f4a'},
                    sort_by=[],
                    fill_width=False
                    ),
                    ],
                style={"display": "flex", "justifyContent": "center","marginBottom":50}),
        html.Div(id="output-div2", style = {
                                            'line-height': '1.8',
                                            'border': '2px solid black',
                                            'outline-style': 'solid',
                                            'outline-color': 'orange'}),
        html.Label('Contents of Article', style = {'font-size': '35px'}),
        html.Div(id="output-div", style = {
                                            'line-height': '1.8',
                                            'border': '2px solid black',
                                            'outline-style': 'solid',
                                            'outline-color': 'orange'}),
         
])
    
#Function to generate wordcloud
def display_wordcloud2(choices_tag):
    text_g.text1["Text"] = text_g.text1["Text"].astype("string")
    wc_text = ""
    for row in text_g.text1.itertuples():
        if choices_tag in row[4]:               
            # wc_text += row[5] # adds the text body
            wc_text += row[2] # adds the title
            
    stopwords = set(STOPWORDS)
    stopwords.add("said")
    stopwords.add("will")     
    stopwords.add("S")
    stopwords.add("s")         
            
    wordcloud = WordCloud(max_words=300, width=1080, height=720, stopwords=stopwords, background_color="white").generate(wc_text)
    return wordcloud.to_image()

@app.callback(
    Output(component_id = 'word-cloud', component_property ='figure'),
    Input(component_id ='tags-number', component_property = 'value'))
def display_wordcloud(choices_tag):
    liste1 = []
    for row in text_g.text1.itertuples():
        if choices_tag in row[4]:         
            liste1.append(row[2])
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


#Callback to display the wordcloud
@app.callback(dd.Output('image_wc', 'src'), [dd.Input('tags-number', 'value')])
def make_image(choices_tag):    
    img = BytesIO()    
    display_wordcloud2(choices_tag).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


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
            if choices_tag not in row[4]:
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
    Output(component_id='table', component_property='data'),
    Input(component_id="tekstinput", component_property='value'))
def change_table(word):
    if word!=None:
        liste=[]
        liste2=[]
        for row in text_g.text1.itertuples():
            if word in row[4] or word in str(row[5]):
                liste.append(row[2])
                liste2.append(row[4])
        dic={"name":liste, "Tags":liste2}
        df=pd.DataFrame(dic)
        return df.to_dict('records')
    else:
        return text_g.text2.to_dict('records')

@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id="table", component_property='active_cell'),
    Input(component_id="table",component_property="data"))
def get_article(active_cell, data):
    artikeltekst=[]
    if active_cell!=None:
        chosenrow=active_cell["row"]
        both=data[chosenrow]["name"]
        for row in text_g.text1.itertuples():
            if both==row[2]:
                artikeltekst.append(row[5])
        return(artikeltekst)
    else:
        return('no cell selected')


@app.callback(
    Output(component_id='table2', component_property='data'),
    Input(component_id="table", component_property='active_cell'),
    Input(component_id="table",component_property="data"),
    Input(component_id="minimum",component_property="value"))
def forslag(artikelnavn, tags, minimum):
    
    liste_af_forslag=[]
    if artikelnavn!=None:
        chosenrow=artikelnavn["row"]
        chosenarticle_tags=tags[chosenrow]["Tags"]
        chosenname=tags[chosenrow]["name"]
        checkliste_tags=chosenarticle_tags.replace("[","").replace("]","").split(",")
        for row in tags:
            if len(liste_af_forslag)==4:
                break
            else:
                counter=0
                for enkelte_tags in checkliste_tags:
                    if enkelte_tags in row["Tags"]:
                        counter+=1
                        if counter==int(minimum) and chosenname!=row["name"]:
                            liste_af_forslag.append(row["name"])
        dic={"name":liste_af_forslag}
        df=pd.DataFrame(dic)
        
        return(df.to_dict('records'))
@app.callback(
    Output(component_id='output-div2', component_property='children'),
    Input(component_id="table2", component_property='active_cell'),
    Input(component_id="table2",component_property="data"))
def get_article2(active_cell, data):
    artikeltekst=[]
    if active_cell!=None:
        chosenrow=active_cell["row"]
        both=data[chosenrow]["name"]
        for row in text_g.text1.itertuples():
            if both==row[2]:
                artikeltekst.append(row[5])
        return(artikeltekst)
    else:
        return('no cell selected')


if __name__ == '__main__':
    app.run_server(debug=False, port=8080)