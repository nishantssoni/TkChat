import tkinter as tk
from tkinter import scrolledtext
from chat2 import push_message_to_user, read_messages_from_user, get_user_list

class ChatAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")

        # Dictionary to store user-specific text areas
        self.text_areas = {}

        # Listbox to display user list
        self.user_listbox = tk.Listbox(self.root)
        self.user_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.user_listbox.bind('<Double-Button-1>', self.open_chat)

        # Pre-populating user list (demo)
        self.populate_user_list()

    def populate_user_list(self):
        # For demo purposes, let's populate with some users
        users = get_user_list()
        for user in users:
            self.user_listbox.insert(tk.END, user)

    def open_chat(self, event):
        selected_user_index = self.user_listbox.curselection()
        if selected_user_index:
            selected_user = self.user_listbox.get(selected_user_index)
            self.open_chat_window(selected_user)

    def open_chat_window(self, user):
        chat_window = tk.Toplevel(self.root)
        chat_window.title(f"Chat with {user}")

        # Text area for chat messages
        text_area = scrolledtext.ScrolledText(chat_window, width=40, height=10)
        text_area.pack(padx=10, pady=10)
        self.text_areas[user] = text_area


        # Entry field for typing messages
        entry_field = tk.Entry(chat_window, width=30)
        entry_field.pack(padx=10, pady=5)

        # Button to send messages
        send_button = tk.Button(chat_window, text="Send", command=lambda: self.send_message(user, entry_field,text_area))
        send_button.pack(padx=5, pady=5)

        # Bind Enter key to send message
        chat_window.bind('<Return>', lambda event: self.send_message(user, entry_field,text_area))

        self.display_message(user,text_area)

    def send_message(self, user, entry_field,text_area):
        message = entry_field.get()
        if message:
            push_message_to_user(user,message)
            self.display_message(user,text_area)
            entry_field.delete(0, 'end')

    def display_message(self, user, text_area):
        self.clear_text_area(text_area)
        if user in self.text_areas:
            self.text_areas[user].configure(state='normal')
            for i in read_messages_from_user(user):
                self.text_areas[user].insert('end', i + '\n')
            self.text_areas[user].configure(state='disabled')
    
    def clear_text_area(self, text_area):
        text_area.configure(state='normal')
        text_area.delete('1.0', tk.END)
        text_area.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatAppGUI(root)
    root.mainloop()
