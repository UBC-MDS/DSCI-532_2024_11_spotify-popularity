# Proposal - Spotify Popularity Dashboard

Rachel Bouwer, Koray Tecimer, He Ma, Yimeng Xia

## Motivation and Purpose

Our role: Data scientist consultancy firm

Target audience: Record Companies

One of the biggest sectors in the entertainment industry in terms of market size is music. It was valued at USD 27,898.47 million in 2022 according to Industry Research Co. In this huge economy, record companies can strategize in a data driven way to make smart investments to artists - but it might not be clear which artists are worth investing in. To address this issue, we will create a dashboard application that will be easy to browse thorough artists and genres. Record labels will be able to see which factors play into account for artists and songs to be popular. Our app will allow them to identify past songs and evaluate current artists, but also give them ideas on which artist they should invest next. Our app will allow users to filter artists and genres and show plots that will allow them to compare artists and also factors that make that artist popular or unpopular.


## Description of the Data

## Research Questions

Jane is a music producer at a record company. She aims to explore the unique characteristics that define popular music within individual genres to offer precise modification advice for artists. Her objective is to [explore] a detailed dataset to check whether popular tracks within each specific genre exhibit shared characteristics and to [identify] significant, actionable attributes that can be used as guidance for artists aiming to enhance their music's appeal.

When Jane logs on to our “Spotify Popularity Dashboard”, she is presented with two tabs, “By Genre” and “By Artist”. She can apply filters to discover the top tracks within a particular genre by specific artists over a chosen timeframe, and examine the overall summary of music features associated with these hits. When she does so, Jane may e.g. notice that a low ‘valence’ score is a common trait among popular cantopop tracks during 2015 to 2020, highlighting a preference towards more somber or less cheerful music within this genre.

Informed by her insights from the app, Jane hypothesizes that Cantopop artists could potentially increase their tracks' popularity by focusing on songs with lower valence scores, reflecting a preference for more somber tones among listeners. She decides to initiate a more detailed analysis or consult directly with artists, suggesting they could experiment with this attribute in their upcoming tracks, as the emotional tone seems to play a crucial role in the genre's listener appeal.

## App Sketch and Description

The Spotify Popularity Dashboard is comprised of two lab views - 'By Genre' and 'By Artist'. The 'By Genre' tab allows you to select one genre and explore the popularity of artists and songs in the given genre. Similarly, the 'By Artist' tab allows you to select one artist and browse the popularity of this artist across the songs in their different genres. Common across both tabs is the 'Song Features - Top 5 Popular Songs' statistics (on the right) where the average values across the different features of the top 5 popular songs that match the selected criteria are displayed. For each of the four views, there are four different plots (in the middle of the screen) that give insights on how features of the given subset of songs are related to popularity. Finally, above the plots are where you can customize the view which includes a drop down (to select either one genre or one artist), a date range picker to choose the time frame you wish to analyze, and a bar allowing you to select either multiple artists in a given genre (By Genre view), or multiple genres for a given artist (By Artist view).

### 'By Genre' View

 !["By Genre view"](../img/sketch_genre.png)

### 'By Artist' View

 !["By Artist view"](../img/sketch_artist.png)
