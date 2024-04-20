from dash import Dash, html, Input, Output
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import altair as alt
from itertools import product
from dash.exceptions import PreventUpdate
import os
import sys
sys.path.insert(1, os.path.dirname(sys.path[0]))
import src.components as cmp
from src.components import tracks_df

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Spotify Popularity Dashboard"

# Layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1('Spotify', style={'color': 'white', 'align-items': 'left', 'margin-left': '15px'}),
                html.H1('Popularity', style={'color': 'white', 'align-items': 'left', 'margin-left': '15px'}),
                html.H1('Dashboard', style={'color': 'white', 'align-items': 'left', 'margin-left': '15px', 'margin-bottom': '30px'}),
                html.P(
                    "This dashboard is designed for helping record companies to make data driven decisions, so that they can provide valuable and actionable suggestions that can be used as guidance for artists aiming to enhance their music's appeal.",
                    style={"font-size": "15px", 'color': '#D3D3D3', 'margin-left': '15px'}),
                html.P("Authors: Rachel Bouwer, He Ma, Koray Tecimer, Yimeng Xia",
                       style={"font-size": "12px", 'color': '#D3D3D3', 'margin-left': '15px'}),
                html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2024_11_spotify-popularity",
                       target="_blank", style={"font-size": "12px", 'margin-left': '15px'}),
                html.P("Last deployed on April 16, 2024",
                       style={"font-size": "12px", 'color': '#D3D3D3', 'margin-left': '15px'})
            ])
        ], width=2, style={'background-color': '#196543',
                  'display': 'flex',
                  'flex-direction': 'column',
                  'justify-content': 'center'}),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label('Select one genre you want to analyze:'),
                        cmp.genre_dropdown,
                        html.Label('Select the start and end year for the analysis:'),
                        cmp.year_range_selector,
                        html.Label('Select up to five artists you want to analyze:'),
                        cmp.artist_dropdown,
                        html.Label('Select an artist to compare (optional):'),
                        dbc.Row([
                            dbc.Col([cmp.optional_artist_selector_dropdown]),
                            dbc.Col([cmp.submit_button])
                        ])
                    ], style={'margin-top': '10px'}),
                    html.Br()
                ])
            ]),
            cmp.plot_layout
        ], width=8, style={'background-color': '#24BA56'}),
        dbc.Col([
            cmp.summary_statistics
        ], width=2, style={'background-color': '#196543'}),
    ], style={'min-height': '100vh', 'margin': '0', 'overflow': 'hidden'}),
], style={'height': '100vh', 'margin': '0'})


@app.callback(
    [Output('mean-danceability', 'children'),
     Output('mean-energy', 'children'),
     Output('mean-loudness', 'children'),
     Output('mean-speechiness', 'children'),
     Output('mean-acousticness', 'children'),
     Output('mean-instrumentalness', 'children'),
     Output('mean-liveness', 'children'),
     Output('mean-valence', 'children'),
     Output('top-five-title', 'children')],
    [Input('artists-dropdown', 'value'),
     Input('start-year', 'value'),
     Input('end-year', 'value'),
     Input('artists-dropdown-compare', 'value'),
     Input('submit-button', 'n_clicks')]
)
def display_artist_tracks(selected_artists, start_year, end_year, artists_dropdown_compare, n_clicks):
    changed_ids = [p['prop_id'] for p in dash.callback_context.triggered]
    if 'submit-button' not in changed_ids[0]:
        raise PreventUpdate
    if selected_artists is None or start_year is None or end_year is None:
        return "", "", "", "", "", "", "", "", "Top 5 Popular Songs"
    else:
        up_arrow = "\u2191"
        down_arrow = "\u2193"
        tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                       (tracks_df['release_year'] >= start_year) &
                                       (tracks_df['release_year'] <= end_year)]
        tracks_df_filtered_top_five = tracks_df_filtered.sort_values('popularity', ascending=False).iloc[:5]

        format_string = "{:.3g}"
        stats_dict = {}
        stats = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                 'valence']
        for stat in stats:
            stats_dict[stat] = tracks_df_filtered_top_five[stat].mean()

        top_five_title = "Top 5 Popular Songs"
        if artists_dropdown_compare is not None:
            for stat in stats:
                stats_dict[f"{stat}_compare"] = tracks_df[tracks_df['artist'] == artists_dropdown_compare][stat].mean()
            top_five_title = f"Top 5 Popular Songs vs {artists_dropdown_compare}"

            for stat in stats:
                stats_dict[f"{stat}_emoji"] = up_arrow if stats_dict[stat] < stats_dict[
                    f"{stat}_compare"] else down_arrow
                stats_dict[
                    f"{stat}_string"] = f"{format_string.format(stats_dict[stat])} vs {format_string.format(stats_dict[stat + '_compare'])} {stats_dict[f'{stat}_emoji']}"
        else:
            for stat in stats:
                stats_dict[f"{stat}_string"] = format_string.format(stats_dict[stat])

        card_mean_danceability = dbc.Card([
            dbc.CardHeader('Danceability', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable", 
                        target="tooltip-target-danceability", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["danceability_string"], className='text-center', style={'padding': '10px'}),
        ], id="tooltip-target-danceability")
        card_mean_energy = dbc.Card([
            dbc.CardHeader('Energy', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.", 
                        target="tooltip-target-energy", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["energy_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-energy")
        card_mean_loudness = dbc.Card([
            dbc.CardHeader('Loudness', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("The overall loudness of a track in decibels (dB)", 
                        target="tooltip-target-loudness", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["loudness_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-loudness")
        card_mean_speechiness = dbc.Card([
            dbc.CardHeader('Speechiness', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.", 
                        target="tooltip-target-speechiness", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["speechiness_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-speechiness")
        card_mean_acousticness = dbc.Card([
            dbc.CardHeader('Acousticness', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.", 
                        target="tooltip-target-acousticness", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["acousticness_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-acousticness")
        card_mean_instrumentalness = dbc.Card([
            dbc.CardHeader('Instrumentalness', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.", 
                        target="tooltip-target-instrumentalness", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["instrumentalness_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-instrumentalness")
        card_mean_liveness = dbc.Card([
            dbc.CardHeader('Liveness', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.", 
                        target="tooltip-target-liveness", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["liveness_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-liveness")
        card_mean_valence = dbc.Card([
            dbc.CardHeader('Valence', style={"color": "#1db954"}, className='text-center'),
            dbc.Tooltip("A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).", 
                        target="tooltip-target-valence", placement="left", style={"padding": "2px"}),
            dbc.CardBody(stats_dict["valence_string"], className='text-center', style={'padding': '10px'})
        ], id="tooltip-target-valence")
        return card_mean_danceability, card_mean_energy, card_mean_loudness, card_mean_speechiness, card_mean_acousticness, \
               card_mean_instrumentalness, card_mean_liveness, card_mean_valence, top_five_title


@app.callback(
    Output('artists-dropdown', 'options'),
    [Input('genre-dropdown', 'value'),
     Input('start-year', 'value'),
     Input('end-year', 'value')]
)
def update_artist_dropdown(selected_genres,start_year, end_year):
    if not selected_genres or not start_year or not end_year:
        return []
    filtered_artists = tracks_df[tracks_df['genres'].apply(lambda x: any(genre in selected_genres for genre in x))]
    filtered_artists = filtered_artists[(filtered_artists['release_year'] >= start_year) & (filtered_artists['release_year'] <= end_year)]
    artist_options = [{'label': artist, 'value': artist} for artist in filtered_artists['artist'].unique()]
    return artist_options


@app.callback(
    Output('start-year', 'options'),
    [Input('end-year', 'value')]
)
def update_start_year_dropdown(end_year):
    if end_year is None:
        return []
    return [{'label': year, 'value': year} for year in sorted(tracks_df['release_year'].unique().tolist()) if year <= end_year]


@app.callback(
    Output('end-year', 'options'),
    [Input('start-year', 'value')]
)
def update_start_year_dropdown(start_year):
    if start_year is None:
        return []
    return [{'label': year, 'value': year} for year in sorted(tracks_df['release_year'].unique().tolist()) if year >= start_year]


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
        Input('end-year', 'value'),
        Input('artists-dropdown-compare', 'value'),
        Input('submit-button', 'n_clicks')
    ]
)
def update_time_chart(selected_artists, start_year, end_year, artists_dropdown_compare, n_clicks):
    hex_color_scale = ['80ED99', '#57CC99', '#438A70', '#11999E', '#3C3C3C']
    changed_ids = [p['prop_id'] for p in dash.callback_context.triggered]
    if 'submit-button' not in changed_ids[0]:
        raise PreventUpdate
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    # if artists_dropdown_compare is not None:
    #     selected_artists.append(artists_dropdown_compare)
    tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                   (tracks_df['release_year'] >= start_year) &
                                   (tracks_df['release_year'] <= end_year)]

    unique_years = sorted(tracks_df_filtered['release_year'].unique())

    chart = alt.Chart(tracks_df_filtered).mark_point().encode(
        x=alt.X('release_year:Q',
                scale=alt.Scale(domain=[int(start_year), int(end_year)]),
                axis=alt.Axis(values=unique_years, format='0'),
                title='Release Year'),
        y=alt.Y('mean(popularity)', title='Popularity'),
        color=alt.Color('artist', scale=alt.Scale(
            domain=selected_artists,
            range=['#FFEEAF', '#A8CD9F', '#57CC99', '#438A70', '#12372A']),
                        legend=alt.Legend(title="Artist")),
        tooltip=['artist', 'release_year', 'mean(popularity)']
    ).properties(
        # # title='Artist Popularity Over Time',
        width=250,
        height=180
    )

    chart = chart + chart.mark_line()
    if artists_dropdown_compare is not None:
        # selected_artists.append(artists_dropdown_compare)
        compare_artist_df = tracks_df[(tracks_df['artist'] == artists_dropdown_compare) & 
                                   (tracks_df['release_year'] >= start_year) &
                                   (tracks_df['release_year'] <= end_year)]
        compare_artist = alt.Chart(compare_artist_df).mark_point(color='red').encode(
            x='release_year:Q',
            y=alt.Y('mean(popularity)', title='Popularity'),
            color=alt.Color('artist', legend=alt.Legend(title="Compare"), scale=alt.Scale(domain=[artists_dropdown_compare], range=['red'])),
            tooltip=['artist', 'release_year', 'mean(popularity)']
        )
        compare_artist_layer =  compare_artist + compare_artist.mark_line(color='red')
        chart = alt.layer(chart, compare_artist_layer).resolve_scale(color='independent')
    return chart.to_dict()


@app.callback(
    Output('explicit-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value'),
        Input('artists-dropdown-compare', 'value'),
        Input('submit-button', 'n_clicks')
    ]
)
def create_explicit_chart(selected_artists, start_year, end_year, artists_dropdown_compare, n_clicks):
    changed_ids = [p['prop_id'] for p in dash.callback_context.triggered]
    if 'submit-button' not in changed_ids[0]:
        raise PreventUpdate
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    if artists_dropdown_compare is not None:
        selected_artists.append(artists_dropdown_compare)

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
        alt.X('song_type:N', axis=alt.Axis(title=None, labels=True, ticks=True), 
                             sort=alt.SortArray(['Clean', 'Explicit']), 
                             scale=alt.Scale(domain=['Clean', 'Explicit'])),
        alt.Y('popularity:Q', axis=alt.Axis(title='Mean Popularity', grid=False)),
        color=alt.Color('song_type:N', legend=alt.Legend(title="Song Type")).scale(scheme="greens"),
        column=alt.Column('artist:N', header=alt.Header(title=None, labelOrient='bottom'))
    ).configure_view(
        stroke='transparent'
    ).properties(
        width=25,
        height=170,
        # title='Mean Popularity of Songs by Type and Artist'
    ).transform_calculate(
    adjusted_song_type=alt.expr.if_(alt.datum.song_type == 'Clean', 'C', 'E')
).encode(
    x=alt.X('adjusted_song_type:N', axis=alt.Axis(title=None, labels=True, ticks=True, labelAngle=0)),
)

    return chart.to_dict()


@app.callback(
    Output("top5songs-barchart", 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value'),
        Input('submit-button', 'n_clicks')
    ]
)
def update_top_songs_bar_chart(selected_artists, start_year, end_year, n_clicks):
    changed_ids = [p['prop_id'] for p in dash.callback_context.triggered]
    if 'submit-button' not in changed_ids[0]:
        raise PreventUpdate
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
        tooltip=['artist', 'release_year']
    ).properties(
        # title='Popularity of Top Songs',
        width=350,
        height=166
    ).to_dict()

    return fig


@app.callback(
    Output('speechiness-chart', 'spec'),
    [
        Input('artists-dropdown', 'value'),
        Input('start-year', 'value'),
        Input('end-year', 'value'),
        Input('submit-button', 'n_clicks')
    ]
)
def update_speechiness_chart(selected_artists, start_year, end_year, n_clicks):
    changed_ids = [p['prop_id'] for p in dash.callback_context.triggered]
    if 'submit-button' not in changed_ids[0]:
        raise PreventUpdate
    if selected_artists is None or start_year is None or end_year is None:
        return {}
    tracks_df_filtered = tracks_df[(tracks_df['artist'].isin(selected_artists)) &
                                   (tracks_df['release_year'] >= start_year) &
                                   (tracks_df['release_year'] <= end_year)]
    tracks_df_filtered['speechiness_label'] = tracks_df_filtered['speechiness_binned'].map({0: 'Low', 1: 'High'})

    unique_years = sorted(tracks_df_filtered['release_year'].unique())

    chart = alt.Chart(tracks_df_filtered).mark_point(opacity=0.7).encode(
        x=alt.X('release_year:Q',
                scale=alt.Scale(domain=[int(start_year), int(end_year)]),
                axis=alt.Axis(values=unique_years, format='0'),
                title='Release Year'),
        y=alt.Y('popularity', title='Popularity'),
        color=alt.Color('speechiness_label:N', legend=alt.Legend(title="Speechiness")).scale(scheme="greens"),
        tooltip=['artist', 'name', 'release_year', 'popularity']
    ).properties(
        # title='Popularity by Speechiness over Time',
        width=200,
        height=180
    )

    fig = chart + chart.transform_regression('release_year', 'popularity', groupby=['speechiness_label']).mark_line()

    return fig.to_dict()


# Run the app/dashboard
if __name__ == '__main__':

    print("dash version=", dash.__version__)
    app.run(debug=True)
