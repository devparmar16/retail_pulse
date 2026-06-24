import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Product Recommendations",
    page_icon="🛒",
    layout="wide"
)

from utils.load_data import resolve_path

rules_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/recommendation_association_rules.csv")
)

strong_rules_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/recommendation_strong_rules.csv")
)

comparison_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/recommendation_approach_comparison.csv")
)

itemsets_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/recommendation_frequent_itemsets.csv")
)


# ----------------------------------
# TITLE
# ----------------------------------

st.title("🛒 Product Recommendation Engine")

st.markdown(
    """
    Market Basket Analysis and Collaborative Filtering Recommendations
    """
)

# ----------------------------------
# KPI SECTION
# ----------------------------------

total_rules = len(rules_df)

strong_rules = len(strong_rules_df)

frequent_itemsets = len(itemsets_df)

best_lift = rules_df["lift"].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Association Rules",
    f"{total_rules:,}"
)

col2.metric(
    "Strong Rules",
    f"{strong_rules:,}"
)

col3.metric(
    "Frequent Itemsets",
    f"{frequent_itemsets:,}"
)

col4.metric(
    "Best Lift",
    f"{best_lift:.2f}"
)

# ----------------------------------
# TOP RULES
# ----------------------------------

st.divider()

st.subheader(
    "Top Recommendation Rules"
)

top_rules = (
    rules_df
    .sort_values(
        "lift",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_rules,
    use_container_width=True
)

# ----------------------------------
# LIFT VISUALIZATION
# ----------------------------------

st.divider()

st.subheader(
    "Highest Lift Rules"
)

plot_rules = (
    rules_df
    .sort_values(
        "lift",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    plot_rules,
    x="lift",
    y="antecedents",
    color="confidence",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PRODUCT LOOKUP
# ----------------------------------

st.divider()

st.subheader(
    "Recommendation Explorer"
)

products = sorted(
    rules_df["antecedents"]
    .astype(str)
    .unique()
)

selected_product = st.selectbox(
    "Choose Product",
    products
)

recommendations = rules_df[
    rules_df["antecedents"]
    .astype(str)
    == selected_product
]

recommendations = recommendations.sort_values(
    "lift",
    ascending=False
)

st.dataframe(
    recommendations.head(20),
    use_container_width=True
)

# ----------------------------------
# STRONG RULES
# ----------------------------------

st.divider()

st.subheader(
    "Strong Association Rules"
)

st.dataframe(
    strong_rules_df.head(50),
    use_container_width=True
)

# ----------------------------------
# FREQUENT ITEMSETS
# ----------------------------------

st.divider()

st.subheader(
    "Most Frequent Product Bundles"
)

top_itemsets = (
    itemsets_df
    .sort_values(
        "support",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_itemsets,
    use_container_width=True
)

fig = px.bar(
    top_itemsets,
    x="support",
    y="itemsets",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# APPROACH COMPARISON
# ----------------------------------

st.divider()

st.subheader(
    "Recommendation Method Comparison"
)

st.dataframe(
    comparison_df,
    use_container_width=True
)

# ----------------------------------
# RECOMMENDATION SEARCH
# ----------------------------------

st.divider()

st.subheader(
    "Rule Search"
)

search_text = st.text_input(
    "Search Product Name"
)

if search_text:

    filtered = rules_df[
        rules_df["antecedents"]
        .astype(str)
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

# ----------------------------------
# DOWNLOAD
# ----------------------------------

st.divider()

st.download_button(
    "Download Recommendation Rules",
    rules_df.to_csv(index=False),
    "recommendation_rules.csv",
    "text/csv"
)