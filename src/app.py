from dash import Dash, html, dcc, Input, Output, callback_context
import pandas as pd
import dash_bootstrap_components as dbc
import ast
import dash_vega_components as dvc
import altair as alt
from itertools import product
from collections import Counter



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
genres_exploded = tracks_df.explode('genres')
genre_counts = genres_exploded['genres'].value_counts()


genre_dropdown_options = [{'label': genre, 'value': genre} for genre in genre_counts.index]

# Configuration
dropdown_style = {'margin-top': '10px', 'margin-bottom': '10px'}

genre_dropdown = html.Div(
    [
        html.Label('Select one genre you want to analyze:', className='mb-1'),
        dcc.Dropdown(
            options=genre_dropdown_options,
            multi=False,
            placeholder='Select a genre...',
            id='genre-dropdown'
        ),
    ],
    style=dropdown_style
)

artist_dropdown = html.Div(
    [
        html.Label('Select up to five artists you want to analyze:', className='mb-1'),
        dcc.Dropdown(
            options=[{'label': artist, 'value': artist} for artist in tracks_df['artist'].unique()],
            multi=True,
            placeholder='Select multiple artists...',
            id='artists-dropdown'
        ),
    ],
    style=dropdown_style
)

year_range_selector = dbc.Row(
    [
        dbc.Col(
            [
                html.Label('Select the start year for the analysis:', className='mb-1'),
                dcc.Dropdown(
                    options=[{'label': year, 'value': year} for year in sorted(tracks_df['release_year'].unique())],
                    multi=False,
                    placeholder='Select the start year...',
                    id='start-year'
                ),
            ],
            style=dropdown_style
        ),
        dbc.Col(
            [
                html.Label('Select the end year for the analysis:', className='mb-1'),
                dcc.Dropdown(
                    options=[{'label': year, 'value': year} for year in sorted(tracks_df['release_year'].unique())],
                    multi=False,
                    placeholder='Select the end year...',
                    id='end-year'
                ),
            ],
            style=dropdown_style
        ),
    ],
    no_gutters=True
)

# year_range_selector = dbc.Row([
#     dbc.Col(
#         dcc.Dropdown(
#             options=sorted(tracks_df['release_year'].unique()),
#             multi=False,
#             placeholder='Select the start year...',
#             id='start-year'
#         )),
#     dbc.Col(
#         dcc.Dropdown(
#             options=sorted(tracks_df['release_year'].unique()),
#             multi=False,
#             placeholder='Select the end year...',
#             id='end-year'
#         ))
# ])

artist_time_chart =  dvc.Vega(id='artist-time-chart', spec={})
explicit_chart = dvc.Vega(id='explicit-chart', spec={})
top5songs_barchart = dvc.Vega(id='top5songs-barchart', spec={})
speechiness_chart = dvc.Vega(id='speechiness-chart', spec={})

summary_statistics = dbc.Col([
    html.Br(),
    html.H4('Song features (Mean)', className='text-center', style={"color": 'white'}),
    html.H5('Top 5 Popular Songs', className='text-center', style={"color": 'white'}),
    dbc.Row(
        dbc.Card(id='mean-danceability', style={"border": 0, "width": "75%"},className="mb-2 mx-auto", outline=True,)
    ),
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

# Layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1('Spotify', style={'color':'white','align-items': 'left','margin-left': '30px'}),
                html.H1('Popularity', style={'color':'white', 'align-items': 'left','margin-left': '30px'}),
                html.H1('Dashboard', style={'color':'white', 'align-items': 'left','margin-left': '30px'}),
                html.P("This dashboard is designed for helping record companies to make data driven decisions, so that they can provide valuable and actionable suggestions that can be used as guidance for artists aiming to enhance their music's appeal.",
                    style={"font-size": "16px",'color':'#D3D3D3', 'margin-left': '15px'}),
                html.P("Authors: Rachel Bouwer, He Ma, Koray Tecimer, Yimeng Xia",
                    style={"font-size": "12px",'color':'#D3D3D3','margin-left': '15px'}),
                html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_11_spotify-popularity",
                    target="_blank", style={"font-size": "12px",'margin-left': '15px'}),
                html.P("Last deployed on April 6, 2024",
                    style={"font-size": "12px",'color':'#D3D3D3','margin-left': '15px'})
            ])
        ], style={'height': '100vh', 
                  'background-color': '#196543', 
                  'display': 'flex',
                    'flex-direction': 'column', 
                    'justify-content': 'center'}),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    #html.Label('Select one genre you want to analyze:'),
                    genre_dropdown,
                    #html.Label('Select up to five artists you want to analyze:'),
                    artist_dropdown,
                    #html.Label('Select the start and end year for the analysis:'),
                    year_range_selector,
                    html.Br()
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(artist_time_chart), style={'width': '45%','background-color': 'white', 'margin-left': '5%'}),
                        dbc.Col(html.Div(explicit_chart),  style={'width': '45%','background-color': 'white',  'margin-right': '5%'})
                    ], style={'margin-top': '100px'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(top5songs_barchart), style={'width': '45%','background-color': 'white',
                                                                      'margin-left': '5%'
                                                                     }),
                        dbc.Col(html.Div(speechiness_chart), style={'width': '45%','background-color': 'white', 
                                                                    'margin-right': '5%'
                                                                    }),  
                    ])
                ])
            ])
        ], width=7, className="col-7",style={'background-color': '#24BA56'}),
        dbc.Col([
            summary_statistics
        ], width=2, className="col-2", style={'background-color': '#196543'})
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
            dbc.CardBody(mean_danceability, className='text-center', style={'padding': '10px'})
        ]
        card_mean_energy = [
            dbc.CardHeader('Energy', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_energy, className='text-center', style={'padding': '10px'})
        ]
        card_mean_loudness = [
            dbc.CardHeader('Loudness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_loudness, className='text-center', style={'padding': '10px'})
        ]
        card_mean_speechiness = [
            dbc.CardHeader('Speechiness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_speechiness, className='text-center', style={'padding': '10px'})
        ]
        card_mean_acousticness = [
            dbc.CardHeader('Acousticness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_acousticness, className='text-center', style={'padding': '10px'})
        ]
        card_mean_instrumentalness = [
            dbc.CardHeader('Instrumentalness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_instrumentalness, className='text-center', style={'padding': '10px'})
        ]
        card_mean_liveness = [
            dbc.CardHeader('Liveness', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_liveness, className='text-center', style={'padding': '10px'})
        ]
        card_mean_valence = [
            dbc.CardHeader('Valence', style={"color" : "#1db954"}, className='text-center'),
            dbc.CardBody(mean_valence, className='text-center', style={'padding': '10px'})
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


@app.callback(
    Output('artists-dropdown', 'value'),
    [Input('artists-dropdown', 'value')]
)
def limit_artists(selected_artists):
    if selected_artists is None:
        return []
    
    if len(selected_artists) > 5:
        return selected_artists[:5]
    
    return selected_artists






@app.callback(
    Output('artist-time-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value')
    ]
)

def update_time_chart(selected_artists, start_year, end_year):
    hex_color_scale = ['80ED99', '#57CC99', '#438A70', '#11999E','#3C3C3C']

    if selected_artists is None or start_year is None or end_year is None:
        return {}
    tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)]
    

    chart = alt.Chart(tracks_df_filtered).mark_point().encode(
        x=alt.X('release_year', 
                scale=alt.Scale(domain=[start_year, end_year]),
                axis=alt.Axis(format=''),
                title='Release Year'),
        y=alt.Y('mean(popularity)', title='Popularity'),
        color=alt.Color('artist', scale=alt.Scale(
        domain=selected_artists,  
        range=['#FFEEAF','#A8CD9F', '#57CC99', '#438A70', '#12372A']),  
        legend=alt.Legend(title="Artist")),
        tooltip=['artist', 'release_year', 'mean(popularity)']
    ).properties(
        title='Artist Popularity Over Time',
        width=250,
        height=200
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


    chart = alt.Chart(merged_df).mark_bar().encode(
        alt.X('song_type:N', axis=alt.Axis(title=None, labels=True, ticks=True)),
        alt.Y('popularity:Q', axis=alt.Axis(title='Mean Popularity', grid=False)),
        color=alt.Color('song_type:N', legend=alt.Legend(title="Song Type")).scale(scheme="greens"),
        column=alt.Column('artist:N', header=alt.Header(title=None, labelOrient='bottom'))
    ).configure_view(
        stroke='transparent'
    ).properties(
        width = 20,
        height = 200,
        title='Mean Popularity of Songs by Type and Artist'
    )

    return chart.to_dict()

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
    fig = alt.Chart(tracks_df_filtered_top_five).mark_bar().encode(
        y=alt.Y('popularity', title="Popularity"),
        x=alt.X('name', axis=alt.Axis(labelAngle=-15), title='Song Name').sort('-y'),
        color=alt.Color('artist', legend=None).scale(scheme="greens"),
        tooltip=['artist','release_year']
    ).properties(
        title='Popularity of Top Songs',
        width=350,
        height=200
    ).to_dict()
    
    return fig

@app.callback(
    Output('speechiness-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value')
    ]
)

def update_speechiness_chart(selected_artists, start_year, end_year):
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
        y=alt.Y('popularity', title='Popularity'),
        color=alt.Color('speechiness_binned:N', legend=alt.Legend(title="Speechiness")).scale(scheme="greens"),
        tooltip=['artist', 'name', 'release_year', 'popularity']
    ).properties(
        title='Popularity by Speechiness over Time',
        width=250,
        height=200
    )
    
    fig = chart + chart.transform_regression('release_year', 'popularity', groupby=['speechiness_binned']).mark_line()

    return fig.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    import dash

    print("dash version=", dash.__version__)
    app.run(debug=True)