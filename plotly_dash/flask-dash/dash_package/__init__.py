from flask import Flask
import dash
<<<<<<< HEAD
<<<<<<< HEAD
import dash_bootstrap_components as dbc
=======
>>>>>>> refs/remotes/origin/master
=======
>>>>>>> refs/remotes/origin/master

server = Flask(__name__)

server.config['DEBUG'] = True

<<<<<<< HEAD
<<<<<<< HEAD
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, server=server,external_stylesheets=[external_stylesheets], assets_folder='templates' ,url_base_pathname='/dash/')
=======
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
>>>>>>> refs/remotes/origin/master
=======
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
>>>>>>> refs/remotes/origin/master
app.config['suppress_callback_exceptions']=True

from dash_package import routes
