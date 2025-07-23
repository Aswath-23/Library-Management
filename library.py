import datetime

books = {
    "ISBN001": {"title": "Python Programming", "author": "Aswath", "quantity": 5, "price": 400},
    "ISBN002": {"title": "Data Structures", "author": "warner", "quantity": 3, "price": 500},
    "ISBN003": {"title": "Harry Potter", "author": "Miller", "quantity": 2, "price": 350}
}

users = {
    "admin@library.com": {"password": "admin123", "role": "admin"},
    "user@library.com": {"password": "user123", "role": "borrower", "deposit": 1500, "borrowed_books": []}
}

transactions = []
fines = {}

def authenticate():
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    if email in users and users[email]["password"] == password:
        return users[email]["role"], email
    return None, None

def admin_menu(email):
    while True:
        print("\n=========== Admin Menu ===========")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. View Reports")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            isbn = input("Enter ISBN: ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))

            books[isbn] = {"title": title, "author": author, "quantity": quantity, "price": price}
            print("Book Added Successfully!")

        elif choice == "2":
            print("\nAll Books")
            for isbn, details in books.items():
                print(f"ISBN: {isbn}, Title: {details['title']}, Available: {details['quantity']}")

        elif choice == "3":
            search_item = input("Enter title or ISBN to search: ")
            found = False
            for isbn, details in books.items():
                if search_item.lower() in details['title'].lower() or search_item == isbn:
                    print(f"ISBN: {isbn}, Title: {details['title']}, Author: {details['author']}, Available: {details['quantity']}")
                    found = True
            if not found:
                print("No books found.")

        elif choice == "4":
            print("\n========= Reports Menu =========")
            print("1. Books with low quantity (need refill)")
            print("2. Books never borrowed")
            print("3. Most popular books")
            print("4. Students with overdue books")
            print("5. Book status by ISBN")
            print("6. Back to main menu")
        
            report_choice = input("Enter report choice: ")
        
            if report_choice == "1":
                print("\nBooks needing refill:")
                threshold = int(input("Enter minimum quantity threshold : "))
                for isbn, details in books.items():
                    if details['quantity'] <= threshold:
                        print(f"{details['title']} (ISBN: {isbn}) - Only {details['quantity']} left")
        
            elif report_choice == "2":
                print("\nBooks never borrowed:")
                borrowed_isbns = {t['isbn'] for t in transactions}
                for isbn, details in books.items():
                    if isbn not in borrowed_isbns:
                        print(f"{details['title']} (ISBN: {isbn}) - Never borrowed")
        
            elif report_choice == "3":
                print("\nMost popular books:")
                borrow_counts = {}
                for t in transactions:
                    borrow_counts[t['isbn']] = borrow_counts.get(t['isbn'], 0) + 1
            
                sorted_books = sorted(borrow_counts.items(), key=lambda x: x[1], reverse=True)
                for isbn, count in sorted_books[:5]:  
                    print(f"{books[isbn]['title']} (ISBN: {isbn}) - Borrowed {count} times")
        
            elif report_choice == "4":
                print("\nStudents with overdue books:")
                today = datetime.date.today()
                overdue_books = {}
        
                for t in transactions:
                    if not t['returned'] and t['due_date'] < today:
                        if t['email'] not in overdue_books:
                            overdue_books[t['email']] = []
                        overdue_books[t['email']].append(t)
        
                for email, books_list in overdue_books.items():
                    print(f"\nStudent: {email}")
                    for book in books_list:
                        days_overdue = (today - book['due_date']).days
                        print(f"- {books[book['isbn']]['title']} (Due: {book['due_date']}, {days_overdue} days overdue)")
        
            elif report_choice == "5":
                isbn = input("Enter ISBN to check status: ")
                if isbn in books:
                    print(f"\nBook: {books[isbn]['title']}")
                    print(f"Available Quantity: {books[isbn]['quantity']}")
            
                    borrowed = False
                    for t in transactions:
                        if t['isbn'] == isbn and not t['returned']:
                            borrowed = True
                            days_left = (t['due_date'] - datetime.date.today()).days
                            print(f"Borrowed by: {t['email']}")
                            print(f"Due Date: {t['due_date']} ({days_left} days remaining)")
                            break
            
                    if not borrowed:
                        print("Status: Available on shelf")
                else:
                    print("Book not found!")
        
            elif report_choice == "6":
                continue
        
        elif choice == "5":
            break

def borrower_menu(email):
    while True:
        print("\n========== Borrower Menu ===========")
        print("1. View Available Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View Borrowing History")
        print("5. Logout")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            print("\nAvailable Books:")
            for isbn, details in books.items():
                if details['quantity'] > 0:
                    print(f"ISBN: {isbn}, Title: {details['title']}, Author: {details['author']}")
                    
        elif choice == "2":
            if len(users[email]["borrowed_books"]) >= 3:
                print("You can't borrow more than 3 books.")
                continue
                
            isbn = input("Enter ISBN of book to borrow: ")
            if isbn in books and books[isbn]['quantity'] > 0:
                if isbn in users[email]["borrowed_books"]:
                    print("You've already borrowed this book.")
                else:
                    if users[email]["deposit"] >= 500:
                        books[isbn]['quantity'] -= 1
                        users[email]["borrowed_books"].append(isbn)
                        due_date = datetime.date.today() + datetime.timedelta(days=15)
                        transactions.append({
                            "email": email,
                            "isbn": isbn,
                            "borrow_date": datetime.date.today(),
                            "due_date": due_date,
                            "returned": False
                        })
                        print(f"Book borrowed successfully! Due date: {due_date}")
                    else:
                        print("Minimum security deposit of 500 required.")
            else:
                print("Book not available.")
                
        elif choice == "3":
            isbn = input("Enter ISBN of book to return: ")
            if isbn in users[email]["borrowed_books"]:
                books[isbn]['quantity'] += 1
                users[email]["borrowed_books"].remove(isbn)
                
                for t in transactions:
                    if t["email"] == email and t["isbn"] == isbn and not t["returned"]:
                        t["returned"] = True
                        t["return_date"] = datetime.date.today()
                        
                
                        if t["return_date"] > t["due_date"]:
                            days_late = (t["return_date"] - t["due_date"]).days
                            fine = days_late * 2  
                            fines[email] = fines.get(email, 0) + fine
                            print(f"Book returned late! Fine: Rs.{fine}")
                
                print("Book returned successfully!")
            else:
                print("You haven't borrowed this book.")
                
        elif choice == "4":
            print("\nYour Borrowing History:")
            for t in transactions:
                if t["email"] == email:
                    status = "Returned" if t["returned"] else "Borrowed"
                    print(f"Book: {books[t['isbn']]['title']}, Borrowed on: {t['borrow_date']}, Status: {status}")
                    
        elif choice == "5":
            break

def main():
    print("=========== Welcome to Library Management System =============")
    
    while True:
        role, email = authenticate()
        if role == "admin":
            admin_menu(email)
        elif role == "borrower":
            borrower_menu(email)
        else:
            print("Invalid credentials. Try again.")
            
        cont = input("Do you want to continue (y/n)? ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
