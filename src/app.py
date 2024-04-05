from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
tracks_df = pd.read_csv('../data/raw/tracks_processed.csv')

# Layout
app.layout = dbc.Container([
    html.Title('Spotify Popularity Dashboard'),
    html.Label('Select the artists you want to analyze:'),
    html.Br(),
    dcc.Dropdown(
        options=tracks_df['artist'].unique(),
        multi=True,
        placeholder='Select multiple artists...',
        id='artists-dropdown'
    ),
    html.Label('Select the start and end year for the analysis:'),
    html.Br(),
    dbc.Row([
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
            ))]),
    html.Br(),
    html.Label('Song features - Top 5 Popular Songs'),
    html.Br(),
    html.Label('Mean danceability:'),
    html.Div(id='mean-danceability'),
    html.Label('Mean energy:'),
    html.Div(id='mean-energy'),
    html.Label('Mean loudness:'),
    html.Div(id='mean-loudness'),
    html.Label('Mean speechiness:'),
    html.Div(id='mean-speechiness'),
    html.Label('Mean acousticness:'),
    html.Div(id='mean-acousticness'),
    html.Label('Mean instrumentalness:'),
    html.Div(id='mean-instrumentalness'),
    html.Label('Mean liveness:'),
    html.Div(id='mean-liveness'),
    html.Label('Mean valence:'),
    html.Div(id='mean-valence')
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
        return []
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
        return mean_danceability, mean_energy, mean_loudness, mean_speechiness, mean_acousticness, \
               mean_instrumentalness, mean_liveness, mean_valence


# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=True)
