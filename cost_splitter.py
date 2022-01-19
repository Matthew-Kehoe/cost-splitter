class Person:
    def __init__(self, name):
        
        '''
            takes a name, initiliases a balance to 0 and an event lock to empty string
        '''
        self.name = name
        self.__balance = 0
        self.event_lock  = ""
        
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        self.__balance = value
        
class Event:
 
    def __init__(self, event_name, participants):
        '''
        takes an event name and list of participants
        
        1.Checks that all elements in list are Person objects
        2.Checks participant event lock to see if participants are already participating in a different event
        
        '''
        
        #validation
        
        if not all(isinstance(x, Person) for x in participants):
            print("Only partcipants who are people objects can be added")
        
        elif any(x.event_lock != "" for x in participants):
            print("Already participating in an event, cannot add")
            
        self.event_name = event_name
        self.participants = participants
        self.expenses = []
        self.__total = 0
        
    @property
    def total(self):
        
        
        return self.__total
    
    @total.setter
    def total(self, value):
        self.__total = value
        
    def add_trans(self, name, amount, payee):
        """
        method, takes a name, amount and payee
        
        1.Checks that amount is above zero and is either a float or int
        2.Checks that transaction name is a string
        3.Checks that payee is in event participant list
        
        If all okay:
        1. creates a transaction instance, appends it's name to the exepnses list
        2. increments the event total by the transaction amount
        3. increments payee balance by the transaction amount
        
        
        """
        
        if (amount <= 0) or not isinstance(amount, (float,int)):
            return f"Amount input({amount}) is not a positive number, transaction not created."
            
        elif not isinstance(name, str):
            return f"Transaction name must be a string input."
            
        elif not any(x == payee for x in self.participants):
            return f"Payee entered is not in participant list, please enter a payee who is participating in the event"
        else:
            name = Transaction(name, amount, payee)
            self.expenses.append(name) 
            self.total += amount
            payee.balance += amount
            
        
    def release_participants(self):
        """
            If event total is zero (can only take place following reconciliation or when no transactions added yet):
                -set all participant event locks to empty string and participant list to empty
                -print info string 
            Else:
                - print info string 
        """
        if self.total == 0:
            for i in range(len(self.participants)):
                self.participants[i].event_lock = ""
            self.participants= []
            
            print("Participants may now take part in another event, have a nice day.")
        else:
            print("Outstanding balance, participants must first reconcile event balance")
                
        
        
        
        
    def total_cost(self):
        """
        Method for checking the current total and the amount per participant:
        1. prints formatted string where it prints the total amount, and the total amount divided by nubmer of paritcipants
        
        """
        return f"Total: €{self.total}, that is €{round(self.total/len(self.participants), 2)} each."
    
    
    def reconcile(self):
        
        """
        Used to reconcile the amounts owed by partipants to one another
        
        1.Prints formatted balance for all participants
        2. Subtracts contribution for each participcants(also truncates values past 2nd decimal place)
        3. Prints formatted balance following contribution
        4. Adds participants to either creditor or debitor list
        5. Uses a nested for loop to iterate all debitors over all creditors
            - if debitor abs balance is greater than creditor abs balance:
                -adds creditor balance to debitor balance
                -print formatted message of operation
                - set creditor balance to 0
                -break
             - else if creditor abs value greater than debitor abs value
                -add creditor balance to debitor balance
                -print formatted message of operation
                -set debitor balance to 0
             - else (creditor balance = debitor balance)
                 - set both to zero
                 -print formatted message of operation
                 
            -set event_total to 0
                
        
        """
        
        #printing overall total
        
        for i in range(len(self.participants)):
            print(f"{self.participants[i].name} has a balance of {self.participants[i].balance}")
            
        #subtracting contribution
        for i in range(len(self.participants)):
            self.participants[i].balance -= self.total/len(self.participants)
            
            #truncating values beyond 2 decimal places for all participantss
            self.participants[i].balance = int(self.participants[i].balance*100)/100
        
        print()
        
        
        #printing explination of breakdown for users
        print(f"After subtracting contribution of {round(self.total/len(self.participants), 2)} each, total is as follows: ")
        for i in range(len(self.participants)):
            print("{} has a balance of {}".format(self.participants[i].name,self.participants[i].balance))
            
        print("\n")
        
        creditors = []
        debitors = []

        for i in range(len(self.participants)):
            if self.participants[i].balance > 0:
                creditors.append(self.participants[i]) 
            elif self.participants[i].balance < 0:
                debitors.append(self.participants[i])
                
        
                
        for i in range(len(creditors)):
            for j in range(len(debitors)):
                if (creditors[i].balance + debitors[j].balance) < 0:
        
                    print(f"{debitors[j].name} pays {creditors[i].name} €{round(creditors[i].balance,2)} ")
                    debitors[j].balance += creditors[i].balance
                    creditors[i].balance = 0
                    break
            
            
                elif (creditors[i].balance + debitors[j].balance) > 0:

                    print(f"{debitors[j].name} pays {creditors[i].name} €{round(debitors[j].balance,2)} ")
                    creditors[i].balance += debitors[j].balance
                    debitors[j].balance = 0
            
                else:
                    
                    print(f"{debitors[j].name} pays {creditors[i].name} €{round(creditors[i].balance,2)} ")
                    creditors[i].balance = 0
                    debitors[j].balance = 0

                    break
        
        #handling imprecision associated with floats
        
        for i in range(len(self.participants)):
            if self.participants[i].balance < 0.01:
                self.participants[i].balance = 0
            
        self.total = 0
        self.expenses = []
        
        

#transaction class
            
class Transaction():
    def __init__(self, name, amount, payee):
        """
        Takes a name, amount and payee. 
        Input validation is performed in the add_trans() method in the Event class
        """
   
        self.name = name
        self.amount= amount
        self.payee = payee    
    
