import pandas as pd
import requests
from io import StringIO

url = (
    "https://sdmx.oecd.org/public/rest/v1/data/"
    "OECD.SDD.TPS,DSD_PDB@DF_PDB,2.0/all"
    "?startPeriod=2014"
    "&endPeriod=2023"
    "&dimensionAtObservation=AllDimensions"
)

headers = {"Accept": "text/csv"}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

df = pd.read_csv(StringIO(response.text))

# 4 quốc gia của nhóm
countries = ["DEU", "USA", "KOR", "JPN"]

# Lọc đúng GDP per hour worked
df = df[
    (df["REF_AREA"].isin(countries)) &
    (df["FREQ"] == "A") &
    (df["MEASURE"] == "GDPHRS") &
    (df["ACTIVITY"] == "_T") &
    (df["UNIT_MEASURE"] == "USD_PPP_H") &
    (df["PRICE_BASE"] == "LR") &
    (df["TRANSFORMATION"] == "N") &
    (df["CONVERSION_TYPE"] == "PPP")
].copy()

print("Số dòng sau khi lọc:", len(df))

# Chọn các cột cần thiết
df = df[
    [
        "REF_AREA",
        "TIME_PERIOD",
        "OBS_VALUE"
    ]
].copy()

# Đổi tên theo Data Contract
df = df.rename(
    columns={
        "REF_AREA": "Country_Code",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "Value"
    }
)

# Thêm thông tin chỉ tiêu
df["Indicator_Code"] = "GDPHOUR"
df["Indicator"] = "GDP per hour worked"
df["Unit"] = "USD PPP per hour"

# Country name
country_names = {
    "DEU": "Germany",
    "USA": "United States",
    "KOR": "South Korea",
    "JPN": "Japan"
}

df["Country"] = df["Country_Code"].map(country_names)

# Sắp xếp
df = df[
    [
        "Country",
        "Country_Code",
        "Year",
        "Indicator_Code",
        "Indicator",
        "Value",
        "Unit"
    ]
].sort_values(["Country_Code", "Year"])

# Kiểm tra dữ liệu
print("\nKiểm tra:")
print("Số dòng:", len(df))
print("Số quốc gia:", df["Country_Code"].nunique())
print("Các quốc gia:", df["Country_Code"].unique())
print("Số năm:", df["Year"].nunique())
print("Năm:", sorted(df["Year"].unique()))
print("Missing:", df.isna().sum().sum())

print("\nDữ liệu:")
print(df.to_string(index=False))

# Lưu file
output_path = "data/processed/oecd_productivity_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nĐã lưu: {output_path}")