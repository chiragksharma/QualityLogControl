import streamlit as st
import requests

st.title("Log Search Interface")


# API Calls Section
st.header("API Calls")

# Button for API1
if st.button("Call API1"):
    with st.spinner("Calling API1..."):
        response = requests.get("http://localhost:5000/api1")
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Button for API2
if st.button("Call API2"):
        with st.spinner("Calling API2..."):
            response = requests.post("http://localhost:5000/api2")
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error(f"Error: {response.status_code} - {response.text}")



# Button for API3
if st.button("Call API3"):
    with st.spinner("Calling API3..."):
        response = requests.get("http://localhost:5000/api3")
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Inserting Logs
if st.button("Insert Logs"):
    with st.spinner("Inserting Logs..."):
        response = requests.post("http://localhost:5000/insert_logs")
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")



query = st.text_input("Search Query",value="API Response")
level = st.selectbox("Log Level", ["", "success", "error"],index=1)
start_time = st.text_input("Start Time (YYYY-MM-DDTHH:MM:SSZ)",value="2024-05-14T00:00:00Z")
end_time = st.text_input("End Time (YYYY-MM-DDTHH:MM:SSZ)",value="2024-05-14T23:59:59Z")


if st.button("Search"):
    with st.spinner("Searching..."):
        params = {
            "query": query,
            "level": level,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get("http://localhost:5000/search", params=params)
        results = response.json()
            
        if response.status_code == 200:
            results = response.json()
            if not results:
                st.write("No such results")
            else:
                for result in results:
                    st.write(result["_source"])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")