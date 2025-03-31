import csv
'''-------------------------------------------------------------
   Login Class to maintain user details
   Roles : NURSE / DOCTOR / ADMIN
-------------------------------------------------------------'''
class User:
    def __init__(self, userid, password, role):
        self.userid = userid
        self.password = password
        self.role = role
    def __str__(self):
        s = self.userid
        s=s+' '+self.role
        
        return s
class UserNode:
    def __init__(self,user=None,next=None):
        self.user=user
        self.next=next
    def getUser(self):
        return self.user
    
class LoginList:
    def __init__(self):
        self.head=None
        self.tail=None
    def append(self,user):
        new_user=UserNode(user)
        if self.head == None:
            # First time linked list creation, update head & tail
            self.head = UserNode()
            self.head.next = new_user
            self.tail = new_user
        else:
            # add new node to tail of linked list
            self.tail.next = new_user
            self.tail = new_user
    def isEmpty(self):
        if self.head == None :
            return True
    def delete(self,userid):
        user=self.find(userid)
        if not self.isEmpty():
            current=self.head
            while current:
                if current.next.user==user:
                    current.next=current.next.next
                    user.next=None
                    return 
                
                else:
                    current=current.next
                    
            print('value not found ')
            return   
            
        
        
    def find(self, userid):
        if self.head == None: # Empty List
            return None
        
        current = self.head.next
        while current:
            user = current.getUser()
            if user.userid == userid:
                return current.user
            current = current.next
        return None
    
    def get_all_user_ID(self):
        data_list = []
        if self.head == None:  # Empty List
            return data_list
        
        current = self.head.next
        while current:
            if current.user != None:
                data_list.append(current.user.userid)
            current = current.next
        return data_list
    
    def user_to_list(self):
        data_list = []
        if self.head == None:  # Empty List
            return data_list
        
        current = self.head.next
        while current:
            if current.user != None:
                data_list.append(current.user)
            current = current.next
        return data_list

    def __str__(self):
        data_list = self.user_to_list()
        return "".join(data_list)


def create_user(user_list,userid,password,role):
    if user_list.find(userid) is None:
        new_user = User(userid,password,role)
        user_list.append(new_user)
        return True
    else:
        return False

def get_user_record(user_list, userid):
    return user_list.find(userid)

def get_all_user_ID(user_list):
    return user_list.get_all_user_ID()

def validate_user(user_list,userid,password):
    user = user_list.find(userid)
    if user == None:
        print('User doesnot exist')
        return False
    elif user.password == password:
        print('valid password')
        return True
    else:
        print('invalid password')
        return False
    
def change_password(user_list,userid,password,newpassword):
    
    if validate_user(user_list,userid,password):
        
        user=user_list.find(userid)
        user.password=newpassword
        return True
    else:
        return False
def delete_user(user_list,userid,password):
    if validate_user(user_list,userid,password):
        user_list.delete(userid)
        return True
    else:
        return False
        
def write_user_records(filename, user_list):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['userid','password','role']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for user in user_list.user_to_list():
            record = {
                'userid':user.userid,
                'password':user.password,
                'role':user.role,
            }                
            csv_writer.writerow(record)
            

'''-------------------------------------------------------------
   Read user records from CSV file and store to LinkedList 
-------------------------------------------------------------'''
def read_user_records(filename):
    # Create new LinkedList for maintianing patients
    user_list = LoginList()
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # parse each row
                userid=row['userid']
                password=row['password']
                role=row['role']
                # create new user
                user = User(userid,password,role)
                # Add user to LinkedList
                user_list.append(user)
    except FileNotFoundError:
        pass

    # return linked list of users
    return user_list


# Read File and creates Patient Linked List
user_list = read_user_records('user_records.csv')


def showApplication():
    filename = 'user_records.csv'

    # Read File and creates Patient Linked List 
    #user_list = read_user_records(filename)
        
    while True:
        print("\n1. add user")
        print("2. change password ")
        print("3. Delete user")
        print("4. View All user")
        print("5. Exit")
        

        choice=input('enter your choice :')
        if choice =='1':
            userid=input('enter user id')
            password=input('enter password')
            role=input('enter role')
            new_user=create_user(user_list,userid,password,role)
            print('new user created : ',new_user)
        elif choice =='2':
            userid=input('enter user id')
            change_password(user_list,userid)
        elif choice =='4':
            all_user_list = user_list.user_to_list()
            if len(all_user_list) == 0:
                print("\nNo Users found\n")
            else:
                print("\nList of Users are...")
                for user in all_user_list:
                    print(user)
        elif choice=='3':
            userid=input('enter user id')
            delete_user(user_list,userid)
            
        elif choice=='5':
            write_user_records(filename, user_list)
            break
        else:
            print("\nInvalid choice. Please try again.")

#showApplication()
            

        
