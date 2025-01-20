from promo_processor.processor import PromoProcessor
from promo_processor import base_round


class TargetCircleDealProcessor(PromoProcessor):
    """Processor for Target Circle Deals"""

    patterns = [
            r"Target Circle Deal\s*:\s*\$(\d+\.?\d*)\s+price\s+on\s+select\s+(.+)"
        ]
    
    
    
    # Example: "Target Circle Deal: $10.99 price on select items"

    def calculate_deal(self, item, match):
        """Calculate the final price after applying a coupon discount."""
        item_data = item.copy()
        select_price = float(match.group(1))
        
        item_data['volume_deals_price'] = base_round(select_price)
        item_data['unit_price'] = base_round(select_price)
        item_data['digital_coupon_price'] = ""
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        select_price = float(match.group(1))
        
        item_data['volume_deals_price'] = base_round(select_price)
        item_data['unit_price'] = base_round(select_price)
        item_data['digital_coupon_price'] = ""
        return item_data