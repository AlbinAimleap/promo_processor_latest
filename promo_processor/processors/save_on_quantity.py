from promo_processor.processor import PromoProcessor
from promo_processor import base_round


class SaveOnQuantityTotalProcessor(PromoProcessor, version=1):
    patterns = [
        r"\$(?P<total_price>\d+(?:\.\d+)?)\s+SAVE\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\w+)\s+\(\d+\)",
    ]

    def calculate_deal(self, item, match):
        """Process '$X SAVE $Y on Z' type promotions."""
        item_data = item.copy()
        try:
            total_price = float(match.group('total_price'))
        except IndexError:
            total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))
            
        discount = float(match.group('discount'))
        quantity = float(match.group('quantity'))        
        
        volume_deals_price = (total_price * quantity) - discount
        
        item_data["volume_deals_price"] = base_round(discount, 2)
        item_data["unit_price"] = base_round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for Save $X on Y promotions."""
        item_data = item.copy()
        unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        if isinstance(unit_price, str) and not unit_price:
            unit_price = 0
        
        quantity = float(match.group('quantity'))
        discount = float(match.group('discount'))
        
        total_price = (unit_price * quantity) - discount
        unit_price = total_price / quantity if quantity > 0 else 0
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount, 2)
        return item_data


class SaveOnQuantityProductProcessor(PromoProcessor, version=2):
    patterns = [
        r"(?i)SAVE\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\d+)\s+(?P<product>[\w\s-]+)",
    ]

    def calculate_deal(self, item, match):
        """Process '$X SAVE $Y on Z' type promotions."""
        item_data = item.copy()
        try:
            total_price = float(match.group('total_price'))
        except IndexError:
            total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))
            
        discount = float(match.group('discount'))
        quantity = float(match.group('quantity'))        
        
        volume_deals_price = (total_price * quantity) - discount
        
        item_data["volume_deals_price"] = base_round(discount, 2)
        item_data["unit_price"] = base_round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for Save $X on Y promotions."""
        item_data = item.copy()
        unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        if isinstance(unit_price, str) and not unit_price:
            unit_price = 0
        
        quantity = float(match.group('quantity'))
        discount = float(match.group('discount'))
        
        total_price = (unit_price * quantity) - discount
        unit_price = total_price / quantity if quantity > 0 else 0
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount, 2)
        return item_data


class SaveOnQuantityLimitProcessor(PromoProcessor, version=3):
    patterns = [
        r"\$(?P<discount>\d+(?:\.\d+)?)\s+OFF\s+When\s+Buy\s+(?P<quantity>\d+)(?:\s+Limit\s+(?P<limit>\d+))?",
    ]

    def calculate_deal(self, item, match):
        """Process '$X SAVE $Y on Z' type promotions."""
        item_data = item.copy()
        try:
            total_price = float(match.group('total_price'))
        except IndexError:
            total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))
            
        discount = float(match.group('discount'))
        quantity = float(match.group('quantity'))        
        
        volume_deals_price = (total_price * quantity) - discount
        
        item_data["volume_deals_price"] = base_round(discount, 2)
        item_data["unit_price"] = base_round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for Save $X on Y promotions."""
        item_data = item.copy()
        unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        if isinstance(unit_price, str) and not unit_price:
            unit_price = 0
        
        quantity = float(match.group('quantity'))
        discount = float(match.group('discount'))
        
        total_price = (unit_price * quantity) - discount
        unit_price = total_price / quantity if quantity > 0 else 0
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount, 2)
        return item_data


class SaveOnQuantitySimpleProcessor(PromoProcessor, version=4):
    patterns = [
        r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\d+)",
        r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\d+)",
        r"Buy\s+(?P<quantity>\d+),\s+Save\s+\$(?P<discount>\d+(?:\.\d+)?)",
    ]

    def calculate_deal(self, item, match):
        """Process '$X SAVE $Y on Z' type promotions."""
        item_data = item.copy()
        try:
            total_price = float(match.group('total_price'))
        except IndexError:
            total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))
            
        discount = float(match.group('discount'))
        quantity = float(match.group('quantity'))        
        
        volume_deals_price = (total_price * quantity) - discount
        
        item_data["volume_deals_price"] = base_round(discount, 2)
        item_data["unit_price"] = base_round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for Save $X on Y promotions."""
        item_data = item.copy()
        unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        if isinstance(unit_price, str) and not unit_price:
            unit_price = 0
        
        quantity = float(match.group('quantity'))
        discount = float(match.group('discount'))
        
        total_price = (unit_price * quantity) - discount
        unit_price = total_price / quantity if quantity > 0 else 0
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(discount, 2)
        return item_data