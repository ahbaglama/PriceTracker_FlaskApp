import requests
from bs4 import BeautifulSoup

def fetch_trendyol_product_data(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    
    # Get the page content
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the product name
    product_name_tag = soup.find("h1", {"class": "pr-new-br"})
    if not product_name_tag:
        product_name_tag = soup.find("span", {"class": "product-name"})  # Alternative selector, you can adjust this
    product_name = product_name_tag.text.strip() if product_name_tag else "Product name not found"

    # Extract the product image URL
    product_image_tag = soup.select_one("div.gallery-container img")
    product_image = product_image_tag["src"] if product_image_tag else "Product image not found"

    # Extract the product price
    product_price_tag = soup.find("span", {"class": "prc-dsc"})
    if not product_price_tag:
        product_price_tag = soup.find("span", {"class": "prc-slg"})  # Alternative selector for price
    product_price = product_price_tag.text.strip() if product_price_tag else "Product price not found"

    return {
        "name": product_name,
        "image": product_image,
        "price": product_price
    }

# Example usage
product_url = "https://www.trendyol.com/supplementler/com-creatine-creapure-120-kapsul-p-770005297?boutiqueId=61&merchantId=105100"
product_data = fetch_trendyol_product_data(product_url)

print(product_data)
