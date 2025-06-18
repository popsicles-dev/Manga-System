import streamlit as st
import requests
import random

st.set_page_config(page_title="Manga Recommender", layout="centered")

st.title("📚 Manga Recommendation System")

# User input
title = st.text_input("Enter a Manga Title (e.g., Naruto):")
top_n = st.slider("Number of Recommendations", 1, 10, 5)

if st.button("Get Recommendations"):
    if not title:
        st.warning("Please enter a manga title.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json={"title": title, "top_n": top_n}
            )
            if response.status_code == 200:
                recommendations = response.json()
                st.success("Top Recommendations:")
                for i, manga in enumerate(recommendations, 1):
                    st.markdown(f"{i}. **{manga}**")
            else:
                error_json = response.json()
                error_detail = error_json.get("detail", "Unknown error.")
                all_titles = error_json.get("all_titles", [])
                if error_detail.lower() == "manga title not found" and all_titles:
                    suggestions = random.sample(all_titles, min(3, len(all_titles)))
                    st.error(f"❌ {error_detail}")
                    st.info("Did you mean one of these?")
                    for suggestion in suggestions:
                        st.markdown(f"- **{suggestion}**")
                else:
                    st.error(f"❌ Error: {error_detail}")
        except Exception as e:
            st.error(f"Server error: {e}")