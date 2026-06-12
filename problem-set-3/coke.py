def main():
    cost  = 50
    paid = 0
    accepted_coins = [25, 10, 5]


    while paid < cost:
        
        print(f"Amount Due: {cost - paid}")
        
        coin = int(input("Insert Coin: "))

        
        if coin in accepted_coins:
            paid  += coin


    change_owed = paid - cost 
    print("change owed:",change_owed )


main()