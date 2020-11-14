# google-analytics-ETL-use-case

I present here a case study allowing to visualize the traffic volumes on a website on two graphs according to the hours of the day and the days of the week. To this is added the variable origin of the user which allows to know from which other website the visitor comes. Data is collected for the last seven days prior to the time of execution.

The program takes as input a GCP service account file and the ID of a google analytics view (We will see in the next how to obtain the two preceding elements) and returns as output the two charts mentioned above.

## Before coding
To be able to extract data from google analytics it is essential that you have three things: A website, a google Analytics account on which the website is registered and a GCP service account file.

Indeed, for google to collect traffic data on your site, you must add a tracker to your site that it provides to you. https://support.google.com/analytics/answer/1008015 

then you can note your viewID of the view created by default by going to http://analytics.google.com/ > admin tab >  view tab

And then to be able to request the data you must with the same google mail:
 - create a GCP account
 - create a GCP project
 - Activate API Google Analytics Reporting
 - Create the service account and download the JSON file
All this is well explained here: https://support.google.com/cloudidentity/answer/7378726 


## Make way for code.

### prerequisite
have git installed
have python3.x and pip3 installed

After cloning, please install the dependencies via the command pip3 install -r requirements.txt this being done you can already run the application and do some tests.

### project structure
The project is structured as follows:
root/
    App.py
    MainMenu.py
    StartPage.py
    FinalPage.py
    googleAnalyticsTools/
        GAExplorer.py

### Using Tkinter for interface

The files App.py, MainMenu.py, StartPage.py, FinalPage.py are mainly dedicated to the development of the graphical interface. We will not dwell on this aspect here. 

### The data collector-extractor: The GAExplorer.py file

This is where we request the Google Analytics Reporting API using the GCP service account JSON file and view ID.

Function initialize_analyticsreporting  returns an object authorized to query the Analytics Reporting V4 API for the service account linked to the json.

Function get_report returns a json in response to an API request. It takes as input the object authorized to request the API, the time interval for which we want the report, the metrics, and the dimensions. A good tool to simulate the API is the Query Explorer https://ga-dev-tools.appspot.com/query-explorer/ 

Functions **week_report_by_days** et **week_report_by_hours** use the previous one by defining the appropriate metrics and dimensions. Indeed the first recovers the number of user sessions according to the days and the origin, the second does it according to the hours of the day and the origin; under this on the seven days preceding the time of execution. Then, they transform the received JSON into an easily exploitable dictionary in python.  

### The FinalPage.py file
This is where the graphics are displayed. Functions matplotCanvasDays and matplotCanvasHours respectively call on the last two previously mentioned and use the dictionaries to build the graphics via the matplotlib library.

Resources:

1 - Analytics Academy  https://analytics.google.com/analytics/academy/
2 - openclassrooms
Apprenez à programmer en Python https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python 
Perfectionnez-vous en Python https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python 
3 - Parwiz Forogh https://www.youtube.com/playlist?list=PL1FgJUcJJ03sm4WuVCPMbT0RIf2uMmoAj 
