from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class SelectDealProcessor(PromoProcessor):
    patterns = [
        r"Deal:\s+\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+on\s+" 
    ]
    
    
    def calculate_deal(self, item, match):
        """Process 'Deal: $X price on select' type promotions."""
        item_data = item.copy()
        select_price = float(match.group('price'))
        
        item_data["volume_deals_price"] = base_round(select_price)
        item_data["unit_price"] = base_round(select_price)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    
    def calculate_coupon(self, item, match):
        """Calculate the price for 'Deal: $X price on select' promotions when a coupon is applied."""
        item_data = item.copy()
        select_price = float(match.group('price'))
        unit_price = (item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - select_price
        
        item_data["unit_price"] = base_round(unit_price)
        item_data["digital_coupon_price"] = base_round(select_price)
        return item_data
        