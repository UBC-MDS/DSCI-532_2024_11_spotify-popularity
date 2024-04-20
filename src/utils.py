import ast
import joblib

memory = joblib.Memory("tmp", verbose=0)

@memory.cache()
def convert_string_to_list(string):
    try:
        return ast.literal_eval(string)
    # Return an empty list if the string is not a valid list representation
    except ValueError:
        return []


# convert stringified lists into actual lists
@memory.cache()
def create_genre_dropdown_options(tracks_df):
    tracks_df['genres'] = tracks_df['genres'].apply(convert_string_to_list)
    genres_exploded = tracks_df.explode('genres')
    genre_counts = genres_exploded['genres'].value_counts()
    genre_dropdown_options = [{'label': genre, 'value': genre} for genre in genre_counts.index]
    return genre_dropdown_options