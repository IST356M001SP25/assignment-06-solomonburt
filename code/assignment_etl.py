import streamlit as st
import pandas as pd
import requests
import json
import os
import sys  # Import the sys module

# Add the 'code' directory to sys.path
if __name__ == "__main__":
    sys.path.append('.')  # Add current directory
    from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition
else:
    from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition


PLACE_IDS_SOURCE_FILE = "cache/place_ids.csv"
CACHE_REVIEWS_FILE = "cache/reviews.csv"
CACHE_SENTIMENT_FILE = "cache/reviews_sentiment_by_sentence.csv"
CACHE_ENTITIES_FILE = "cache/reviews_sentiment_by_sentence_with_entities.csv"


def reviews_step(place_ids: str | pd.DataFrame) -> pd.DataFrame:
    """
    1. place_ids --> reviews_step --> reviews: place_id, name (of place), author_name, rating, text
    """
    if isinstance(place_ids, str):
        place_ids_df = pd.read_csv(place_ids)
    else:
        place_ids_df = place_ids

    reviews = []
    for index, row in place_ids_df.iterrows():
        place_details = get_google_place_details(row['Google Place ID'])
        if place_details and 'result' in place_details:
            place_name = place_details['result'].get('name', 'N/A')  # handle missing name
            if 'reviews' in place_details['result']:
                for review in place_details['result']['reviews']:
                    review['place_id'] = row['Google Place ID']
                    review['name'] = place_name
                    reviews.append(review)
            else:
                st.warning(
                    f"No reviews found for {place_name} (ID: {row['Google Place ID']})"
                )
        else:
            st.warning(f"Could not retrieve details for place ID {row['Google Place ID']}")

    reviews_df = pd.DataFrame(reviews)
    if not reviews_df.empty:
        reviews_df = reviews_df[['place_id', 'name', 'author_name', 'rating', 'text']]
        reviews_df.to_csv(CACHE_REVIEWS_FILE, index=False, header=True)
    else:
        # Create an empty DataFrame with the correct columns
        reviews_df = pd.DataFrame(columns=['place_id', 'name', 'author_name', 'rating', 'text'])
        reviews_df.to_csv(CACHE_REVIEWS_FILE, index=False,
                         header=True)  # create empty file

    return reviews_df


def sentiment_step(reviews: str | pd.DataFrame) -> pd.DataFrame:
    """
    2. reviews --> sentiment_step --> review_sentiment_by_sentence
    """
    if isinstance(reviews, str):
        reviews_df = pd.read_csv(reviews)
    else:
        reviews_df = reviews

    sentiments = []
    for index, row in reviews_df.iterrows():
        sentiment_data = get_azure_sentiment(row['text'])
        if sentiment_data and 'results' in sentiment_data and sentiment_data['results']['documents']:
            sentiment_item = sentiment_data['results']['documents'][0]
            sentiment_item['place_id'] = row['place_id']
            sentiment_item['name'] = row['name']
            sentiment_item['author_name'] = row['author_name']
            sentiment_item['rating'] = row['rating']
            if 'sentences' in sentiment_item:
                for sentence in sentiment_item['sentences']:
                    sentence['place_id'] = row['place_id']
                    sentence['name'] = row['name']
                    sentence['author_name'] = row['author_name']
                    sentence['rating'] = row['rating']
                    sentiments.append(sentence)
            else:
                sentiments.append(sentiment_item)
        else:
            st.warning(
                f"No sentiment data for review from {row['author_name']} for place {row['name']}"
            )

    sentiment_df = pd.DataFrame(sentiments)
    if not sentiment_df.empty:
        sentiment_df = sentiment_df.rename(columns={'text': 'sentence_text', 'sentiment': 'sentence_sentiment'},
                                            errors='ignore')
        sentiment_df = sentiment_df[
            ['place_id', 'name', 'author_name', 'rating', 'sentence_text',
             'sentence_sentiment', 'confidenceScores.positive',
             'confidenceScores.neutral', 'confidenceScores.negative']]
        sentiment_df.to_csv(CACHE_SENTIMENT_FILE, index=False, header=True)
    else:
        sentiment_df = pd.DataFrame(
            columns=['place_id', 'name', 'author_name', 'rating', 'sentence_text',
                     'sentence_sentiment', 'confidenceScores.positive',
                     'confidenceScores.neutral', 'confidenceScores.negative'])
        sentiment_df.to_csv(CACHE_SENTIMENT_FILE, index=False,
                         header=True)  # create empty file
    return sentiment_df



def entity_extraction_step(sentiment: str | pd.DataFrame) -> pd.DataFrame:
    """
    3. review_sentiment_by_sentence --> entity_extraction_step --> review_sentiment_entities_by_sentence
    """
    if isinstance(sentiment, str):
        sentiment_df = pd.read_csv(sentiment)
    else:
        sentiment_df = sentiment

    entities = []
    for index, row in sentiment_df.iterrows():
        entity_data = get_azure_named_entity_recognition(row['sentence_text'])
        if entity_data and 'results' in entity_data and entity_data['results']['documents']:
            entity_item = entity_data['results']['documents'][0]
            for col in sentiment_df.columns:
                entity_item[col] = row[col]
            if 'entities' in entity_item:
                for entity in entity_item['entities']:
                    entity.update(entity_item)
                    entities.append(entity)
            else:
                entities.append(entity_item)
        else:
            st.warning(f"No entities found in sentence: {row['sentence_text']}")

    entities_df = pd.DataFrame(entities)
    if not entities_df.empty:
        entities_df = entities_df.rename(
            columns={'text': 'entity_text', 'category': 'entity_category', 'subcategory': 'entity_subcategory',
                     'confidenceScore': 'confidenceScores.entity'}, errors='ignore')
        entities_df = entities_df[['place_id', 'name', 'author_name', 'rating', 'sentence_text',
                                   'sentence_sentiment', 'confidenceScores.positive', 'confidenceScores.neutral',
                                   'confidenceScores.negative',
                                   'entity_text', 'entity_category', 'entity_subcategory', 'confidenceScores.entity']]
        entities_df.to_csv(CACHE_ENTITIES_FILE, index=False, header=True)
    else:
        entities_df = pd.DataFrame(
            columns=['place_id', 'name', 'author_name', 'rating', 'sentence_text',
                     'sentence_sentiment', 'confidenceScores.positive', 'confidenceScores.neutral',
                     'confidenceScores.negative',
                     'entity_text', 'entity_category', 'entity_subcategory', 'confidenceScores.entity'])
        entities_df.to_csv(CACHE_ENTITIES_FILE, index=False,
                         header=True)  # create empty file
    return entities_df


if __name__ == '__main__':
    import streamlit as st  # helpful for debugging as you can view your dataframes and json outputs

    # Create dummy data for testing
    place_ids_data = {'Google Place ID': ['ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'ChIJl2h_-pjz2YkR-VUHD9dpOF0',
                                        'ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'ChIJl2h_-pjz2YkR-VUHD9dpOF0',
                                        'ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'ChIJl2h_-pjz2YkR-VUHD9dpOF0',
                                        'ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'ChIJl2h_-pjz2YkR-VUHD9dpOF0',
                                        'ChIJUTtvv9Tz2YkRhneTbRT-1mk', 'ChIJl2h_-pjz2YkR-VUHD9dpOF0']}
    pd.DataFrame(place_ids_data).to_csv(PLACE_IDS_SOURCE_FILE, index=False)

    reviews_df = reviews_step(PLACE_IDS_SOURCE_FILE)
    sentiment_df = sentiment_step(CACHE_REVIEWS_FILE)
    entities_df = entity_extraction_step(CACHE_SENTIMENT_FILE)
    st.write(entities_df)