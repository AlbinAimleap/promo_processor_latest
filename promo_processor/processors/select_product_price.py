from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class SelectProductPriceProcessor(PromoProcessor):
    """Processor for handling '$X price on select Product' type promotions."""

    patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+on\s+select\s+(?P<product>[\w\s-]+)']
    
    
    def calculate_deal(self, item, match):
        """Process '$X price on select Product' type promotions for deals."""
        item_data = item.copy()
        select_price = float(match.group('price'))
        weight = item_data.get('weight', 1)
        
        item_data["volume_deals_price"] = base_round(select_price)
        item_data["unit_price"] = base_round(select_price / 1)
        item_data["digital_coupon_price"] = 0
        

    def calculate_coupon(self, item, match):
        """Process '$X price on select Product' type promotions for coupons."""
        item_data = item.copy()
        select_price = float(match.group('price'))
        weight = item_data.get('weight', 1)
        
        item_data["unit_price"] = base_round(select_price / 1)
        item_data["digital_coupon_price"] = base_round(select_price)
        return item_data
        
       