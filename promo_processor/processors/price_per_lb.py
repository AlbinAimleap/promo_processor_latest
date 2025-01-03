from promo_processor.processor import PromoProcessor

class BasicPricePerLbProcessor(PromoProcessor, version=1):
    """Processor for handling basic '$X/lb' promotions."""
    
    patterns = [
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
            item_data["volume_deals_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)
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
            item_data["digital_coupon_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)

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
            item_data["volume_deals_price"] = round(total_price, 2)
            item_data["unit_price"] = round(price_per_lb * weight, 2)
            item_data["digital_coupon_price"] = 0

            savings_per_lb = float(match.group('savings'))
            item_data["volume_deals_price"] = round(savings_per_lb * weight, 2)
        else:
            item_data["volume_deals_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)
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
            item_data["digital_coupon_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(item_data['unit_price'] - coupon_savings, 2)

        return item_data