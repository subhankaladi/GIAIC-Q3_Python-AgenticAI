class Bank:
    bank_name = "State Bank"

    @classmethod
    def change_bank_name(cls, name):
        cls.bank_name = name

# Test
b1 = Bank()
b2 = Bank()
print(Bank.bank_name)
Bank.change_bank_name("New Bank")
print(b1.bank_name)
print(b2.bank_name)
