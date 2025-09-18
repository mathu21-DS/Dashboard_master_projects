README

Our code package can scrape the Guardian API for articles with a chosen tag and display a UI to interact with the scraped articles. 
You need all files in the same folder. 
The user-interface is loaded by running the dash_guardian program. 
The folder contains an example webscrape as .csv that is ready for use immediately in the dash_guardian program.
The user can also do their own webscrape with the webscraping_guardian program.

What each file does:

webscraping_guardian: 
Contains a function for scraping the Guardian API by a chosen keyword that looks for matching tags. 
The function is called at the end of the code, where you can insert the parameters. 
The parameter 'pages' scrapes 200 articles per page. For example, a selection of 5 will result in 1000 articles.
You can insert your own Guardian API-key as a parameter in the function call.
The function creates a csv-file named Articles_(keyword).csv

text_g: 
The code builds a dictionary from the scraped articles.
This document will be imported to the dash/plotly document.

dash_guardian:
This program builds a user-interface to interact with the data. 
The document "text_g" is called and must be in the same folder.

Articles_Denmark.csv:
This csv-file contains a scrape of 1000 articles with the tag 'Denmark'. It is ready for use by the Dash/Plotly program.
We recommend renaming the file or placing it in a different folder before doing another scrape for articles with the same tag.