# ONLINE BANKING SYSTEM
# One interface that allows bank account holders to do a lot of things with their money is probably the best final year project to develop.


import os


# Placeholder Values
transactee = None
transaction_amount = None
customer_name = None
customer_street_address = None
customer_city = None
customer_state = None
customer_zip = None
customer_social_security_number = None
customer_credit_rating = None
type_of_account = None
deposit_amount = 0.00
balance = 0.00
count = 0


# Collections
transactions = transactee, transaction_amount
demographics = [
                        customer_name,
                        customer_street_address,
                        customer_city,
                        customer_state,
                        customer_zip
]
protected_information = [
                                    customer_social_security_number,
                                    customer_credit_rating
]
account = [
                transactions,
                demographics, protected_information, balance, type_of_account]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def request_balance():
    print("Balance: $" + str(account[3]))


def deposit():
    clear_screen()

    transaction_amount = input("How much do you wish to deposit?  $")
    account[3] += float(transaction_amount)

    request_balance()


def withdrawl():
    clear_screen()

    transaction_amount = input("How much do you wish to withdrawl?  $")
    account[3] -= float(transaction_amount)

    request_balance()


def new_account():
    account[4] = input("""
        'PERSONAL'
        '-----------------'
        'Personal Checking'
        'Personal Savings'
        'Personal Credit'
        'Personal Loan'
        '-----------------'

        'BUSINESS'
        '-----------------'
        'Business Checking'
        'Business Savings'
        'Business Credit'
        'Business Loan'
        '-----------------'

        'INVESTMENT'
        '-----------------'
        'IRA'
        'Custodial'
        'Real Estate'
        '-----------------'


Account TYPE """)

    account[1][0] = input("Customer's NAME ")
    account[1][1] = input("Customer's STREET ADDRESS ")
    account[1][2] = input("Customer's CITY ")
    account[1][3] = input("Customer's STATE ")
    account[1][4] = input("Customer's ZIP ")
    account[2][0] = input("Customer's SOCIAL SECURITY NUMBER ")
    account[2][1] = input("Customer's CREDIT RATING ")


def tellers_menu():
    clear_screen()

    print("How may we proceed?")
    print("""
Enter 'NEW' to open a new account.
Enter 'DEPOSIT' to deposit into an account.
Enter 'WITHDRAWL' to withdrawl from an account.
Enter 'BALANCE' to view account balance.
Enter 'EXIT' to signout.
""")

    while True:
        tellers_input = input("> ")

        if tellers_input.upper() == 'EXIT':
            break

        elif tellers_input.upper() == 'NEW':
            new_account()
            continue

        elif tellers_input.upper() == 'DEPOSIT':
            deposit()
            continue

        elif tellers_input.upper() == 'WITHDRAWL':
            withdrawl()
            continue

        elif tellers_input.upper() == 'BALANCE':
            request_balance()
            continue


tellers_menu()
