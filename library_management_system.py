import datetime
import sys

# Data storage (can be changed to file-based easily)
books = {}  # key: book_id, value: {'title': ..., 'author': ..., 'issued_to': ..., 'issue_date': ...}
students = {}  # key: student_id, value: {'name': ..., 'issued_books': set()}

FINE_PER_DAY = 5  # Amount of fine per day after due date
ISSUE_DAYS = 14   # Number of days a book can be issued

def add_book():
    book_id = input("Enter Book ID: ").strip()
    if book_id in books:
        print("Book ID already exists.")
        return
    title = input("Enter Book Title: ").strip()
    author = input("Enter Book Author: ").strip()
    books[book_id] = {'title': title, 'author': author, 'issued_to': None, 'issue_date': None}
    print("Book added successfully.")

def remove_book():
    book_id = input("Enter Book ID to remove: ").strip()
    if book_id not in books:
        print("Book does not exist.")
        return
    if books[book_id]['issued_to']:
        print("Book is currently issued to a student. Cannot remove.")
        return
    del books[book_id]
    print("Book removed successfully.")

def add_student():
    student_id = input("Enter Student ID: ").strip()
    if student_id in students:
        print("Student ID already exists.")
        return
    name = input("Enter Student Name: ").strip()
    students[student_id] = {'name': name, 'issued_books': set()}
    print("Student added successfully.")

def issue_book():
    book_id = input("Enter Book ID to issue: ").strip()
    if book_id not in books:
        print("Book does not exist.")
        return
    if books[book_id]['issued_to']:
        print("Book is already issued.")
        return
    student_id = input("Enter Student ID: ").strip()
    if student_id not in students:
        print("Student does not exist.")
        return
    today = datetime.date.today()
    books[book_id]['issued_to'] = student_id
    books[book_id]['issue_date'] = today
    students[student_id]['issued_books'].add(book_id)
    print(f"Book issued to {students[student_id]['name']} on {today}.")

def return_book():
    book_id = input("Enter Book ID to return: ").strip()
    if book_id not in books:
        print("Book does not exist.")
        return
    if not books[book_id]['issued_to']:
        print("Book is not issued.")
        return
    student_id = books[book_id]['issued_to']
    issued_date = books[book_id]['issue_date']
    today = datetime.date.today()
    delta_days = (today - issued_date).days
    fine = 0
    if delta_days > ISSUE_DAYS:
        fine = (delta_days - ISSUE_DAYS) * FINE_PER_DAY
    # Update records
    students[student_id]['issued_books'].remove(book_id)
    books[book_id]['issued_to'] = None
    books[book_id]['issue_date'] = None
    print(f"Book returned by {students[student_id]['name']} on {today}.")
    if fine > 0:
        print(f"Fine to be paid: Rs.{fine}")
    else:
        print("No fine.")

def list_books():
    if not books:
        print("No books in the library.")
        return
    print("Books in library:")
    for book_id, info in books.items():
        status = f"Issued to {info['issued_to']}" if info['issued_to'] else "Available"
        print(f"ID: {book_id}, Title: {info['title']}, Author: {info['author']}, Status: {status}")

def list_students():
    if not students:
        print("No students registered.")
        return
    print("Students:")
    for student_id, info in students.items():
        print(f"ID: {student_id}, Name: {info['name']}, Books Issued: {list(info['issued_books'])}")

def main_menu():
    menu = """
    ===== Library Book Management System =====
    1. Add Book
    2. Remove Book
    3. Add Student
    4. Issue Book
    5. Return Book
    6. List All Books
    7. List All Students
    8. Exit
    =========================================
    """
    while True:
        print(menu)
        choice = input("Enter your choice (1-8): ").strip()
        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            add_student()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            list_books()
        elif choice == '7':
            list_students()
        elif choice == '8':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
