from promo_processor.processor import PromoProcessor

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
        
        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
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
        
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = round(volume_deals_price, 2)
        
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
        total_quantity = quantity + free
        
        total_price = price * total_quantity
        discount_amount = total_price * (1 - discount / 100)
        unit_price = (total_price - discount_amount) / total_quantity
        
        item_data['volume_deals_price'] = round(discount_amount, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = 0
        
        return item_data
    
    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Get Y % off' promotions."""
        item_data = item.copy()
        
        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        discount = int(match.group('discount'))
        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_quantity = quantity + free
        
        total_price = price * total_quantity
        discount_amount = total_price * (1 - discount / 100)
        unit_price = (total_price - discount_amount) / total_quantity
        
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = round(discount_amount, 2)
        
        return item_data