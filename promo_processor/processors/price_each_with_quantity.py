from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class PriceEachWithQuantityProcessor(PromoProcessor):
    """Processor for handling '$X price each with Y' type promotions."""
    
    patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+each\s+(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)']
    
    
    
    def calculate_deal(self, item, match):
        """Process '$X price each with Y' type promotions for deals."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        total_price = price_each * quantity
        
        item_data["volume_deals_price"] = base_round(total_price, 2)
        item_data["unit_price"] = base_round(price_each, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Process '$X price each with Y' type promotions for coupons."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        unit_price = base_round((item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - (price_each / quantity), 2)
        
        item_data["unit_price"] = base_round(unit_price)
        item_data["digital_coupon_price"] = base_round(price_each)
        return item_data
        
        