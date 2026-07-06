import requests
from bs4 import BeautifulSoup

url = "https://www.ananthapurihospitals.com/doctors/Dr.-Anilkumar-T.-V"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

doctor_info = soup.find("ul", class_="doctor-info-list")

items = doctor_info.find_all("li")

for item in items:
    print(item.text.strip())