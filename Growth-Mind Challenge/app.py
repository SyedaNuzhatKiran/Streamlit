import streamlit as st
import pandas as pd
import os
from io import BytesIO

# ✅ Page Configuration — this must be the FIRST Streamlit command
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title("Datasweeper Sterling Integrator By Nuzhat Kiran")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")


# File Uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for index, file in enumerate(uploaded_files):
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        st.divider()
        st.header(f"📄 File: {file.name}")

        # File Info
        st.write(f"**Size:** {file.size / 1024:.2f} KB")
        st.write("📊 Preview:")
        st.dataframe(df.head())

        # Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Enable Cleaning for: {file.name}", key=f"clean_{index}"):

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates", key=f"dedup_{index}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values", key=f"fillna_{index}"):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled!")

            # Column Selector
            st.subheader("🧩 Column Selector")
            selected_columns = st.multiselect("Select Columns to Keep", df.columns.tolist(), default=df.columns.tolist(), key=f"columns_{index}")
            df = df[selected_columns]

            # Visualization
            st.subheader("📈 Data Visualization")
            if st.checkbox("Show Bar Chart", key=f"viz_{index}"):
                numeric_df = df.select_dtypes(include='number')
                if not numeric_df.empty:
                    st.bar_chart(numeric_df.iloc[:, :2])
                else:
                    st.info("No numeric data to display.")

            # File Conversion
            st.subheader("📤 Export & Convert")
            conversion_type = st.radio("Choose export format", ["CSV", "Excel"], key=f"convert_{index}")

            if st.button("Convert and Download", key=f"convert_button_{index}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime = "text/csv"
                else:
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"⬇ Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime
                )

        st.success(f"🎉 All {file.name} processed successfully!")




