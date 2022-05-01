# Bushra Amjad
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.zameen.com/Plots/Rawalpindi_Bahria_Town_Rawalpindi-632-1.html"
base = "https://www.zameen.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

data = []
amenities = []
for page in range(1, 20):
    print("Scraping data from page ", page, " ...")
    k = requests.get('https://www.zameen.com/Plots/Rawalpindi_Bahria_Town_Rawalpindi-632-{}.html'.format(page)).text
    soup = BeautifulSoup(k, 'html.parser')
    productlist = soup.find_all("li", {"class": "ef447dde"})

    productlinks = []
    for product in productlist:
        link = product.find("a", {"class": "_7ac32433"}).get('href')
        productlinks.append(base + link)

    for link in productlinks:
        f = requests.get(link, headers=headers).text
        hun = BeautifulSoup(f, 'html.parser')

        try:
            type = hun.find("span", {"aria-label": "Type"}).text.replace('\n', "")
        except:
            type = None

        try:
            price = hun.find("div", {"class": "c4fc20ba"}).text.replace('\n', "")
        except:
            price = None

        try:
            location = hun.find("div", {"class": "cbcd1b2b"}).text.replace('\n', "")
        except:
            location = None

        try:
            bath = hun.find("span", {"aria-label": "Baths"}).text.replace('\n', "")
        except:
            bath = None

        try:
            area = hun.find("span", {"aria-label": "Area"}).text.replace('\n', "")
        except:
            area = None

        try:
            bed = hun.find("span", {"aria-label": "Beds"}).text.replace('\n', "")
        except:
            bed = None

        try:
            spans = hun.find_all('span', "_17984a2c")
            Possesion = "-"
            Corner = "-"
            Balloted = "-"
            Sewerage = "-"
            Electricity = "-"
            Water = "-"
            Sui = "-"
            Boundary = "-"
            School = "-"
            Hospital = "-"
            Restaurant = "-"
            Transport = "-"
            Security = "-"
            for span in spans:
                if span.text == "Possesion":
                    Possesion = "Yes"

                elif span.text == "Corner":
                    Corner = "Yes"

                elif span.text == "Balloted":
                    Balloted = "Yes"

                elif span.text == "Sewerage":
                    Sewerage = "Yes"

                elif span.text == "Electricity":
                    Electricity = "Yes"

                elif span.text == "Water Supply":
                    Water = "Yes"

                elif span.text == "Sui Gas":
                    Sui = "Yes"

                elif span.text == "Boundary Wall":
                    Boundary = "Yes"

                elif span.text == "Nearby Schools":
                    School = "Yes"

                elif span.text == "Nearby Hospitals":
                    Hospital = "Yes"

                elif span.text == "Nearby Restaurants":
                    Restaurant = "Yes"

                elif span.text == "Nearby Public Transport Service":
                    Transport = "Yes"

                elif span.text == "Security Staff":
                    Security = "Yes"

            amentity = {"Possession": Possesion, "Balloted": Balloted, "Sewerage": Sewerage,
                        "Electricity": Electricity,"Water Supply": Water, "Sui Gas": Sui,
                        "Boundary Wall": Boundary, "Nearby Schools": School,
                        "Nearby Hospitals": Hospital, "Public Transport": Transport,
                        "Nearby Restaurants": Restaurant,"Security Staff": Security}
            amenities.append(amentity)
        except:
            amenities.append(None)

        plot = {"type": type, "price": price, "location": location, "bath": bath, "area": area, "bed": bed, }
        data.append(plot)

plots_df = pd.DataFrame(data)
amenities_df = pd.DataFrame(amenities)
final_plots_df = pd.concat([plots_df, amenities_df], axis=1)
print(final_plots_df)
final_plots_df.to_csv(r'C:\Users\Bushra Amjad\scraper\final_scraped_data.csv', index=False)
