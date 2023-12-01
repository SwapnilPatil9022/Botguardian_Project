
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time as t
import webbrowser
import pickle
from cryptography.fernet import Fernet

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def pwd():
    def generate_key():
        return Fernet.generate_key()

    def encrypt_password(key, password):
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(encrypted_password, key):
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password)
        return decrypted_password.decode('utf-8')

    def save_password(account, username, password):
        key = generate_key()
        encrypted_password = encrypt_password(key, password)

        with open('passwords.pkl', 'ab') as file:
            pickle.dump((account, username, key, encrypted_password), file)

        print("Password saved successfully!")

    def get_password(account, username):
        with open('passwords.pkl', 'rb') as file:
            try:
                while True:
                    entry = pickle.load(file)
                    if entry[0] == account and entry[1] == username:
                        decrypted_password = decrypt_password(entry[3], entry[2])
                        return decrypted_password
            except EOFError:
                pass

        return None

    def main():
        print("1. Save Password")
        print("2. Get Password")

        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            account = input("Enter the account name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")

            save_password(account, username, password)

        elif choice == '2':
            account = input("Enter the account name: ")
            username = input("Enter the username: ")

            password = get_password(account, username)

            if password:
                print(f"Password for {account} ({username}): {password}")
            else:
                print("Password not found.")

        else:
            print("Invalid choice.")

    if __name__ == "__main__":
        main()


def reminder(message, time):
    while True:
        now = t.time()
        if now >= time:
            print(message)
            break
        t.sleep(1)


def joke():
    a = pyjokes.get_joke()
    talk(a)
    print(a)


def take_command():
    command = input("Enter your command: ")
    return command.lower()


def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


key = load_key()
fer = Fernet(key)


def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:",
                  str(fer.decrypt(passw.encode()).decode()))


def add():
    name = input('Account name: ')
    pwd = input('Password: ')

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + str(fer.encrypt(pwd.encode()).decode()) + "\n")


def bot_guard():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)
    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'joke' in command:
        joke()
    elif 'remind me to' in command:
        message = input("Enter the reminder: ")
        time = 60 * 5  # 5 minutes
        reminder(message, time)
    elif 'search' in command:
        query = command.replace("search", "").strip()
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
    elif 'start the password manager' in command:
        pwd()
    else:
        talk('Please say the command again.')


while True:
    bot_guard()
