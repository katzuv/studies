price = float(input())
discount = float(input())

price -= price * discount
tax = price * 0.17

print(round(price))
print(round(tax))
