#desafio - modularizado
    
def withdrawal(*, balance, value, statement, limit, withdrawal_number, withdrawal_limit):
    if value < balance:

        if withdrawal_number >= withdrawal_limit:
            print("You have exceeded the daily withdrawal limit!")
            return balance, statement, withdrawal_number
        
        elif value > limit:
             print("You have exceeded the LIMIT(R$ 500)!")
             return balance, statement, withdrawal_number
           

        balance -= value
        print("Withdrawal successful!")
        withdrawal_number += 1
        
        statement += f"Withdrawal made: R$ {value:.2f}!\n"
        
        print(f"SUCESS: withdrawal = R$ {value:.2f}")
        
        return balance, statement, withdrawal_number

    else:
        print("FAIL: Withdrawal, insufficient balance!")
        return statement, balance, withdrawal_number

def display_bank_statement( balance, /, *, statement):
    
    print(
            f"""
            =========STATEMENT=========
            {statement}
            Balance: {balance:.2f}
            ===========================
            """ if statement 
            else  f"""=========STATEMENT=========
                    FAIL: No transactions were made!
                    Balance: {balance:.2f}
                    ===========================""" 
        )

def deposit(balance, value, statement, /):
    
    if value > 0:
        balance += value
        statement+= f"Deposit made: R$ {value:.2f}!\n"
        print(f"SUCESS: Desposit = R$ {value:.2f}")
        return balance, statement
    else: 
        print("Invalid deposit amount!")
        return balance, statement

def new_account(agency: str, number_account: int, users: list):
    
    cpf = input("Enter the CPF for inquiry: ")
    
    user = user_filter(cpf, users)
    
    if user:
        print("SUCESS: User valid! New account created!")
        return {"agency": agency, "number_account": number_account, "user": cpf}
    
    print("FAIL: User invalid! Account was not created!")
    return False

def user_filter(cpf: str, users_list: list) -> bool:
    user_valid = [user for user in users_list if cpf in user.values()]
    return True if user_valid else False

def new_user(users_list):
    cpf = input("Please enter a valid CPF: ")
    
    get_cpf = user_filter(cpf, users_list)

    if get_cpf:
        return
    
    name = input("Please enter a name: ")
    date_birth = input("Please enter a valid date of birth(mm-dd-yyyy): ")
    address = input("Please enter a valid address: ")
    
    users_list.append({"name": name, "cpf": cpf, "address": address, "date_birth": date_birth})
    
    print("SUCESS: New User create!")

def main():

    LIMIT = 500
    WITHDRAWAL_LIMIT = 3
    AGENCY = "0001"
    
    balance = 0.0
    statement = ""
    num_withdrawal = 0
    num_account = 0
    users_list = []
    accounts = []
    
    choice = """"
    Insert - CHOICES:
    d = deposit
    w = withdrawal
    s = statement
    nu = New User
    na = New Account
    q = quit
    """
    while True:

        op = input(choice).lower()

        if op == "d":
            value = float(input("Please enter the amount you with to deposit: "))
            balance, statement = deposit(balance,
                                         value, 
                                         statement
                                         )
     
        elif op == "w":
            
            value = float(input("Please enter the amount you wish to withdrawal: "))

            balance, statement, num_withdrawal = withdrawal(balance=balance,
                                                            value=value, 
                                                            statement=statement, 
                                                            limit=LIMIT,
                                                            withdrawal_limit=WITHDRAWAL_LIMIT, 
                                                            withdrawal_number=num_withdrawal)
                
        elif op == "s":
            display_bank_statement(balance, statement=statement)

        elif op == "nu":
            new_user(users_list)
        
        elif op == "na":
            num_account+=1
            valid_account = new_account(AGENCY, num_account, users_list)
            if valid_account:
                accounts.append(valid_account)
                continue
            num_account-= 1

        elif op == "q":
            print("Good Bye!")
            break

        else:
            print("""
                ERROR:
                Invalid option!""")
            continue

main()



