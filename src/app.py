from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
tracks_df = pd.read_csv('data/raw/tracks_processed.csv')

# Configuration
artist_dropdown = dcc.Dropdown(
    options=tracks_df['artist'].unique(),
    multi=True,
    placeholder='Select multiple artists...',
    id='artists-dropdown'
)
year_range_selector = dbc.Row([
    dbc.Col(
        dcc.Dropdown(
            options=sorted(tracks_df['release_year'].unique()),
            multi=False,
            placeholder='Select the start year...',
            id='start-year'
        )),
    dbc.Col(
        dcc.Dropdown(
            options=sorted(tracks_df['release_year'].unique()),
            multi=False,
            placeholder='Select the end year...',
            id='end-year'
        ))
])
summary_statistics = html.Div([
    html.Br(),
    html.H4('Song features (Mean)', className='text-center'),
    html.H5('Top 5 Popular Songs', className='text-center'),
    dbc.Row(
        dbc.Card(id='mean-danceability', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-energy', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-loudness', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-speechiness', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-acousticness', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-instrumentalness', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-liveness', style={"border": 0, "color" : "#1db954"}, outline=True)
    ),
    dbc.Row(
        dbc.Card(id='mean-valence', style={"border": 0, "color" : "#1db954"}, outline=True)
    )
])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        html.Title('Spotify Popularity Dashboard'),
        html.Label('Select the artists you want to analyze:'),
        html.Br(),
        artist_dropdown,
        html.Label('Select the start and end year for the analysis:'),
        html.Br(),
        year_range_selector,
        html.Br()
    ]),
    dbc.Row([
        dbc.Col(
            html.Label('Plots will go here')
        ),
        dbc.Col(
            summary_statistics, width=3
        )
    ])
])

@app.callback(
    [Output('mean-danceability', 'children'),
     Output('mean-energy', 'children'),
     Output('mean-loudness', 'children'),
     Output('mean-speechiness', 'children'),
     Output('mean-acousticness', 'children'),
     Output('mean-instrumentalness', 'children'),
     Output('mean-liveness', 'children'),
     Output('mean-valence', 'children')],
    [Input('artists-dropdown', 'value'),
     Input('start-year', 'value'),
     Input('end-year', 'value')]
)
def display_artist_tracks(selected_artists, start_year, end_year):
    if selected_artists is None or start_year is None or end_year is None:
        return "", "", "", "", "", "", "", ""
    else:
        tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)]
        tracks_df_filtered_top_five = tracks_df_filtered.sort_values('popularity', ascending=False).iloc[:5]

        mean_danceability = "{:.3g}".format(tracks_df_filtered_top_five['danceability'].mean())
        mean_energy = "{:.3g}".format(tracks_df_filtered_top_five['energy'].mean())
        mean_loudness = "{:.3g}".format(tracks_df_filtered_top_five['loudness'].mean())
        mean_speechiness = "{:.3g}".format(tracks_df_filtered_top_five['speechiness'].mean())
        mean_acousticness = "{:.3g}".format(tracks_df_filtered_top_five['acousticness'].mean())
        mean_instrumentalness = "{:.3g}".format(tracks_df_filtered_top_five['instrumentalness'].mean())
        mean_liveness = "{:.3g}".format(tracks_df_filtered_top_five['liveness'].mean())
        mean_valence = "{:.3g}".format(tracks_df_filtered_top_five['valence'].mean())

        card_mean_danceability = [
            dbc.CardHeader('Danceability', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_danceability, className='text-center')
        ]
        card_mean_energy = [
            dbc.CardHeader('Energy', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_energy, className='text-center')
        ]
        card_mean_loudness = [
            dbc.CardHeader('Loudness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_loudness, className='text-center')
        ]
        card_mean_speechiness = [
            dbc.CardHeader('Speechiness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_speechiness, className='text-center')
        ]
        card_mean_acousticness = [
            dbc.CardHeader('Acousticness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_acousticness, className='text-center')
        ]
        card_mean_instrumentalness = [
            dbc.CardHeader('Instrumentalness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_instrumentalness, className='text-center')
        ]
        card_mean_liveness = [
            dbc.CardHeader('Liveness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_liveness, className='text-center')
        ]
        card_mean_valence = [
            dbc.CardHeader('Valence', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_valence, className='text-center')
        ]
        
        return card_mean_danceability, card_mean_energy, card_mean_loudness, card_mean_speechiness, card_mean_acousticness, \
               card_mean_instrumentalness, card_mean_liveness, card_mean_valence


# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=False)
