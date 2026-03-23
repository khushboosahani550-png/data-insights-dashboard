import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Lulu UAE Performance Dashboard", layout="wide")

# Title
st.title("📊 Lulu UAE Performance Dashboard")

# Load your CSV
df = pd.read_csv("lulu_uae_master_2000.csv")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
city = st.sidebar.multiselect("City", df["city"].unique(), default=df["city"].unique())
channel = st.sidebar.multiselect("Channel", df["channel"].unique(), default=df["channel"].unique())
department = st.sidebar.multiselect("Department", df["department"].unique(), default=df["department"].unique())
gender = st.sidebar.multiselect("Gender", df["gender"].unique(), default=df["gender"].unique())
loyalty = st.sidebar.selectbox("Loyalty Member", ["All", "Yes", "No"], index=0)

# Extra filters (AFTER loyalty, but BEFORE applying filters)
date_range = st.sidebar.date_input("Select Date Range", [])
brand_search = st.sidebar.text_input("Search Brand")

# Apply filters (define filtered_df first)
filtered_df = df[
    (df["city"].isin(city)) &
    (df["channel"].isin(channel)) &
    (df["department"].isin(department)) &
    (df["gender"].isin(gender))
]
if loyalty != "All":
    filtered_df = filtered_df[filtered_df["loyalty_member"] == (1 if loyalty == "Yes" else 0)]

# Apply brand search filter AFTER filtered_df exists
if brand_search:
    filtered_df = filtered_df[filtered_df["brand"].str.contains(brand_search, case=False)]

# ✅ Download button AFTER filtered_df is fully defined
st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_data.csv",
    mime="text/csv"
)


# KPIs
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

# Safe calculations with checks
total_revenue = f"AED {filtered_df['line_value_aed'].sum():,.0f}"
avg_order_value = f"AED {filtered_df['line_value_aed'].mean():,.0f}"
return_rate = f"{round((filtered_df['returned'].sum()/filtered_df.shape[0])*100,1)}%" if "returned" in filtered_df else "N/A"
loyalty_pct = f"{round((filtered_df[filtered_df['loyalty_member']==1].shape[0]/filtered_df.shape[0])*100,1)}%" if "loyalty_member" in filtered_df else "N/A"
total_discounts = f"AED {filtered_df['discount_aed'].sum():,.0f}" if "discount_aed" in filtered_df else "N/A"

# Display metrics
col1.metric("Total Revenue", total_revenue)
col2.metric("Avg Order Value", avg_order_value)
col3.metric("Return Rate", return_rate)
col4.metric("Loyalty %", loyalty_pct)
col5.metric("Total Discounts", total_discounts)


# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Geography & Channels", 
    "🏷️ Products & Brands", 
    "👥 Customer Demographics", 
    "📈 Revenue Trends",
    "🔗 Analytics"
])

with tab1:
    st.subheader("🌍 Revenue by City")
    city_summary = filtered_df.groupby("city")["line_value_aed"].sum().reset_index()
    fig_city = px.bar(city_summary, x="city", y="line_value_aed", text="line_value_aed",
                      title="Revenue by City", color="city", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_city, use_container_width=True)

    st.subheader("📡 Channel Split")
    channel_summary = filtered_df.groupby("channel")["line_value_aed"].sum().reset_index()
    fig_channel = px.pie(channel_summary, names="channel", values="line_value_aed", hole=0.4,
                         title="Revenue by Channel", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_channel, use_container_width=True)

    # ✅ Drill-down stays inside tab1
    st.subheader("🔍 Drill-Down by City")
    selected_city = st.selectbox("Choose a City", filtered_df["city"].unique())
    city_data = filtered_df[filtered_df["city"] == selected_city]
    brand_city = city_data.groupby("brand")["line_value_aed"].sum().reset_index()
    fig_city_brand = px.bar(brand_city, x="brand", y="line_value_aed", color="brand",
                            title=f"Sales by Brand in {selected_city}")
    st.plotly_chart(fig_city_brand, use_container_width=True)


with tab2:
    st.subheader("🏷️ Sales by Brand")
    brand_summary = filtered_df.groupby("brand")["line_value_aed"].sum().reset_index()
    fig_brand = px.bar(brand_summary, x="brand", y="line_value_aed", text="line_value_aed",
                       title="Sales by Brand", color="brand", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_brand, use_container_width=True)

    st.subheader("🏢 Department Revenue by Channel")
    dept_channel = filtered_df.groupby(["department", "channel"])["line_value_aed"].sum().reset_index()
    fig_dept = px.bar(dept_channel, x="department", y="line_value_aed", color="channel",
                      title="Department Revenue Split", barmode="stack")
    st.plotly_chart(fig_dept, use_container_width=True)


with tab3:
    st.subheader("👥 Customer Age Distribution")
    fig_age = px.histogram(filtered_df, x="age", nbins=20, color="gender",
                           title="Customer Age Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_age, use_container_width=True)

    st.subheader("🌐 Nationality Group Split")
    nationality_summary = filtered_df.groupby("nationality_group")["line_value_aed"].sum().reset_index()
    fig_nat = px.pie(nationality_summary, names="nationality_group", values="line_value_aed", hole=0.3,
                     title="Revenue by Nationality Group", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig_nat, use_container_width=True)

    # ✅ Keep this inside tab3
    st.subheader("👩‍💼 Revenue by Department & Gender")
    gender_dept = filtered_df.groupby(["department","gender"])["line_value_aed"].sum().reset_index()
    fig_gender_dept = px.bar(gender_dept, x="department", y="line_value_aed", color="gender",
                             title="Revenue by Department & Gender", barmode="stack")
    st.plotly_chart(fig_gender_dept, use_container_width=True)


with tab4:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_summary = filtered_df.groupby("order_month")["line_value_aed"].sum().reset_index()

    fig_line = px.line(monthly_summary, x="order_month", y="line_value_aed", markers=True,
                       title="Revenue Trend Over Time", color_discrete_sequence=["#FF5733"])

    # Add moving average
    monthly_summary["moving_avg"] = monthly_summary["line_value_aed"].rolling(3).mean()
    fig_line.add_scatter(x=monthly_summary["order_month"], y=monthly_summary["moving_avg"], 
                         mode="lines", name="3-Month Avg", line=dict(color="blue", width=2, dash="dash"))

    st.plotly_chart(fig_line, width="stretch")


with tab5:
    import plotly.figure_factory as ff
    st.subheader("📊 Correlation Heatmap")
    corr = filtered_df[["line_value_aed", "discount_aed", "age"]].corr()

    # Create heatmap first
    fig_heatmap = ff.create_annotated_heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.columns),
        colorscale="Viridis"
    )

    # Then update layout
    fig_heatmap.update_layout(
        title="Correlation Heatmap of Key Metrics",
        xaxis=dict(title="Metrics"),
        yaxis=dict(title="Metrics")
    )

    # Render chart
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer stays at the end
st.markdown(
    "<hr style='border:1px solid #ddd;'>"
    "<center><b>© 2026 Lulu UAE Dashboard | Powered by Streamlit & Plotly</b></center>",
    unsafe_allow_html=True
)

