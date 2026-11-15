"""独立业务规则，仅依赖冻结资料。"""
def quote(data, request):
    visit = request['visit']
    basket = request['basket']
    if visit not in data['opportunities'] or len(basket) != 4:
        raise ValueError('到访或商品向量非法')
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in basket):
        raise ValueError('篮子数量必须为非负整数')
    opportunity = data['opportunities'][visit]
    subtotal = sum(price * quantity for price, quantity in zip(opportunity['prices'], basket))
    discount = opportunity['discount'] if subtotal >= opportunity['threshold'] else 0
    payable = max(0, subtotal - discount)
    stock_ok = all(quantity <= limit for quantity, limit in zip(basket, opportunity['limits']))
    feasible = stock_ok and payable <= opportunity['budget'] and sum(basket) <= opportunity['bag_capacity']
    return {'feasible': feasible, 'payable_yuan': round(payable, 2),
            'subtotal_yuan': round(subtotal, 2), 'discount_yuan': discount,
            'opportunity_id': opportunity['id'], 'weight_tolerance': opportunity['weight_tolerance'],
            'stock_ok': stock_ok, 'budget_yuan': opportunity['budget']}

def opportunity(data, request):
    visit = request['visit']
    if visit not in data['opportunities']:
        raise ValueError('到访不存在')
    return data['opportunities'][visit]

detail = opportunity
