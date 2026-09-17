import pandas as pd

# Đọc 3 file clean
productivity = pd.read_csv(
    "data/processed/oecd_productivity_clean.csv"
)

hours = pd.read_csv(
    "data/processed/oecd_hours_clean.csv"
)

wages = pd.read_csv(
    "data/processed/oecd_wages_clean.csv"
)

# Gộp 3 bộ dữ liệu LONG
df_long = pd.concat(
    [productivity, hours, wages],
    ignore_index=True
)

# Sắp xếp
df_long = df_long.sort_values(
    ["Country_Code", "Year", "Indicator_Code"]
)

# Lưu bộ dữ liệu LONG cuối cùng
long_path = "data/processed/oecd_all_indicators_long.csv"
df_long.to_csv(long_path, index=False)

# Chuyển sang WIDE
df_wide = df_long.pivot_table(
    index=["Country", "Country_Code", "Year"],
    columns="Indicator_Code",
    values="Value"
).reset_index()

# Đảm bảo thứ tự cột
df_wide = df_wide[
    [
        "Country",
        "Country_Code",
        "Year",
        "GDPHOUR",
        "AVGHOURS",
        "WAGES"
    ]
]

# Kiểm tra
print("=== VALIDATION ===")
print("Số dòng:", len(df_wide))
print("Số quốc gia:", df_wide["Country_Code"].nunique())
print("Số năm:", df_wide["Year"].nunique())
print("Missing:")
print(df_wide.isna().sum())

print("\n=== DATA ===")
print(df_wide.to_string(index=False))

# Lưu WIDE
wide_path = "data/processed/oecd_productivity_clean.csv"
df_wide.to_csv(wide_path, index=False)

print("\nĐã lưu:")
print(long_path)
print(wide_path)