soda = [
            "Coca-Cola",
            "Monster Energy Drink",
            "Vernors Ginger Ale",
            "A&W Root Beer",
            "Sprite"
]


chips = [
            "Cooler Ranch Doritos",
            "Sour Cream & Onion Pringles",
            "BBQ Kettle Chips",
            "Ranch Kale Chips"
]


candy = [
              "Skittles",
              "3 Musketters",
              "Reeses Big Cups",
              "Airheads",
              "Nerds",
              "Runts",
              "Gummy Bears / Worms"
]


while True:
    choice = input("Would you like a SODA, some CHIPS, or CANDY? ").lower()
    try:
        if choice == 'soda':
            snack = soda.pop()
        elif choice == 'chips':
            snack = chips.pop()
        elif choice == 'candy':
            snack = candy.pop()
        else:
            print("Sorry I didn't understand that.")
            continue
    except IndexError:
        print("We're all out of {}.  Sorry!".format(choice))
    else:
        print("Here's your {}. {}".format(choice, snack))
