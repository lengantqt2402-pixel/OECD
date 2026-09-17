import requests
from io import StringIO
import pandas as pd

url = (
    "https://sdmx.oecd.org/public/rest/v1/data/"
    "OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0/all"
    "?startPeriod=2014"
    "&endPeriod=2023"
    "&dimensionAtObservation=AllDimensions"
)

headers = {"Accept": "text/csv"}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

df = pd.read_csv(StringIO(response.text))

# 4 quốc gia
countries = ["DEU", "USA", "KOR", "JPN"]

# Lọc đúng series Average Annual Wages
df = df[
    (df["REF_AREA"].isin(countries)) &
    (df["MEASURE"] == "WG") &
    (df["UNIT_MEASURE"] == "USD_PPP") &
    (df["PAY_PERIOD"] == "A") &
    (df["PRICE_BASE"] == "Q") &
    (df["AGGREGATION_OPERATION"] == "MEAN") &
    (df["SEX"] == "_Z")
].copy()

print("Số dòng sau khi lọc:", len(df))

# Chỉ lấy các cột cần thiết
df = df[
    [
        "REF_AREA",
        "TIME_PERIOD",
        "OBS_VALUE"
    ]
].copy()

# Đổi tên
df = df.rename(
    columns={
        "REF_AREA": "Country_Code",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "Value"
    }
)

# Thông tin chỉ tiêu
df["Indicator_Code"] = "WAGES"
df["Indicator"] = "Average annual wages"
df["Unit"] = "USD PPP per year"

# Tên quốc gia
country_names = {
    "DEU": "Germany",
    "USA": "United States",
    "KOR": "South Korea",
    "JPN": "Japan"
}

df["Country"] = df["Country_Code"].map(country_names)

# Sắp xếp cột
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

# Validation
print("\nKiểm tra:")
print("Số dòng:", len(df))
print("Số quốc gia:", df["Country_Code"].nunique())
print("Các quốc gia:", df["Country_Code"].unique())
print("Số năm:", df["Year"].nunique())
print("Năm:", sorted(df["Year"].unique()))
print("Missing:", df.isna().sum().sum())

print("\nDữ liệu:")
print(df.to_string(index=False))

# Lưu
output_path = "data/processed/oecd_wages_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nĐã lưu: {output_path}")