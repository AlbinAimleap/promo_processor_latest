from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class DollarDiscountProcessor(PromoProcessor, version=1):
    """Processor for handling '$X off' type promotions."""
    
    patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off'
    ]
    
    def calculate_deal(self, item, match):
        """Process '$X off' type promotions for deals."""
        
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        volume_deals_price = price - discount_value
        
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(volume_deals_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["quantity"] = 1
        return item_data
        
    def calculate_coupon(self, item, match):
        """Process '$X off' type promotions for coupons."""
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        unit_price = price - discount_value
            
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount_value, 2)
        item_data["quantity"] = 1
        return item_data

class DollarDiscountQuantityProcessor(PromoProcessor, version=2):
    """Processor for handling '$X off when buy Y' type promotions."""
    
    patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+when\s+buy\s+(?P<quantity>\d+)(?:\s+limit\s+(?P<limit>\d+))?'
    ]
    
    def calculate_deal(self, item, match):
        """Process '$X off when buy Y' type promotions for deals."""
        
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        quantity = int(match.group('quantity'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        volume_deals_price = (price * quantity - discount_value) / quantity
        
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(volume_deals_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["quantity"] = quantity
        return item_data
        
    def calculate_coupon(self, item, match):
        """Process '$X off when buy Y' type promotions for coupons."""
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        quantity = int(match.group('quantity'))
        limit = int(match.group('limit')) if 'limit' in match.groupdict() else quantity
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        if limit > quantity:
            unit_price = (price * limit) - (discount_value / quantity)
        else:
            unit_price = price - (discount_value / quantity)
            
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount_value, 2)
        item_data["quantity"] = quantity
        return item_data

class DollarDiscountLimitProcessor(PromoProcessor, version=3):
    """Processor for handling '$X off limit Y' type promotions."""
    
    patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+limit\s+(?P<limit>\d+)'
    ]
    
    def calculate_deal(self, item, match):
        """Process '$X off limit Y' type promotions for deals."""
        
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        limit = int(match.group('limit'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        volume_deals_price = price - (discount_value / limit)
        
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(volume_deals_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["quantity"] = limit
        return item_data
        
    def calculate_coupon(self, item, match):
        """Process '$X off limit Y' type promotions for coupons."""
        item_data = item.copy()
        discount_value = float(match.group('discount'))
        limit = int(match.group('limit'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        unit_price = price - (discount_value / limit)
            
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount_value, 2)
        item_data["quantity"] = limit
        return item_data

class BuyNGetMDiscountProcessor(PromoProcessor, version=4):
    """Processor for handling 'Buy N Get M $X Off' type promotions."""
    
    patterns = [
        r'Buy\s+(?P<buy>\d+)\s+Get\s+(?P<get>\d+)\s+\$(?P<discount>\d+(?:\.\d+)?)\s+Off'
    ]
    
    def calculate_deal(self, item, match):
        """Process 'Buy N Get M $X Off' type promotions for deals."""
        
        item_data = item.copy()
        buy_quantity = int(match.group('buy'))
        get_quantity = int(match.group('get'))
        discount_value = float(match.group('discount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_quantity = buy_quantity + get_quantity
        volume_deals_price = (price * total_quantity - discount_value) / total_quantity
        
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(volume_deals_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["quantity"] = total_quantity
        return item_data
        
    def calculate_coupon(self, item, match):
        """Process 'Buy N Get M $X Off' type promotions for coupons."""
        item_data = item.copy()
        buy_quantity = int(match.group('buy'))
        get_quantity = int(match.group('get'))
        discount_value = float(match.group('discount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_quantity = buy_quantity + get_quantity
        unit_price = price - (discount_value / total_quantity)
            
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount_value / total_quantity, 2)
        item_data["quantity"] = total_quantity
        return item_data