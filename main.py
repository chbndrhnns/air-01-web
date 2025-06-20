import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="IT Salary Calculator", layout="wide")

st.title("IT Salary Calculator (JetBrains Developer Ecosystem Survey 2024)")

# Load and flatten data
def load_flat_data():
    with open("calculatorData.json", "r") as f:
        raw = json.load(f)
    rows = []
    for country, langs in raw.items():
        for language, data in langs.items():
            for entry in data.get("entries", []):
                row = {
                    "Country": country,
                    "Language": language,
                    "value": entry.get("value"),
                    "category": entry.get("category")
                }
                if "metadata" in entry:
                    row.update(entry["metadata"])
                rows.append(row)
    return pd.DataFrame(rows)

df = load_flat_data()

st.sidebar.header("Filters")

# Only use columns with a reasonable number of unique values for filters
filterable_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() < 30]
filters = {}
for col in filterable_cols:
    options = ["All"] + sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.selectbox(f"{col}", options, key=col)
    if selected != "All":
        filters[col] = selected
# Numeric filters
for col in df.select_dtypes(include='number').columns:
    min_val, max_val = df[col].min(), df[col].max()
    if min_val != max_val:
        selected = st.sidebar.slider(f"{col}", float(min_val), float(max_val), (float(min_val), float(max_val)), key=col)
        filters[col] = selected

def apply_filters(df, filters):
    for col, val in filters.items():
        if isinstance(val, tuple):
            df = df[df[col].between(val[0], val[1])]
        else:
            df = df[df[col] == val]
    return df

filtered_df = apply_filters(df, filters)

st.write(f"### Filtered Results: {len(filtered_df)} records")
st.dataframe(filtered_df, use_container_width=True)

# Visualization (example: Salary distribution if present)
salary_col = None
for col in df.columns:
    if 'salary' in col.lower():
        salary_col = col
        break
if salary_col and pd.api.types.is_numeric_dtype(pd.to_numeric(filtered_df[salary_col].str.replace("$", "").str.replace("K", "").str.replace("/ year", "").str.replace(",", ""), errors='coerce')):
    st.write(f"### {salary_col} Distribution")
    salary_vals = pd.to_numeric(filtered_df[salary_col].str.replace("$", "").str.replace("K", "").str.replace("/ year", "").str.replace(",", ""), errors='coerce')
    st.bar_chart(salary_vals.value_counts().sort_index())
else:
    st.info("No numeric salary column found for visualization.")

st.markdown("---")
st.markdown("[Figma design](https://www.figma.com/design/pmxb4N3i62YgFVzE5Nq74b/IT-Salary-Calculator?node-id=0-1&p=f) | [Reference page](https://www.jetbrains.com/lp/devecosystem-it-salary-calculator/)")
