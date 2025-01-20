from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class AboutEachPriceProcessor(PromoProcessor, version=1):
    patterns = [r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+limit\s+(?P<quantity>\d+)\s+.*?limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+Each",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+limit\s+(?P<quantity>\d+)\s+.*?limit\s+(?P<min_quantity>\d+)\s"
                ]
    
    
    # Example: "$5.99 Each" or "$2.50 Each"

    def calculate_deal(self, item, match):
        item_data = item.copy()
        unit_price = float(match.group('unit_price'))
        quantity = item_data.get("quantity", 1)
        volume_deals_price = unit_price * quantity
        unit_price_calculated = volume_deals_price / quantity
        
        item_data['volume_deals_price'] = base_round(volume_deals_price)
        item_data['unit_price'] = base_round(unit_price_calculated)
        item_data['digital_coupon_price'] = 0
        
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        unit_price = float(match.group('unit_price'))
        quantity = item_data.get("quantity", 1)
        volume_deals_price = unit_price * quantity
        unit_price_calculated = volume_deals_price / quantity
        
        item_data['digital_coupon_price'] = base_round(unit_price)
        item_data["unit_price"] = base_round(unit_price_calculated)
        
        return item_data

class SaveEachWhenBuyMoreProcessor(PromoProcessor, version=2):
    patterns = [r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+each\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more"]
    # Save $1 each when you buy 5 or more
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount = float(match.group('discount'))
        min_quantity = int(match.group('min_quantity'))
        quantity = item_data.get("quantity", 1)
        original_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        volume_deals_price = discount * min_quantity
        unit_price = ((original_price * min_quantity) - volume_deals_price) / min_quantity
        item_data['volume_deals_price'] = base_round(volume_deals_price)
        item_data['unit_price'] = base_round(unit_price)
        
        
        item_data['digital_coupon_price'] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount = float(match.group('discount'))
        min_quantity = int(match.group('min_quantity'))
        quantity = item_data.get("quantity", 1)
        original_price = item_data.get("unit_price", 0)

        if quantity >= min_quantity:
            discounted_price = original_price - discount
            item_data['digital_coupon_price'] = base_round(discount)
            item_data["unit_price"] = base_round(discounted_price)
            
        return item_data