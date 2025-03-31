import csv

'''-------------------------------------------------------------
   Patient Class to maintain data about patients
-------------------------------------------------------------'''
class Patient:
    def __init__(self, patient_id, name, age, gender, contact, address, medical_history):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact
        self.address = address
        self.medical_history = medical_history

    def __str__(self):
        s = self.patient_id
        s = s + " " + self.name
        s = s + " " + str(self.age)
        s = s + " " + self.gender
        s = s + " " + str(self.contact)
        s = s + " " + self.address
        s = s + " " + self.medical_history
        return s
       

'''-------------------------------------------------------------  
   PatientHashMap Class to maintain Patient details
   in the form of Dictionary
   -------------------------------------------------------------'''
class PatientHashMap:
    def __init__(self):
        self.patients = {}  # dictionary to hold patient data
        
    def add_patient(self, patient):
        patient_id = patient.patient_id
        if patient_id in self.patients:
            print(f"Patient with ID {patient_id} already exists.")
            return False
        else:
            self.patients[patient_id] = patient
            return True
    
    def update_patient(self, patient_id, age, contact, address):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            
            patient.age = age
            patient.contact = contact
            patient.address = address
            
            self.patients[patient_id] = patient
            return True
        else:
            print(f"Patient with ID {patient_id} not found.")  
            return False

    def delete_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            return True
        else:
            print(f"Patient with ID {patient_id} not found.")  
            return False  
        
    def is_patient_id_already_exists(self, patient_id):
        if patient_id in self.patients:
            return True
        else:
            return False 
    
    def find_patient(self, patient_id):
        if patient_id in self.patients:
            return self.patients[patient_id]
        else:
            return None 

    def get_all_patient_ID(self):
        return list(self.patients.keys())
    
    def get_all_patients(self):
        return list(self.patients.values())
    
    def __str__(self):
        return "\n".join(str(patient) for patient in self.patients.values())
    
    
'''-------------------------------------------------------------
   Create new Patient record and add to Map
   and returns back either True or False as response
   -------------------------------------------------------------'''

def create_patient_record(patient_id, name, age, gender, contact, address, medical_history):
    # create new patient
    new_patient = Patient(patient_id, name, age, gender, contact, address, medical_history)
    # Add patient to HashMap
    response = patient_map.add_patient(new_patient)
    if response:
        write_patient_records()   # Write to File

    return response


'''-------------------------------------------------------------
   Update patient record using patient_id
   and returns back either True or False as response
-------------------------------------------------------------'''

def update_patient_record(patient_id, age, contact, address):
    # Update patient details
    response = patient_map.update_patient(patient_id, age, contact, address)
    if response:
         write_patient_records()   # Write to File
        
    return response
    

'''-------------------------------------------------------------
   Delete patient record using patient_id
   and returns back either True or False as response
-------------------------------------------------------------'''

def delete_patient_record(patient_id):
     # Delete patient record
    response = patient_map.delete_patient(patient_id)
    if response:
         write_patient_records()   # Write to File
    return response

'''-------------------------------------------------------------
   Check if patient with given patient_id already exists
-------------------------------------------------------------'''
def is_patient_id_already_exists(patient_id):
    return patient_map.is_patient_id_already_exists(patient_id)

'''-------------------------------------------------------------
   Retrive patient using patient_id
-------------------------------------------------------------'''
def get_patient_record(patient_id):
    return patient_map.find_patient(patient_id)


'''-------------------------------------------------------------
   Get all patient IDs registered in the application
-------------------------------------------------------------'''
def get_all_patient_ID():
    return patient_map.get_all_patient_ID()


'''-------------------------------------------------------------
   Get all patient objects registered in the application
-------------------------------------------------------------'''
def get_all_patients():
    return patient_map.get_all_patients()



'''-------------------------------------------------------------
   Write all the contents of HashMap data to file
-------------------------------------------------------------'''
def write_patient_records():
    with open(patient_filename, mode='w', newline='') as file:
        fieldnames = ['Patient_ID', 'Name', 'Age', 'Gender', 'Contact', 'Address', 'Medical_History']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for patient in patient_map.get_all_patients():
            record = {
                'Patient_ID': patient.patient_id,
                'Name': patient.name,
                'Age': patient.age,
                'Gender': patient.gender,
                'Contact': patient.contact,
                'Address': patient.address,
                'Medical_History': patient.medical_history
            }                
            csv_writer.writerow(record)
            

'''-------------------------------------------------------------
   Read patient records from CSV file and store to Hashmap 
-------------------------------------------------------------'''
def read_patient_records():
    # Create new HashMap for maintianing patients
    patient_map = PatientHashMap()
    try:
        with open(patient_filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # parse each row
                patient_id = row['Patient_ID']
                name = row['Name']
                age = row['Age']
                gender = row['Gender']
                contact = row['Contact']
                address = row['Address']
                medical_history = row['Medical_History']
                # create new patient
                patient = Patient(patient_id, name, age, gender, contact, address, medical_history)
                # Add patient to HashMap
                patient_map.add_patient(patient)
    except FileNotFoundError:
        pass

    # return Hashmap of patients
    return patient_map


# CSV FILENAME
patient_filename = 'patient_records.csv'
# Read File and creates Patient HashMap
patient_map = read_patient_records()

'''-------------------------------------------------------------
   Application menue for command line demo
-------------------------------------------------------------'''
def showPatientMenu():    
    while True:
        print("\n1. Create New Patient Record")
        print("2. Update Patient Record")
        print("3. Delete Patient Record")
        print("4. Retrieve Patient Record")
        print("5. View All Patients")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            # collect patient details
            patient_id = input("Enter Patient ID: ")
            name = input("Enter Patient Name: ")
            age = input("Enter Patient Age: ")
            gender = input("Enter Patient Gender: ")
            contact = input("Enter Contact details: ")
            address = input("Enter Address: ")
            medical_history = input("Enter Medical history: ")

            # create new patient and add to HashMap
            response = create_patient_record(patient_id, name, age, gender, contact, address, medical_history)
            if response:
                print(f"New Patient Record with ID {patient_id} created successfully")
            else:
                print("Unable to create New Patient Record")
        
        elif choice == '2': 
            # Update patient details
            patient_id = input("Enter Patient ID to update: ")
            patient = patient_map.find_patient(patient_id)
            if patient:
                print(patient)
                print("Enter following details to update the record : ")
                age = input("Enter Patient Age: ")
                contact = input("Enter Contact details: ")
                address = input("Enter Address: ")
                
                response = update_patient_record(patient_id, age, contact, address)
                if response:
                    print(f"Patient ID {patient_id} updated successfully")
                else:
                    print(f"Unable to update Patient ID {patient_id}")
            else:
                print("\nPatient with ID ", patient_id, " not found.")
                    
        elif choice == '3':
            # Delete patient details           
            patient_id = input("Enter Patient ID to delete: ")
            response = delete_patient_record(patient_id)
            if response:
                print(f"Patient ID {patient_id} deleted successfully")
            else:
                print(f"Unable to delete Patient ID {patient_id}")
           
        elif choice == '4':
            # Search and retrieve patient details
            patient_id = input("Enter Patient ID: ")
            patient = get_patient_record(patient_id)
            if patient:
                print("\nPatient Record: ", patient)
            else:
                print("\nPatient with ID ", patient_id, " not found.")
        
            
        elif choice == '5':
            all_patient_map = patient_map.get_all_patients()
            if len(all_patient_map) == 0:
                print("\nNo Patients found\n")
            else:
                print("\nList of Patients are...")
                for patient in all_patient_map:
                    print(patient)
                
        elif choice == '6':
            # Write the Patient HashMap to File
            write_patient_records()
            break
        
        else:
            print("\nInvalid choice. Please try again.")


#main program
#showPatientMenu()


