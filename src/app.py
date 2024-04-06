from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import ast
import dash_vega_components as dvc
import altair as alt
from itertools import product


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
title= [html.H1('Spotify Popularity Dashboard'), html.Br()]
genre_dropdown = dcc.Dropdown(
    options= genre_dropdown_options,
    multi=False,
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

artist_time_chart =  dvc.Vega(id='artist-time-chart', spec={})
explicit_chart = dvc.Vega(id='explicit-chart', spec={})

summary_statistics = dbc.Col([
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
        html.Title('Spotify Popularity Dashboard'),
        html.Label('Select the genre you want to analyze:'),
        genre_dropdown,
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
           dbc.Row([
               dbc.Col(html.Div(artist_time_chart)),
               dbc.Col(html.Div(explicit_chart))
            ]),
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

@app.callback(
    Output('artist-time-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value')
    ]
)

def update_time_chart(selected_artists, start_year, end_year):
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)]
    chart = alt.Chart(tracks_df_filtered).mark_point(opacity=0.7).encode(
        x=alt.X('release_year', 
                scale=alt.Scale(domain=[start_year, end_year]),
                axis=alt.Axis(format=''),
                title='Release Year'),
        y=alt.Y('mean(popularity)', title='Popularity'),
        color=alt.Color('artist', legend=alt.Legend(title="Artist")),
        tooltip=['artist', 'release_year', 'mean(popularity)']
    ).properties(
        title='Artist Popularity Over Time'  # Add a title to the chart
    )
    chart = chart + chart.mark_line()
    return chart.to_dict()



@app.callback(
    Output('explicit-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value')
    ]
)

def create_explicit_chart(selected_artists, start_year, end_year):
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    
    all_combinations = pd.DataFrame(list(product(selected_artists, ['Clean', 'Explicit'])),
                                    columns=['artist', 'song_type'])
    
    all_combinations['popularity'] = 0


    df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)].copy()
    df_filtered['song_type'] = tracks_df['explicit'].map({1: 'Explicit', 0: 'Clean'})
    grouped = df_filtered.groupby(['artist', 'song_type'])['popularity'].mean().reset_index()
    
    
    # Merge the all_combinations dataframe with the grouped data to fill in actual popularity values
    merged_df = pd.merge(all_combinations, grouped, on=['artist', 'song_type'], how='left', suffixes=('', '_actual'))
    merged_df['popularity'] = merged_df['popularity_actual'].fillna(0)
    merged_df.drop(columns='popularity_actual', inplace=True)
    merged_df['artist'] = merged_df['artist'].apply(lambda x: x.split()[0] if ' ' in x else x)


    chart =  alt.Chart(merged_df).mark_bar().encode(
        alt.X('song_type:N', axis=alt.Axis(title=None, labels=True, ticks=True)),
        alt.Y('popularity:Q', axis=alt.Axis(title='Mean Popularity', grid=False)),
        color=alt.Color('song_type:N', legend=alt.Legend(title="Song Type")),
        column=alt.Column('artist:N', header=alt.Header(title=None, labelOrient='bottom'))
    ).configure_view(
        stroke='transparent'
    ).properties(width = 20,
        title='Mean Popularity of Songs by Type and Artist'
    )

    return chart.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=True)
