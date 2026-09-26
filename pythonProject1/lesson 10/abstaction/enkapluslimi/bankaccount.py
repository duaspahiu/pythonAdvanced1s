class backaccount:

    def __init__(self,owner,balance):
    self.owner = owner
    self.__balance = balance

    def deposit(self,account):
        self.__balance+=account

    def get_balence(self):
        return sel.__balance

account = backaccount("dua",100)

print(account.get_balence())
account.deposit(50)

print(account.get_balence())