import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.gsmarena.com"

def get_brands():
    url = f"{BASE_URL}/makers.php3"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    brands = soup.select("td > a")
    return [(b.text.strip(), BASE_URL + "/" + b['href']) for b in brands]

def get_phone_models_from_brand_page(brand_url):
    phones = []
    while brand_url:
        response = requests.get(brand_url)
        soup = BeautifulSoup(response.text, "html.parser")
        models = soup.select(".makers a")
        for model in models:
            name_tag = model.find("strong")
            if name_tag:
                name = name_tag.text.strip()
                link = BASE_URL + "/" + model["href"]
                phones.append({"name": name, "url": link})
        
        # Get next page link if available
        next_page = soup.find("a", text="Next")
        if next_page:
            brand_url = BASE_URL + "/" + next_page['href']
        else:
            break
        time.sleep(1)  # Be nice to the server
    return phones

def main():
    all_data = {}
    brands = get_brands()

    for brand_name, brand_url in brands:
        print(f"Scraping {brand_name}...")
        models = get_phone_models_from_brand_page(brand_url)
        all_data[brand_name] = models
        time.sleep(1)

    with open("all_phones.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print("✅ All phone models saved to all_phones.json")

if __name__ == "__main__":
    main()
