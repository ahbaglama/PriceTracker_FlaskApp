from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ProductURL(BaseModel):
    url: str

def fetch_trendyol_product_data(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_name_tag = soup.find("h1", {"class": "pr-new-br"})
    if not product_name_tag:
        product_name_tag = soup.find("span", {"class": "product-name"})
    product_name = product_name_tag.text.strip() if product_name_tag else "Product name not found"

    product_image_tag = soup.select_one("div.gallery-container img")
    product_image = product_image_tag["src"] if product_image_tag else "Product image not found"

    product_price_tag = soup.find("span", {"class": "prc-dsc"})
    if not product_price_tag:
        product_price_tag = soup.find("span", {"class": "prc-slg"})
    product_price = product_price_tag.text.strip() if product_price_tag else "Product price not found"

    return {
        "name": product_name,
        "image": product_image,
        "price": product_price
    }

@app.post("/fetch-product-data")
async def get_product_data(product_url: ProductURL):
    try:
        product_data = fetch_trendyol_product_data(product_url.url)
        return product_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
