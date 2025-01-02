from pydantic import BaseModel
from typing import Optional
from datetime import date
import argparse
import json
import sys
import re


class StoreProduct(BaseModel):
    zipcode: Optional[int]
    store_name: str
    store_location: str
    store_logo: str
    store_brand: str
    category: str
    sub_category: str
    product_title: str
    weight: str
    regular_price: Optional[float]
    sale_price: Optional[float]
    volume_deals_description: Optional[str]
    volume_deals_price: Optional[float]
    digital_coupon_description: Optional[str]
    digital_coupon_price: Optional[float]
    unit_price: Optional[float]
    image_url: str
    url: str
    upc: Optional[str]
    crawl_date: date
    remarks: Optional[str] = ""
    qc_remarks: Optional[str] = ""

    @staticmethod
    def validate_product(data):
        remarks = []
        qc_remarks = []
        remarks = []

        # Helper function to safely parse float values
        def parse_float(value, field_name):
            if value == '' or value is None:
                return 0
            try:
                return float(value)
            except ValueError:
                qc_remarks.append(f"{field_name} contains invalid value")
                return 0

        # Parse numeric fields
        data['regular_price'] = parse_float(data.get('regular_price'), 'regular_price')
        data['sale_price'] = parse_float(data.get('sale_price'), 'sale_price')
        data['volume_deals_price'] = parse_float(data.get('volume_deals_price'), 'volume_deals_price')
        data['digital_coupon_price'] = parse_float(data.get('digital_coupon_price'), 'digital_coupon_price')
        data['unit_price'] = parse_float(data.get('unit_price'), 'unit_price')
        
        if data.get('unit_price') and data.get('sale_price') and (data.get('digital_coupon_description') and data.get('unit_price') == data.get('sale_price')):
            qc_remarks.append('processed:fail')
            remarks.append("promo already applied")
        # Volume deals validation
        elif data.get('volume_deals_description') and not data.get('volume_deals_price'):
            qc_remarks.append('processed:fail')

        # Digital coupon validation
        elif data.get('digital_coupon_description') and not data.get('digital_coupon_price'):
            qc_remarks.append('processed:fail')
        
        # Sale price validation
        if data.get('sale_price') is not None and data.get('sale_price') >= data.get('regular_price', 0):
            qc_remarks.append('sale_price:fail')

        # Unit price validation
        if data.get('unit_price') is not None and any([data.get('digital_coupon_description'), data.get('volume_deals_description')]) and data.get('unit_price') <= 0:
            qc_remarks.append('unit_price:fail')
        
        

        # UPC validation
        if not data.get('upc'):
            qc_remarks.append('upc:fail')

        # Zipcode validation
        if data.get('zipcode') and (len(str(data.get('zipcode'))) != 5):
            qc_remarks.append('zipcode:fail')

        # Additional validation for specific patterns
        exclude = [r"Earn \d+X Points*", r"Free with Purchase", r"\d+X Fuel Points"]
        if data.get('digital_coupon_description') or data.get('volume_deals_description'):
            for exclude_item in exclude:
                if (data.get('digital_coupon_description') and re.search(exclude_item, data.get('digital_coupon_description'))) or \
                   (data.get('volume_deals_description') and re.search(exclude_item, data.get('volume_deals_description'))):
                    qc_remarks.append('excluded_promotion:fail')
                    break

        if not data.get('remarks') and data.get('volume_deals_description') and not data.get('volume_deals_price'):
            remarks.append('unable to process promo/invalid promo')

        elif data.get('digital_coupon_description') and not data.get('digital_coupon_price'):
            remarks.append('unable to process promo/invalid promo')

        if data.get('unit_price') and data.get('unit_price') < 0:
            qc_remarks.append('unprocessed:fail')

        data['qc_remarks'] = '; '.join(qc_remarks) if qc_remarks else ""
        data['remarks'] = '; '.join(remarks) if remarks else ""
        return data

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }
def format_zeros(data):
    keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
    for item in data:
        for key in keys:
            if item[key] == 0 or item[key] == 0.0:
                item[key] = ""
    return data

def main():
    parser = argparse.ArgumentParser(description='Process store product data')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output JSON file path')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            data = json.load(f)

        validated_products = []
        for item in data:
            # try:
                item = StoreProduct.validate_product(item)
                product = StoreProduct(**item)
                product_dict = product.model_dump()
                product_dict['crawl_date'] = product_dict['crawl_date'].isoformat()  # Serialize date
                validated_products.append(product_dict)
            # except Exception as e:
            #     print(f"Validation error for item: {item.get('product_title', 'Unknown')}", file=sys.stderr)
            #     print(f"Error: {str(e)}", file=sys.stderr)

        with open(args.output_file, 'w') as f:
            json.dump(format_zeros(validated_products), f, indent=2)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()