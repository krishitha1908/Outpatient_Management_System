from datetime import datetime
import csv

'''-------------------------------------------------------------
   Visit Class to maintain various visits of a patient
-------------------------------------------------------------'''
class PatientVisit:
    def __init__(self, patient_id, date, doctor, diagnosis, prescription):
        self.patient_id = patient_id

        if isinstance(date, str) :
            self.date = datetime.strptime(date, date_format)
        else:
            self.date = date
        
        self.doctor = doctor
        self.diagnosis = diagnosis
        self.prescription = prescription

    def __str__(self):
        s = self.patient_id
        s = s + " " + self.date.strftime(date_format)
        s = s + " " + self.doctor
        s = s + " " + self.diagnosis
        s = s + " " + self.prescription
        return s
    

'''-------------------------------------------------------------
   TreeNode Class to be used as a Node in Tree
-------------------------------------------------------------'''
class TreeNode:  # Node with multiple children
    def __init__(self, data=None, parent=None):
        self.data = data
        self.children = [] 
        self.parent = parent

    def appendChild(self, item):
        self.children.append(item)
    
    def getChildNode(self, value):
        for child in self.children:
            # returns PatientVisit object if search for patient_id
            if isinstance(child, PatientVisit) :
                if child.patient_id == value:
                    return child
            # returns TreeNode if search for year or month or day
            elif child.data == value:
                return child
            
        return None
        

'''-------------------------------------------------------------  
   VisitTree Class to maintain Visit details in the form of Tree

   Tree Structure -- Node with multiple children

    Root: Dummy node.
    Level 1: Children are years.
    Level 2: Children are months 
    Level 3: Children are days 
    Level 4: Store multiple PatientVisit objects.

   -------------------------------------------------------------'''


class VisitTree:
    def __init__(self):
        self.root = TreeNode() # root node is a dummy node

    def isEmpty(self):
        if len(self.root.children) == 0 :
            return True
        else:
            return False

    def insert_visit(self, visit):
        year = visit.date.year
        month = visit.date.month
        day = visit.date.day

        yearNode = self.root.getChildNode(year)
        if yearNode == None:  # if year not found ,  newly add year to root
            yearNode = TreeNode(year, self.root)
            self.root.appendChild(yearNode)
                  
        monthNode = yearNode.getChildNode(month)
        if monthNode == None:  # if month not found , newly add month to year node
            monthNode = TreeNode(month, yearNode)
            yearNode.appendChild(monthNode)

        dayNode = monthNode.getChildNode(day)
        if dayNode == None:  # if date not found , newly add date to month node
            dayNode = TreeNode(day, monthNode)
            monthNode.appendChild(dayNode)

        dayNode.appendChild(visit)
        return True
    
    def update_visit(self, patient_id, visit_date, newdiagnosis, newprescription):
        dayNode = self.get_day_node(visit_date)
        if dayNode == None:  # if visit with given patient id and visit_date not found 
            print(f"No Patients visited on {visit_date}")
            return False  
        else:
            visit_obj = dayNode.getChildNode(patient_id)
            if visit_obj == None:
                print(f"Patient ID {patient_id} NOT visited on {visit_date}")
                return False
            else:
                # Found visit with matching date and patient id, hence update the visit
                visit_obj.diagnosis = newdiagnosis
                visit_obj.prescription = newprescription
                return True


    def delete_visit(self, patient_id, visit_date):
        dayNode = self.get_day_node(visit_date)
        if dayNode == None:  # if visit with given patient id and visit_date not found 
            print(f"No Patients visited on {visit_date}")
            return False  
        else:
            visit_obj = dayNode.getChildNode(patient_id)
            if visit_obj == None:
                print(f"Patient ID {patient_id} NOT visited on {visit_date}")
                return False
            else:
                # Found visit with matching date and patient id, hence delete the visit
                dayNode.children.remove(visit_obj)
                print(f"Visit with Patient ID {patient_id}  and date_of_vist {visit_date} deleted successfully.")
                return True
        
    def get_visit(self, patient_id, visit_date):
        dayNode = self.get_day_node(visit_date)
        if dayNode == None:  # if visit with given visit_date not found 
            return None
        else:
            visit_obj = dayNode.getChildNode(patient_id)
            if visit_obj == None:
                return None
            else:
                # Found visit with matching date and patient id, hence return the visit_obj
                return visit_obj
    
    def get_day_node(self, visit_date):
        date = visit_date
        if isinstance(date, str) :
            date = datetime.strptime(date, date_format)

        year = date.year
        month = date.month
        day = date.day

        yearNode = self.root.getChildNode(year)
        if yearNode == None:  # if year not found 
            return None
        
        monthNode = yearNode.getChildNode(month)
        if monthNode == None:  # if month not found 
            return None

        dayNode = monthNode.getChildNode(day)
        if dayNode == None:  # if date not found 
            return None
        else:
            # Found day Node with matching date , hence return the day Node
            return dayNode 
    
    def get_all_visit(self):
        all_visit = []
        for year_node in self.root.children:
            for month_node in year_node.children:
                for day_node in month_node.children:
                    for visit_obj in day_node.children:
                        all_visit.append(visit_obj)

        return all_visit

   
'''-------------------------------------------------------------
   Create new visit record and update to Linked List
   and returns back new visit object
   -------------------------------------------------------------'''
def create_visit_record(patient_id, date, doctor, diagnosis, prescription):
    # create new visit
    new_visit = PatientVisit(patient_id, date, doctor, diagnosis, prescription)
    
    # Add visit to Tree
    response = visit_tree.insert_visit(new_visit)
    if response:
        write_visit_records()   # Write to File
    return response

'''-------------------------------------------------------------
   Update visit details using patient_id
-------------------------------------------------------------'''

def update_visit(patient_id, date, newdiagnosis, newprescription):
    # Update patient visit details
    response = visit_tree.update_visit(patient_id, date, newdiagnosis, newprescription)
    if response:
         write_visit_records()   # Write to File
    return response

'''-------------------------------------------------------------
   Delete visit details using patient_id
-------------------------------------------------------------'''
def delete_visit(patient_id, date):
    # Delete patient visit details
    response = visit_tree.delete_visit(patient_id, date)
    if response:
         write_visit_records()   # Write to File
    return response

'''-------------------------------------------------------------
   Retrive patient visit using patient_id and date of visit
-------------------------------------------------------------'''
def get_visit_record(patient_id, date):
    return visit_tree.get_visit(patient_id, date)


'''-------------------------------------------------------------
   Get all patient visit objects 
-------------------------------------------------------------'''
def get_all_visit():
    return visit_tree.get_all_visit()


'''-------------------------------------------------------------
   Write all the contents of LinkedList data to file using Dict
-------------------------------------------------------------'''

def write_visit_records():
    with open(visit_filename, mode='w', newline='') as file:
        fieldnames = ['Patient_ID', 'Date', 'Doctor', 'Diagnosis','Prescription']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for visit in visit_tree.get_all_visit():
            record = {
                'Patient_ID': visit.patient_id,
                'Date': visit.date.strftime(date_format),
                'Doctor':visit.doctor,
                'Diagnosis':visit.diagnosis,
                'Prescription':visit.prescription
            }                
            csv_writer.writerow(record)
            

'''-------------------------------------------------------------
   Read visit records from CSV file and store to LinkedList 
-------------------------------------------------------------'''
def read_visit_records():
    # Create new LinkedList for maintianing patients
    visit_tree = VisitTree()
    try:
        with open(visit_filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # parse each row
                patient_id = row['Patient_ID']
                date = row['Date']
                doctor = row['Doctor']
                diagnosis = row['Diagnosis']
                prescription = row['Prescription']
                # create new patient
                visit = PatientVisit(patient_id,date,doctor,diagnosis,prescription)
                # Add patient to LinkedList
                visit_tree.insert_visit(visit)
    except FileNotFoundError:
        pass

    # return linked list of patients
    return visit_tree

# CSV FILENAME
date_format = '%Y-%m-%d'
visit_filename = 'visit_records.csv'
# Read File and creates Patient Visit Tree
visit_tree = read_visit_records()

'''-------------------------------------------------------------
   Application menue for command line demo
-------------------------------------------------------------'''
def showApplication():
        
    while True:
        print("\n1. Create New visit Record")
        print("2. Update visit Record")
        print("3. Delete visit Record")
        print("4. Retrieve visit Record")
        print("5. View All visits")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            # collect visit details
            patient_id = input("Enter Patient ID: ")
            date = input("Enter Date: ")
            diagnosis = input("Enter Diagnosis: ")
            prescription = input("Enter prescription: ")
            doctor = input("Enter doctor: ")

            # create new visit and add to Tree
            response = create_visit_record(patient_id, date, doctor, diagnosis, prescription)
            if response:
                print(f"New Visit Record with Patient ID {patient_id} and date of visit {date} created successfully")
            else:
                print("Unable to create New Visit Record")
        
        elif choice == '2': 
            # Update visit details
            patient_id = input("Enter Patient ID to update: ")
            date = input("Enter Date of Visit: ")
            visit = get_visit_record (patient_id, date)
            if visit:
                print("\nVisit Record: ", visit)
                print("Enter following details to update the visit record : ")
                newdiagnosis = input("Enter New Diagnois to update: ")
                newprescription = input("Enter new Prescription to update: ")
                
                response = update_visit(patient_id, date, newdiagnosis, newprescription)
                if response:
                    print(f"Visit record with Patient ID {patient_id} and date of visit {date} updated successfully")
                else:
                    print(f"Unable to update visit with Patient ID {patient_id} and date of visit {date}")
            else:
                print(f"Patient ID {patient_id} not visited on {date}")

        elif choice == '3':
            # Delete visit details 
            patient_id = input("Enter Patient ID to delete: ")
            date = input("Enter Date of Visit: ")
            response = delete_visit(patient_id, date)
            if response:
                print(f"Visit record with Patient ID {patient_id} and date of visit {date} deleted successfully")
            else:
                print(f"Unable to delete visit with Patient ID {patient_id} and date of visit {date}")

        elif choice == '4':
            # Search and retrieve visit details
            patient_id = input("Enter Patient ID: ")
            date = input("Enter Date of Visit: ")
            visit = get_visit_record (patient_id, date)
            if visit:
                print("\nVisit Record: ", visit)
            else:
                print(f"Patient ID {patient_id} not visited on {date}")
        
            
        elif choice == '5':
            all_patientVisit = get_all_visit()
            if len(all_patientVisit) == 0:
                print("\nNo Patient Visits found\n")
            else:
                print("\nList of Patient Visits are...")
                for visit in all_patientVisit:
                    print(visit)
                
        elif choice == '6':
            # Write the Patient Visit Tree to File
            write_visit_records()
            break
        
        else:
            print("\nInvalid choice. Please try again.")


#main program
#showApplication()
    
    
