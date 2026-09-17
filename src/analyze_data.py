import pandas as pd

# ==============================
# 1. Đọc dữ liệu
# ==============================

df = pd.read_csv(
    "data/processed/oecd_productivity_clean.csv"
)

print("=== DATASET ===")
print(df.head())


# ==============================
# 2. Thống kê theo quốc gia
# ==============================

summary = df.groupby("Country").agg(
    GDPHOUR_mean=("GDPHOUR", "mean"),
    AVGHOURS_mean=("AVGHOURS", "mean"),
    WAGES_mean=("WAGES", "mean")
).round(2)

print("\n=== TRUNG BÌNH 2014–2023 ===")
print(summary)


# ==============================
# 3. So sánh năm 2023
# ==============================

df_2023 = df[df["Year"] == 2023].copy()

print("\n=== NĂM 2023 ===")

print(
    df_2023[
        [
            "Country",
            "GDPHOUR",
            "AVGHOURS",
            "WAGES"
        ]
    ].sort_values("GDPHOUR", ascending=False)
    .to_string(index=False)
)


# ==============================
# 4. Quốc gia có GDP/giờ cao nhất
# ==============================

highest_productivity = df_2023.loc[
    df_2023["GDPHOUR"].idxmax()
]

lowest_productivity = df_2023.loc[
    df_2023["GDPHOUR"].idxmin()
]

print("\n=== GDP PER HOUR ===")

print(
    "Cao nhất:",
    highest_productivity["Country"],
    "-",
    round(highest_productivity["GDPHOUR"], 2)
)

print(
    "Thấp nhất:",
    lowest_productivity["Country"],
    "-",
    round(lowest_productivity["GDPHOUR"], 2)
)


# ==============================
# 5. Quốc gia làm việc nhiều/ít giờ nhất
# ==============================

most_hours = df_2023.loc[
    df_2023["AVGHOURS"].idxmax()
]

least_hours = df_2023.loc[
    df_2023["AVGHOURS"].idxmin()
]

print("\n=== GIỜ LÀM VIỆC ===")

print(
    "Nhiều nhất:",
    most_hours["Country"],
    "-",
    round(most_hours["AVGHOURS"], 1),
    "giờ"
)

print(
    "Ít nhất:",
    least_hours["Country"],
    "-",
    round(least_hours["AVGHOURS"], 1),
    "giờ"
)


# ==============================
# 6. Kiểm tra mối quan hệ
# ==============================

correlation = df_2023[
    ["AVGHOURS", "GDPHOUR"]
].corr().loc["AVGHOURS", "GDPHOUR"]

print("\n=== CORRELATION 2023 ===")

print(
    "Correlation giữa giờ làm việc và GDP/giờ:",
    round(correlation, 3)
)


# ==============================
# 7. Thay đổi 2014 → 2023
# ==============================

df_start = df[df["Year"] == 2014].set_index("Country")
df_end = df[df["Year"] == 2023].set_index("Country")

change = pd.DataFrame({
    "GDPHOUR_change_%":
        (df_end["GDPHOUR"] / df_start["GDPHOUR"] - 1) * 100,

    "AVGHOURS_change_%":
        (df_end["AVGHOURS"] / df_start["AVGHOURS"] - 1) * 100,

    "WAGES_change_%":
        (df_end["WAGES"] / df_start["WAGES"] - 1) * 100
}).round(2)

print("\n=== THAY ĐỔI 2014 → 2023 (%) ===")
print(change)