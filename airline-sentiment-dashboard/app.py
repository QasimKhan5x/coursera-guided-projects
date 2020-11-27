import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Tentinment Analysis of Tweets about US airlines")
st.sidebar.title("Tentinment Analysis of Tweets about US airlines")
st.markdown('This application is a streamlit dashboard to analyze the sentiment of tweets Ã°ÂÂÂ¦')
st.sidebar.markdown('This application is a streamlit dashboard to analyze the sentiment of tweets Ã°ÂÂÂ¦')

data_url = ('Tweets.csv')

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader('Show random tweet')
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(1).iat[0, 0])

st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Vizualization type', ['Histogram', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown('#### Number of Tweets by sentiment')
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader('When and where are users tweeting from')
hour = st.sidebar.slider('Hour of day', 0, 23)
#hour = st.sidebar.number_input('Hour of day', min_value=1, max_value=23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close', True, key='1'):
    st.markdown('### Tweets locations by time of day')
    st.markdown(f'{len(modified_data)} tweets between {hour}:00 and {(hour + 1) % 24}:00')
    st.map(modified_data)
    if st.sidebar.checkbox('Show row data', False):
        st.write(modified_data)


st.sidebar.subheader('Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick airline',
('US Airways', 'United', 'American', 'South', 'Delta', 'Virgin America'),
key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment',
    histfunc='count', color='airline_sentiment', facet_col='airline_sentiment',
    labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header('World Cloud')
word_sentiment = st.sidebar.radio('Display word cloud for which sentiment?',
('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox('Hide', True, key='2'):
    st.subheader(f'Word clod for {word_sentiment} sentiment')
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() \
    if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',
    width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()