from promo_processor.processor import PromoProcessor
from promo_processor import base_round
import math
class DollarOffProcessor(PromoProcessor, version=1):
    patterns = [
        r'^Save\s+\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<quantity>\d+)\s+',  # Matches "Save $3.00 off 10 ..."
        r'^Save\s+\$(?P<savings>\d+(?:\.\d{2})?)',  # Matches "Save $3.00" or "Save $3"
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.50 off  15.4-21-oz."
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.25 off 15.25-oz."
        r'^\$(?P<savings>\d+)\s+Target\s+GiftCard\s+on\s+Crest\s+teeth-whitening\s+strips',  # Matches "$5 Target GiftCard on Crest teeth-whitening strips"
        r'^\$(?P<savings>\d+)\s+Target\s+GiftCard\s+with\s+purchase',  # Matches "$20 Target GiftCard with purchase"
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
            
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
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
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(savings_value, 2)
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
            
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
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
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(savings_value, 2)
        return item_data

class PercentOffProcessor(PromoProcessor, version=3):
    patterns = [
        r'^Save\s+(?P<percent>\d+)%\s+Off',  # Matches "Save 20% Off"
        r'^Save\s+(?P<percent>\d+)%\s+in\s+cart'  # Matches "Save 10% in cart on Altitude"
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')
        
        percent = float(match.group('percent'))
        savings_value = price * (percent / 100)
        
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
            
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        percent = float(match.group('percent'))
        savings_value = price * (percent / 100)
        
        volume_deals_price = price - savings_value
        unit_price = volume_deals_price
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(savings_value, 2)
        return item_data
    
class PayPalRebateProcessor(PromoProcessor, version=4):
    patterns = [
        r"\$(?P<rebate>\d+\.\d{2})\s+REBATE\s+via\s+PayPal\s+when\s+you\s+buy\s+(?P<quantity>ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\s*(?:\(\d+\))?",
        r"Rebate:\s+\$(?P<rebate>\d+)\s+back\s+when\s+you\s+buy\s+(?P<quantity>\d+)"    ]    
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        rebate_amount = float(match.group('rebate'))
        quantity = self.NUMBER_MAPPING[match.group('quantity').upper()] if match.group('quantity').isalpha() else float(match.group('quantity'))
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        
        discounted_price = price - (rebate_amount / quantity)
        unit_price = discounted_price
        
        item_data["volume_deals_price"] = base_round(discounted_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
        
    def calculate_coupon(self, item, match):
        item_data = item.copy()
        rebate_amount = float(match.group('rebate'))
        quantity = self.NUMBER_MAPPING[match.group('quantity').upper()] if match.group('quantity').isalpha() else float(match.group('quantity'))
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        
        discounted_price = base_price - (rebate_amount / quantity)
        
        item_data["unit_price"] = base_round(discounted_price, 2)
        item_data["digital_coupon_price"] = base_round(rebate_amount / quantity ,2)
        return item_data

class WinePackProcessor(PromoProcessor, version=5):
    patterns = [
        r'^Wine\s+(?P<percent>\d+)%\s+(?P<quantity>\d+)\s+Pack\s+\$(?P<price>\d+\.\d{2})\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{1})'
    ]
    #Wine 10% 4 Pack $10.99 Save Up To: $5.0
    def calculate_deal(self, item, match):
        item_data = item.copy()
        percent = float(match.group('percent'))
        quantity = float(match.group('quantity'))
        pack_price = float(match.group('price'))
        savings = float(match.group('savings'))
        
        unit_price = pack_price / quantity
        volume_deals_price = pack_price
            
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        percent = float(match.group('percent'))
        quantity = float(match.group('quantity'))
        pack_price = float(match.group('price'))
        savings = float(match.group('savings'))
        
        unit_price = pack_price / quantity
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(pack_price, 2)
        return item_data

class HealthyAislesProcessor(PromoProcessor, version=6):
    patterns = [
        r'^Healthy\s+Aisles\s+\$(?P<price>\d+\.\d{2})\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{1})'
    ]
    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = float(match.group('price'))
        savings = float(match.group('savings'))
        
        volume_deals_price = price
        unit_price = price
            
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = float(match.group('price'))
        savings = float(match.group('savings'))
        
        unit_price = price
        
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(savings, 2)
        return item_data
    

    
class DollarOffOnMoreProcessor(PromoProcessor, version=7):
    #$1.00 OFF of $1 or more
    patterns = [
        r'\$(?P<savings>\d+\.\d{2})\s+off\s+of\s+\$(?P<min_price>\d+)\s+or\s+more',  # Matches "$1.00 OFF of $1 or more"
    ]    
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')
        savings_value = float(match.group('savings'))
        min_price = float(match.group('min_price'))
        if price>min_price:
            volume_deals_price = price - savings_value
            unit_price = volume_deals_price
        elif price == min_price:
            quantity_needed = math.ceil(min_price/price)+1
            total_price = quantity_needed * price
            volume_deals_price = total_price - savings_value
            unit_price = volume_deals_price / quantity_needed
        else:
            quantity_needed = math.ceil(min_price/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price - savings_value
            unit_price = volume_deals_price / quantity_needed
        item_data["volume_deals_price"] = base_round(volume_deals_price, 2)
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        savings_value = float(match.group('savings'))
        min_price = float(match.group('min_price'))
        if price>min_price:
            volume_deals_price = price - savings_value
            unit_price = volume_deals_price
        elif price == min_price:
            quantity_needed = math.ceil(min_price/price)+1
            total_price = quantity_needed * price
            volume_deals_price = total_price - savings_value
            unit_price = volume_deals_price / quantity_needed
        else:
            quantity_needed = math.ceil(min_price/price)
            total_price = quantity_needed * price
            volume_deals_price = total_price - savings_value
            unit_price = volume_deals_price / quantity_needed  
        item_data["unit_price"] = base_round(unit_price, 2)
        item_data["digital_coupon_price"] = base_round(volume_deals_price, 2)
        return item_data
