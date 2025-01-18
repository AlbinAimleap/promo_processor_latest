import math

# spend = 10
# discount = 25
# discounted_rate = discount/100
# price = 6
# if price>spend:
#     volume_deals_price = price
#     unit_price = price * discounted_rate
# else:
#     quantity = 1 / price
#     quantity_needed = math.ceil(spend/price)
#     total_price = quantity_needed * price
#     volume_deals_price = total_price - (total_price*discounted_rate)
#     unit_price = volume_deals_price /quantity_needed 
# print(quantity)
# print(quantity_needed)
# print(total_price)
# print(volume_deals_price)
# print(unit_price)

#4 For $5.0 Save Up To:$ 2.16 On 4
# quantity = 4
# volume_deals_price = 5.0
# volume_deals_price=base_round(volume_deals_price, 2)
# unit_price= base_round(volume_deals_price / quantity, 2)#1.25
#$1.00 OFF of $1 or more
price =0.69
savings_value = 1.00
min_price = 1.00
if price>min_price:
    volume_deals_price = price - savings_value
    unit_price = volume_deals_price
    quantity_needed=0
    total_price=0
elif price == min_price:
    
    quantity_needed = math.ceil(min_price/price)+1
    total_price = quantity_needed * price
    volume_deals_price = total_price -savings_value
    unit_price = volume_deals_price / quantity_needed
else:
    
    quantity_needed = math.ceil(min_price/price)
    total_price = quantity_needed * price
    volume_deals_price = total_price - savings_value
    unit_price = volume_deals_price / quantity_needed  
print(quantity_needed)#2
print(total_price)#12
print(volume_deals_price)#0.25
print(unit_price)#0.25

#$1.00 OFF When Buy 2 Limit 1 $1.00 OFF when you buy TWO(2) Pillsbury Refrigerated and Frozen Baked Goods. Any variety. Items must appear on the same receipt.
#\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+when\s+buy\s+(?P<quantity>\d+)(?:\s+limit\s+(?P<limit>\d+))?
# discount_value = 1.00
# quantity = 2
# limit = 1
# price = 3.49

# if limit > quantity:
#     unit_price = (price * limit) - (discount_value / quantity)
# else:
#     unit_price = price - (discount_value / quantity)#3.49-(1/2)=0.5
    
# unit_price = base_round(unit_price, 2)
# digital_coupon_price = base_round(discount_value / quantity, 2)
# quantity= quantity
# print(unit_price)
# print(digital_coupon_price)
# print(quantity)



# 12.99
#Wine 10% 4 Pack $15.99 Save Up To: $2.0
# percent = 10
# quantity = 4
# pack_price = 15.99
# savings = 2.0
# unit_price = pack_price / quantity#15.99/4=3.99
# volume_deals_price = pack_price#15.99
# #Save 10% on 4. When you buy 4.
# discount_percentage = 10
# limit = 4
# discount_decimal = discount_percentage / 100#0.1
# base_price = 12.99
# total_price = base_price * limit#12.99*4=51.96
# discounted_price = total_price - (total_price * discount_decimal)#51.96-(51.96*0.1)=46.76

# unit_price = base_round(discounted_price/limit, 2)
# digital_coupon_price = base_round(discounted_price, 2)
# print(unit_price)
# print(volume_deals_price)
# print(unit_price)
# print(digital_coupon_price)