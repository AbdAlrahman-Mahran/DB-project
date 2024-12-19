from tkinter import messagebox

import mysql.connector
import customtkinter as ctk

db = mysql.connector.connect(
    host="localhost",
    user="yami",
    passwd="yami",
    database="hotel"
)


cursor = db.cursor()

app = ctk.CTk()
def popup(text):
    messagebox.showinfo(message=text)

def list_available_rooms_1():
    cursor.execute("SELECT Room_number, Room_Type, Rate,cost FROM rooms WHERE available=1")
    rooms = cursor.fetchall()
    return rooms


def check_availability_1(room_number):
    if room_number is None:
        return
    cursor.execute("SELECT available FROM rooms WHERE Room_number=%s", (room_number,))
    result = cursor.fetchone()
    if result is None:
        return 0
    return result[0]


def billing_1(guest):
    if guest is None:
        return
    cursor.execute("SELECT Guest_ID FROM guests WHERE Name=%s", (guest,))
    guest_id = cursor.fetchone()
    if guest_id is None:
        popup("Guest not found")
        return
    guest_id= guest_id[0]
    cursor.execute("SELECT Bill FROM reservations WHERE Guest_ID=%s", (guest_id,))
    bills = cursor.fetchall()
    return bills

def room_inquiry_1(guest):
    if guest is None:
        return
    cursor.execute("SELECT Room_number FROM reservations join rooms on rooms.Room_ID = reservations.Room_ID WHERE Guest_ID=%s", (guest,))
    room_numbers = cursor.fetchall()
    return room_numbers


def add_room_1(room_number,room_type,room_rate,cost):
    if room_number is None or room_type is None or room_rate is None:
        return
    cursor.execute("SELECT Room_number FROM rooms")
    rooms = cursor.fetchall()

    for room in rooms:
        if room[0] == room_number:
            popup("Room number already exists")
            return

    cursor.execute("Insert Into rooms (Room_number,Room_type,Rate,cost) VALUES (%s, %s, %s, %s)", (room_number, room_type, room_rate,cost))
    db.commit()

def add_guest_1(guest,phone,email):
    if guest is None or phone is None or email is None:
        return
    cursor.execute("SELECT Phone FROM guests")
    phones = cursor.fetchall()
    for phone_no in phones:
        if phone_no[0] == phone:
            popup("Phone number already exists")
            return
    cursor.execute("Insert Into guests (Name,Phone,Email) VALUES (%s,%s,%s)", (guest,phone,email,))
    db.commit()

def reserve_1(guest, room_number,check_in,check_out):
    if guest is None or room_number is None or check_in is None or check_out is None:
        return
    cursor.execute("SELECT Guest_ID FROM guests WHERE Name=%s", (guest,))
    guest_id =(cursor.fetchone())
    cursor.execute("SELECT Room_ID FROM rooms WHERE Room_number=%s", (room_number,))
    room_id =(cursor.fetchone())
    if guest_id is None:
        popup("Guest not found")
        return
    if room_id is None:
        popup("Room not found")
        return
    guest_id = guest_id[0]
    room_id = room_id[0]
    cursor.execute("SELECT cost FROM rooms WHERE Room_ID=%s", (room_id,))
    cost = (cursor.fetchone())[0]
    cursor.execute("UPDATE rooms SET available = 1 WHERE Room_ID=%s", (room_id,))
    cursor.execute("Insert Into reservations (Check_in,Check_out,Bill,Guest_ID,Room_ID) VALUES (%s,%s,%s,%s,%s)", (check_in,check_out,cost,guest_id,room_id))

    db.commit()

def reserve():
    guest = ctk.CTkInputDialog(text="Guest Name").get_input()
    room_number = ctk.CTkInputDialog(text="Room Number").get_input()
    check_in = ctk.CTkInputDialog(text="Check_in date").get_input()
    check_out = ctk.CTkInputDialog(text="Check_out date").get_input()
    available = check_availability_1(room_number)
    if available == 0:
        popup("Room is not available")
        return
    reserve_1(guest,room_number,check_in,check_out)

def add_guest():
    guest = ctk.CTkInputDialog(text="Guest Name").get_input()
    phone = ctk.CTkInputDialog(text="Phone Number").get_input()
    email = ctk.CTkInputDialog(text="Email Address").get_input()
    add_guest_1(guest,phone,email)

def add_room():

    room_number = ctk.CTkInputDialog(text="Room Number").get_input()
    room_type = ctk.CTkInputDialog(text="Room Type").get_input()
    rate = ctk.CTkInputDialog(text="Rate").get_input()
    cost = ctk.CTkInputDialog(text="Cost").get_input()
    add_room_1(room_number,room_type,rate,cost)

def check_availability():

    room_number = ctk.CTkInputDialog(text="Room Number").get_input()
    temp = check_availability_1(room_number)

    if temp == 1:
        popup("Room is available")
    else:
        popup("Room is not available")

def billing():
    guest = ctk.CTkInputDialog(text="Guest Name").get_input()

    bills = billing_1(guest)
    if bills is None:
        return
    new_window = ctk.CTkToplevel(app)
    new_window.title("Billing")
    new_window.geometry("300x300")
    i = 1
    for bill in bills:
        temp = ctk.CTkLabel(new_window,text=f"Bill{i} = {bill[0]}$")
        temp.pack(pady=10)
        i+=1

def room_inquiry():
    guest = ctk.CTkInputDialog(text="Guest Name").get_input()

    rooms = room_inquiry_1(guest)
    if rooms is None:
        return
    new_window = ctk.CTkToplevel(app)
    new_window.title("Billing")
    new_window.geometry("300x300")
    temp = ctk.CTkLabel(new_window,text=f"Guest {guest} has {len(rooms)} rooms")
    temp.pack(pady=20)
    for room in rooms:
        temp = ctk.CTkLabel(new_window, text=f"Room{room[0]}$")
        temp.pack(pady=20)

def list_available_rooms():
    rooms = list_available_rooms_1()
    new_window = ctk.CTkToplevel(app)
    new_window.title("Billing")
    new_window.geometry("500x500")
    temp = ctk.CTkLabel(new_window, text=f"There are {len(rooms)} rooms available.")
    temp.pack(pady=20)
    for room in rooms:
        st = f"Room{room[0]} of type {room[1]} has rating of {room[2]} and costs {room[3]}$"
        temp = ctk.CTkLabel(new_window, text=st)
        temp.pack(pady=20)


def display():


    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app.geometry("1024x720")
    app.title("Hotel")

    frame = ctk.CTkFrame(app,700, 700)
    frame.pack(padx=10, pady=10)

    header = ctk.CTkLabel(frame,text="Hotel",font=("Arial",20,"bold"),width=500)
    header.pack(padx=10, pady=15)
    list_all =ctk.CTkButton(frame,text="List Available Rooms",command=list_available_rooms,width=300)
    list_all.pack(padx=10, pady=15)
    add = ctk.CTkButton(frame,text="Add a room",command=add_room,width=300)
    add.pack(padx=10,pady=15)
    check = ctk.CTkButton(frame,text="Check Availability",command=check_availability,width=300)
    check.pack(padx=10, pady=15)
    bill = ctk.CTkButton(frame,text="Bills",command=billing,width=300)
    bill.pack(padx=10, pady=15)
    room_no = ctk.CTkButton(frame,text="Room Inquiry",command=room_inquiry,width=300)
    room_no.pack(padx=10, pady=15)
    guest = ctk.CTkButton(frame,text="Add a guest",command=add_guest,width=300)
    guest.pack(padx=10, pady=15)
    reservation = ctk.CTkButton(frame,text="Reserve",command=reserve,width=300)
    reservation.pack(padx=10, pady=15)
    app.mainloop()


display()