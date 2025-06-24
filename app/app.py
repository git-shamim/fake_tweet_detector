import streamlit as st
from utils.infer import predict_tweet

st.set_page_config(page_title="Fake Tweet Detector", page_icon="🔍")
st.title("🧠 Fake Tweet Detector (BERTweet)")

tweet = st.text_area("Paste your tweet here 👇", height=150)

if st.button("Check"):
    if tweet.strip():
        label, confidence = predict_tweet(tweet)
        st.markdown(f"### Prediction: {label}")
        st.markdown(f"**Confidence:** Fake: `{confidence[0]:.2f}`, Real: `{confidence[1]:.2f}`")
    else:
        st.warning("Please enter a tweet.")
