#!/usr/bin/env python3
"""
Bulk upload script for remaining HR employees to FileNet repository.
This script will upload documents for COG003, COG004, and COG005.
"""

import os
import subprocess
import json

# Employee folders to process
EMPLOYEES = [
    "COG003_Antoine El Haddad",
    "COG004_Louis Faure",
    "COG005_Alice Bernard"
]

# Document categories
CATEGORIES = [
    "01_Recruitment",
    "02_Employment_Contract",
    "03_Personal_Administration",
    "04_Payroll",
    "05_Performance",
    "06_Training",
    "07_Disciplinary",
    "08_Exit"
]

BASE_SOURCE_PATH = "HR"
BASE_TARGET_PATH = "/BOB_LAB/Santander"

def create_folders_for_employee(employee_name):
    """Create folder structure for an employee"""
    print(f"\nCreating folders for {employee_name}...")
    
    # Create employee folder (already created for COG003)
    if employee_name != "COG003_Antoine El Haddad":
        cmd = f'roo create-folder "{employee_name}" "{BASE_TARGET_PATH}"'
        print(f"  Creating: {BASE_TARGET_PATH}/{employee_name}")
        # Would execute: subprocess.run(cmd, shell=True)
    
    # Create category subfolders
    for category in CATEGORIES:
        folder_path = f"{BASE_TARGET_PATH}/{employee_name}"
        print(f"  Creating: {folder_path}/{category}")
        # Would execute folder creation command

def upload_documents_for_employee(employee_name):
    """Upload all documents for an employee"""
    print(f"\nUploading documents for {employee_name}...")
    
    source_base = os.path.join(BASE_SOURCE_PATH, employee_name)
    
    for category in CATEGORIES:
        category_path = os.path.join(source_base, category)
        if not os.path.exists(category_path):
            continue
            
        # Get all .txt files in category
        files = [f for f in os.listdir(category_path) if f.endswith('.txt')]
        
        for filename in files:
            source_file = os.path.join(category_path, filename)
            target_folder = f"{BASE_TARGET_PATH}/{employee_name}/{category}"
            
            print(f"  Uploading: {filename} -> {target_folder}")
            # Would execute document upload command

def main():
    print("=" * 60)
    print("Bulk Upload Script for HR Employees")
    print("=" * 60)
    
    for employee in EMPLOYEES:
        create_folders_for_employee(employee)
        upload_documents_for_employee(employee)
    
    print("\n" + "=" * 60)
    print("Upload process would be complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

# Made with Bob
