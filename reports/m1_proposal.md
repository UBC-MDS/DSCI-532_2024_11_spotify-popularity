
### Section 2: Description of the data

We will be working with a dataset from [kaggle](https://www.kaggle.com/) of [Spotify tracks](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data) over a range of 125 different genres. The dataset has 114,000 records and 20 variables including track id, artist, popularity, danceability, valence, and other information. These variables offer deep insights into the musical features and popularity of the tracks, which are vital for strategic planning in the music industry.

The variables in the dataset can be basically categorized into several types:

* **Identification**:  including `track_id`, `artists`, `album_name`, and `track_name`.  These variables can help in theunique identification of each track.
* **Popularity**: Our variable of interest, `popularity`, reflects the listener engagement and is crucial for understanding the listener behavior and making data-driven decisions in the music industry.
* **Musical Features** : variables that quantify the musical elements, including `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, and `valence`.
* **Temporal Features** :  `duration_ms`, `tempo`, and `time_signature` offer insights into the rhythm and length of the tracks.
* **Categorical Data** :  `track_genre` categorizes tracks by genre, which could be crucial for genre-specific analysis. And `explicit` is a binary categorical variable indicating whether a track contains explicit content.

Additionally, we plan to engineer new categorical variables from the `speechiness` and `liveness` features to aid in the visualizations and analysis.

`speechiness_category`: categorize tracks into  `High Speechiness` for speechiness values above 0.66, `Medium Speechiness` for speechiness values between 0.33 and 0.66 and `Low Speechiness` for speechiness values below 0.33, which can help to identify the types of songs that are most popular.

`live `: classify tracks as `Live` for liveness values above 0.8 and `Not Live` for liveness values at or below 0.8. This can inform producers and labels about the potential benefits of investing in live albums.

Our project will focus on the features that are most important to understand the track popularity on Spotify. Among these selected features are `danceability`, `energy`, `valence`, and ` name`, each offering unique insights into the musical and thematic content of the tracks, and  two newly derived features:  `speechiness_category `and `live` as well.
