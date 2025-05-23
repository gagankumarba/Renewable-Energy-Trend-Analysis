# dashboard_app.py
import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import date, timedelta, datetime
import plotly.express as px
import os

# --- Configuration (ensure these match your project) ---
# Construct the absolute path to the database file
# This assumes the script is in the same directory as the database
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # This fallback is for running in environments where __file__ is not defined (like some IDEs/notebooks)
    # It assumes the current working directory is the project directory.
    BASE_DIR = os.getcwd()
    
DATABASE_NAME = os.path.join(BASE_DIR, "trend_analyzer.db")
ANALYSIS_TOPIC = "Advancements in Renewable Energy Technologies"

# --- Database Connection ---
def create_dashboard_connection():
    """Creates a database connection to the SQLite database."""
    try:
        # Using check_same_thread=False for Streamlit, as it runs in different threads.
        conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        st.error(f"Database Connection Error: {e}")
        return None

# --- Data Fetching Functions (with Streamlit Caching for performance) ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_daily_trends_data(_conn, days=30):
    """Fetches daily trend data for the specified number of past days."""
    if _conn is None:
        return pd.DataFrame()
    today = date.today()
    start_date = today - timedelta(days=days - 1)
    query = """
        SELECT trend_date, average_sentiment_score, top_keywords, emerging_keywords
        FROM daily_trends
        WHERE trend_date >= ?
        ORDER BY trend_date ASC
    """
    try:
        df = pd.read_sql_query(query, _conn, params=(start_date.isoformat(),))
        if not df.empty:
            df['trend_date'] = pd.to_datetime(df['trend_date'])
        return df
    except Exception as e:
        st.error(f"Error fetching daily trends: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_recent_articles_with_sentiment(_conn, limit=20):
    """Fetches recent articles along with their sentiment."""
    if _conn is None:
        return pd.DataFrame()
    query = """
        SELECT a.id, a.title, a.source_name, a.publication_date, a.source_url, s.sentiment_label, s.sentiment_score
        FROM articles a
        LEFT JOIN sentiments s ON a.id = s.article_id
        ORDER BY a.publication_date DESC
        LIMIT ?
    """
    try:
        df = pd.read_sql_query(query, _conn, params=(limit,))
        if not df.empty:
            df['publication_date'] = pd.to_datetime(df['publication_date'])
        return df
    except Exception as e:
        st.error(f"Error fetching recent articles: {e}")
        return pd.DataFrame()

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="Trend Analyzer Dashboard")
st.title(f"📊 Trend Analyzer: {ANALYSIS_TOPIC}")

# Create a single connection for the duration of the script run
db_connection = create_dashboard_connection()

if db_connection:
    # --- Data Loading ---
    trends_df = fetch_daily_trends_data(db_connection, days=30)
    recent_articles_df = fetch_recent_articles_with_sentiment(db_connection, limit=20)
    
    # --- Sidebar ---
    st.sidebar.info(f"Displaying trends for '{ANALYSIS_TOPIC}'.")
    st.sidebar.markdown("---")
    if st.sidebar.button("Refresh Data"):
        st.cache_data.clear() # Clear the cache to force a re-run of data fetching
        st.experimental_rerun()

    # --- Sentiment Trend ---
    st.header("Sentiment Trend (Last 30 Days)")
    if not trends_df.empty and 'average_sentiment_score' in trends_df.columns:
        current_trends_df = trends_df
        if not current_trends_df.empty:
            fig_sentiment = px.line(current_trends_df, x='trend_date', y='average_sentiment_score',
                                    title='Average Daily Sentiment Score', markers=True,
                                    labels={'trend_date': 'Date', 'average_sentiment_score': 'Avg. Sentiment'})
            fig_sentiment.update_layout(xaxis_title="Date", yaxis_title="Avg. Sentiment Score (-1 to 1)")
            st.plotly_chart(fig_sentiment, use_container_width=True)
        else:
            st.warning("No daily sentiment trend data available for the selected range or last 30 days.")
    else:
        st.warning("No daily sentiment trend data available.")

    # --- Keywords Sections ---
    st.header("Keyword Insights (Latest Available Day)")
    if not trends_df.empty:
        latest_trends_day = trends_df.sort_values(by='trend_date', ascending=False).iloc[0]
        st.subheader(f"Keywords for: {pd.to_datetime(latest_trends_day['trend_date']).strftime('%Y-%m-%d')}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top Keywords**")
            top_keywords_json = latest_trends_day.get('top_keywords', '[]')
            try:
                top_keywords = json.loads(top_keywords_json)
                if top_keywords:
                    for item in top_keywords:
                        st.markdown(f"- **{item['keyword']}** (Count: {item.get('count', 'N/A')})")
                else: st.info("No top keywords data for the latest day.")
            except json.JSONDecodeError: st.error("Error decoding top keywords.")
        
        with col2:
            st.markdown("**Emerging Keywords**")
            emerging_keywords_json = latest_trends_day.get('emerging_keywords', '[]')
            try:
                emerging_keywords = json.loads(emerging_keywords_json)
                if emerging_keywords:
                    for keyword in emerging_keywords: st.markdown(f"- **{keyword}**")
                else: st.info("No emerging keywords for the latest day.")
            except json.JSONDecodeError: st.error("Error decoding emerging keywords.")
    else:
        st.info("No daily trend data available to show keyword insights.")

    # --- Recent Articles Table ---
    st.header("Recent Articles & Sentiment")
    if not recent_articles_df.empty:
        def make_clickable(link):
            return f'<a target="_blank" href="{link}">{link}</a>'
        
        df_display_articles = recent_articles_df.copy()
        if 'source_url' in df_display_articles.columns:
            df_display_articles['source_url'] = df_display_articles['source_url'].apply(make_clickable)

        # Display with clickable links (HTML needs to be allowed)
        st.markdown(df_display_articles[['title', 'source_name', 'publication_date', 'sentiment_label', 'sentiment_score', 'source_url']].to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No recent articles with sentiment data found.")

    if db_connection:
        db_connection.close()
else:
    st.error("Failed to establish database connection. Dashboard cannot load data.")