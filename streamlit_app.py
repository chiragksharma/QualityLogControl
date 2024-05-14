import streamlit as st
import requests

st.title("Log Search Interface")

query = st.text_input("Search Query")
level = st.selectbox("Log Level", ["", "success", "error"])
start_time = st.text_input("Start Time (YYYY-MM-DDTHH:MM:SSZ)")
end_time = st.text_input("End Time (YYYY-MM-DDTHH:MM:SSZ)")

if st.button("Search"):
    params = {
        "query": query,
        "level": level,
        "start_time": start_time,
        "end_time": end_time
    }
    response = requests.get("http://localhost:5000/search", params=params)
    results = response.json()
        
    if response.status_code == 200:
        results = response.json()
        st.write("Results:", results)  # Debugging line to check the response structure
        for result in results:
            st.write(result["_source"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")