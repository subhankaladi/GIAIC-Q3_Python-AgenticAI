import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import json
import os
import time

# File path for persistent storage
DATA_FILE = "secure_data.json"
ATTEMPTS_FILE = "attempts.json"

# Load or initialize storage
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_attempts():
    if os.path.exists(ATTEMPTS_FILE):
        with open(ATTEMPTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_attempts(attempts):
    with open(ATTEMPTS_FILE, "w") as f:
        json.dump(attempts, f)

# Initialize session state
if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
if "authorized" not in st.session_state:
    st.session_state.authorized = True

fernet = Fernet(st.session_state.fernet_key)
stored_data = load_data()
failed_attempts = load_attempts()

# Utility: Hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Insert new data
def insert_data(user_id, text, passkey):
    encrypted_text = fernet.encrypt(text.encode()).decode()
    hashed_passkey = hash_passkey(passkey)
    stored_data[user_id] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
    save_data(stored_data)
    st.success(f"Data stored securely for user: {user_id}")

# Retrieve data
def retrieve_data(user_id, passkey):
    if user_id not in stored_data:
        st.error("No data found for this user.")
        return

    if failed_attempts.get(user_id, 0) >= 3:
        st.session_state.authorized = False
        st.warning("Too many failed attempts. Redirecting to login.")
        time.sleep(1)
        st.rerun()
        return

    hashed_input = hash_passkey(passkey)
    if hashed_input == stored_data[user_id]["passkey"]:
        try:
            decrypted = fernet.decrypt(stored_data[user_id]["encrypted_text"].encode()).decode()
            st.success(f"Decrypted Data: {decrypted}")
            failed_attempts[user_id] = 0
            save_attempts(failed_attempts)
        except Exception as e:
            st.error("Error while decrypting. Possibly incorrect key.")
    else:
        failed_attempts[user_id] = failed_attempts.get(user_id, 0) + 1
        save_attempts(failed_attempts)
        attempts_left = 3 - failed_attempts[user_id]
        st.error(f"Incorrect passkey. Attempts left: {attempts_left}")

# Login Page
def login_page():
    st.title("🔐 Reauthorization Required")
    username = st.text_input("Enter Admin Username")
    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.authorized = True
            failed_attempts.clear()
            save_attempts(failed_attempts)
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid credentials.")

# Main App
def main():
    if not st.session_state.get("authorized", True):
        login_page()
        return

    st.sidebar.title("🔐 Secure Data Storage")
    menu = st.sidebar.radio("Navigate", ["Home", "Insert Data", "Retrieve Data", "Login"])

    if menu == "Home":
        st.title("Welcome to Secure Data Encryption System")
        st.write("Use the sidebar to insert or retrieve encrypted data.")

    elif menu == "Insert Data":
        st.title("📥 Store Your Secure Data")
        user_id = st.text_input("Enter User ID")
        data = st.text_area("Enter Data to Encrypt")
        passkey = st.text_input("Set a Passkey", type="password")
        if st.button("Store Data"):
            if user_id and data and passkey:
                insert_data(user_id, data, passkey)
            else:
                st.warning("All fields are required.")

    elif menu == "Retrieve Data":
        st.title("🔓 Retrieve Your Encrypted Data")
        user_id = st.text_input("Enter Your User ID")
        passkey = st.text_input("Enter Your Passkey", type="password")
        if st.button("Decrypt Data"):
            if user_id and passkey:
                retrieve_data(user_id, passkey)
            else:
                st.warning("Both User ID and Passkey are required.")

    elif menu == "Login":
        login_page()

if __name__ == "__main__":
    main()
