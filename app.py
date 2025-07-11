import streamlit as st
import pandas as pd
import random
import unicodedata


# Load the CSV file
df = pd.read_csv("stories.csv")
st.subheader("📋 Dataset Preview")
st.dataframe(df)

# Function to normalize Telugu/Unicode text
def normalize_text(text):
    return unicodedata.normalize('NFC', str(text)).strip().lower()

# Page settings
st.set_page_config(page_title="Telugu Folk Tales Explorer", layout="wide")
st.title("📖 తెలుగు జానపద కథల అన్వేషణ")

# Search input
query = st.text_input("🔍 కథ శీర్షిక లేదా కీలక పదం నమోదు చేయండి:")

# Normalize the search query
normalized_query = normalize_text(query)

# Filter results using improved partial matching
if normalized_query:
    results = df[df.apply(
        lambda row: any([
            normalize_text(row['title']).startswith(normalized_query),
            normalize_text(row['story']).startswith(normalized_query),
            normalized_query in normalize_text(row['title']),
            normalized_query in normalize_text(row['story'])
        ]),
        axis=1
    )]

    if not results.empty:
        for _, row in results.iterrows():
            st.subheader(row['title'])
            st.write(row['story'])
            st.markdown("---")
    else:
        st.warning("ఏమైనా కథ కనిపించలేదు. మరో పదంతో ప్రయత్నించండి.")
else:
    st.info("కథ కోసం పై సెర్చ్ బాక్స్‌ను ఉపయోగించండి లేదా క్రింద యాదృచ్ఛిక కథను చూడండి.")

# Random story button
if st.button("🎲 ఒక యాదృచ్ఛిక కథ చూపించు"):
    story = random.choice(df.to_dict(orient='records'))
    st.subheader(story['title'])
    st.write(story['story'])

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Mamatha | Summer of AI 2025")
