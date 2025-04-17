import streamlit as st
import pandas as pd
from io import BytesIO

# Page Configurations
st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File Upload Section
uploaded_files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split(".")[-1]
        
        # Read File
        try:
            df = pd.read_csv(uploaded_file) if file_extension == "csv" else pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {e}")
            continue

        st.subheader(f"Preview - {uploaded_file.name}")
        st.write(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {uploaded_file.name}"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates Removed!")
            st.write(df.head())

        # Fill Missing Values
        if st.checkbox(f"Fill Missing Values - {uploaded_file.name}"):
            numeric_cols = df.select_dtypes(include=["number"])
            df.fillna(numeric_cols.mean(), inplace=True)
            st.success("Missing values filled with column mean.")
            st.write(df.head())

        # Column Selection
        selected_cols = st.multiselect(f"Select Columns - {uploaded_file.name}", df.columns, default=df.columns)
        df = df[selected_cols]
        st.write(df.head())
        
        # Data Visualization
        if st.checkbox(f"Show Chart - {uploaded_file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Conversion Options
        file_format = st.radio(f"Convert {uploaded_file.name} to", ["csv", "Excel"], key=uploaded_file.name)

        if st.button(f"Download {uploaded_file.name} as {file_format}"):
            output = BytesIO()
            if file_format == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_filename = uploaded_file.name.replace(file_extension, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_filename = uploaded_file.name.replace(file_extension, "xlsx")
            
            output.seek(0)
            st.download_button("Download File", data=output, file_name=new_filename, mime=mime_type)
        
        st.success("Processing Completed!")
