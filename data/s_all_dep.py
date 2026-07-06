import requests
from bs4 import BeautifulSoup
import pandas as pd
doctor_data=[]

url = "https://www.ananthapurihospitals.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

department_links = []

ignore = {
    "Patient_Care",
    "health-package",
    "homecare",
    "contact",
    "chairman",
    "privacy-policy",
    "terms-and-condition",
    "clinical-careers",
    "blood-bank",
    "support-services",
    "health-insurances",
    "nursing",
    "paramedical",
    "index",
    "about",
    "Patient_Care",
    "health-package",
    "homecare",
    "contact",
    "chairman",
    "privacy-policy",
    "terms-and-condition",
    "clinical-careers",
    "blood-bank",
    "support-services",
    "health-insurances",
    "nursing",
    "paramedical",
    "index",
    "International-patients",
    "ananthapuri_blog",
    "dnb-course",
    "emergency",
    "#"

}

for link in soup.find_all("a"):
    href = link.get("href")

    if not href:
        continue

    if not href.startswith("https://www.ananthapurihospitals.com/"):
        continue

    if "/doctors/" in href:
        continue

    if href.startswith("mailto:") or href.startswith("tel:"):
        continue

    page = href.split("/")[-1]

    if page in ignore:
        continue

    if href not in department_links:
        department_links.append(href)

print("Departments Found:", len(department_links))

for department in department_links:

    print("Opening:", department)

    try:
        response = requests.get(
            department,
            headers=headers,
            timeout=10
        )

        print("Status:", response.status_code)

        # Parse department page
        department_soup = BeautifulSoup(response.text, "html.parser")

        # Collect doctor links
        doctor_links = set()

        for link in department_soup.find_all("a"):
            href = link.get("href")

            if href and "/doctors/" in href:
                doctor_links.add(href)

        print("=" * 50)
        print("Department:", department)
        print("Doctors Found:", len(doctor_links))
        for doctor in doctor_links:
         print(doctor)

        # Visit each doctor's page
        for doctor_url in doctor_links:

            doctor_response = requests.get(
                doctor_url,
                headers=headers,
                timeout=10
            )

            doctor_soup = BeautifulSoup(
                doctor_response.text,
                "html.parser"
            )

            doctor_name = doctor_soup.find("h2").text.strip()

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
                print(
    "Adding:",
    doctor_name,
    "| Department:",
    details.get("Department", "")
)
      
            doctor_data.append({
    "Doctor Name": doctor_name,
    "Qualification": details.get("Qualification", ""),
    "Designation": details.get("Designation", ""),
    "Department": details.get("Department", ""),
    "OP Days": details.get("OP Days", "")
})

    except requests.exceptions.RequestException:
        print("Skipped:", department)
        continue
print("Total doctors collected:", len(doctor_data))

df = pd.DataFrame(doctor_data)

df.to_excel("doctors.xlsx", index=False)

print("Excel file created successfully!")