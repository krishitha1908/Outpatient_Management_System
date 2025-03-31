import streamlit as st
from streamlit_option_menu import option_menu
from Login import  user_list,write_user_records, create_user, change_password, delete_user, validate_user,get_all_user_ID
from Patient_final import create_patient_record, update_patient_record, delete_patient_record, is_patient_id_already_exists, get_patient_record, get_all_patient_ID, get_all_patients
from PatientVisit import create_visit_record, update_visit, delete_visit, get_visit_record, get_all_visit, date_format
from sdpq import penqueue,pdequeue,aqueue, front

def patient_management(): # only for nurse
    st.subheader("Patient Management")
    operation = st.selectbox("Select operation", ["View All Patients", "Get Patient Record", "Create New Patient record", "Update Patient Record", "Delete Patient Record"])
    
    if operation == "View All Patients":
        st.subheader("View All Patients")

        all_patient_list = get_all_patients()
        if len(all_patient_list) == 0:
            st.info("No Patients found")
        else:
            data = []
            for patient in all_patient_list:
                data.append({
                    'Patient_ID': patient.patient_id,
                    'Name': patient.name,
                    'Age': patient.age,
                    'Gender': patient.gender,
                    'Contact': patient.contact,
                })                
           
            # Display the table
            st.table(data)
    
    elif operation== 'Create New Patient record':
        st.write("Creating new patient records")

        patient_id = st.text_input("Patient ID")
        if is_patient_id_already_exists(patient_id):
            st.error("Patient ID already exist. Enter different ID")  
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact")
        address = st.text_area("Address")
        medical_history = st.text_area("Medical History")

        if st.button("Create Patient Record"):
            if name and age and gender and contact and address and medical_history:
                response = create_patient_record(patient_id, name, age, gender, contact, address, medical_history)
                if response:
                    st.success(f"New Patient Record with ID {patient_id} created successfully")
                else:
                    st.error("Unable to create New Patient Record")
            else:
                st.error("Fill all the fields")

    elif operation == "Get Patient Record":
        all_patient_ID = get_all_patient_ID()
        if len(all_patient_ID) == 0:
            st.error("No Patient Records found")
        else:
            patient_id = st.selectbox("Patient ID", all_patient_ID)  
            if st.button("Retrive Patient Record"):  
                if patient_id:
                    patient = get_patient_record(patient_id)
                    if patient:
                        st.write("Patient Record Found:")
                        st.write("Name :", patient.name)
                        st.write("Age :", patient.age)
                        st.write("Gender: ", patient.gender)
                        st.write("Contact :",patient.contact)
                        st.write("Address :",patient.address)
                        st.write("Medical history :",patient.medical_history)

                    else:
                        st.warning("Unable to fetch Patient record")
            
    elif operation == "Update Patient Record":
        all_patient_ID = get_all_patient_ID()
        if len(all_patient_ID) == 0:
            st.error("No Patient Records found")
        else:
            patient_id = st.selectbox("Patient ID", all_patient_ID)    
            if patient_id:
                patient = get_patient_record(patient_id)
                age = st.number_input("Age", min_value=0, max_value=120, value=int(patient.age), step=1)
                contact=st.text_input('Enter Contact details',patient.contact )
                address=st.text_area('Enter Address',patient.address)

            if st.button("Update Patient Record"):
                if patient_id:
                    response = update_patient_record( patient_id, age, contact, address)
                    if response:
                        st.success(f"Patient ID {patient_id} updated successfully")      
                    else:
                        st.error(f"Unable to update Patient ID {patient_id}")
                else:
                    st.error("Select Patient ID")
                

    elif operation == "Delete Patient Record":
        all_patient_ID = get_all_patient_ID()
        if len(all_patient_ID) == 0:
            st.error("No Patient Records found")
        else:
            patient_id = st.selectbox("Patient ID", all_patient_ID)  
            if patient_id:
                patient = get_patient_record(patient_id)
                if patient:
                    st.write("Patient Record Found:")
                    st.write("Name :", patient.name)
                    st.write("Age :", patient.age)
                    st.write("Gender: ", patient.gender)
                    st.write("Contact :",patient.contact)
                    st.write("Address :",patient.address)
                    st.write("Medical history :",patient.medical_history)
                else:
                    st.warning("Unable to fetch Patient record")
        
            if st.button("Delete Patient Record"):
                if patient_id:
                    response = delete_patient_record(patient_id)
                    if response:
                        st.success(f"Patient ID {patient_id} deleted successfully")        
                    else:
                        st.error(f"Unable to delete Patient ID {patient_id}")
                else:
                    st.error("Select Patient ID")

def new_patient_visit(): # only for doctor
    st.subheader("New Patient Visit")
    operation = st.selectbox("Select operation", ["View Patient waiting in Queue", "Today's Visit"])
    
    patient_id = front(aqueue) 
    if patient_id == None:
        st.error("No patient is waiting in Queue")
    else:
        patient = get_patient_record(patient_id)
        if operation == "View Patient waiting in Queue":
            if patient == None:
                st.write("Patient ID :", patient_id)
                st.warning(f"Patient other details not found for Patient ID {patient_id}")
            else:
                st.write("Patient ID :", patient_id)
                st.write("Name       :", patient.name)
                st.write("Age        :", patient.age)
                st.write("Medical history :", patient.medical_history)

        elif operation == "Today's Visit":
            st.subheader("Today's Visit Details")
            st.write("Patient ID :", patient_id)
            if patient != None:
                st.write("Name       :", patient.name)
                st.write("Age        :", patient.age)
                
            date = st.date_input("Date", key ="date", format="YYYY-MM-DD")
            doctor = st.text_input("Doctor", key = "doctor")
            diagnosis =  st.text_area("Diagnosis")
            prescription =  st.text_area("Prescription")

            if st.button("Save Record"):
                if patient_id and date and doctor and diagnosis and prescription:
                    response = create_visit_record(patient_id, date, doctor, diagnosis, prescription)
                    if response:
                        patient_id = pdequeue(aqueue) 
                        st.success(f"New Visit Record with Patient ID {patient_id} and date of visit {date} created successfully")
                    else:
                        st.error("Unable to create New Visit Record")
                else:
                    st.error("Please fill out all fields")


def patient_visit_management(): # for both doctor and nurse
    st.subheader("Patient Visit Management")
    
    action = st.selectbox("Choose Action", ["View All Visits","Retrieve Visit", "Update Visit", "Delete Visit"])

    if action == "Retrieve Visit":
        patient_id = st.text_input("Patient ID")
        date = st.date_input("Date", format="YYYY-MM-DD" )
        
        if st.button("Retrieve"):
            if patient_id and date: 
                visit = get_visit_record (patient_id, date)
                if visit:
                    st.write(f"Date: {visit.date.strftime(date_format)}")
                    st.write(f"Doctor: {visit.doctor}")
                    st.write(f"Diagnosis: {visit.diagnosis}")
                    st.write(f"Prescription: {visit.prescription}")
                else:
                    st.error(f"Patient ID {patient_id} not visited on {date}")
            else:
                st.error("Please fill out all fields")
  
        
    elif action == "Update Visit":
        patient_id = st.text_input("Patient ID")
        date = st.date_input("Date", format="YYYY-MM-DD")
        
        if patient_id and date:
            visit = get_visit_record (patient_id, date)
            if visit:
                new_diagnosis =  st.text_area("New Diagnosis", value=visit.diagnosis)
                new_prescription =  st.text_area("New Prescription", value=visit.prescription)
                if st.button("Update Record"):
                    if new_diagnosis and new_prescription:
                        response = update_visit(patient_id, date, new_diagnosis, new_prescription)
                        if response:
                            st.success(f"Visit record with Patient ID {patient_id} and date of visit {date} updated successfully")
                        else:
                            st.error(f"Unable to update visit with Patient ID {patient_id} and date of visit {date}")
                    else:
                        st.error("Please fill Diagnosis and Prescription to update the visit record")
            else:
                st.error(f"Patient ID {patient_id} not visited on {date}")
            


    elif action == "Delete Visit":
        patient_id = st.text_input("Patient ID")
        date = st.date_input("Date", format="YYYY-MM-DD")
        
        if patient_id and date:
            visit = get_visit_record (patient_id, date)
            if visit:
                st.write(f"Patient ID: {visit.patient_id}")
                st.write(f"Date: {visit.date.strftime(date_format)}")
                st.write(f"Doctor: {visit.doctor}")
                st.write(f"Diagnosis: {visit.diagnosis}")
                st.write(f"Prescription: {visit.prescription}")
                if st.button("Delete"):
                    response = delete_visit(patient_id, date)
                    if response == True:
                        st.success(f"Visit record with Patient ID {patient_id} and date of visit {date} deleted successfully")
                    else:
                        st.error(f"Unable to delete visit with Patient ID {patient_id} and date of visit {date}")
            else:
                st.error(f"Patient ID {patient_id} not visited on {date}")
        else:
            st.error("Please fill Patient ID and Date of visit")
        

    elif action == "View All Visits":
        all_visits = get_all_visit()
        if len(all_visits) == 0:
            st.info("No visits found")
        else:
            visit_data = []
            for visit in all_visits:
                visit_data.append({
                    "Patient ID": visit.patient_id,
                    "Date": visit.date.strftime(date_format),
                    "Doctor": visit.doctor,
                    "Diagnosis": visit.diagnosis,
                    "Prescription": visit.prescription
                })

            # Display the table
            st.table(visit_data)

def user_management(): # only for admin
    st.subheader("User Management")
    
    # Admin functionalities
    admin_option = st.selectbox("Select an admin option", ["View All Users","Add User", "Change Password", "Delete User"])
    
    if admin_option == "Add User":
        st.subheader("Add User")
        all_user_ID = get_all_user_ID(user_list)
        new_userid = st.text_input("New User ID")
       

        if new_userid:
            if len(all_user_ID) != 0 and new_userid in all_user_ID:
                st.error("User ID already exist. Enter different ID") 
        
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["nurse", "doctor", "admin"])
        
        if st.button("Add User"):
            flag = create_user(user_list, new_userid, new_password, new_role)
            if flag:
                write_user_records('user_records.csv', user_list)
                st.success(f"User {new_userid} added successfully")
            else:
                st.error("Unable to create User")

    elif admin_option == "Change Password":
        st.subheader("Change Password")
        target_userid = st.text_input("User ID")
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        if st.button("Change Password"):
            if change_password(user_list, target_userid, old_password, new_password):
                write_user_records('user_records.csv', user_list)
                st.success("Password changed successfully")
            else:
                st.error("Failed to change password. Invalid user ID or old password")

    elif admin_option == "Delete User":
        st.subheader("Delete User")
        del_userid = st.text_input("User ID")
        del_password = st.text_input("Password", type="password")
        if st.button("Delete User"):
            if delete_user(user_list, del_userid, del_password):
                write_user_records('user_records.csv', user_list)
                st.success(f"User {del_userid} deleted successfully")
            else:
                st.error("Failed to delete user. Invalid user ID or password")

    elif admin_option == "View All Users":
        st.subheader("View All Users")
        all_user_list = user_list.user_to_list()
        if len(all_user_list) == 0:
            st.info("No Users found")
        else:
            data = []
            for user in all_user_list:
                data.append({
                    "User Name": user.userid,
                    "Role": user.role,
                })

           
            # Display the table
            st.table(data)
    

def logout():
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['userid'] = None
    st.rerun()

def patient_appointment(patient_id):
    penqueue(aqueue,patient_id)

def userLoggedIn():
    
    role = st.session_state['role']
    userid = st.session_state['userid']
    st.sidebar.title(f"Welcome User {userid}")
    st.sidebar.write(f"Logged in as {role.capitalize()}")
    if role == "nurse":
        with st.sidebar:
            nurse_menu = option_menu(
                menu_title="Main Menu",
                options=["Patient Management",'Patient Appointment' ,"Patient Visit Management", "Logout"],
                icons= ['house', 'hand-thumbs-up', 'cloud-sun'], 
                menu_icon= 'cast', 
                default_index= 0,
            )

        if nurse_menu == "Patient Management":
            patient_management()

        elif nurse_menu=='Patient Appointment':
            all_patient_ID = get_all_patient_ID()
            if len(all_patient_ID) == 0:
                st.error("No Patient Records found. Crate New patient before visit")
            else:
                patient_id = st.selectbox("Patient ID", all_patient_ID)
                # Create two columns
                col1, col2, col3 = st.columns([1, 1, 2])
                # Fix Appointment Button (left side)
                with col1:
                    if st.button('Fix Appointment'):
                        patient_appointment(patient_id)
                        st.success(f"Appointment Fixed for Patient ID {patient_id}")

                
                # View Appointment Button (right side)
                with col3:
                    if st.button('View Appointments'):
                        st.subheader("All Appointments")
                        if len(aqueue.items) == 0:
                            st.write("No patients waiting in Queue")
                        else:
                            for index, patient in enumerate(aqueue.items):
                                st.write(f"{index+1}. {patient}")
            
        elif nurse_menu == "Patient Visit Management":
            patient_visit_management()
        
        elif nurse_menu == "Logout":
            logout()
        
    elif role == "doctor":
        with st.sidebar:
            doctor_menu = option_menu(
                menu_title="Main Menu",
                options=["Patient Visiting Doctor", "Patient Visit Management", "Logout"],
                icons= ['house', 'hand-thumbs-up', 'cloud-sun'], 
                menu_icon= 'cast', 
                default_index= 0,
            )

        if doctor_menu == "Patient Visiting Doctor":
            new_patient_visit()
       
        elif doctor_menu == "Patient Visit Management":
            patient_visit_management()

        elif doctor_menu == "Logout":
            logout()

    elif role == "admin":
        with st.sidebar:
            admin_menu = option_menu(
                menu_title="Main Menu",
                options= ["User Login Management", "Logout"],
                icons= ['house', 'cloud-sun'], 
                menu_icon= 'cast', 
                default_index= 0,
            )
        if admin_menu == "User Login Management":
            user_management()

        elif admin_menu == "Logout":
            logout()



def main():
   

    st.title("Out Patient Management System")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['userid'] = None
        st.session_state['show_signup'] = False



    # Toggle between login and signup
    if st.session_state['show_signup']:
        st.subheader("New User Sign Up")
        new_userid = st.text_input("New User ID")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["nurse", "doctor", "admin"])

        # Create two columns
        col1, col2, col3 = st.columns([2, 1, 1])
        # Sign UP Button (left side)
        with col1:
            if st.button("New User Sign Up"):
                if new_userid == '' or new_password =='':
                    st.error('enter valid credentials')
                    st.session_state['show_signup'] = False
                else:
                    if user_list.find(new_userid) is None:
                        flag = create_user(user_list, new_userid, new_password, new_role)
                        if flag:
                            write_user_records('user_records.csv', user_list)
                            st.success(f"User {new_userid} registered successfully")
                            st.session_state['show_signup'] = False
                        else:
                            st.error(f"Unable to create User {new_userid}")
                    else:
                        st.error("User ID already exists")
        # Go To Login Button (right side)
        with col3:
            if st.button("Go to Login"):
                st.session_state['show_signup'] = False
                st.rerun()
    else:
        if not st.session_state['logged_in']:
            st.subheader("Login")
            userid = st.text_input("User ID")
            password = st.text_input("Password", type="password")
            
            # Create two columns
            col1, col2, col3 = st.columns([2, 1, 1])
            # Login Button (left side)
            with col1:
                if st.button("Login"):
                    if userid and password:
                        if validate_user(user_list, userid, password):
                            user = user_list.find(userid)
                            st.session_state['logged_in'] = True
                            st.session_state['role'] = user.role
                            st.session_state['userid'] = user.userid

                            st.success(f"Successfully logged in as {user.role}")
                            st.rerun()
                        else:
                            st.error("Invalid User ID or Password")
                    else:
                        st.error("Please fill out all fields")

            # Sign Up Button  (right side)
            with col3:        
                if st.button("New User Sign Up"):
                    st.session_state['show_signup'] = True
                    st.rerun()
        else:
             userLoggedIn()
    

if __name__ == "__main__":
    main()
