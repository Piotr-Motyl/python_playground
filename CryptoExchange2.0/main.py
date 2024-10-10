from api import *

#Descriptions panel
greeting_desc = " Welcome in Crypto Exchange "
farewell_desc = " GOODBYE "
centering_desc_length = 50

print("*".center(centering_desc_length, "*"))
print(greeting_desc.center(centering_desc_length, "*"))
print("*".center(centering_desc_length, "*"))

cart_coins = {"bitcoin": 0,
              "ethereum": 0}
cart_value = 0

try:
    while True:
        crypto_symbol_to_buy = input("Choose (Bitcoin/btc) or (Ethrerum/eth) to buy or exit(e) to leave exchange")
        if crypto_symbol_to_buy == "exit" or crypto_symbol_to_buy == "e":
            print(farewell_desc.center(centering_desc_length, "*"))
            break

        if crypto_symbol_to_buy.lower() == "btc":
            crypto_symbol_to_buy = "bitcoin"
        if crypto_symbol_to_buy.lower() == "eth":
            crypto_symbol_to_buy = "ethereum"

        coin_data = find_coin_by_symbol(crypto_symbol_to_buy)
        if coin_data is None:
            print("We dont have it, check later")
            continue

        coin_price = get_coin_price_in_currency(coin_data["id"], currency_type)
        print("Price ", str(coin_data["id"]), coin_price, currency_type)

        while True:
            try:
                customer_spending_money = float(input("How much USD you want to spent" + currency_type + " for purchasing?"))
                cart_value += customer_spending_money
                break
            except ValueError:
                print("Please enter a valid number.")

        customer_crypto_purchases = customer_spending_money / coin_price

        if crypto_symbol_to_buy == "bitcoin":
            cart_coins["bitcoin"] += customer_crypto_purchases

        if crypto_symbol_to_buy == "ethereum":
            cart_coins["ethereum"] += customer_crypto_purchases

        print("Congratulations, you bought " + str(customer_crypto_purchases) + " " + crypto_symbol_to_buy + " :)")
        print("*".center(centering_desc_length, "*"))
        print(" Your cart: ".center(centering_desc_length, "*"))
        print("Value: ", cart_value, currency_type.upper())
        print("Coins", cart_coins)
        print("*".center(centering_desc_length, "*"))

except KeyboardInterrupt:
    print("\n" + farewell_desc.center(centering_desc_length, "*"))