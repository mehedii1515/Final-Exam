import random
from uuid import uuid1
from datetime import datetime


class BankSystem:
    accounts = {}
    total_loan_amount = 0
    

    def __init__(self):
        self.loan_limit = 2
        self.bankrupt = False
        self.loan_available = True 
   
        
    def create_account(self, name, email, address, account_type):
        account_no = random.randrange(100000000, 9000000000)
        self.accounts[account_no] = {
            "name": name,
            "email": email,
            "address": address,
            "account_type": account_type,
            "transaction_history": [],
            "balance": 0,
            "loan_count": 0
        }
        print(f"{name}, welcome to our bank!. Your account has been created successfully!. Your Account No: {account_no}")
    
    
    def check_balance(self, ac_no):
        if ac_no in self.accounts:
            print(f"Your Available balance is: {self.accounts[ac_no]['balance']}")
        else:
            print("Invalid account")


    def deposit(self, account_no, amount):
        if account_no in self.accounts:
            self.accounts[account_no]["balance"] += amount
            self.accounts[account_no]["transaction_history"].append(f"Transaction no: TrxID-{uuid1()}, Deposited {amount}, datetime: {datetime.now()}")
            print(f"{amount} Deposited Successfully in Your Account")
        else:
            print("Invalid account!!")


    def withdraw(self, account_no, amount):
        if account_no in self.accounts:
            if not self.bankrupt:
                if amount <= self.accounts[account_no]["balance"]:
                    self.accounts[account_no]["balance"] -= amount
                    self.accounts[account_no]["transaction_history"].append(f"Transaction no: TrxID-{uuid1()}, Withdraw {amount}, datetime: {datetime.now()}")
                    print(f"{amount} Withdrawn Successfully from Your Account")
                else:
                    print("Withdrawal amount exceeded")
            else:
                print("The bank is bankrupt. There is no money for withdrawal!!")
        else:
            print("Invalid account")


    def get_total_balance(self):
        total_balance = sum(account_info["balance"] for account_info in self.accounts.values())
        print(f"Total Bank Balance is: {total_balance}")
          
    def transaction_history(self, account_no):
        if account_no in self.accounts:
            print("Transaction History")
            print("-------------------------")
            print(self.accounts[account_no]["transaction_history"])
            
    def money_transfer(self, account_no, receiver_account_no, amount):
        if account_no in self.accounts:
            if receiver_account_no in self.accounts:
                if amount <= self.accounts[account_no]["balance"] and amount > 0:
                    self.accounts[account_no]["balance"] -= amount
                    self.accounts[receiver_account_no]["balance"] += amount
                    print(f"{amount} transferred successfully from {account_no} to {receiver_account_no}")
                else:
                    print("Insufficient transfer amount")
            else:
                print("Invalid receiver account number")
        else:
            print("Invalid sender account number")


    def take_loan(self, ac_no, amount):
        if self.loan_available:  
            if not self.bankrupt:  
                if ac_no in self.accounts:  
                    if self.accounts[ac_no]["loan_count"] < self.loan_limit:
                        self.accounts[ac_no]["balance"] += amount
                        self.total_loan_amount += amount
                        self.accounts[ac_no]["transaction_history"].append(f"Transaction no: TrxID-{uuid1()}, Took loan {amount}, datetime: {datetime.now()}")
                        self.accounts[ac_no]["loan_count"] += 1
                        print(f"{amount} tk loan got successful!!")
                    else:
                        print("Maximum loan limit reached!!")
                else:
                    print("Account does not exist!!")
            else:
                print("The bank is bankrupt")
        else:
            print("The loan feature is currently disabled!!")

                
    def delete_account(self, account_no):
        if account_no in self.accounts:
            del self.accounts[account_no]
            print("Account deleted successfully!!")
        else:
            print("Invalid account!!")
    

    
    def off_loan(self):
        self.loan_available = False
        print("Loan system is now disabled!!")

    def on_loan(self):
        self.loan_available = True
        print("Loan system is now enabled!!")
                   
class User:
    def __init__(self, bank_system):
        self.BankSystem = bank_system


    def create_account(self, name, email, address, bank_type):
        self.BankSystem.create_account(name, email, address, bank_type)
    
    def deposit(self, ac_no, amount):
        self.BankSystem.deposit(ac_no, amount)

    def withdraw(self, ac_no, amount):
        self.BankSystem.withdraw(ac_no, amount)

    def check_balance(self, ac_no):
        self.BankSystem.check_balance(ac_no)

    def transaction_history(self, ac_no):
        self.BankSystem.transaction_history(ac_no)

    def money_transfer(self, ac_no, receiver_account_number, amount):
        self.BankSystem.money_transfer(ac_no, receiver_account_number, amount)

    def take_loan(self, ac_no, amount):
        self.BankSystem.take_loan(ac_no, amount)

# **Admin**

class Admin:
    def __init__(self, username, password,bank_system):
        self.username = username
        self.password = password
        self.BankSystem=bank_system

    def login(self, username, password):
        if username == self.username and password == self.password:
            return True
        else:
            return False

    def create_account(self, name, email, address, account_type):
        self.BankSystem.create_account(name, email, address, account_type)

    def delete_account(self, ac_no):
        self.BankSystem.delete_account(ac_no)

    def get_all_accounts(self):
        for ac_no, account_info in self.BankSystem.accounts.items():
            print("\n")
            print(f"""
                    --------------------------------------------
                    Account Number: {ac_no}
                    Name: {account_info['name']}
                    Email: {account_info['email']}
                    Address: {account_info['address']}
                    Account Type: {account_info['account_type']}
                    Balance: {account_info['balance']}
                    --------------------------------------------
                """)

    def get_total_balance(self):
        self.BankSystem.get_total_balance()

    def get_total_loan_amount(self):
        print(f"Total loan amount: { self.BankSystem.total_loan_amount}")
    
    def off_loan(self):
         self.BankSystem.off_loan()

    def on_loan(self):
        self.BankSystem.on_loan()

    def change_bankrupt_status(self, status):
        self.BankSystem.bankrupt = status
        if status:
            print("Bankrupt system is now Enabled!!.")
        else:
            print("Bankrupt system is now Disabled!!..")



def user(bank_system):
    users = User(bank_system)
    while True:
        print("Options")
        print("--------------------------------")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transaction History")
        print("5. Money Transfer")
        print("6. Check User Balance")
        print("7. Take Bank Loan")
        print("8. Exit")
        print("--------------------------------")
        choice = int(input("Enter the option: "))

        if choice == 1:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter your account_type (Savings/Current): ")
            users.create_account(name, email, address, account_type)

        elif choice == 2:
            ac_no = int(input("Enter account Number: "))
            amount = int(input("Enter amount: "))
            users.deposit(ac_no, amount)

        elif choice == 3:
            ac_no = int(input("Enter account Number: "))
            amount = int(input("Enter amount: "))
            users.withdraw(ac_no, amount)

        elif choice == 4:
            ac_no = int(input("Enter account Number: "))
            users.transaction_history(ac_no)

        elif choice == 5:
            ac_no = int(input("Enter sender account Number: "))
            receiver_account = int(input("Enter receiver account number: "))
            amount = int(input("Enter amount: "))
            users.money_transfer(ac_no, receiver_account, amount)

        elif choice == 6:
            ac_no = int(input("Enter account Number: "))
            users.check_balance(ac_no)
            
        elif choice == 7:
            ac_no = int(input("Enter account Number: "))
            amount = int(input("Enter amount: "))
            users.take_loan(ac_no, amount)
        elif choice == 8:
            break
        else:
            print("Invalid input!!")

def admin(bank_system):
    admin_username = "admin"
    admin_password = "123"
    admn = Admin(admin_username, admin_password,bank_system)

    print("Admin Login")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if admn.login(username, password):
        print("Admin login successful!")
    else:
        print("Invalid username or password. Admin login failed.")
        return admin(bank_system) 
    while True:
        print("Options")
        print("--------------------------------")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. All User Accounts")
        print("4. Total Available Bank Balance")
        print("5. Total loan Amount")
        print("6. Change Loan Status")
        print("7. Change Bankrupt Status")
        print("8. Exit")
        print("--------------------------------")
        choice = int(input("Enter the option: "))
        if choice == 1:
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            account_type = input("Enter account_type (Savings/Current): ")
            admn.create_account(name, email, address, account_type)
        elif choice == 2:
            ac_no = int(input("Enter account Number: "))
            admn.delete_account(ac_no)
        elif choice == 3:
            admn.get_all_accounts()
        elif choice == 4:
            admn.get_total_balance()
        elif choice == 5:
            admn.get_total_loan_amount()
        elif choice == 6:
            option = input("Enter (ON/OFF) for Enable or Disable loan availablity: ").lower()
            if option == 'on':
                admn.on_loan()
            elif option == 'off':
                admn.off_loan()
            else:
                print("Invalid input")
        elif choice == 7:
            status = input("Enter (ON/OFF) for Enable or Disable bankrupt status: ").lower()
            if status == 'on':
                admn.change_bankrupt_status(True)
            elif status == 'off':
                admn.change_bankrupt_status(False)
            else:
                print("Invalid input!!")
        elif choice == 8:
            break
        else:
            print("Invalid input!!")

bank_system = BankSystem()
while True:
    print("Options")
    print("----------")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    print("----------")
    choice = int(input("Enter choice option: "))
    if choice == 1:
        user(bank_system)
    elif choice == 2:
        admin(bank_system)
    elif choice == 3:
        break
    else:
        print("Invalid option!")
