from abc import ABC, ABCMeta, abstractmethod, abstractproperty, abstractclassmethod
from datetime import datetime




class Account():
    def __init__(self, number: int, client) -> None:
        self._balance = 0
        self._number = number
        self._client = client
        self._history = History()
        self._agency = "0001"
    
    #method fabrica para fazer ele mesmo por outras class
    @classmethod
    def new_account(cls, client, number: int ):
        return cls(number, client)
    
    @property        
    def balance(self):
        return self._balance
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def history(self):
        return self._history
    
    @property
    def client(self):
        return self._client
    
    def withdrawal(self, value):
        
        if value < self._balance and value > 0:    
            self._balance -= value
            print("Withdrawal successful!")
            print(f"SUCESS: withdrawal = R$ {value:.2f}")
            return True

        else:
            print("FAIL: Withdrawal, insufficient balance!")
            return False
        
    def deposit(self, value):
        
        if value > 0:
            self._balance += value
            print(f"SUCESS: Desposit = R$ {value:.2f}")
            return True 
        else: 
            print("Invalid deposit amount!")
            return False

class AccountIterator():
    def __init__(self, accounts) -> None:
        self.accounts = accounts
        self.index_account = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        
        try:
            account = self.accounts[self.index_account]
            return f"""\
                Agency:\t{account.agency}
                Number:\t\t{account.number}
                Name:\t{account.name}
                Balance:\t\t{account.balance}
                """
        except IndexError:
            raise StopIteration
    
        finally :
            self.index_account+= 1   
class CheckingAccount(Account):  
    def __init__(self, number: int, client) -> None:
        super().__init__(number, client)
        self._limit = 500
        self._max_day_withdrawal_limit  = 3
        
    def withdrawal(self, value):
        
        Withdrawal_number = len([
            transaction for transaction in self.history.transaction if transaction["type"] == Withdrawal.__name__
        ])
        
        check_max_limite = (value <= self._limit) 
        check_negative_value = value > 0
        check_balance = value < self._balance 
        check_daily_limit = Withdrawal_number <= self._max_day_withdrawal_limit 
        
        
        if not check_balance:
            print("FAIL: Balance insuficent")
            return
        
        elif not check_negative_value:
            print("FAIL: Negative Value!")
            return
        
        elif not check_max_limite:
            print("FAIL: Withdrawal amount exceeded!")
            return
        
        elif not check_daily_limit:
            print("FAIL: Maximum withdrawal limit reached!")
            
        else:
            print("Withdrawal successful!")
            print(f"SUCESS: withdrawal = R$ {value:.2f}")
            return super().withdrawal(value)
        
    def __str__(self) -> str:
        return  f"""\
            Agency:\t{self._agency}
            C/C:\t\t{self._number}
            Titular:\t{self.client.name}
        """
    
class Client():
    
    def __init__(self, address: str) -> None:
        self.address = address
        self.accounts = []
        self.index_account = 0
    
    def carry_out_transaction(self, account: Account, transaction):
        
        if len(account.history.transactions_day()) >= 10:
            print("### ERROR: You exceeded the limit of transactions!")
            return
            
        return transaction.register(account)
    
    def add_account(self,account: Account):
        return self._accounts.append(account)
    
class IndividualClient(Client):
    def __init__(self, address: str, cpf:str, name:str, date_birth) -> None:
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.date_birth = date_birth

class History():
    
    def __init__(self):
        self._transactions = []
    
    @property    
    def transaction(self):
        return self._transactions 
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
                "date": datetime.now().replace(microsecond=0).strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }
        )

    def generate_report(self, type_transaction=None):
        for transaction in self._transactions:
            if type_transaction is None or transaction["type"].lower() == type_transaction.lower():
                yield transaction

    def transactions_day(self):
        date_now = datetime.utcnow().date() # horario atual
        
        transactions = []

        for transaction in self._transactions:        
            date_transaction = datetime.strptime(transaction["date"],  "%d-%m-%Y %H:%M:%S").date()   # data em string,converter a data da transaction!
            if date_now == date_transaction:
                transactions.append(transaction)
        
        return transactions 
                 
class Transaction(ABC):
    
    @property
    @abstractproperty
    def value(self):
        ...

    @abstractclassmethod
    def register(self, account):
        ...
     
class Withdrawal(Transaction):
    
    def __init__(self, value) -> None:
        self._value = value
        
    @property #Class herdada de abstract
    def value(self):
        return self._value
    
    def register(self, account):
        
        status_transaction = account.withdrawal(self._value)
        
        if status_transaction:
            account.history.add_transaction(self)
    
class Deposit(Transaction):
    
    def __init__(self, value) -> None:
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    def register(self, account: Account):
        status_transaction = account.deposit(self.value)
        
        if status_transaction:
            account.history.add_transaction(self)
 
 
def log_date(func):
    def date_action(*args, **kwargs):
        resultado = func(*args, **kwargs)
        date=  datetime.now().replace(microsecond=0)
        print(f"Action {func.__name__.upper()} carried out successfully! {date} !")
    return date_action        

@log_date  
def withdrawal(clients:list):
    
    cpf = input("Please enter a valid cpf! ")
    client = user_filter(cpf, clients)
    
    if not client:
        print("XXX FAIL: Customer not found! XXX")
        return
    
    value = float(input("Please enter a valid value: "))
    
    transaction = Withdrawal(value)
    
    acc = retrieve_account(client)
    
    if not acc:
        return
    
    client.carry_out_transaction(acc, transaction)  
    
def display_bank_statement(clients: list):
    
    cpf = input("Please enter a valid CPF of client: ")
    
    client = user_filter(cpf, clients)
    
    if not client:
        print("XXX FAIL: Client not found! XXX")
        return
    
    acc = retrieve_account(client)
    
    if not acc:
        return

    print("########### STATEMENT ###########")
    
    transactions = False

    statement = ""
    
    for transaction in acc.history.generate_report():
            transactions =  True
            statement += f'\n{transaction["date"]}\n{transaction["type"]}: \n\tR$ {transaction["value"]}.'
    
    
    if not transactions:
        statement+= "No transactions were carried out!"
    
    print(statement)
    print(f'\nSaldo:\n{acc.balance:.2f}')
    print("########### STATEMENT ###########")

@log_date    
def deposit(clients:list):
    
    cpf = input("Please enter a valid CPF of client: ")

    client = user_filter(cpf, clients)
    
    if not client:
        print("XXXX Fail: CPF not found! XXXX")
        return
    
    value = float(input("Please enter the deposit amount: "))
    
    transaction = Deposit(value)
    
    acc = retrieve_account(client)
    
    if not acc:
        print("XXX FAIL: Costumer needs an account! XXX")
        return
    
    client.carry_out_transaction(acc, transaction)

@log_date  
def new_account(number_account: int, clients: list, accounts_list: list):
    
    cpf = input("Enter the CPF for inquiry: ")
    
    client = user_filter(cpf, clients)
    
    if not client:
        print("FAIL: User invalid! Account was not created!")
        return
         
    account = CheckingAccount.new_account(client=client, number=number_account)
    
    accounts_list.append(account)
    client.accounts.append(account) 
    
    print("SUCESS: User valid! New account created!")
 
@log_date     
def new_client(clients: list):
    
    cpf = input("Please enter a valid CPF: ")
    get_client = user_filter(cpf, clients)

    if get_client:
        print(f"Fail: CPF {cpf} already exists!")
        return 
    
    address = input("Please enter a valid address: ")
    name = input("Please enter a name: ")
    date_birth = input("Please enter a valid date of birth(mm-dd-yyyy): ")
    
    
    new_client = IndividualClient(address, cpf, name, date_birth)
    
    clients.append(new_client)
    
    print("SUCESS: New User create!")

def user_filter(cpf: str, clients: list):
    filtered_user = [client for client in clients if client.cpf == cpf]
    print(filtered_user)
    return filtered_user[0] if filtered_user else None

def retrieve_account(client : Client):
    
    if not client.accounts:
        print("XXX Fail: Customer has no account! XXX")
        return
    
    return client.accounts[0]

def list_accounts(accounts): 
    for account in AccountIterator(accounts):
        print(50 * "#")
        print(str(account))

def main():
    
    clients = []
    accounts = []
    
    choice = """
    Insert - CHOICES:
    d = deposit
    w = withdrawal
    s = statement
    nc = New Client
    na = New Account
    q = quit
    la = list accounts
    """
    
    while True:

        op = input(choice).lower()

        if op == "d":
            deposit(clients)
        elif op == "w":
            withdrawal(clients)
                
        elif op == "s":
            display_bank_statement(clients)

        elif op == "nc":
            new_client(clients)
        
        elif op == "na":
            number_account = len(accounts) + 1
            new_account(number_account,clients, accounts)
            
        elif op == "q":
            print("Good Bye!")
            break
        
        elif op == "la":
            list_accounts(accounts)

        else:
            print("""
                ERROR:
                Invalid option!""")
            continue

main()



