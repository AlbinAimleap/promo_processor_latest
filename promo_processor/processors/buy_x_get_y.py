from promo_processor.processor import PromoProcessor
from promo_processor import base_round
import math

class BuyGetFreeProcessor(PromoProcessor, version=1):
    patterns = [
        r"Buy\s+(?P<quantity>\d+),?\s+Get\s+(?P<free>\d+)\s+Free"
    ]
    
    def calculate_deal(self, item, match):
        """Process 'Buy X Get Y Free' specific promotions."""
        item_data = item.copy()
        
        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        price = item_data.get('regular_price', 0)
        total_quantity = quantity + free
        
        volume_deals_price = price * quantity
        unit_price = volume_deals_price / total_quantity if total_quantity > 0 else 1
        
        item_data['volume_deals_price'] = base_round(volume_deals_price)
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = 0
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Get Y Free' promotions."""
        item_data = item.copy()
        
        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_quantity = quantity + free
        
        price = float(price) if price else 0
        volume_deals_price = price * quantity
        unit_price = volume_deals_price / total_quantity
        
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = base_round(volume_deals_price)
        
        return item_data


class BuyGetDiscountProcessor(PromoProcessor, version=2):
    patterns = [
        r"Buy\s+(?P<quantity>\d+),\s+get\s+(?P<free>\d+)\s+(?P<discount>\d+)%\s+off"
    ]
    
    def calculate_deal(self, item, match):
        """Process 'Buy X Get Y % off' specific promotions."""
        item_data = item.copy()
        
        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        discount = int(match.group('discount'))
        price = item_data.get('sale_price') or item_data.get('regular_price', 0)
        volume_deals_price = price + price -(price * (discount / 100))
        unit_price = volume_deals_price / (quantity + free)
       
        
        item_data['volume_deals_price'] = base_round(volume_deals_price)
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = 0
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Get Y % off' promotions."""
        item_data = item.copy()
        
        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        discount = int(match.group('discount'))
        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        digital_coupon_price = price + price - (price * (discount / 100))
        unit_price = digital_coupon_price / (quantity + free)
        
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = base_round(digital_coupon_price)
        
        return item_data
    

class SpendGetFreeProcessor(PromoProcessor, version=3):
    #Spend $10 Get 1 Free
    patterns = [
        #r"Spend\s+\$(?P<price>\d+),?\s+Get\s+(?P<free>\d+)\s+Free"
    ]
    
    def calculate_deal(self, item, match):
        """Process 'Spend X Get Y Free' specific promotions."""
        item_data = item.copy()
        
        spend = int(match.group('price'))
        free = int(match.group('free'))
        price = item_data.get('regular_price', 0)
        if price>spend:
            volume_deals_price = price
            unit_price = price / free
        else:
            quantity = 1 / price
            quantity_needed = math.ceil(spend/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price
            unit_price = price / (quantity_needed+free)
            
        item_data['volume_deals_price'] = base_round(volume_deals_price)
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = 0
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Spend X Get Y Free' promotions."""
        item_data = item.copy()
        
        spend = int(match.group('price'))
        free = int(match.group('free'))
        price = item_data.get('regular_price', 0)
        if price>spend:
            volume_deals_price = price
            unit_price = price / free
        else:
            quantity = 1 / price
            quantity_needed = math.ceil(spend/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price
            unit_price = price / (quantity_needed+free)
            
        item_data['unit_price'] = base_round(unit_price)
        item_data['digital_coupon_price'] = base_round(volume_deals_price)
        
        return item_data
