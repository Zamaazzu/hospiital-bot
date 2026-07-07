import pandas as pd
import requests
from bs4 import BeautifulSoup
doctor_data = []

url = "https://www.ananthapurihospitals.com/Neurology"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

doctor_links = set()  # Stores only unique links

for link in soup.find_all("a"):
    href = link.get("href")

    if href and "/doctors/" in href:
        doctor_links.add(href)
print("Total doctor links:", len(doctor_links))
for link in doctor_links:

    response = requests.get(link, headers=headers)
    doctor_soup = BeautifulSoup(response.text, "html.parser")

    doctor_name = doctor_soup.find("h2").text.strip()
    print("Processing:", doctor_name)
    doctor_info = doctor_soup.find("ul", class_="doctor-info-list")

    details = {}

    if doctor_info:
        for item in doctor_info.find_all("li"):
            text = item.text.strip()

            if "Qualifications" in text:
                details["Qualification"] = text.replace("Qualifications", "").strip()

            elif "Designation" in text:
                details["Designation"] = text.replace("Designation", "").strip()

            elif "OP days" in text:
                details["OP Days"] = text.replace("OP days :", "").strip()

            elif "Area/Working Department" in text:
                details["Department"] = text.replace("Area/Working Department", "").strip()

    doctor_data.append({
        "Doctor Name": doctor_name,
        "Qualification": details.get("Qualification", ""),
        "Designation": details.get("Designation", ""),
        "Department": details.get("Department", ""),
        "OP Days": details.get("OP Days", "")
    })
for doctor in doctor_data:
    print(doctor)
df = pd.DataFrame(doctor_data)

df.to_excel("doctors.xlsx", index=False)

print("Doctors saved successfully!")