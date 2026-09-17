import pandas as pd

# 1. Đọc dữ liệu OECD
file_path = "data/raw/oecd_hours_2014_2023.csv"

df = pd.read_csv(file_path)

# 2. Chỉ giữ 4 quốc gia của nhóm
countries = ["DEU", "USA", "KOR", "JPN"]

df = df[df["REF_AREA"].isin(countries)]

df = df[df["WORKER_STATUS"] == "_T"]

# 3. Chỉ giữ các cột cần thiết
df = df[
    [
        "REF_AREA",
        "TIME_PERIOD",
        "OBS_VALUE",
        "UNIT_MEASURE",
        "HOURS_TYPE",
        "LABOUR_FORCE_STATUS",
        "WORKER_STATUS",
        "AGGREGATION_OPERATION"
    ]
]

# 4. Đổi tên cột cho dễ sử dụng
df = df.rename(columns={
    "REF_AREA": "Country_Code",
    "TIME_PERIOD": "Year",
    "OBS_VALUE": "Value"
})

# 5. Chuyển kiểu dữ liệu
df["Year"] = df["Year"].astype(int)
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# 6. Sắp xếp
df = df.sort_values(
    ["Country_Code", "Year"]
).reset_index(drop=True)

# 7. Hiển thị thông tin
print("\n===== THÔNG TIN DATASET =====")
print("Số dòng:", len(df))
print("Số quốc gia:", df["Country_Code"].nunique())

print("\n===== SỐ NĂM THEO QUỐC GIA =====")
print(df.groupby("Country_Code")["Year"].count())

print("\n===== CÁC NĂM CÓ DỮ LIỆU =====")
for country in countries:
    years = sorted(df.loc[
        df["Country_Code"] == country, "Year"
    ].unique())

    print(country, ":", years)

print("\n===== KIỂM TRA MISSING =====")
print(df.isna().sum())

print("\n===== 10 DÒNG ĐẦU =====")
print(df.head(10))

# 8. Tạo dữ liệu sạch theo Data Contract
clean_df = df[
    [
        "Country_Code",
        "Year",
        "Value",
        "UNIT_MEASURE"
    ]
].copy()

# Thêm tên chỉ tiêu và mã chỉ tiêu
clean_df["Country"] = clean_df["Country_Code"].map({
    "DEU": "Germany",
    "USA": "United States",
    "KOR": "South Korea",
    "JPN": "Japan"
})

clean_df["Indicator_Code"] = "AVGHOURS"
clean_df["Indicator"] = "Average annual hours actually worked per worker"
clean_df["Unit"] = "Hours per year per person"

# Sắp xếp đúng thứ tự cột của Data Contract
clean_df = clean_df[
    [
        "Country",
        "Country_Code",
        "Year",
        "Indicator_Code",
        "Indicator",
        "Value",
        "Unit"
    ]
]

# Sắp xếp dữ liệu
clean_df = clean_df.sort_values(
    ["Country_Code", "Year"]
).reset_index(drop=True)

# Lưu file
output_path = "data/processed/oecd_hours_clean.csv"

clean_df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n===== ĐÃ TẠO FILE CLEAN =====")
print(output_path)

print("\n===== CẤU TRÚC FILE CLEAN =====")
print(clean_df.head())

print("\nSố dòng:", len(clean_df))