import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import seaborn as sns

@st.cache_data
def load_data(file):
    """
    Load CSV data using pandas and return a DataFrame.
    """
    df = pd.read_csv(file, encoding='latin1')
    return df

def clean_data(df, drop_duplicates=True, drop_missing='none'):
    """
    Perform basic data cleaning on the DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame to clean.

    drop_duplicates : bool
        Whether to drop duplicate rows.

    drop_missing : str
        How to handle missing values:
        - 'none': do nothing
        - 'drop_rows': drop any rows with missing values
        - 'fill_mean': fill missing numeric values with column mean
        - 'fill_zero': fill missing numeric values with 0

    Returns:
    --------
    pd.DataFrame
        The cleaned DataFrame.
    """
    # 1. Drop duplicates
    if drop_duplicates:
        df = df.drop_duplicates()

    # 2. Handle missing values
    if drop_missing == 'drop_rows':
        df = df.dropna()
    elif drop_missing == 'fill_mean':
        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            mean_val = df[col].mean()
            df[col].fillna(mean_val, inplace=True)
    elif drop_missing == 'fill_zero':
        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            df[col].fillna(0, inplace=True)

    return df

def auto_dashboard():
    """
    Streamlit app function for uploading a CSV, cleaning/preprocessing the data,
    and then generating basic statistics, insights, and interactive charts.
    """
    st.title("Auto Dashboard")

    # ----- Additional Explanatory Text -----
    # Provide context on data analysis, trends, patterns, etc.
    st.markdown(
        """
        ### Features Included:
        
        1. CSV Upload
        2. Data Cleaning & Preprocessing
        3. Data Preview & Basic Statistics
        4. Missing Values Summary
        5. Additional Insights (Group-by, Pivot Table)
        6. Multiple Charts (Altair, Plotly, Seaborn)
        7. Download Cleaned Data
        8. Explanatory Text on Why Data Analysis Matters
        ---
        ### Why Analyze Your Data?
        1. **Trends and Patterns**  
           Data visualization tools can help identify trends and patterns in data, including outliers.
        
        2. **Customer Needs**  
           By interpreting data patterns, organizations can forecast customer needs and make more effective decisions.
        
        3. **Product Popularity**  
           Data insights can help identify which products are most popular with specific customer demographics.
        
        """
    )

    # ----- CSV Upload -----
    uploaded_csv = st.file_uploader(
        "Upload a CSV ⬇️",
        type=["csv"],
        key="sidebar_csv"
    )

    if uploaded_csv:
        st.subheader("Data Cleaning & Preprocessing Options")
        drop_dup = st.checkbox("Drop duplicate rows", value=True)

        missing_option = st.selectbox(
            "Handle Missing Values",
            [
                "none (leave missing values as is)",
                "drop_rows (remove rows with missing values)",
                "fill_mean (fill numeric columns with mean)",
                "fill_zero (fill numeric columns with 0)"
            ],
            help="Choose how to handle rows or columns with missing values."
        )

        # Map the selected text to the internal key
        missing_mapping = {
            "none (leave missing values as is)": "none",
            "drop_rows (remove rows with missing values)": "drop_rows",
            "fill_mean (fill numeric columns with mean)": "fill_mean",
            "fill_zero (fill numeric columns with 0)": "fill_zero"
        }

        with st.spinner("Loading and cleaning data..."):
            df = load_data(uploaded_csv)
            df = clean_data(
                df,
                drop_duplicates=drop_dup,
                drop_missing=missing_mapping[missing_option]
            )

        # ----- Data Preview -----
        st.subheader("Data Preview")
        max_preview = min(100, df.shape[0])
        row_count = st.slider("Number of rows to preview:", 1, max_preview, 5)
        st.write(f"**Preview of the first {row_count} rows:**")
        st.write(df.head(row_count))

        st.write("**Shape (rows, columns):**", df.shape)
        st.write("**Data Types:**")
        st.write(df.dtypes.astype(str))

        st.subheader("Basic Statistics")
        st.write(df.describe(include="all"))

        # ----- Missing Values Summary -----
        st.subheader("Missing Values Summary")
        missing_df = df.isna().sum().reset_index()
        missing_df.columns = ["Column", "Missing Values"]
        st.dataframe(missing_df)

        # ----- Additional Insights / Group-by Analysis -----
        st.subheader("Additional Insights / Group-by Analysis")
        categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if categorical_cols:
            group_col = st.selectbox(
                "Select a categorical column to group by:", 
                options=categorical_cols
            )

            agg_col = st.selectbox(
                "Select a numeric column to aggregate:", 
                options=numeric_cols
            )

            agg_func = st.selectbox("Select aggregation function:", ["mean", "sum", "count", "max", "min"])

            if st.button("Compute Group-by"):
                if agg_func == "mean":
                    grouped = df.groupby(group_col)[agg_col].mean()
                elif agg_func == "sum":
                    grouped = df.groupby(group_col)[agg_col].sum()
                elif agg_func == "count":
                    grouped = df.groupby(group_col)[agg_col].count()
                elif agg_func == "max":
                    grouped = df.groupby(group_col)[agg_col].max()
                elif agg_func == "min":
                    grouped = df.groupby(group_col)[agg_col].min()

                st.write("**Group-by Results:**")
                st.write(grouped)
        else:
            st.write("No categorical columns found for group-by analysis.")

        # ----- Simple Pivot Table -----
        st.subheader("Build a Simple Pivot Table")
        if categorical_cols and numeric_cols:
            pivot_index = st.selectbox("Pivot Table: Select a column for rows:", categorical_cols)
            pivot_values = st.selectbox("Pivot Table: Select a numeric column for values:", numeric_cols)
            pivot_aggfunc = st.selectbox("Pivot Table: Aggregation function:", ["mean", "sum", "count", "max", "min"])

            if st.button("Generate Pivot Table"):
                pivot_table = pd.pivot_table(
                    df,
                    index=pivot_index,
                    values=pivot_values,
                    aggfunc=pivot_aggfunc
                )
                st.dataframe(pivot_table)
        else:
            st.write("Need at least one categorical and one numeric column to build a pivot table.")

        # ----- Chart Section -----
        st.subheader("Charts")
        chart_type = st.selectbox(
            "Select Chart Type:",
            [
                "area_chart",
                "bar_chart",
                "line_chart",
                "scatter_chart (Altair)",
                "pie_chart (Plotly)",
                "histogram (Plotly)",
                "box_plot (Plotly)",
                "heatmap (Seaborn)"
            ],
            help="Choose which chart to display."
        )

        # Axis selection if needed
        if chart_type == "scatter_chart (Altair)":
            x_axis = st.selectbox("Select X-axis (numeric):", numeric_cols)
            y_axis = st.selectbox("Select Y-axis (numeric):", numeric_cols)
        elif chart_type in ["histogram (Plotly)", "box_plot (Plotly)"]:
            x_axis = st.selectbox("Select numeric column:", numeric_cols)
        elif chart_type == "pie_chart (Plotly)":
            category_axis = st.selectbox("Select category column for Pie Chart:", categorical_cols)
        else:
            x_axis, y_axis, category_axis = None, None, None

        # Render the chosen chart
        if chart_type == "area_chart":
            st.area_chart(df[numeric_cols])
        elif chart_type == "bar_chart":
            st.bar_chart(df[numeric_cols])
        elif chart_type == "line_chart":
            st.line_chart(df[numeric_cols])
        elif chart_type == "scatter_chart (Altair)":
            scatter_chart = alt.Chart(df).mark_circle().encode(
                x=x_axis,
                y=y_axis,
                tooltip=df.columns.tolist()
            ).interactive()
            st.altair_chart(scatter_chart, use_container_width=True)
        elif chart_type == "pie_chart (Plotly)":
            fig = px.pie(df, names=category_axis)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "histogram (Plotly)":
            fig = px.histogram(df, x=x_axis)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "box_plot (Plotly)":
            fig = px.box(df, y=x_axis)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "heatmap (Seaborn)":
            corr = df.corr(numeric_only=True)
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
            st.pyplot(fig)

        # ----- Download Options -----
        st.subheader("Download Cleaned Data")
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload a CSV file to get started.")

if __name__ == "__main__":
    auto_dashboard()
