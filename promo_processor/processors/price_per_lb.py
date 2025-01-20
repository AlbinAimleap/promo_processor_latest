from promo_processor.processor import PromoProcessor
from promo_processor import base_round

class BasicPricePerLbProcessor(PromoProcessor, version=1):
    """Processor for handling basic '$X/lb' promotions."""
    
    patterns = [
        r'\$(?P<price_per_lb>\d+(?:\.\d{2})?)\s*per\s*lb\.\s*Limit\s*(?P<weight>\d+)\-lbs?\.\s*Limit\s*(?P<weight1>\d+)\-lbs?\.',
        r'\$(?P<price_per_lb>\d+(?:\.\d{2})?)\/lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\/lb'
    ]

    def calculate_deal(self, item, match):
        """Process basic '$X/lb' type promotions for deals."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight', 0), str):
            weight = 1 
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            total_price = price_per_lb * weight
            item_data["volume_deals_price"] = base_round(price_per_lb)
            item_data["unit_price"] = base_round(price_per_lb)
            item_data["digital_coupon_price"] = 0

        return item_data

    def calculate_coupon(self, item, match):
        """Process basic '$X/lb' type promotions for coupons."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        unit_price = float(item_data.get('unit_price', 0) or 0)
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            coupon_savings = price_per_lb * weight
            item_data["digital_coupon_price"] = base_round(price_per_lb)
            item_data["unit_price"] = base_round(price_per_lb)

        return item_data

class SaveUpToPricePerLbProcessor(PromoProcessor, version=2):
    """Processor for handling '$X/lb with Save Up To' promotions."""
    
    patterns = [
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{2})\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)'
    ]

    def calculate_deal(self, item, match):
        """Process '$X/lb with Save Up To' type promotions for deals."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight'), str):
            if len(item_data.get('weight')) > 1 and any(i for i in item_data.get('weight') if  i.isdigit()):
                weight = float("".join([i for i in item_data.get('weight') if i.isdigit() or i == "."]))
            else:
                weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            total_price = price_per_lb / weight
            item_data["volume_deals_price"] = base_round(total_price)
            item_data["unit_price"] = base_round(price_per_lb * weight)
            item_data["digital_coupon_price"] = 0

            savings_per_lb = float(match.group('savings'))
            item_data["volume_deals_price"] = base_round(savings_per_lb * weight)
        else:
            item_data["volume_deals_price"] = base_round(price_per_lb)
            item_data["unit_price"] = base_round(price_per_lb)
            item_data["digital_coupon_price"] = 0


        return item_data

    def calculate_coupon(self, item, match):
        """Process '$X/lb with Save Up To' type promotions for coupons."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            savings_per_lb = float(match.group('savings'))
            coupon_savings = savings_per_lb * weight
            item_data["digital_coupon_price"] = base_round(price_per_lb)
            item_data["unit_price"] = base_round(item_data['unit_price'] - coupon_savings)

        return item_data