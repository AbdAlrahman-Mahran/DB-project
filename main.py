from datetime import datetime
from tkinter import messagebox

import mysql.connector
import customtkinter as ctk

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="yami",
    port = 3306,
    database="hotel"
)

cursor = db.cursor()

db.commit()
app = ctk.CTk()
def popup(text):
    messagebox.showinfo(message=text)

def list_available_rooms_1():
    cursor.execute("SELECT Room_number, Room_Type, Rate,Price FROM rooms WHERE Available=1")
    rooms = cursor.fetchall()
    return rooms


def check_availability_1(room_number):
    if room_number is None:
        return
    cursor.execute("SELECT Available FROM rooms WHERE Room_number=%s", (room_number,))
    result = cursor.fetchone()
    if result is None:
        return 0
    return result[0]


def billing_1(guest):
    if guest is None:
        return
    cursor.execute("SELECT Guest_ID FROM guests WHERE Name=%s", (guest,))
    geust = cursor.fetchone()
    if guest is None:
        return
    guest = geust[0]
    cursor.execute("SELECT Amount FROM billings join bookings on bookings.Billing_ID = billings.Billing_ID  WHERE Guest_ID=%s", (guest,))
    bills = cursor.fetchall()
    return bills

def room_inquiry_1(guest):
    if guest is None:
        return
    cursor.execute("SELECT Guest_ID FROM guests WHERE Name=%s", (guest,))
    guest_id = cursor.fetchone()
    if guest_id is None:
        return
    guest_id= guest_id[0]
    cursor.execute("SELECT bookings.Room_Number FROM bookings  join rooms on rooms.Room_Number = bookings.Room_Number WHERE Guest_ID=%s", (guest_id,))
    room_numbers = cursor.fetchall()
    return room_numbers


def add_room_1(room_number,room_type,room_rate,price):
    if room_number is None or room_type is None or room_rate is None:
        return
    cursor.execute("SELECT Room_number FROM rooms")
    rooms = cursor.fetchall()

    for room in rooms:
        if room[0] == room_number:
            popup("Room number already exists")
            return

    cursor.execute("Insert Into rooms (Room_number,Room_type,Rate,Price) VALUES (%s, %s, %s,%s)", (room_number, room_type, room_rate, price))
    db.commit()

def add_guest_1(guest,phone,email):
    if guest is None or phone is None or email is None:
        return

    cursor.execute("Insert Into guests (Name,Phone,Email) VALUES (%s,%s,%s)", (guest,phone,email,))
    db.commit()

def reserve_1(guest, room_number,check_in,check_out):
    if guest is None or room_number is None or check_in is None or check_out is None:
        return
    cursor.execute("SELECT Guest_ID FROM guests WHERE Name=%s", (guest,))
    guest_id =(cursor.fetchone())
    if guest_id is None:
        popup("Guest not found")
        return
    guest_id = guest_id[0]
    cursor.execute("Select Price from rooms where Room_number=%s", (room_number,))
    price = cursor.fetchone()
    if price is None:
        popup("Room not found")
        return
    price = price[0]
    cursor.execute("Insert Into billings(Amount,Date) VALUE (%s, %s)", (price, datetime.now()))
    cursor.execute("SELECT billing_id FROM billings WHERE Amount=%s", (price,))
    temp = cursor.fetchall()
    if temp is None:
        return
    billing_id = -1

    for billing in temp:
        billing_id = max(billing[0], billing_id)
    if billing_id == -1:
        return

    cursor.execute("UPDATE rooms SET Available = 0 WHERE Room_Number=%s", (room_number,))
    cursor.execute("Insert Into bookings (Check_in,Check_out,Guest_ID,Room_Number,Billing_ID) VALUES (%s,%s,%s,%s,%s)", (check_in,check_out,guest_id,room_number,billing_id))
    db.commit()

def add_service(room_number,service,cost):
    if room_number is None or service is None:
        return
    cursor.execute("Insert into services (Room_Number, Name, Cost) values(%s,%s,%s)", (room_number, service, cost,))
    db.commit()
def reserve():
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("700x700")
    guest = ctk.CTkEntry(new_window, placeholder_text="Guest Name")
    guest.pack(pady=20)
    room_number = ctk.CTkEntry(new_window, placeholder_text="Room Number")
    room_number.pack(pady=20)
    check_in = ctk.CTkEntry(new_window, placeholder_text="Check_in Date")
    check_in.pack(pady=20)
    check_out = ctk.CTkEntry(new_window, placeholder_text="Check_out Date")
    check_out.pack(pady=20)

    def temp():
        available = check_availability_1(room_number.get())
        if available == 0:
            popup("Room is not available")
            return
        reserve_1(guest.get(), room_number.get(), check_in.get(),check_out.get())
        new_window.destroy()

    button = ctk.CTkButton(new_window, text="Book", command=temp)
    button.pack(pady=20)


def add_guest():
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("700x700")
    guest = ctk.CTkEntry(new_window, placeholder_text="Guest Name")
    guest.pack(pady = 20)
    phone = ctk.CTkEntry(new_window, placeholder_text="Phone")
    phone.pack(pady = 20)
    email = ctk.CTkEntry(new_window,placeholder_text= "Email")
    email.pack(pady = 20)
    def temp():
        add_guest_1(guest.get(),phone.get(),email.get())
        new_window.destroy()
    button = ctk.CTkButton(new_window, text="Add Guest",command=temp)
    button.pack(pady = 20)



def add_room():
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("700x700")
    room_number= ctk.CTkEntry(new_window,placeholder_text="Room Number")
    room_number.pack(pady = 20)
    room_type = ctk.CTkEntry(new_window,placeholder_text="Room Type")
    room_type.pack(pady = 20)
    rate = ctk.CTkEntry(new_window,placeholder_text="Rate")
    rate.pack(pady = 20)
    price = ctk.CTkEntry(new_window,placeholder_text="Price")
    price.pack(pady = 20)

    def temp():
        add_room_1(room_number.get(),room_type.get(),rate.get(),price.get())
        new_window.destroy()


    button = ctk.CTkButton(new_window, text="Add Room", command=temp)
    button.pack(pady=20)


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
        temp = ctk.CTkLabel(new_window, text=f"Room{room[0]}")
        temp.pack(pady=20)

def list_available_rooms():
    rooms = list_available_rooms_1()
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("700x700")
    temp = ctk.CTkLabel(new_window, text=f"There are {len(rooms)} rooms available.")
    temp.pack(pady=20)
    for room in rooms:
        st = f"Room {room[0]} of type {room[1]} has rating of {room[2]} and costs {room[3]}$"
        temp = ctk.CTkLabel(new_window, text=st)
        temp.pack(pady=20)

def add_service():
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("700x700")
    room_number= ctk.CTkEntry(new_window,placeholder_text="Room Number")
    room_number.pack(pady=20)
    Name = ctk.CTkEntry(new_window,placeholder_text="Name")
    Name.pack(pady=20)
    price = ctk.CTkEntry(new_window,placeholder_text="Price")
    price.pack(pady=20)

    def temp():
        add_service(room_number.get(),Name.get(),price.get())
        new_window.destroy()

    button = ctk.CTkButton(new_window, text="Add Service", command=temp)
    button.pack(pady=20)


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
    check = ctk.CTkButton(frame,text="Check Availability",command=check_availability,width=300)
    check.pack(padx=10, pady=15)
    add = ctk.CTkButton(frame,text="Add a room",command=add_room,width=300)
    add.pack(padx=10,pady=15)
    room_no = ctk.CTkButton(frame,text="Room Inquiry",command=room_inquiry,width=300)
    room_no.pack(padx=10, pady=15)

    guest = ctk.CTkButton(frame,text="Add a guest",command=add_guest,width=300)
    guest.pack(padx=10, pady=15)
    service = ctk.CTkButton(frame, text="Add a service", command=add_service, width=300)
    service.pack(padx=10, pady=15)
    reservation = ctk.CTkButton(frame,text="Reserve",command=reserve,width=300)
    reservation.pack(padx=10, pady=15)
    bill = ctk.CTkButton(frame,text="Bills",command=billing,width=300)
    bill.pack(padx=10, pady=15)

    app.mainloop()


display()