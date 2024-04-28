#desafio
choice = """"
CHOICES:
d = deposit
w = withdrawal
s = statement
q = quit 
=>"""

balance = 0
LIMIT = 500
statement = ""

num_withdrawal = 0
WITHDRAWAL_LIMIT = 3


while True:

    op = input(choice)

    if op == "d":
        
        value = float(input("Please enter the amount you with to deposit: "))

        if value > 0:
            balance += value
            statement+= f"Deposit made: R$ {value:.2f}!\n"
            print(f"SUCESS: Desposit = R$ {value:.2f}")

        else: 
            print("Invalid deposit amount!")
            continue

    elif op == "w":
        
        value = float(input("Please enter the amount you wish to withdrawal: "))

        if value < balance:

            if num_withdrawal > WITHDRAWAL_LIMIT:
                print("You have exceeded the daily withdrawal limit!")
                continue
            
            elif value > LIMIT:
                print("You have exceeded the LIMIT(R$ 500)!")
                continue

            balance -= value
            print("Withdrawal successful!")
            num_withdrawal += 1
            statement += f"Withdrawal made: R$ {value:.2f}!\n"
            print(f"SUCESS: withdrawal = R$ {value:.2f}")

        else:
            print("FAIL: Withdrawal, insufficient balance!")
    
    elif op == "s":

        repr_statement = "FAIL: No transactions were made!" if not statement else statement
        print(
            f"""
            =========STATEMENT=========
            {repr_statement}
            Balance: {balance:.2f}
            ===========================
            """
     )

    elif op == "q":
        print("Good Bye!")
        break

    else:
        print("""
              ERROR:
              Invalid option!""")
        continue