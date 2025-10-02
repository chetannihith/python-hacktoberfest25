import os

# File to store patient records
FILE_NAME = "patients.txt"

# Function to add a new patient
def add_patient():
    print("\n--- Add New Patient ---")
    patient_id = input("Enter Patient ID: ")
    name = input("Enter Patient Name: ")
    age = input("Enter Patient Age: ")
    gender = input("Enter Gender: ")
    disease = input("Enter Disease/Problem: ")
    
    with open(FILE_NAME, "a") as file:
        file.write(f"{patient_id},{name},{age},{gender},{disease}\n")
    
    print(f"\nPatient {name} added successfully!")

# Function to view all patients
def view_patients():
    print("\n--- All Patients ---")
    if not os.path.exists(FILE_NAME):
        print("No patient records found.")
        return
    
    with open(FILE_NAME, "r") as file:
        for line in file:
            patient_id, name, age, gender, disease = line.strip().split(",")
            print(f"ID: {patient_id}, Name: {name}, Age: {age}, Gender: {gender}, Disease: {disease}")

# Function to search a patient by ID
def search_patient():
    print("\n--- Search Patient ---")
    search_id = input("Enter Patient ID to search: ")
    
    if not os.path.exists(FILE_NAME):
        print("No patient records found.")
        return
    
    with open(FILE_NAME, "r") as file:
        for line in file:
            patient_id, name, age, gender, disease = line.strip().split(",")
            if patient_id == search_id:
                print(f"\nPatient Found!\nID: {patient_id}\nName: {name}\nAge: {age}\nGender: {gender}\nDisease: {disease}")
                return
    print("Patient not found.")

# Function to delete a patient record
def delete_patient():
    print("\n--- Delete Patient ---")
    delete_id = input("Enter Patient ID to delete: ")
    
    if not os.path.exists(FILE_NAME):
        print("No patient records found.")
        return
    
    lines = []
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
    
    with open(FILE_NAME, "w") as file:
        found = False
        for line in lines:
            patient_id, name, age, gender, disease = line.strip().split(",")
            if patient_id != delete_id:
                file.write(line)
            else:
                found = True
    
    if found:
        print(f"Patient ID {delete_id} deleted successfully.")
    else:
        print("Patient not found.")

# Main menu
def main_menu():
    while True:
        print("\n===== Hospital Management System =====")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Delete Patient")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            print("Exiting... Stay healthy!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
