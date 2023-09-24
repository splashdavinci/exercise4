import sqlite3

# 连接到数据库
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 创建Books表
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID TEXT PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT)''')

# 创建Users表
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID TEXT PRIMARY KEY,
                    Name TEXT,
                    Email TEXT)''')

# 创建Reservations表
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID TEXT PRIMARY KEY,
                    BookID TEXT,
                    UserID TEXT,
                    ReservationDate TEXT,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID))''')

# 添加新书到数据库
def add_book():
    book_id = input("Please enter the book ID：")
    title = input("Please enter the book title：")
    author = input("Please enter the author name：")
    isbn = input("Please enter the book ISBN：")
    status = input("Please enter the book status（Available或Reserved）：")
    
    cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                   (book_id, title, author, isbn, status))
    conn.commit()
    print("The book was successfully added to the database.")

# 根据BookID查找书籍详情
def find_book_by_id():
    book_id = input("请输入书籍ID：")
    
    # 使用JOIN关键字联结三个表进行查询
    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN,
                      Books.Status, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))
    result = cursor.fetchone()
    
    if result:
        book_id, title, author, isbn, status, user_name, user_email = result
        print(f"BookID：{book_id}")
        print(f"Book title：{title}")
        print(f"Author's name：{author}")
        print(f"Books ISBN：{isbn}")
        print(f"Book state：{status}")
        if user_name and user_email:
            print(f"Subscriber name：{user_name}")
            print(f"Booking user email：{user_email}")
        else:
            print("The book is not pre-ordered.")
    else:
        print("No books can be found.")

# 根据BookID、Title、UserID或ReservationID查找图书的预订状态
def find_reservation_status():
    text = input("Please enter BookID, Title, UserID, or ReservationID：")
    
    # 判断输入文本的前两个字母确定查询条件
    if text[:2] == "LB":
        # 根据BookID查询书籍详情和预订状态
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN,
                          Books.Status, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.BookID = ?''', (text,))
        result = cursor.fetchone()
        
        if result:
            book_id, title, author, isbn, status, user_name, user_email = result
            print(f"BookID：{book_id}")
            print(f"Book title：{title}")
            print(f"Author's name：{author}")
            print(f"Books ISBN：{isbn}")
            print(f"Book state：{status}")
            if user_name and user_email:
                print(f"Subscriber name：{user_name}")
                print(f"Booking user email：{user_email}")
            else:
                print("The book is not pre-ordered.")
        else:
            print("No books can be found.")
    elif text[:2] == "LU":
        # 根据UserID查询预订状态和对应的书籍详情
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN,
                          Books.Status, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Users.UserID = ?''', (text,))
        result = cursor.fetchone()
        
        if result:
            book_id, title, author, isbn, status, user_name, user_email = result
            print(f"BookID：{book_id}")
            print(f"Book title：{title}")
            print(f"Author's name：{author}")
            print(f"Books ISBN：{isbn}")
            print(f"Book state：{status}")
            print(f"Subscriber name：{user_name}")
            print(f"Booking user email：{user_email}")
        else:
            print("No booking record could be found.")
            
# 查找所有书籍
def find_all_books():
    cursor.execute("SELECT * FROM Books")
    results = cursor.fetchall()
    
    if results:
        for result in results:
            book_id, title, author, isbn, status = result
            print(f"BookID：{book_id}")
            print(f"Book title：{title}")
            print(f"Author's name：{author}")
            print(f"Books ISBN：{isbn}")
            print(f"Book state：{status}")
    else:
        print("There are no books in the database.")

# 修改书籍详情
def update_book_details():
    book_id = input("Please enter the ID of the book you want to modify：")
    new_title = input("Please enter a new book title：")
    new_author = input("Please enter a new author name：")
    new_isbn = input("Please enter the new book ISBN：")
    new_status = input("Please enter the new book status（Available或Reserved）：")
    
    # 更新Books表中的书籍详情
    cursor.execute('''UPDATE Books SET Title = ?, Author = ?, ISBN = ?, Status = ?
                      WHERE BookID = ?''', (new_title, new_author, new_isbn, new_status, book_id))
    conn.commit()
    
   
    if new_status == "Reserved":
        cursor.execute('''UPDATE Reservations SET ReservationDate = date('now')
                          WHERE BookID = ?''', (book_id,))
        conn.commit()
    
    print("Book details have been successfully updated.")

def delete_book():
    book_id = input("Enter the ID of the book you want to delete：")
    
   
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    

    cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    
    conn.commit()
    print("The book was successfully deleted from the database.")


while True:
    print("\nWelcome to the library Management system! Please select the following:")
    print("1. Add new book")
    print("2. Find book Details")
    print("3. Find booking status")
    print("4. Find all Books")
    print("5. Modify book details")
    print("6. Delete book")
    print("7. Quit")
    
    choice = input("Please enter the operation number：")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_by_id()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid operation number, please re-enter.")

# Close database connection
conn.close()