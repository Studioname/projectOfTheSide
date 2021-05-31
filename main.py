from tkinter import *
import smtplib
from tkinter import messagebox
import json


def add_contact():
    contact = email_entry.get()
    if "@" not in contact:
        messagebox.showwarning(title="Error",message="Please input a valid email address")
    else:
        try:
            with open("data.json") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                address_list = [contact]
                json.dump(address_list,file)
                email_entry.delete(0, "end")
        else:
            data.append(contact)
            with open("data.json", "w") as file:
                json.dump(data, file)
            email_entry.delete(0, "end")


def remove_contact():
    contact = email_entry.get()
    if "@" not in contact:
        messagebox.showwarning(title="Error",message="Please input a valid email address")
    else:
        try:
            with open("data.json") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showwarning(title="Error", message="The address list is empty")
        else:

            for entry in data:
                if entry == contact:
                    data.remove(entry)
                    with open("data.json", "w") as file:
                        json.dump(data, file)
                    email_entry.delete(0, END)
                else:
                    messagebox.showwarning(title="Error", message="That entry is not in the address list")


def send():
    smtp = smtp_entry.get()
    connection = smtplib.SMTP(smtp)
    connection.starttls()
    email = sender_email_entry.get()
    password = sender_password_entry.get()
    email_subject = email_header_entry.get()
    email_main = email_body.get("1.0", "end-1c")
    if len(email) == 0 or len(password) == 0 or len(smtp) == 0:
        messagebox.showwarning(title="Error", message="Make sure your SMTP address and your login details are correct")
    else:
        connection.login(user=email,password=password)
        with open("data.json") as file:
            data = json.load(file)
        for address in data:
            connection.sendmail(from_addr=email, to_addrs=address,msg=f"Subject: {email_subject}\n\n{email_main}")
        messagebox.showinfo(title="Success!", message="Emails sent successfully.")


window = Tk()

window.config(padx=50,pady=50)
window.title("Mailing list manager")

#0,0

email_entry_label = Label(text="Enter an e-mail address",)
email_entry_label.grid(column=0,row=0, sticky="W")

#1,0/1

email_entry = Entry(width=50)
email_entry.grid(column=0,row=1,columnspan=2, sticky="W")

#1,2

add_contact_button = Button(text="Add contact", width=25, command=add_contact)
add_contact_button.grid(column=2,row=1)

#1,3

remove_contact_button = Button(text="Remove contact", width=25, command=remove_contact)
remove_contact_button.grid(column=3,row=1)

#2,0

email_header_label = Label(text="Email header")
email_header_label.grid(column=0,row=2, sticky="W")

#3,0/2

email_header_entry = Entry(width=50)
email_header_entry.grid(column=0,row=3,columnspan=2, sticky="W")

#3,0

email_body_label = Label(text="Email body",)
email_body_label.grid(column=0,row=4,sticky="W")

#3,0/4

email_body = Text(width=95,height=20)
email_body.grid(column=0,row=5,columnspan=4,sticky="W")

#4,4

text_scrollbar = Scrollbar(command=email_body.yview)
email_body.config(yscrollcommand = text_scrollbar.set)
text_scrollbar.grid(column=5,row=5,sticky="NS")

#1,6

smtp_entry_label = Label(text="SMTP address")
smtp_entry_label.grid(column=1,row=6)

#2,6

sender_email_label = Label(text="Enter your email")
sender_email_label.grid(column=2,row=6)

#3,6

sender_password_label = Label(text="Enter your password")
sender_password_label.grid(column=3,row=6,)

#0,7

send_button = Button(text="Send", width=25,command=send)
send_button.grid(column=0,row=7,sticky="W")

#1,7

smtp_entry = Entry(width=25)
smtp_entry.grid(column=1,row=7)

#2,7

sender_email_entry = Entry(width=25)
sender_email_entry.grid(column=2,row=7,)

#3,7

sender_password_entry = Entry(width=25,show="*")
sender_password_entry.grid(column=3,row=7,)


window.mainloop()