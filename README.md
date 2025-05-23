# Automated News & Social Sentiment Trend Analyzer: Renewable Energy

This project implements an automated data pipeline that scrapes news articles and Reddit posts related to "Advancements in Renewable Energy Technologies." It then performs Natural Language Processing (NLP) to analyze sentiment, extract key entities and keywords, calculates daily trends, and visualizes these insights on an interactive Streamlit dashboard.

**Live Demo:** https://renewable-energy-trend-analysis-svqeraef6ou49sjcrqrlbx.streamlit.app/

## Key Features

* **Automated Data Collection:** Scrapes data from configured RSS feeds and Reddit subreddits.
* **NLP Processing Pipeline:**
    * **Sentiment Analysis:** Determines the sentiment (positive, negative, neutral) of each article/post using VADER.
    * **Named Entity Recognition (NER):** Identifies and categorizes entities like organizations, people, and locations using spaCy.
    * **Keyword Extraction:** Extracts significant keywords and bi-grams using TF-IDF with scikit-learn.
* **Trend Analysis:** Calculates daily average sentiment, top keywords, and emerging keywords.
* **Data Storage:** Utilizes SQLite for storing scraped articles, NLP results, and aggregated daily trends.
* **Interactive Dashboard:** A Streamlit application visualizes sentiment trends over time, top/emerging keywords, and recent articles with their sentiment.

## Technology Stack

* **Language:** Python 3.x
* **Data Scraping:** `Requests`, `BeautifulSoup4` (minimal use), `feedparser`, `newspaper3k`
* **NLP:** `spaCy` (for NER, tokenization, stop words), `VADER Sentiment` (for sentiment analysis), `scikit-learn` (for TF-IDF keyword extraction)
* **Data Handling & Analysis:** `Pandas`
* **Database:** `SQLite3`
* **Dashboarding:** `Streamlit`, `Plotly Express` (for charts)
* **Development Environment:** Jupyter Notebooks

* **Web Scraping:** Developed Python scripts to collect and parse data from diverse online sources (RSS feeds, Reddit JSON endpoints), handling different HTML/XML structures and using libraries like `Requests`, `feedparser`, and `newspaper3k`.
* **Natural Language Processing (NLP):** Implemented an NLP pipeline using `spaCy` for Named Entity Recognition and `VADER Sentiment` for robust sentiment analysis. Extracted meaningful keywords using `scikit-learn`'s `TfidfVectorizer`.
* **Data Science & Data Analytics:** Performed trend analysis by aggregating processed data to calculate daily average sentiment scores, identify top keywords through frequency analysis, and determine emerging keywords by comparing daily sets. Utilized `Pandas` for data manipulation.
* **Database Management:** Designed and implemented an `SQLite` database schema to store structured data including articles, sentiment scores, extracted keywords, entities, and daily aggregated trends. Handled data insertion and querying.
* **Software Development & Integration (Python):** Developed a modular project structure integrating various components (scraping, NLP, data storage, analytics, dashboarding) into a cohesive pipeline using Python.
* **API Usage (Implicit):** Interacted with Reddit's public JSON API for data collection.
* **Dashboarding & Visualization:** Built an interactive web-based dashboard using `Streamlit` and `Plotly Express` to present complex data insights in an accessible and user-friendly manner.
* **Real-time Model/Data Updating Concepts:** Designed the system for periodic data refreshes (via scraping) and subsequent updates to analytical outputs (daily trends), demonstrating principles of maintaining and updating data-driven "models" (in this case, the analytical state of trends).
* **Problem Solving:** Addressed challenges such as handling various date formats, dealing with inconsistent web source structures, managing timezones (standardizing to UTC), and ensuring data integrity during the pipeline execution.
* **Version Control:** Utilized Git and GitHub for project versioning and hosting.
* **AI Ethics and Data Privacy Awareness (Considerations):**
    * Implemented polite scraping practices (e.g., user-agent, delays).
    * Focused on publicly available data.

## Project Architecture

The system follows a modular pipeline architecture:

1.  **(Manual/External Trigger):** The data pipeline is run to collect and process new data.
2.  **Scraper Module (`Requests`, `feedparser`, `newspaper3k`):** Fetches raw content from configured RSS feeds and Reddit subreddits.
3.  **NLP Processing Pipeline (`spaCy`, `VADER`, `scikit-learn`):** Cleans text, performs sentiment analysis, extracts named entities, and identifies keywords from the scraped content.
4.  **Data Storage (`SQLite`):** Stores raw article data, processed NLP outputs, and daily aggregated trends.
5.  **Analytics Engine (`Pandas`, Python):** Queries the database to calculate daily average sentiment, top keywords, and emerging keywords, storing these in the `daily_trends` table.
6.  **Streamlit Dashboard (`Streamlit`, `Plotly Express`):** Queries the database (primarily `daily_trends` and recent `articles`/`sentiments`) to visualize insights for the user.

```mermaid
graph TD
    A["Manual Pipeline Execution"] --> B["Scraper Module <br/> RSS/Reddit"];
    B --> C["NLP Processing Pipeline <br/> Sentiment, NER, Keywords"];
    C --> D["Data Storage <br/> (SQLite)"];
    D --> E["Analytics Engine <br/> Daily Trends"];
    E --> D;
    D --> F["Streamlit Dashboard <br/> Visualization"];

    subgraph "Data Sources"
        DS1["News RSS Feeds"]
        DS2["Reddit API"]
    end

    DS1 --> B;
    DS2 --> B;
