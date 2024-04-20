from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import src.utils as ut
import dash_vega_components as dvc


tracks_df = pd.read_parquet('data/processed/tracks_processed.parquet')

# Configuration
genre_dropdown = dcc.Dropdown(
    options=ut.create_genre_dropdown_options(tracks_df),
    value="pop",
    multi=False,
    placeholder='Select a genre...',
    id='genre-dropdown'
)
artist_dropdown = dcc.Dropdown(
    options=tracks_df['artist'].unique(),
    value=['Taylor Swift', 'Ed Sheeran', 'The Weeknd', 'Justin Bieber'],
    multi=True,
    placeholder='Select multiple artists...',
    id='artists-dropdown'
)
year_range_selector = dbc.Row([
    dbc.Col(
        dcc.Dropdown(
            options=sorted(tracks_df['release_year'].unique()),
            value=2010,
            multi=False,
            placeholder='Select the start year...',
            id='start-year'
        )),
    dbc.Col(
        dcc.Dropdown(
            options=sorted(tracks_df['release_year'].unique()),
            value=2021,
            multi=False,
            placeholder='Select the end year...',
            id='end-year'
        ))
])

optional_artist_selector_dropdown = dcc.Dropdown(
    options=tracks_df['artist'].unique(),
    multi=False,
    placeholder='Select an artist you want to compare...',
    id='artists-dropdown-compare'
)

submit_button = dbc.Button('Plot!', id='submit-button', style={'background-color': '#196543'})

# artist_time_chart = dvc.Vega(id='artist-time-chart', spec={}, opt={'actions': False})
# explicit_chart = dvc.Vega(id='explicit-chart', spec={}, opt={'actions': False})
# top5songs_barchart = dvc.Vega(id='top5songs-barchart', spec={}, opt={'actions': False})
# speechiness_chart = dvc.Vega(id='speechiness-chart', spec={}, opt={'actions': False})

summary_statistics = dbc.Col([
    html.Br(),
    html.H4('Song features (Mean)', className='text-center', style={"color": 'white'}),
    html.H5('Top 5 Popular Songs', id='top-five-title', className='text-center', style={"color": 'white'}),
    dbc.Row([
        dbc.Card(id='mean-danceability', style={"border": 0, "width": "75%"},className="mb-2 mx-auto", outline=True,),
]),
    dbc.Row(
        dbc.Card(id='mean-energy', style={"border": 0, "width": "75%" }, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-loudness', style={"border": 0,"width": "75%"}, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-speechiness', style={"border": 0,"width": "75%"}, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-acousticness', style={"border": 0,"width": "75%"}, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-instrumentalness', style={"border": 0,"width": "75%"}, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-liveness', style={"border": 0,"width": "75%"}, className="mb-2 mx-auto", outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-valence', style={"border": 0,"width": "75%"},className="mb-2 mx-auto", outline=True)
    )
])

milestone_blurb=[
    html.P("This dashboard is designed for helping record companies to make data driven decisions, so that they can provide valuable and actionable suggestions that can be used as guidance for artists aiming to enhance their music's appeal.",
           style={"font-size": "20px"}),
    html.P("Authors: Rachel Bouwer, He Ma, Koray Tecimer, Yimeng Xia",
           style={"font-size": "12px"}),
    html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_11_spotify-popularity",
           target="_blank", style={"font-size": "12px"}),
    html.P("Last deployed on April 6, 2023",
           style={"font-size": "12px"})
           ]


artist_popularity_card = dbc.Card([
    dbc.CardHeader('Artist Popularity Over Time', className='text-center', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='artist-time-chart',
            opt={'actions': False},  # Remove the three dots button

        ),
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }
    )
])

explicit_card = dbc.Card([
    dbc.CardHeader('Mean Popularity of Songs by Type and Artist',  className='text-center',style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='explicit-chart',
            opt={'actions': False},  # Remove the three dots button

        ),
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }
    )
])

top_songs_card = dbc.Card([
    dbc.CardHeader('Popularity of Top Songs',  className='text-center', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='top5songs-barchart',
            opt={'actions': False},  # Remove the three dots button

        ),
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }
    )
])

speechiness_card = dbc.Card([
    dbc.CardHeader('Popularity by Speechiness Over Time', className='text-center', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='speechiness-chart',
            opt={'actions': False},  

        ),
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }
    )
])

plot_layout = html.Div([
    dbc.Row([
        dbc.Col(artist_popularity_card, style={'width': '47%', 'margin-left': '3%'}),
        dbc.Col(explicit_card, style={'width': '47%', 'margin-right': '3%'})
    ]),
    dbc.Row([
        dbc.Col(top_songs_card, style={'width': '47%', 'margin-left': '3%'}),
        dbc.Col(speechiness_card, style={'width': '47%', 'margin-right': '3%'})
    ], style={'margin-top': '0.5%'})
])
