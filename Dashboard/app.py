import streamlit as st
import pandas as pd

# ==============================
# CẤU HÌNH TRANG
# ==============================

st.set_page_config(
    page_title="OECD Productivity Project",
    page_icon="📊",
    layout="wide"
)

# ==============================
# ĐỌC DỮ LIỆU
# ==============================

df = pd.read_csv(
    "data/processed/oecd_productivity_clean.csv"
)

# ==============================
# TIÊU ĐỀ
# ==============================

st.title("📊 OECD Productivity Project")

st.markdown(
    """
    ### Năng suất lao động vs Giờ làm việc

    **Tại sao các quốc gia làm việc ít giờ hơn lại tạo ra
    giá trị kinh tế trên mỗi giờ làm cao hơn?**
    """
)

st.divider()
# ==============================
# KEY FINDINGS
# ==============================

st.subheader("💡 Key Findings")

st.markdown(
    """
    ### 1. Germany: fewer working hours, higher productivity

    In 2023, Germany recorded the **lowest average annual hours worked**
    among the four economies, at **1,338.8 hours**, while its GDP per hour
    worked was the **highest**, at **83.25 USD PPP**.

    ### 2. South Korea: more hours, lower GDP per hour

    South Korea recorded the **highest average annual hours worked**
    in 2023, at **1,872 hours**, but its GDP per hour worked was
    **51.08 USD PPP**, the lowest among the four economies.

    ### 3. A negative cross-country association

    In the 2023 data, the correlation between annual hours worked and
    GDP per hour worked is **-0.44**.

    This indicates a moderate negative association in this sample.
    However, correlation does not establish a causal relationship.
    """
)

st.divider()
# ==============================
# SIDEBAR - FILTER
# ==============================

st.sidebar.header("🔎 Bộ lọc")

# Chọn quốc gia
countries = sorted(df["Country"].unique())

selected_countries = st.sidebar.multiselect(
    "Chọn quốc gia",
    countries,
    default=countries
)

# Chọn năm
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Khoảng thời gian",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# ==============================
# LỌC DATA
# ==============================

filtered_df = df[
    (df["Country"].isin(selected_countries))
    &
    (df["Year"].between(
        selected_years[0],
        selected_years[1]
    ))
].copy()

# ==============================
# KPI
# ==============================

st.subheader("📌 Tổng quan")

col1, col2, col3 = st.columns(3)

if len(filtered_df) > 0:

    latest_year = filtered_df["Year"].max()
    latest_df = filtered_df[
        filtered_df["Year"] == latest_year
    ]

    avg_productivity = latest_df["GDPHOUR"].mean()
    avg_hours = latest_df["AVGHOURS"].mean()
    avg_wages = latest_df["WAGES"].mean()

    col1.metric(
        "GDP/giờ trung bình",
        f"{avg_productivity:.2f} USD"
    )

    col2.metric(
        "Giờ làm việc trung bình",
        f"{avg_hours:,.1f} giờ"
    )

    col3.metric(
        "Lương trung bình",
        f"{avg_wages:,.0f} USD"
    )

else:
    st.warning("Vui lòng chọn ít nhất một quốc gia.")


# ==============================
# BIỂU ĐỒ 1
# GDP PER HOUR THEO THỜI GIAN
# ==============================

import plotly.express as px

st.subheader("📈 GDP trên mỗi giờ làm việc")

fig_productivity = px.line(
    filtered_df,
    x="Year",
    y="GDPHOUR",
    color="Country",
    markers=True,
    labels={
        "Year": "Năm",
        "GDPHOUR": "GDP/giờ (USD PPP)",
        "Country": "Quốc gia"
    }
)

fig_productivity.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_productivity,
    use_container_width=True
)

# ==============================
# HIỂN THỊ DATA
# ==============================

st.subheader("Dữ liệu đang được chọn")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.write(
    f"Số dòng dữ liệu: **{len(filtered_df)}**"
)
# ==============================
# BIỂU ĐỒ 2
# AVERAGE HOURS WORKED THEO THỜI GIAN
# ==============================

st.subheader("⏱️ Số giờ làm việc bình quân mỗi năm")

fig_hours = px.line(
    filtered_df,
    x="Year",
    y="AVGHOURS",
    color="Country",
    markers=True,
    labels={
        "Year": "Năm",
        "AVGHOURS": "Giờ làm việc (giờ/năm)",
        "Country": "Quốc gia"
    }
)

fig_hours.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_hours,
    use_container_width=True
)
# ==============================
# BIỂU ĐỒ 3
# HOURS WORKED VS GDP PER HOUR
# ==============================

st.subheader("🔎 Giờ làm việc và GDP trên mỗi giờ")

fig_scatter = px.scatter(
    filtered_df,
    x="AVGHOURS",
    y="GDPHOUR",
    color="Country",
    hover_data=["Year"],
    labels={
        "AVGHOURS": "Giờ làm việc (giờ/năm)",
        "GDPHOUR": "GDP/giờ (USD PPP)",
        "Country": "Quốc gia",
        "Year": "Năm"
    }
)

fig_scatter.update_traces(
    marker=dict(size=10)
)

fig_scatter.update_layout(
    hovermode="closest"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)
# ==============================
# BIỂU ĐỒ 4
# GDP PER HOUR VS AVERAGE WAGES
# ==============================

st.subheader("💰 GDP trên mỗi giờ và tiền lương bình quân")

fig_wages = px.scatter(
    filtered_df,
    x="GDPHOUR",
    y="WAGES",
    color="Country",
    hover_data=["Year"],
    labels={
        "GDPHOUR": "GDP/giờ (USD PPP)",
        "WAGES": "Lương bình quân (USD PPP/năm)",
        "Country": "Quốc gia",
        "Year": "Năm"
    }
)

fig_wages.update_traces(
    marker=dict(size=10)
)

fig_wages.update_layout(
    hovermode="closest"
)

st.plotly_chart(
    fig_wages,
    use_container_width=True
)
# ==============================
# BIỂU ĐỒ 5
# THAY ĐỔI 2014 → 2023
# ==============================

st.subheader("📊 Thay đổi các chỉ tiêu: 2014 → 2023")

# Lấy dữ liệu đầu kỳ và cuối kỳ
df_start = df[df["Year"] == 2014].copy()
df_end = df[df["Year"] == 2023].copy()

# Chỉ giữ các quốc gia đang được chọn
df_start = df_start[
    df_start["Country"].isin(selected_countries)
]

df_end = df_end[
    df_end["Country"].isin(selected_countries)
]

# Ghép 2014 và 2023
change_df = df_start[
    ["Country", "GDPHOUR", "AVGHOURS", "WAGES"]
].merge(
    df_end[
        ["Country", "GDPHOUR", "AVGHOURS", "WAGES"]
    ],
    on="Country",
    suffixes=("_2014", "_2023")
)

# Tính % thay đổi
change_df["GDPHOUR"] = (
    (change_df["GDPHOUR_2023"] /
     change_df["GDPHOUR_2014"] - 1) * 100
)

change_df["AVGHOURS"] = (
    (change_df["AVGHOURS_2023"] /
     change_df["AVGHOURS_2014"] - 1) * 100
)

change_df["WAGES"] = (
    (change_df["WAGES_2023"] /
     change_df["WAGES_2014"] - 1) * 100
)

# Chuyển sang LONG để vẽ
change_long = change_df[
    ["Country", "GDPHOUR", "AVGHOURS", "WAGES"]
].melt(
    id_vars="Country",
    var_name="Indicator",
    value_name="Change"
)

# Đổi tên hiển thị
indicator_names = {
    "GDPHOUR": "GDP/giờ",
    "AVGHOURS": "Giờ làm việc",
    "WAGES": "Lương bình quân"
}

change_long["Indicator"] = change_long[
    "Indicator"
].map(indicator_names)

# Vẽ biểu đồ
fig_change = px.bar(
    change_long,
    x="Country",
    y="Change",
    color="Indicator",
    barmode="group",
    labels={
        "Country": "Quốc gia",
        "Change": "Thay đổi (%)",
        "Indicator": "Chỉ tiêu"
    }
)

fig_change.add_hline(
    y=0,
    line_width=1
)

fig_change.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_change,
    use_container_width=True
)
# ==============================
# DATA SOURCE & METHODOLOGY
# ==============================

st.divider()

st.subheader("📚 Data Source & Methodology")

st.markdown(
    """
    ### Data source

    Data are obtained from the **OECD Data Explorer** through the
    OECD SDMX API.

    The analysis covers four economies:

    - Germany
    - United States
    - Japan
    - South Korea

    The study period is **2014–2023**.

    ### Indicators

    **GDP per hour worked (GDPHOUR)**  
    Measures GDP generated per hour worked.  
    Unit: **USD PPP per hour**.

    **Average annual hours actually worked per worker (AVGHOURS)**  
    Measures the average number of hours actually worked per worker
    during a year.  
    Unit: **hours per year**.

    **Average annual wages (WAGES)**  
    Measures average annual wages.  
    Unit: **USD PPP per year**.

    ### Data processing

    The raw OECD data were:

    1. Retrieved through the OECD SDMX API.
    2. Filtered to the four selected economies and 2014–2023.
    3. Filtered according to the relevant OECD indicator dimensions.
    4. Checked for missing values and duplicated observations.
    5. Standardized into a common dataset.
    6. Used to create the visualizations in this dashboard.

    ### Important limitation

    The analysis is **descriptive**. The observed relationships between
    working hours, productivity and wages should not be interpreted as
    causal relationships.

    In particular, the negative association between working hours and
    GDP per hour does not by itself demonstrate that working fewer hours
    causes higher productivity.
    """
)

# ==============================
# SOURCE FILE
# ==============================

st.subheader("🔗 Project Data")

st.write(
    "Processed dataset: "
    "`data/processed/oecd_productivity_clean.csv`"
)