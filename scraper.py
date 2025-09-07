# Import library yang dibutuhkan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# --- Konfigurasi WebDriver dengan opsi khusus ---
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)
# Membuat instance Chrome WebDriver
driver = webdriver.Chrome(options=options)

try:
    # --- Akses halaman Worldometer ---
    url = "https://www.worldometers.info/world-population/population-by-country/"
    driver.get(url)

    # --- Tunggu hingga tabel utama muncul (maksimal 15 detik) ---
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "india"))  # ID dari salah satu baris tabel
    )

    # --- Ambil semua baris data dari tabel ---
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    # --- Siapkan list untuk menyimpan data ---
    data = []

    # --- Iterasi setiap baris untuk mengekstrak data ---
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 0:
            data.append({
                "Country": columns[1].text.strip(),
                "Population": columns[2].text.strip(),
                "Yearly Change": columns[3].text.strip(),
                "Net Change": columns[4].text.strip(),
                "Density (P/Km²)": columns[5].text.strip(),
                "Land Area (Km²)": columns[6].text.strip(),
                "Migrants (net)": columns[7].text.strip(),
                "Fertility Rate": columns[8].text.strip(),
                "Median Age": columns[9].text.strip(),
                "Urban Population (%)": columns[10].text.strip(),
                "World Share (%)": columns[11].text.strip()
            })

    # --- Konversi list data ke DataFrame pandas ---
    df = pd.DataFrame(data)

    # --- Simpan data ke CSV dengan encoding UTF-8 ---
    df.to_csv("data/world_population_by_country.csv", index=False, encoding="utf-8")

    print("✅ Proses scrapping berhasil. Data tersimpan di 'data/world_population_by_country.csv'")

finally:
    # --- Tutup WebDriver meskipun terjadi error ---
    driver.quit()