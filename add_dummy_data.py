# add_dummy_data.py

import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    firebase_key_path = 'homedojo-dashboard-firebase-adminsdk-gxb7g-a46a4cb39b.json'
    
    if not os.path.exists(firebase_key_path):
        raise FileNotFoundError(f"Firebase admin SDK JSON file '{firebase_key_path}' not found.")
    
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def add_dummy_students(db):
    students_ref = db.collection('students')
    
    dummy_students = [
        {
            'Name': 'Elly',
            'Levels': [
                {'level_name': 'Lesson 1', 'new_letter': 'A', 'completed': True, 'accuracy': 90, 'mistakes': ['Confused D with B']},
                {'level_name': 'Lesson 2', 'new_letter': 'B', 'completed': True, 'accuracy': 85, 'mistakes': ['Forgot the letter C']},
                {'level_name': 'Lesson 3', 'new_letter': 'C', 'completed': False, 'accuracy': 0, 'mistakes': []},
                {'level_name': 'Lesson 4', 'new_letter': 'D', 'completed': False, 'accuracy': 0, 'mistakes': []},
                {'level_name': 'Lesson 5', 'new_letter': 'E', 'completed': False, 'accuracy': 0, 'mistakes': []}
            ]
        },
        {
            'Name': 'Bob',
            'Levels': [
                {'level_name': 'Lesson 1', 'new_letter': 'E', 'completed': True, 'accuracy': 75, 'mistakes': ['Confused E with F']},
                {'level_name': 'Lesson 2', 'new_letter': 'F', 'completed': True, 'accuracy': 80, 'mistakes': []},
                {'level_name': 'Lesson 3', 'new_letter': 'G', 'completed': False, 'accuracy': 0, 'mistakes': []},
                {'level_name': 'Lesson 4', 'new_letter': 'H', 'completed': False, 'accuracy': 0, 'mistakes': []},
                {'level_name': 'Lesson 5', 'new_letter': 'I', 'completed': False, 'accuracy': 0, 'mistakes': []}
            ]
        },
        {
            'Name': 'Yeasin',
            'Levels': [
                {'level_name': 'Lesson 1', 'new_letter': 'J', 'completed': True, 'accuracy': 95, 'mistakes': ['Confused J with K']},
                {'level_name': 'Lesson 2', 'new_letter': 'K', 'completed': True, 'accuracy': 90, 'mistakes': []},
                {'level_name': 'Lesson 3', 'new_letter': 'L', 'completed': True, 'accuracy': 85, 'mistakes': []},
                {'level_name': 'Lesson 4', 'new_letter': 'M', 'completed': True, 'accuracy': 80, 'mistakes': []},
                {'level_name': 'Lesson 5', 'new_letter': 'N', 'completed': True, 'accuracy': 88, 'mistakes': []}
            ]
        }
    ]
    
    for student in dummy_students:
        try:
            students_ref.add(student)
            print(f"Added student: {student['Name']}")
        except Exception as e:
            print(f"Error adding student {student['Name']}: {e}")

if __name__ == "__main__":
    db = initialize_firebase()
    add_dummy_students(db)
