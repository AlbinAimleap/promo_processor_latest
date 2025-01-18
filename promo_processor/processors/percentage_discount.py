from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class PercentageOffProcessor(PromoProcessor, version=1):
    patterns = [
        r"^(?P<discount>\d+)%\s+off",
        r"^Deal:\s+(?P<discount>\d+)%\s+off",
        ]    
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        discounted_price = price * (1 - discount_decimal)
        unit_price = discounted_price
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price * (1 - discount_decimal)
        
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = base_round(discounted_price, 2)
        return item_data

class PercentageOffProductProcessor(PromoProcessor, version=2):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"^(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
    ]    
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        discounted_price = price * (1 - discount_decimal)
        unit_price = discounted_price
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price * (1 - discount_decimal)
        
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = base_round(discounted_price, 2)
        return item_data

class PercentageOffQuantityProcessor(PromoProcessor, version=3):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+with\s+(?P<quantity>\d+)",
        r"^Save\s+(?P<discount>\d+)%\s+each\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+or\s+more",
    ]    
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        quantity = int(match.group('quantity'))
        if "or more" in match.string:
            item_data["min_quantity"] = quantity
            discounted_price = price * (1 - discount_decimal)
            unit_price = discounted_price
        else:
            total_price = price * quantity
            discounted_price = total_price * (1 - discount_decimal)
            unit_price = discounted_price / quantity
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price * (1 - discount_decimal)
        
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = base_round(discounted_price, 2)
        return item_data


class PercentageOffSelectProcessor(PromoProcessor, version=4):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+select",
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        discounted_price = price * (1 - discount_decimal)
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price * (1 - discount_decimal)
        
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = base_round(discounted_price, 2)
        return item_data



class PercentageOffSaveProcessor(PromoProcessor, version=5):
    #Save 10% on 4. When you buy 4.
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<limit>\d+).\s+when\s+you\s+buy\s+(?P<count>\d+)",
        r"^Save\s+(?P<discount>\d+)%$",
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        limit = float(match.group('limit')) if 'limit'in match.groupdict() else 1
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        total_price = price * limit
        discounted_price = total_price - (total_price * discount_decimal)
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(discounted_price / limit, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        limit = float(match.group('limit')) if 'limit'in match.groupdict() else 1
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        total_price = base_price * limit
        discounted_price = total_price - (total_price * discount_decimal)
        
        item_data["unit_price"] = base_round(discounted_price / limit, 2)
        item_data["digital_coupon_price"] = base_round(discounted_price, 2)
        return item_data