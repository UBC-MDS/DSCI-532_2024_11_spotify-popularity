from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import ast

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
tracks_df = pd.read_csv('data/raw/tracks_processed.csv')


# convert stringified lists into actual lists
def convert_string_to_list(string):
    try:
        return ast.literal_eval(string)
    # Return an empty list if the string is not a valid list representation
    except ValueError:
        return []  
        
tracks_df['genres'] = tracks_df['genres'].apply(convert_string_to_list)
unique_genres = sorted(set(genre for sublist in tracks_df['genres'] for genre in sublist))
genre_dropdown_options = [{'label': genre, 'value': genre} for genre in unique_genres]

# Configuration
genre_dropdown = dcc.Dropdown(
    options= genre_dropdown_options,
    multi=True,
    placeholder='Select a genre...',
    id='genre-dropdown'
)
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
summary_statistics = dbc.Col([
    html.Label('Song features - Top 5 Popular Songs'),
    html.Br(),
    dbc.Row(
        dbc.Card(id='mean-danceability')
    ),
    dbc.Row(
        dbc.Card(id='mean-energy')
    ),
    dbc.Row(
        dbc.Card(id='mean-loudness')
    ),
    dbc.Row(
        dbc.Card(id='mean-speechiness')
    ),
    dbc.Row(
        dbc.Card(id='mean-acousticness')
    ),
    dbc.Row(
        dbc.Card(id='mean-instrumentalness')
    ),
    dbc.Row(
        dbc.Card(id='mean-liveness')
    ),
    dbc.Row(
        dbc.Card(id='mean-valence')
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
            dbc.CardHeader('Danceability'),
            dbc.CardBody(mean_danceability)
        ]
        card_mean_energy = [
            dbc.CardHeader('Energy'),
            dbc.CardBody(mean_energy)
        ]
        card_mean_loudness = [
            dbc.CardHeader('Loudness'),
            dbc.CardBody(mean_loudness)
        ]
        card_mean_speechiness = [
            dbc.CardHeader('Speechiness'),
            dbc.CardBody(mean_speechiness)
        ]
        card_mean_acousticness = [
            dbc.CardHeader('Acousticness'),
            dbc.CardBody(mean_acousticness)
        ]
        card_mean_instrumentalness = [
            dbc.CardHeader('Instrumentalness'),
            dbc.CardBody(mean_instrumentalness)
        ]
        card_mean_liveness = [
            dbc.CardHeader('Liveness'),
            dbc.CardBody(mean_liveness)
        ]
        card_mean_valence = [
            dbc.CardHeader('Valence'),
            dbc.CardBody(mean_valence)
        ]
        
        return card_mean_danceability, card_mean_energy, card_mean_loudness, card_mean_speechiness, card_mean_acousticness, \
               card_mean_instrumentalness, card_mean_liveness, card_mean_valence

@app.callback(
    Output('artists-dropdown', 'options'),
    [Input('genre-dropdown', 'value')]
)

def update_artist_dropdown(selected_genres):
    if not selected_genres:
        return []
    filtered_artists = tracks_df[tracks_df['genres'].apply(lambda x: any(genre in selected_genres for genre in x))]
    artist_options = [{'label': artist, 'value': artist} for artist in filtered_artists['artist'].unique()]
    return artist_options

# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=False)
