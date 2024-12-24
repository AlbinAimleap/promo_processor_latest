from promo_processor.processor import PromoProcessor

class DollarDiscountProcessor(PromoProcessor):
    """Processor for handling '$X off' type promotions."""
    
    patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off',
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+when\s+buy\s+(?P<quantity>\d+)(?:\s+limit\s+(?P<limit>\d+))?',
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+limit\s+(?P<limit>\d+)'
    ]
    
    def calculate_deal(self, item, match):
        """Process '$X off' type promotions for deals."""
        
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        quantity = int(match.group('quantity')) if 'quantity' in match.groupdict() else 1
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        if quantity > 1:
            volume_deals_price = (price * quantity - discount_value) / quantity
        else:
            volume_deals_price = price - discount_value
        
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(volume_deals_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["quantity"] = quantity
        return item_data
        
    def calculate_coupon(self, item, match):
        """Process '$X off' type promotions for coupons."""
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        quantity = int(match.group('quantity')) if 'quantity' in match.groupdict() else 1
        limit = int(match.group('limit')) if 'limit' in match.groupdict() else None
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        if quantity > 1:
            unit_price = price - (discount_value / quantity)
        else:
            unit_price = price - discount_value
            
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(discount_value / quantity, 2)
        item_data["quantity"] = quantity
        return item_data