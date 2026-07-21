import pandas as pd
import requests
from bs4 import BeautifulSoup

# Target URL
URL = "http://books.toscrape.com/"


def scrape_products():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    data = []

    for product in products:
        # Title
        title = product.h3.a["title"]

        # Price & Cleaning
        price_text = product.find("p", class_="price_color").text
        # Remove unwanted encoding characters while preserving the currency symbol
        price_clean = price_text.replace("Â", "").strip()

        # Availability
        availability = product.find("p", class_="instock availability").text.strip()

        # Rating
        rating_class = product.find("p", class_="star-rating")["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "None"

        data.append(
            {
                "Product Title": title,
                "Price": price_clean,
                "Rating": rating,
                "Stock Status": availability,
            }
        )

    # Convert to DataFrame & Clean Data
    df = pd.DataFrame(data)

    # Save to CSV using utf-8-sig encoding for perfect Excel rendering
    output_filename = "ecommerce_price_tracker.csv"
    df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    print(f" Data successfully scraped and saved to '{output_filename}'")
    return df


if __name__ == "__main__":
    scrape_products()
