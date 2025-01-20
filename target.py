import re
import pandas as pd

class Target:
    def __init__(self, processor, df):
        self.processor = processor
        self.processor.pre_process(self.split_promos)
        self.processor.pre_process(self.sort_promos)
        self.processor.pre_process(self.split_promos)
        self.processor.process_item(df)
        self.processor.apply(self.reorder_item)
        self.processor.apply(self.skip_invalids)
        self.processor.apply(self.get_lowest_unit_price)
        self.processor.apply(self.format_zeros)
        self.processor.apply(self.format_date)
        
        
        
    
    def sort_promos(self, data):
        patterns = [
            r'(\d+)\s*for\s*\$(\d+\.?\d*)',                     # 2 for $5, 3 for $10
            r'(\d+)\s*@\s*\$(\d+\.?\d*)',                       # 2 @ $5, 3 @ $10
            r'(\d+)\s*\/\s*\$(\d+\.?\d*)',                      # 2/$5, 3/$10
            r'Buy\s*(\d+)\s*Get\s*(\d+)\s*Free',                # Buy 1 Get 1 Free, Buy 2 Get 1 Free
            r'Buy\s*(\d+)\s*Get\s*(\d+)\s*at\s*(\d+)%\s*off',   # Buy 1 Get 1 50% off, Buy 2 Get 1 25% off
            r'Buy\s*(\d+)\s*Save\s*\$(\d+\.?\d*)',              # Buy 2 Save $5, Buy 3 Save $10
            r'Mix\s*&\s*Match\s*(\d+)\s*for\s*\$(\d+\.?\d*)',   # Mix & Match 2 for $5, Mix & Match 3 for $10
            r'Save\s*\$(\d+\.?\d*)\s*when\s*you\s*buy\s',       # Save $5 when you buy, Save $10 when you buy
            r'Buy\s*(\d+),\s*get\s*(\d+)\s*free',               # Buy 3, get 1 free
            r'Buy\s*(\d+)\s*for\s*\$(\d+\.?\d*)',               # Buy 2 for $3
            r'Buy\s*(\d+)\s*get\s*(\d+)%\s*off',                # Buy 4 get 10% off
            r'Buy\s*(\d+),\s*get\s*(\d+)\s*(\d+)%\s*off',       # Buy 1, get 1 50% off
            r'Buy\s*1\s*get\s*1\s*25%\s*off',                   # Buy 1 get 1 25% off
            ]              
        for item in data:
            volume_desc = item["volume_deals_description"]
            digital_desc = item["digital_coupon_description"]
            
            if volume_desc:
                matches_pattern = any(re.search(pattern, volume_desc) for pattern in patterns)
                if not matches_pattern:
                    item["digital_coupon_description"] = volume_desc
                    item["volume_deals_description"] = ""
            
            if digital_desc:
                matches_pattern = any(re.search(pattern, digital_desc) for pattern in patterns)
                if matches_pattern:
                    item["volume_deals_description"] = digital_desc
                    item["digital_coupon_description"] = ""
        
        return data
             
    
    def remove_invalid_promos(self, data):
        for item in data:
            description = item["description"]
            description = re.sub(r'\$\d+\.\d+/lb', '', description)
            description = re.sub(r'^about \$\d+\.\d+ each', '', description)
            description = re.sub(r'^\$\d+\.\d{2}', '', description)
            item["description"] = description.strip()
        return data

    def reorder_item(self, data):
        order = [
            "zipcode", "store_name", "store_location", "store_logo", "store_brand",
            "category", "sub_category", "product_title", "weight",
            "regular_price", "sale_price", "volume_deals_description",
            "volume_deals_price", "digital_coupon_description",
            "digital_coupon_price", "unit_price", "image_url", "url",
            "upc", "crawl_date", "remarks"
        ]
        return [{key: item.get(key, "") for key in order} for item in data if item]

    def split_promos(self, data):
        new_data = []
        for item in data:
            if not item["digital_coupon_description"]:
                new_data.append(item.copy())
                continue
            promos = item["digital_coupon_description"].split("||")
            for promo in promos:
                item["digital_coupon_description"] = promo.strip()
                item["many"] = True
                new_data.append(item.copy())
        return new_data

    def get_lowest_unit_price(self, data):
        if not data:
            return data
        
        upc_dict = {}
        
        for item in data:
            upc = item.get("upc")
            unit_price = float(item.get("unit_price", 0) or 0)
            
            if upc not in upc_dict or unit_price < float(upc_dict[upc].get("unit_price", 0) or 0):
                upc_dict[upc] = item.copy()
            
            if item.get("many"):
                del item["many"]
        
        return list(upc_dict.values())

    def skip_invalids(self, data):
        for item in data:
            sale_price = float(item.get("sale_price", 0) or 0)
            regular_price = float(item.get("regular_price", 0) or 0)
            
            if item.get("unit_price") and item["unit_price"] < 0:
                volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
                digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)
                
                if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
                    item.update({"volume_deals_price": ""})
        return data

    def format_zeros(self, data):
        keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
        for item in data:
            for key in keys:
                if item[key] == 0:
                    item[key] = ""
        return data
    
    def format_date(self, data):
        df = pd.DataFrame(data)
        df['crawl_date'] = df['crawl_date'].astype(str)
        return df.to_dict(orient='records')
   
    def get_lowest_unit_price(self, data):
        if not data:
            return data
        
        upc_dict = {}
        
        for item in data:
            upc = item.get("upc")
            unit_price = float(item.get("unit_price", 0) or 0)
            
            if upc not in upc_dict or unit_price < float(upc_dict[upc].get("unit_price", 0) or 0):
                upc_dict[upc] = item.copy()
            
            if item.get("many"):
                del item["many"]
        
        return list(upc_dict.values())

    def skip_invalids(self, data):
        for item in data:
            sale_price = float(item.get("sale_price", 0) or 0)
            regular_price = float(item.get("regular_price", 0) or 0)
            
            if item.get("unit_price") and item["unit_price"] < 0:
                volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
                digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)
                
                if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
                    item.update({"volume_deals_price": ""})
        return data

    def format_zeros(self, data):
        keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
        for item in data:
            for key in keys:
                if item[key] == 0:
                    item[key] = ""
        return data

   