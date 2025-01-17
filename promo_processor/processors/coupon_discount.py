import math
from promo_processor.processor import PromoProcessor

class CouponDiscountProcessor(PromoProcessor):
    patterns = [
        r"(?:Coupon):\s+\$?(?P<discount>\d+(?:\.\d+)?)\s+(?:off|%)",
    ]
    
    
    def calculate_deal(self, item, match):
        """Process 'Coupon: $X off' type promotions."""        
        item_data = item.copy()
        discount = float(match.group('discount'))
        price = item_data.get("promo_price", item_data.get("regular_price", 0))
        volume_deals_price = price - discount
        
        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(volume_deals_price / 1, 2)
        item_data['digital_coupon_price'] = ""
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Process coupon discount calculation."""
        
        item_data = item.copy()
        discount = float(match.group('discount'))
        price = item_data.get("unit_price") or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        volume_deals_price = price - discount
        
        item_data['digital_coupon_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(volume_deals_price / 1, 2)
        return item_data
        
class AddtionalDiscountProcessor(PromoProcessor,version=2):
    #Additional 25% off When you spend $10 When you spend $10 or more on participating items
    patterns = [
        r"Additional\s+(?P<discount>\d+)%\soff\s++when\s+you\s+spend\s+\$(?P<price>\d+)\s"
    ]
    
    
    def calculate_deal(self, item, match):
        """Additional X% off When you spend $Y When you spend $Y or more on participating items."""        
        item_data = item.copy()
        spend = int(match.group('price'))
        discount = int(match.group('discount'))
        discounted_rate = discount/100
        price = item_data.get('regular_price', 0)
        if price>spend:
            volume_deals_price = price
            unit_price = price * discounted_rate
        else:
            quantity = 1 / price
            quantity_needed = math.ceil(spend/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price - (total_price*discounted_rate)
            unit_price = volume_deals_price /quantity_needed 
        
        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = ""
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Process coupon discount calculation."""
        
        item_data = item.copy()
        spend = int(match.group('price'))
        discount = int(match.group('discount'))
        discounted_rate = discount/100
        price = item_data.get('regular_price', 0)
        if price>spend:
            volume_deals_price = price
            unit_price = price * discounted_rate
        else:
            quantity = 1 / price
            quantity_needed = math.ceil(spend/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price - (total_price*discounted_rate)
            unit_price = volume_deals_price /quantity_needed 
        
        item_data['digital_coupon_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
        return item_data