#Doğrulama Kodu
import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)


import requests
import pandas as pd

# Verilen URL'den Excel dosyasını indirin
url = "https://task.haydigiy.com/FaprikaOrderXls/HN5JZR/1/"
response = requests.get(url)
filename = "Bozuk Siparişler.xlsx"

# İndirilen dosyayı kaydedin
with open(filename, 'wb') as file:
    file.write(response.content)

# Excel dosyasını okuyun
df = pd.read_excel(filename)

# "AraToplam" ve "ToplamFiyat" sütunlarındaki virgül sonrasını silin
df["AraToplam"] = df["AraToplam"].str.replace(",.*", "", regex=True)
df["ToplamFiyat"] = df["ToplamFiyat"].str.replace(",.*", "", regex=True)

# "AraToplam" ve "ToplamFiyat" sütunlarını sayısal değerlere dönüştürün
df["AraToplam"] = pd.to_numeric(df["AraToplam"], errors="coerce")
df["ToplamFiyat"] = pd.to_numeric(df["ToplamFiyat"], errors="coerce")

# "Id" sütunundaki aynı olan değerlerin "ToplamFiyat" sütunundaki toplamını hesaplayıp yeni bir sütuna yazın
df["ToplamFiyatToplam"] = df.groupby("Id")["ToplamFiyat"].transform("sum")

# "AraToplam" sütunundan "ToplamFiyatToplam" sütunundaki verileri çıkarıp yeni bir sütuna yazın
df["Sonuc"] = df["AraToplam"] - df["ToplamFiyatToplam"]

# "AraToplam" ve "ToplamFiyatToplam" sütunlarını silin
df.drop(["AraToplam", "ToplamFiyatToplam"], axis=1, inplace=True)

# İstenmeyen sütunları silin
columns_to_keep = ["Id", "Sonuc"]
df = df[columns_to_keep]

# Tekrarlanan satırları düşürün
df.drop_duplicates(inplace=True)

# "Sonuc" sütunundaki değeri 30'dan küçük olan satırları silin
df = df[df["Sonuc"] >= 30]

# Veriyi orijinal Excel dosyasına kaydedin (üzerine yazdırma)
df.to_excel(filename, index=False)

print(f"Veri başarıyla işlendi ve orijinal Excel dosyasının üzerine yazıldı.")
