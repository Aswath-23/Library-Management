import datetime

users = {
    'admin@library.com': {'role': 'admin', 'password': 'admin123', 'name': 'Admin1', 'deposit': 0, 'fines': []},
    'student@domain.com': {'role': 'borrower', 'password': 'student123', 'name': 'Student1', 'deposit': 1500, 'borrowed_books': [], 'fines': []},
}

books = {
    'ISBN001': {'title': 'Python Basics', 'quantity': 3, 'cost': 500, 'borrowed_by': []},
    'ISBN002': {'title': 'Data Structures', 'quantity': 2, 'cost': 600, 'borrowed_by': []},
    'ISBN003': {'title': 'AI Introduction', 'quantity': 5, 'cost': 750, 'borrowed_by': []},
}


def authenticate():
    email = input("Enter Email ID: ")
    password = input("Enter Password: ")
    user = users.get(email)
    if user and user['password'] == password:
        print(f"\nWelcome {user['name']}! Role: {user['role'].capitalize()}")
        return email, user['role']
    else:
        print("Invalid credentials.")
        return None, None


def admin_menu(email):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Book")
        print("2. Modify Book Quantity")
        print("3. Delete Book")
        print("4. View Books Sorted")
        print("5. Search Book")
        print("6. Add User")
        print("7. Reports")
        print("8. Logout")

        choice = input("Choose: ")
        if choice == '1':
            isbn = input("Enter ISBN: ")
            title = input("Enter Title: ")
            qty = int(input("Enter Quantity: "))
            cost = int(input("Enter Cost: "))
            books[isbn] = {'title': title, 'quantity': qty, 'cost': cost, 'borrowed_by': []}
            print("Book added successfully.")
        elif choice == '2':
            isbn = input("Enter ISBN: ")
            if isbn in books:
                qty = int(input("New Quantity: "))
                books[isbn]['quantity'] = qty
                print("Updated.")
            else:
                print("Book not found.")
        elif choice == '3':
            isbn = input("Enter ISBN to delete: ")
            if isbn in books:
                del books[isbn]
                print("Deleted.")
            else:
                print("Not found.")
        elif choice == '4':
            sort_type = input("Sort by (title/quantity): ").lower()
            sorted_books = sorted(books.items(), key=lambda x: x[1]['title'] if sort_type == 'title' else x[1]['quantity'])
            for isbn, book in sorted_books:
                print(f"{isbn} | {book['title']} | Qty: {book['quantity']}")
        elif choice == '5':
            key = input("Search by name or ISBN: ")
            for isbn, book in books.items():
                if key.lower() in book['title'].lower() or key == isbn:
                    print(f"{isbn}: {book['title']} | Qty: {book['quantity']}")
        elif choice == '6':
            role = input("Enter role (admin/borrower): ")
            email = input("Enter email: ")
            pwd = input("Enter password: ")
            name = input("Enter name: ")
            if role == 'borrower':
                users[email] = {'role': role, 'password': pwd, 'name': name, 'deposit': 1500, 'borrowed_books': [], 'fines': []}
            else:
                users[email] = {'role': role, 'password': pwd, 'name': name, 'deposit': 0, 'fines': []}
            print("User added.")
        elif choice == '7':
            print("\n--- Reports ---")
            print("1. Low stock books")
            print("2. Never borrowed books")
            print("3. Most borrowed books")
            print("4. Overdue books")
            print("5. Book status by ISBN")
            report = input("Choose: ")
            if report == '1':
                for isbn, book in books.items():
                    if book['quantity'] <= 2:
                        print(f"{isbn}: {book['title']} | Qty: {book['quantity']}")
            elif report == '2':
                for isbn, book in books.items():
                    if not book['borrowed_by']:
                        print(f"{isbn}: {book['title']}")
            elif report == '3':
                borrowed_stats = sorted(books.items(), key=lambda x: len(x[1]['borrowed_by']), reverse=True)
                for isbn, book in borrowed_stats:
                    if len(book['borrowed_by']) > 0:
                        print(f"{isbn}: {book['title']} | Times Borrowed: {len(book['borrowed_by'])}")
            elif report == '4':
                today = datetime.date.today()
                for email, user in users.items():
                    if user['role'] == 'borrower':
                        for b in user['borrowed_books']:
                            if b['due_date'] < today:
                                print(f"{email}: {b['isbn']} | Due: {b['due_date']}")
            elif report == '5':
                isbn = input("Enter ISBN: ")
                if isbn in books:
                    for email, user in users.items():
                        for b in user['borrowed_books']:
                            if b['isbn'] == isbn:
                                print(f"Borrowed by: {email}, Due Date: {b['due_date']}")
        elif choice == '8':
            break


def borrower_menu(email):
    while True:
        user = users[email]
        print("\n--- Borrower Menu ---")
        print("1. View Available Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Pay Fine")
        print("5. View Borrowed Books")
        print("6. Add/Update Deposit")
        print("7. Logout")

        choice = input("Choose: ")
        if choice == '1':
            for isbn, book in books.items():
                print(f"{isbn}: {book['title']} | Qty: {book['quantity']}")
        elif choice == '2':
            if len(user['borrowed_books']) >= 3:
                print("Max 3 books can be borrowed.")
                continue
            if user['deposit'] < 500:
                print("Insufficient deposit.")
                continue
            isbn = input("Enter ISBN: ")
            if isbn in books and books[isbn]['quantity'] > 0:
                for b in user['borrowed_books']:
                    if b['isbn'] == isbn:
                        print("Already borrowed this book.")
                        break
                else:
                    today = datetime.date.today()
                    due_date = today + datetime.timedelta(days=15)
                    user['borrowed_books'].append({'isbn': isbn, 'borrowed_on': today, 'due_date': due_date})
                    books[isbn]['quantity'] -= 1
                    books[isbn]['borrowed_by'].append(email)
                    print("Book borrowed successfully.")
            else:
                print("Book not available.")
        elif choice == '3':
            isbn = input("Enter ISBN to return: ")
            for b in user['borrowed_books']:
                if b['isbn'] == isbn:
                    return_date_str = input("Enter return date (DD/MM/YYYY): ")
                    return_date = datetime.datetime.strptime(return_date_str, "%d/%m/%Y").date()
                    delay = (return_date - b['due_date']).days
                    fine = 0
                    if delay > 0:
                        fine = min(2 * delay + (delay // 10) * 5, books[isbn]['cost'] * 0.8)
                        user['deposit'] -= fine
                        user['fines'].append({'isbn': isbn, 'reason': 'Late return', 'amount': fine})
                        print(f"Late by {delay} days. Fine: Rs.{fine}")
                    user['borrowed_books'].remove(b)
                    books[isbn]['quantity'] += 1
                    break
            else:
                print("Book not found in your account.")
        elif choice == '4':
            if user['fines']:
                for fine in user['fines']:
                    print(f"ISBN: {fine['isbn']} | Reason: {fine['reason']} | Amount: Rs.{fine['amount']}")
                pay = input("Pay fine using deposit? (y/n): ")
                if pay.lower() == 'y':
                    user['fines'].clear()
                    print("Fine cleared.")
                else:
                    print("Fine payment cancelled. Fines remain unpaid.")
            else:
                print("No fines.")
        elif choice == '5':
            for b in user['borrowed_books']:
                print(f"ISBN: {b['isbn']} | Due Date: {b['due_date']}")
        elif choice == '6':
            print(f"Current deposit: Rs.{user['deposit']}")
            amount = float(input("Enter amount to add to deposit: "))
            if amount > 0:
                user['deposit'] += amount
                print(f"Deposit updated. New balance: Rs.{user['deposit']}")
            else:
                print("Please enter a positive amount.")
        elif choice == '7':
            break


def main():
    while True:
        print("\n==== Library Management System ====")
        email, role = authenticate()
        if role == 'admin':
            admin_menu(email)
        elif role == 'borrower':
            borrower_menu(email)


if __name__ == "__main__":
    main()
