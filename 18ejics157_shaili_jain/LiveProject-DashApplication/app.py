import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime
import numpy as np

raw_data=requests.get("https://api.covid19india.org/data.json")
data_json=raw_data.json()
#print(data_json.keys())
covid=pd.DataFrame(data_json['statewise'])

#converting the object datatype into numeric data type
covid.active=pd.to_numeric(covid.active,errors="coerce")
covid.confirmed=pd.to_numeric(covid.confirmed,errors="coerce")
covid.deaths=pd.to_numeric(covid.deaths,errors="coerce")
covid.deltaconfirmed=pd.to_numeric(covid.deltaconfirmed,errors="coerce")
covid.deltadeaths=pd.to_numeric(covid.deltadeaths,errors="coerce")
covid.deltarecovered=pd.to_numeric(covid.deltarecovered,errors="coerce")
covid.migratedother=pd.to_numeric(covid.migratedother,errors="coerce")
covid.recovered=pd.to_numeric(covid.recovered,errors="coerce")

# now i will calculate the total cases in india
#The sum method will total up all the values in each of the four columns and assigned the final sum to their respective variables total_active, total_confirmed, total_recovered, and total_deaths.
total_active=covid['active'].sum()-covid['active'][0]
total_confirmed=covid['confirmed'].sum()-covid['confirmed'][0]
total_deaths=covid['deaths'].sum()-covid['deaths'][0]
total_recovered=covid['recovered'].sum()-covid['recovered'][0]

# now we will list the top 10 states for confirmed, deaths, recovered,active cases

#for confirmed cases
top10_covid=covid.nlargest(11,'confirmed')
top10_states_confirm=top10_covid['state'].tolist()
top10_confirmed=top10_covid['confirmed'].tolist()
top10_states_confirm.remove('Total')
top10_confirmed.remove(max(top10_confirmed))

#for active cases
top10_covid=covid.nlargest(10,'active')
top10_states_active=top10_covid['state'].tolist()
top10_active=top10_covid['active'].tolist()
top10_states_active.remove('Total')
top10_active.remove(max(top10_active))


#for recovered cases
top10_covid=covid.nlargest(10,'recovered')
top10_states_recovered=top10_covid['state'].tolist()
top10_recovered=top10_covid['recovered'].tolist()
top10_states_recovered.remove('Total')
top10_recovered.remove(max(top10_recovered))


#for death
top10_covid=covid.nlargest(10,'deaths')
top10_states_deaths=top10_covid['state'].tolist()
top10_death=top10_covid['deaths'].tolist()
top10_states_deaths.remove('Total')
top10_death.remove(max(top10_death))

longitu={
    
    78.9629:"TT",
    73.16017493:"MH",
    79.15004187:"TN",
    77.23000403:"DL",
    71.1924:"GJ",
    78.05000565:"UP",
    74.63998124:"RJ",
    76.13001949:"MP",
    88.32994665:"WB",
    80.9629:"UN",
    76.91999711:"KA",
    77.01999101:"HR",
    87.4799727:"BR",
    78.57002559:"AP",
    74.46665849:"JK",
    79.0194:"TG",
    85.90001746:"OR",
    94.21666744:"AS",
    75.98000281:"PB",
    76.56999263:"KL",
    79.0193:"UT",
    86.41998572:"JH",
    82.15998734:"CT",
    91.27999914:"TR",
    77.16659704:"HP",
    73.81800065:"GA",
    93.95001705:"MN",
    76.78000565:"CH",
    79.83000037:"PY",
    77.577049:"LA",
    94.11657019:"NL",
    92.72001461:"MZ",
    93.61660071:"AR",
    91.8800142:"ML",
    92.73598262:"AN",
    73.0166178:"DN",
    88.6166475:"SK",
    72.63686717:"LD"
}

covid["long"]=longitu

lat={
    20.5937:"TT",
    19.25023195:"MH",
    12.92038576:"TN",
    28.6699929:"DL",
    22.2587:"GJ",
    27.59998069:"UP",
    26.44999921:"RJ",
    21.30039105:"MP",
    22.58039044:"WB",
    22.58753:"UN",
    12.57038129:"KA",
    28.45000633:"HR",
    25.78541445:"BR",
    14.7504291:"AP",
    34.29995933:"JK",
    18.1124:"TG",
    19.82042971:"OR",
    26.7499809:"AS",
    31.51997398:"PB",
    8.900372741:"KL",
    30.32040895:"UT",
    23.80039349:"JH",
    22.09042035:"CT",
    23.83540428:"TR",
    31.10002545:"HP",
    15.491997:"GA",
    24.79997072:"MN",
    30.71999697:"CH",
    11.93499371:"PY",
    34.209515:"LA",
    25.6669979:"NL",
    23.71039899:"MZ",
    27.10039878:"AR",
    25.57049217:"ML",
    11.66702557:"AN",
    20.26657819:"DN",
    27.3333303:"SK",
    10.56257331:"LD"
}

covid["lat"]=lat

message = covid["state"]  + "<br>"
message += "Confirmed: " + covid["confirmed"].astype(str) + "<br>"
message += "Deaths: " + covid["deaths"].astype(str) + "<br>"
message += "Recovered: " + covid["recovered"].astype(str) + "<br>"
message += "Active: " + covid["active"].astype(str) + "<br>"
message += "Last updated: " + covid["lastupdatedtime"].astype(str)
covid["text"] = message

#subplots
fig = make_subplots(
    rows = 4, cols = 6,
    specs=[
            [{"type": "scattergeo", "rowspan": 4, "colspan": 3}, None, None,{"type": "scatter", "colspan":2}, None, {"type": "indicator","rowspan": 1, "colspan": 1}],
            [    None, None, None,               {"type": "scatter", "colspan":2}, None,{"type": "indicator","rowspan": 1, "colspan": 1}],
            [    None, None, None,              {"type": "scatter", "colspan":2}, None, {"type": "indicator","rowspan": 1, "colspan": 1}],
            [  None, None, None,  None, None,    {"type": "indicator","rowspan": 1, "colspan": 1}],
          ]
)


fig.add_trace(
    go.Scattergeo(
        #locations=["India"],
        locationmode = "country names",
        lon = covid["long"],
        lat = covid["lat"],
        hovertext = covid["text"],
        showlegend=False,
        marker = dict(
            size = 10,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            cmin = 0,
            color = covid['confirmed'],
            cmax = covid['confirmed'].max(),
            colorbar_title="Confirmed Cases<br>Latest Update",  
            colorbar_x = -0.05
        )

    ),
    
    row=1, col=1
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_confirmed,
        title="Confirmed",
    ),
    row=1, col=6
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_recovered,
        title="Recovered",
    ),
    row=2, col=6
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_active,
        title="Active",
    ),
    row=3, col=6
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_deaths,
        title="Deaths",
    ),
    row=4, col=6
)

fig.add_trace(
    go.Scatter(
        x=top10_states_confirm,
        y=top10_confirmed, 
        name= "Confirmed Cases",
        marker=dict(color="Orange"), 
        showlegend=True,
    ),
    row=1, col=4
)

fig.add_trace(
    go.Scatter(
        x=top10_states_recovered,
        y=top10_recovered, 
        name= "Recovered Cases",
        marker=dict(color="Green"), 
        showlegend=True),
    row=2, col=4
)

fig.add_trace(
    go.Scatter(
        x=top10_states_deaths,
        y=top10_death, 
        name= "Deaths Cases",
        marker=dict(color="crimson"), 
        showlegend=True),
    row=3, col=4
)

fig.update_layout(
    template="plotly_dark",
    title = "COVID-19 INDIA Cases (Last Updated: " + str(covid["lastupdatedtime"][0]) + ")",
    showlegend=False,
    legend_orientation="h",
    legend=dict(x=0.65, y=0.8),
    geo = dict(
            projection_type="natural earth",
            showcoastlines=True,
            landcolor="LightGreen", 
            showland= True,
            showocean = True,
            lakecolor="LightBlue"
    ),

    annotations=[
        dict(
            text="Source: https://api.covid19india.org/",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.35,
            y=0)
    ]
)
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(style={'textAlign': 'Center'},  children=[
    
    dcc.Graph(
        style={"height":"100vh"} , 
        figure=fig,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)