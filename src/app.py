from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
tracks_df = pd.read_csv('data/raw/tracks_processed.csv')

# Configuration
title= [html.H1('Spotify Popularity Dashboard'), html.Br()]
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
bottom_blub=[
    html.P("This dashboard is designed for helping record companies to make data driven decisions, so that they can provide valuable and actionable suggestions that can be used as guidance for artists aiming to enhance their music's appeal.",
           style={"font-size": "20px"}),
    html.P("Authors: Rachel Bouwer, He Ma, Koray Tecimer, Yimeng Xia",
           style={"font-size": "12px"}),
    html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_11_spotify-popularity",
           target="_blank", style={"font-size": "12px"}),
    html.P("Last deployed on April 6, 2023",
           style={"font-size": "12px"})
           ]
top5songs_barchart = dvc.Vega(id='top5songs-barchart', spec={})


# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        html.Label('Select the artists you want to analyze:'),
        html.Br(),
        artist_dropdown,
        html.Label('Select the start and end year for the analysis:'),
        html.Br(),
        year_range_selector,
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row(html.Label('He Ma\'s plots to go here')),
            dbc.Row([
                dbc.Col(top5songs_barchart),
                dbc.Col(html.Label('Another plot to go here'))
            ])
        ]),
        dbc.Col(
            summary_statistics, width=3
        )
    ]),
    dbc.Row(dbc.Col(bottom_blub))
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
    Output("top5songs-barchart", 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value')
    ]
)
def update_top_songs_bar_chart(selected_artists, start_year, end_year):
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)]
    tracks_df_filtered_top_five = tracks_df_filtered.sort_values('popularity', ascending=False).iloc[:5]
    fig = alt.Chart(tracks_df_filtered_top_five, width='container').mark_bar().encode(
        x=alt.X('popularity', title="Popularity"),
        y=alt.Y('name', title="Song Name").sort('-x'),
        color=alt.Color('artist', legend=None).scale(scheme="greens"),
        tooltip=['artist','release_year']
    ).properties(
        title='Popularity of Top Songs'
    ).to_dict()
    
    return fig


# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=False)
