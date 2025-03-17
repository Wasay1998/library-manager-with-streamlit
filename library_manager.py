import streamlit as st
import pandas as pd
import os

# Custom CSS for UI Improvements
custom_css = """
    <style>
        h1, h2, h3 {
            color: #000000;  /* Black for headings */
        }
        .stTextInput input, .stSelectbox select {
            background-color: white;
            color: #000000 !important;  
            border: 2px solid #000000;
        }
        .stButton>button {
            background-color: #444444;
            color: #FFFFFF;  
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #555555;
            transform: scale(1.05);
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #f5f004; 
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

if 'users' not in st.session_state:
    if os.path.exists("user_data.csv"):
        st.session_state.users = pd.read_csv("user_data.csv")
    else:
        st.session_state.users = pd.DataFrame(columns=["Username", "Email"])

if 'books' not in st.session_state:
    if os.path.exists("library_data.csv"):
        st.session_state.books = pd.read_csv("library_data.csv")
    else:
        st.session_state.books = pd.DataFrame(columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating", "Username"])


def save_users():
    st.session_state.users.to_csv("user_data.csv", index=False)

def save_books():
    st.session_state.books.to_csv("library_data.csv", index=False)

def register_user(username, email):
    if username in st.session_state.users['Username'].values:
        return False
    new_user = pd.DataFrame([[username, email]], columns=["Username", "Email"])
    st.session_state.users = pd.concat([st.session_state.users, new_user], ignore_index=True)
    save_users()
    return True

def login_user(username):
    st.session_state.logged_in_user = username

def logout_user():
    st.session_state.logged_in_user = None


def add_book(title, author, year, status, genre, language, rating, username):
    new_book = pd.DataFrame([[title, author, year, status, genre, language, rating, username]], 
                            columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating", "Username"])
    st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)
    save_books()

def remove_book(title, username):
    st.session_state.books = st.session_state.books[(st.session_state.books['Title'] != title) | (st.session_state.books['Username'] != username)]
    save_books()

def edit_book(title, new_title, new_author, new_year, new_status, new_genre, new_language, new_rating, username):
    st.session_state.books.loc[(st.session_state.books['Title'] == title) & (st.session_state.books['Username'] == username), 
                               ['Title', 'Author', 'Year', 'Status', 'Genre', 'Language', 'Rating']] = [new_title, new_author, new_year, new_status, new_genre, new_language, new_rating]
    save_books()

def search_books(query, search_by="Title", username=None):
    if username:
        books = st.session_state.books[st.session_state.books['Username'] == username]
    else:
        books = st.session_state.books

    if search_by == "Title":
        return books[books['Title'].str.contains(query, case=False)]
    elif search_by == "Author":
        return books[books['Author'].str.contains(query, case=False)]
    elif search_by == "Genre":
        return books[books['Genre'].str.contains(query, case=False)]
    elif search_by == "Language":
        return books[books['Language'].str.contains(query, case=False)]
    elif search_by == "Rating":
        return books[books['Rating'] == int(query)]

def display_stats(username):
    user_books = st.session_state.books[st.session_state.books['Username'] == username]
    total_books = len(user_books)
    read_books = len(user_books[user_books['Status'] == 'Read'])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"📚 Total Books: **{total_books}**")
    st.write(f"✅ Read Books: **{read_books}** ({read_percentage:.2f}%)")

# Streamlit UI
def library_app():
    st.title("📚 Personal Library Manager")

    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None

    # Sidebar with Image and Navigation
    with st.sidebar:
        st.image("https://img.freepik.com/premium-psd/books-with-graduation-success-icon-isolated-3d-render-illustrati_47987-7697.jpg?w=740", caption="Library Manager")
        if st.session_state.logged_in_user is None:
            menu = ["🔐 Login", "📝 Register", "ℹ️ About"]
            choice = st.selectbox("📌 Menu", menu)
        else:
            menu = ["🏠 Home", "➕ Add a Book", "✏️ Edit a Book", "❌ Remove a Book", "🔍 Search for a Book", "📊 Display Stats", "📤 Export Data", "ℹ️ About", "🚪 Logout"]
            choice = st.selectbox("📌 Menu", menu)

    if choice == "ℹ️ About":
        st.markdown("### ℹ️ About This App")
        st.write("""
        Welcome to the **Personal Library Manager**! This app is designed to help you manage your book collection efficiently. Here's what you can do:

        - **Add Books**: Add new books to your library with details like title, author, year, genre, language, and rating.
        - **Edit Books**: Update the details of existing books in your library.
        - **Remove Books**: Delete books from your library.
        - **Search Books**: Search for books by title, author, genre, language, or rating.
        - **View Stats**: Track your reading progress with statistics like total books and read books.
        - **Export Data**: Export your library data as a CSV file.

        This app is developed by **Abdul Wasay** to make book management simple and fun!
        """)

    elif st.session_state.logged_in_user is None:
        if choice == "🔐 Login":
            st.markdown("### 🔐 Login")
            if st.session_state.users.empty:
                st.warning("❌ No users registered yet. Please register first.")
            else:
                username = st.text_input("👤 Username")
                if st.button("Login"):
                    if username in st.session_state.users['Username'].values:
                        login_user(username)
                        st.success(f"✅ Logged in as **{username}**")
                    else:
                        st.error("❌ Username not found. Please register.")

        elif choice == "📝 Register":
            st.markdown("### 📝 Register")
            username = st.text_input("👤 Username")
            email = st.text_input("📧 Email")
            if st.button("Register"):
                if username and email:
                    if register_user(username, email):
                        st.success(f"✅ User **{username}** registered successfully!")
                    else:
                        st.error("❌ Username already exists.")
                else:
                    st.error("❌ Please provide all details to register.")

    else:
        if choice == "🏠 Home":
            st.markdown(f"### 📖 Welcome back, **{st.session_state.logged_in_user}**!")
            st.write("Manage your books effortlessly!")

            # Display all books in a table
            st.markdown("### 📚 All Books")
            if not st.session_state.books.empty:
                st.dataframe(st.session_state.books, use_container_width=True)
            else:
                st.write("No books added yet.")

        elif choice == "➕ Add a Book":
            st.markdown("### ➕ Add a New Book")
            title = st.text_input("📕 Book Title")
            author = st.text_input("✍️ Author")
            year = st.text_input("📅 Year")
            status = st.selectbox("📌 Status", ["Unread", "Read"])
            genre = st.text_input("📚 Genre (e.g. Fiction, Non-Fiction, Fantasy)")
            language = st.text_input("🌍 Language (e.g. English, Spanish)")
            rating = st.slider("⭐ Rating", min_value=1, max_value=5, step=1)

            if st.button("✅ Add Book"):
                if title and author and year and genre and language:
                    add_book(title, author, year, status, genre, language, rating, st.session_state.logged_in_user)
                    st.success(f"✅ Book **'{title}'** added successfully!")
                else:
                    st.error("❌ Please provide all details to add a book.")

        elif choice == "✏️ Edit a Book":
            st.markdown("### ✏️ Edit a Book")
            user_books = st.session_state.books[st.session_state.books['Username'] == st.session_state.logged_in_user]
            title_to_edit = st.selectbox("Select a Book to Edit", user_books['Title'].values)
            book_to_edit = user_books[user_books['Title'] == title_to_edit].iloc[0]

            new_title = st.text_input("📕 New Book Title", value=book_to_edit['Title'])
            new_author = st.text_input("✍️ New Author", value=book_to_edit['Author'])
            new_year = st.text_input("📅 New Year", value=book_to_edit['Year'])
            new_status = st.selectbox("📌 New Status", ["Unread", "Read"], index=0 if book_to_edit['Status'] == "Unread" else 1)
            new_genre = st.text_input("📚 New Genre", value=book_to_edit['Genre'])
            new_language = st.text_input("🌍 New Language", value=book_to_edit['Language'])
            new_rating = st.slider("⭐ New Rating", min_value=1, max_value=5, step=1, value=book_to_edit['Rating'])

            if st.button("✅ Save Changes"):
                edit_book(title_to_edit, new_title, new_author, new_year, new_status, new_genre, new_language, new_rating, st.session_state.logged_in_user)
                st.success(f"✅ Book **'{title_to_edit}'** updated successfully!")

        elif choice == "❌ Remove a Book":
            st.markdown("### ❌ Remove a Book")
            user_books = st.session_state.books[st.session_state.books['Username'] == st.session_state.logged_in_user]
            title = st.selectbox("Select a Book to Remove", user_books['Title'].values)

            if st.button("🗑 Remove Book"):
                remove_book(title, st.session_state.logged_in_user)
                st.success(f"✅ Book **'{title}'** removed successfully!")

        elif choice == "🔍 Search for a Book":
            st.markdown("### 🔍 Search for a Book")
            search_by = st.selectbox("Search By", ["Title", "Author", "Genre", "Language", "Rating"])
            query = st.text_input(f"Enter {search_by} to Search")

            if query:
                search_result = search_books(query, search_by, st.session_state.logged_in_user)
                if not search_result.empty:
                    st.dataframe(search_result, use_container_width=True)
                else:
                    st.write("❌ No books found matching your search.")

        elif choice == "📊 Display Stats":
            st.markdown("### 📊 Library Stats")
            display_stats(st.session_state.logged_in_user)

        elif choice == "📤 Export Data":
            st.markdown("### 📤 Export Library Data")
            if st.button("📥 Download CSV"):
                user_books = st.session_state.books[st.session_state.books['Username'] == st.session_state.logged_in_user]
                user_books.to_csv("library_export.csv", index=False)
                st.success("✅ Library data exported successfully!")
                with open("library_export.csv", "rb") as file:
                    st.download_button(label="⬇️ Download", data=file, file_name="library_export.csv", mime="text/csv")

        elif choice == "🚪 Logout":
            logout_user()
            st.success("👋 Logged out successfully!")
            st.rerun()  

    
    st.markdown("---")
    st.markdown('<p class="footer">Developed by <strong>Abdul Wasay</strong></p>', unsafe_allow_html=True)

if __name__ == "__main__":
    with st.container():
        library_app()