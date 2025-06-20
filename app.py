import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# MySQL Connection
def load_data():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='spotify_dp'
    )
    query = "SELECT * FROM spotify_tracks"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Data
df = load_data()

# Streamlit Page Setup
st.set_page_config(page_title="🎶 Spotify Tracks Dashboard", layout="wide")
st.title("🎧 Spotify Tracks Dashboard")

#  Table View
st.subheader("📋 Track Details")
st.dataframe(df)

# Search Feature
st.subheader("🔎 Search by Track or Artist")
search = st.text_input("Search here:")
if search:
    filtered = df[df['track_name'].str.contains(search, case=False) | df['artist'].str.contains(search, case=False)]
    st.dataframe(filtered)
else:
    filtered = df

# Top 5 Popular Tracks - Bar Chart
st.subheader("🔥 Top 5 Popular Tracks")
top5 = df.sort_values(by='popularity', ascending=False).head(5)
fig1 = px.bar(
    top5,
    x='track_name',
    y='popularity',
    color='artist',
    text='popularity',
    title="Top 5 Most Popular Tracks",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig1.update_traces(textposition='outside')
fig1.update_layout(xaxis_title="Track Name", yaxis_title="Popularity")
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart - Artist Track Share
st.subheader("🥧 Artist Track Share")
artist_counts = df['artist'].value_counts().reset_index()
artist_counts.columns = ['artist', 'count']
fig2 = px.pie(
    artist_counts,
    names='artist',
    values='count',
    title="Track Count by Artist",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Plasma
)
st.plotly_chart(fig2, use_container_width=True)

# Grouped Bar Chart - Artist vs Track Popularity
st.subheader("🎤 Grouped Bar Chart: Track Popularity by Artist")
fig3 = px.bar(
    df,
    x='artist',
    y='popularity',
    color='track_name',
    barmode='group',
    text='popularity',
    title="Track Popularity by Artist",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig3.update_layout(xaxis_title="Artist", yaxis_title="Popularity")
st.plotly_chart(fig3, use_container_width=True)

