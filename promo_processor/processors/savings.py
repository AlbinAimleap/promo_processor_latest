from promo_processor.processor import PromoProcessor

class DollarOffProcessor(PromoProcessor, version=1):
    patterns = [
        r'^Save\s+\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<quantity>\d+)\s+',  # Matches "Save $3.00 off 10 ..."
        r'^Save\s+\$(?P<savings>\d+(?:\.\d{2})?)',  # Matches "Save $3.00" or "Save $3"
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.50 off  15.4-21-oz."
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.25 off 15.25-oz."
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')
        savings_value = float(match.group('savings'))
        
        quantity = 1
        if 'quantity' in match.groupdict() and match.group('quantity'):
            quantity = float(match.group('quantity'))
            price_for_quantity = price * quantity
            savings_value_for_quantity = price_for_quantity - savings_value
            volume_deals_price = price 
            unit_price = savings_value_for_quantity / quantity
        else:
            volume_deals_price = price - savings_value
            unit_price = volume_deals_price
            
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        savings_value = float(match.group('savings'))
        
        quantity = 1
        if 'quantity' in match.groupdict() and match.group('quantity'):
            quantity = float(match.group('quantity'))
            price_for_quantity = price * quantity
            savings_value_for_quantity = price_for_quantity - savings_value
            volume_deals_price = price 
            unit_price = savings_value_for_quantity / quantity
        else:
            volume_deals_price = price - savings_value
            unit_price = volume_deals_price
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(savings_value, 2)
        return item_data

class CentsOffProcessor(PromoProcessor, version=2):
    patterns = [
        r'^Save\s+\$(?P<savings>\.25)\s+',  # Matches "Save $.25 "
        r'^Save\s+(?P<savings>\d+)¢'  # Matches "Save 70¢"
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')
        
        savings_value = float(match.group('savings'))
        if "¢" in item_data["volume_deals_description"]:
            savings_value = savings_value / 100
            
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
            
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        savings_value = float(match.group('savings'))
        if "¢" in item_data["digital_coupon_description"]:
            savings_value = savings_value / 100
            
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(savings_value, 2)
        return item_data

class PercentOffProcessor(PromoProcessor, version=3):
    patterns = [
        r'^Save\s+(?P<percent>\d+)%\s+Off'  # Matches "Save 20% Off"
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')
        
        percent = float(match.group('percent'))
        savings_value = price * (percent / 100)
        
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
            
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        percent = float(match.group('percent'))
        savings_value = price * (percent / 100)
        
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(savings_value, 2)
        return item_data
    
class PayPalRebateProcessor(PromoProcessor, version=4):
    patterns = [
        r"\$(?P<rebate>\d+\.\d{2})\s+REBATE\s+via\s+PayPal\s+when\s+you\s+buy\s+(?P<quantity>ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\s*(?:\(\d+\))?",    ]    
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        rebate_amount = float(match.group('rebate'))
        quantity = self.NUMBER_MAPPING[match.group('quantity').upper()]
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        discounted_price = price - (rebate_amount / quantity)
        unit_price = discounted_price
        
        item_data["volume_deals_price"] = round(discounted_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["rebate_amount"] = rebate_amount
        item_data["rebate_type"] = "PayPal"
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        rebate_amount = float(match.group('rebate'))
        quantity = self.NUMBER_MAPPING[match.group('quantity').upper()]
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price - (rebate_amount / quantity)
        
        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = round(rebate_amount / quantity, 2)
        item_data["rebate_amount"] = rebate_amount
        item_data["rebate_type"] = "PayPal"
        return item_data