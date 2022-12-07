from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd

from numpy import ceil

start_data = pd.read_csv('crimedata.csv')

start_data['all_crimes'] = start_data['murders'] + start_data['rapes'] + \
                           start_data['robberies'] + start_data['assaults'] + \
                           start_data['burglaries'] + start_data['larcenies'] + \
                           start_data['autoTheft'] + start_data['arsons']

start_data['young'] = ceil(start_data.agePct12t29 * start_data.population / 100)
start_data['old'] = ceil(start_data.agePct65up * start_data.population / 100)
start_data['unemployed'] = ceil(start_data.PctUnemployed * start_data.population / 100)
start_data['unmarried'] = ceil((start_data.MalePctDivorce + start_data.MalePctNevMarr) * start_data.population / 100)

updated_crime_data = start_data.groupby(["state"]).agg({"young": "sum", "old": "sum",
                                                        "unemployed": "sum", "unmarried": "sum", "all_crimes": "sum",
                                                        "population": "sum", "murders": "sum",
                                                        "rapes": "sum", "robberies": "sum", "burglaries": "sum",
                                                        "autoTheft": "sum", "arsons": "sum"}).reset_index()

updated_crime_data['young_pct'] = updated_crime_data.young / start_data.population
updated_crime_data['old_pct'] = updated_crime_data.old / start_data.population
updated_crime_data['unemployed_pct'] = updated_crime_data.unemployed / start_data.population
updated_crime_data['unmarried_pct'] = updated_crime_data.unmarried / start_data.population


def update_data(population, young, old, unemployed, unmarried):
    cur_data = updated_crime_data[updated_crime_data.population <= population]
    cur_data = cur_data[cur_data.young_pct <= young]
    cur_data = cur_data[cur_data.old_pct <= old]
    cur_data = cur_data[cur_data.unemployed_pct <= unemployed]
    cur_data = cur_data[cur_data.unmarried_pct <= unmarried]
    cur_data = cur_data.sort_values('population')
    return cur_data


app = Dash(__name__)

app.layout = html.Div([

    html.Div("Choose max state population"),
    html.Div(dcc.Slider(
        min=1e6,
        max=25e6,
        id='population_slider',
        value=125e5
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px'}),

    html.Div("Choose the max percent of young population of the state"),
    html.Div(dcc.Slider(
        min=0,
        max=100,
        id='young_slider',
        value=50
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px'}),

    html.Div("Choose the max percent of old population of the state"),
    html.Div(dcc.Slider(
        min=0,
        max=100,
        id='elder_slider',
        value=50
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px'}),

    html.Div("Choose the max percent of unemployed population of the state"),
    html.Div(dcc.Slider(
        min=0,
        max=100,
        id='unemployed_slider',
        value=50
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px'}),

    html.Div("Choose the max percent of unmarried men population of the state"),
    html.Div(dcc.Slider(
        min=0,
        max=100,
        id='unmarried_men_slider',
        value=50
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px'}),

    html.Div([
        dcc.Graph(
            id='total_crimes'
        )
    ], style={}),

    html.Div([
        dcc.Graph(
            id='robberies'
        )
    ], style={}),

    html.Div([
        dcc.Graph(
            id='rapes'
        )
    ], style={}),

    html.Div([
        dcc.Graph(
            id='autothefts'
        )
    ], style={}),

    html.Div([
        dcc.Graph(
            id='arsons'
        )
    ], style={})
])


@app.callback(
    Output('total_crimes', 'figure'),
    Input('population_slider', 'value'),
    Input('young_slider', 'value'),
    Input('elder_slider', 'value'),
    Input('unemployed_slider', 'value'),
    Input('unmarried_men_slider', 'value'))
def update_graph(population,
                 young, old, unemployed, unmarried):
    cur_data = update_data(population, young, old, unemployed, unmarried)

    fig = go.Figure(data=go.Scatter(x=cur_data["population"], y=cur_data["all_crimes"]),
                    layout=go.Layout(title="Dependence of quantity of crimes on state population", title_x=0.5,
                                     xaxis_title="Population",
                                     yaxis_title="Crimes count"))
    return fig


@app.callback(
    Output('robberies', 'figure'),
    Input('population_slider', 'value'),
    Input('young_slider', 'value'),
    Input('elder_slider', 'value'),
    Input('unemployed_slider', 'value'),
    Input('unmarried_men_slider', 'value'))
def update_graph(population,
                 young, old, unemployed, unmarried):
    cur_data = update_data(population, young, old, unemployed, unmarried)

    fig = go.Figure(data=go.Scatter(x=cur_data["population"], y=cur_data["robberies"]),
                    layout=go.Layout(title="Dependence of quantity of robberies count on state population", title_x=0.5,
                                     xaxis_title="Population",
                                     yaxis_title="Robberies count"))
    return fig


@app.callback(
    Output('rapes', 'figure'),
    Input('population_slider', 'value'),
    Input('young_slider', 'value'),
    Input('elder_slider', 'value'),
    Input('unemployed_slider', 'value'),
    Input('unmarried_men_slider', 'value'))
def update_graph(population,
                 young, old, unemployed, unmarried):
    cur_data = update_data(population, young, old, unemployed, unmarried)

    fig = go.Figure(data=go.Scatter(x=cur_data["population"], y=cur_data["rapes"]),
                    layout=go.Layout(title="Dependence of quantity of rapes count on state population", title_x=0.5,
                                     xaxis_title="Population",
                                     yaxis_title="Rapes count"))
    return fig


@app.callback(
    Output('autothefts', 'figure'),
    Input('population_slider', 'value'),
    Input('young_slider', 'value'),
    Input('elder_slider', 'value'),
    Input('unemployed_slider', 'value'),
    Input('unmarried_men_slider', 'value'))
def update_graph(population,
                 young, old, unemployed, unmarried):
    cur_data = update_data(population, young, old, unemployed, unmarried)

    fig = go.Figure(data=go.Scatter(x=cur_data["population"], y=cur_data["autoTheft"]),
                    layout=go.Layout(title="Dependence of quantity of autothefts count on state population",
                                     title_x=0.5,
                                     xaxis_title="Population",
                                     yaxis_title="Autothefts count"))
    return fig


@app.callback(
    Output('arsons', 'figure'),
    Input('population_slider', 'value'),
    Input('young_slider', 'value'),
    Input('elder_slider', 'value'),
    Input('unemployed_slider', 'value'),
    Input('unmarried_men_slider', 'value'))
def update_graph(population,
                 young, old, unemployed, unmarried):
    cur_data = update_data(population, young, old, unemployed, unmarried)

    fig = go.Figure(data=go.Scatter(x=cur_data["population"], y=cur_data["arsons"]),
                    layout=go.Layout(title="Dependence of quantity of arsons count on state population", title_x=0.5,
                                     xaxis_title="Population",
                                     yaxis_title="Arsons count"))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
