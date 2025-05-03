import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Number Cleaner", layout="centered")
st.title("📊 Excel Mobile Number Cleaner")

st.markdown("""
Upload an Excel file with **Name** and **Number** columns.  
This app will clean the phone numbers and keep only the last 10 digits.
""")

# Function to clean number
def clean_number(number):
    number = str(number)
    digits = ''.join(filter(str.isdigit, number))
    return digits[-10:] if len(digits) >= 10 else ""

# Upload file
uploaded_file = st.file_uploader("🗂 Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if "Name" not in df.columns or "Number" not in df.columns:
            st.error("❌ Excel file must have 'Name' and 'Number' columns.")
        else:
            df["Cleaned Number"] = df["Number"].apply(clean_number)

            st.success("✅ Numbers cleaned successfully!")
            st.write("🔍 Preview of cleaned data:")
            st.dataframe(df)

            # Convert to downloadable Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Cleaned Excel File",
                data=output,
                file_name="cleaned_numbers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Something went wrong: {e}")
