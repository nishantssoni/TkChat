import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase with your service account key
cred = credentials.Certificate("your_json_file.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'your database url'
})


# Function to push message to a specific user's section
def push_message_to_user(user_id, message):
    ref = db.reference(f'/users/{user_id}/messages')
    ref.push(message)

# Function to read messages from a specific user's section
def read_messages_from_user(user_id):
    ref = db.reference(f'/users/{user_id}/messages')
    messages = ref.get()
    temp = list()
    if messages:
        for key, value in messages.items():
            temp.append(value)
    
    return temp


# Function to get the list of users
def get_user_list():
    ref = db.reference('/users')
    user_ids = ref.get()
    if user_ids:
        return user_ids.keys()
    else:
        return []

# Function to delete a user
def delete_user(user_id):
    ref = db.reference(f'/users/{user_id}')
    ref.delete()
    print(f"User with ID '{user_id}' deleted successfully.")


if __name__ == "__main__":
    users =get_user_list()

    print(" current user is:: ")

    for i, v in enumerate(users):
        print(i+1, v)

    
    while True:
        action = input("Enter 'add' for new chatroom or 'del' for deleting chatroom: ")
        if action == "add":
            while True:
                user_id = input("Enter new user ID: ")
                if user_id not in users:
                    print("chatroom created")
                    break
                else:
                    print("chatroom with this name is already existed")
            
            now = datetime.now()
            message = 'created in :: ' + str(now.strftime("%Y-%m-%d %H:%M:%S"))
            push_message_to_user(user_id, message)
        
        elif action == "del":
            while True:
                user_id = input("Enter existed user ID: ")
                if user_id in users:
                    print("User deleted")
                    break
                else:
                    print("chatroom with this name didnt exist")

            delete_user(user_id)
        else:
            print("Invalid action. Please enter 'push' or 'read'.")
