from promo_processor.processor import PromoProcessor

class PercentageDiscountProcessor(PromoProcessor):
    patterns = [
        r"^(?P<discount>20)%\s+off",
        r"^Deal:\s+(?P<discount>\d+)%\s+off", 
        r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s-]+)",
        r"^Save\s+(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"^(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"^Save\s+(?P<discount>\d+)%\s+with\s+(?P<quantity>\d+)",
    ]    
    
    
    def calculate_deal(self, item, match):
        """Process 'X% off' type promotions."""
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        if "quantity" in match.groupdict():
            quantity = int(match.group('quantity'))
            total_price = price * quantity
            discounted_price = total_price * (1 - discount_decimal)
            unit_price = discounted_price / quantity
        else:
            discounted_price = price * (1 - discount_decimal)
            unit_price = discounted_price
        
        item_data["volume_deals_price"] = round(discounted_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon for percentage-based discounts."""
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price * (1 - discount_decimal)
        
        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = round(discounted_price, 2)
        return item_data