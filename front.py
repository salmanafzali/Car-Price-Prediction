# import librarys
from sys import maxsize
import tkinter as tk
from tkinter import PhotoImage, filedialog
from tkinter.ttk import *
from tkinter import messagebox
import Backend_ml as bk
from pathlib import Path


# window and insert operations
def main_insert():
    def save():
        result = bk.insert_connect(make, model, year, select_fuel, engin_hp, cylinders, transmission_select, wheels_select, doors, market_cat,
                                   size_select, style_select, highway, city, popularity)

        num_variabel = ["Year", "Engin HP", "Cylinders",
                        "Doors", "Highway MPG", "City MPG", "Popularity"]
        str_variabel = ["Make", "Model"]

        if result[0:10] == "Successful":
            # Reset insert and select user
            # feilds
            entrys = [make, model, year, engin_hp, cylinders,
                      doors, market_cat, highway, city, popularity]
            optionmenu_s = [select_fuel, transmission_select,
                            wheels_select, size_select, style_select]
            optionmenu_t = [fuel_types, transmission_type,
                            wheels_type, size_type, style_type]

            # entry reset
            for i in entrys:
                i.delete(0, tk.END)

            # option menu reset
            for s, t in zip(optionmenu_s, optionmenu_t):
                s.set(t[0])

            messagebox.showinfo(
                "Inserts", f"Successfully registered \n id is ={result[11:]}")

        elif result == "Number Unsuccessful":
            messagebox.showerror(
                "Error", f"Please fill in  || {" || ".join(num_variabel)} ||  fields with a numerical value")

        elif result == "String Unsuccessful":
            messagebox.showerror(
                "Error", f"Please fill || {" || ".join(str_variabel)}")

    def receive():
        result = bk.receive_connect()

        if result == "Successful":
            messagebox.showinfo(
                "save file", f"Successful \n {Path.home() / "Documents"}")
        else:
            messagebox.showerror("Error", "There is no product")

    # create window input value
    insert_window = tk.Toplevel(main_window)
    insert_window.title("Insert Cars Details")
    insert_window.geometry('760x670')

    # limit size
    insert_window.maxsize(760, 670)

    # create background image
    insert_window.insert_image = tk.PhotoImage(
        file="Images/desert-white-5120x2880-21880.png")
    Label(insert_window, image=insert_window.insert_image).place(
        x=0, y=0, relwidth=1, relheight=1)

    Label(insert_window, text="Please enter your vehicle details carefully!",
          font=("", "15")).pack(pady=5)

    # Back Menu Button
    tk.Button(insert_window, bg="darkred", fg="white", text="Back",
              command=insert_window.destroy).place(x=3, y=3)

    # insert make value
    Label(insert_window, text="< brand >", font=("", "14")).place(x=28, y=60)
    make = Entry(insert_window, font=("", "14"))
    make.place(x=20, y=100, width=100)

    # insert car model
    Label(insert_window, text="< Model >", font=("", "14")).place(x=200, y=60)
    model = Entry(insert_window, font=("", "14"))
    model.place(x=170, y=100, width=150)

    # insert car Year create
    Label(insert_window, text="< Year >", font=("", "14")).place(x=392, y=60)
    year = Entry(insert_window, font=("", "14"))
    year.place(x=380, y=100, width=100)

    # Engin Fuel Type Select
    Label(insert_window, text="Engin Fuel Type",
          font=("", "14")).place(x=550, y=60)
    select_fuel = tk.StringVar()

    fuel_types = ["regular unleaded", "regular unleaded", "premium unleaded (required)", "premium unleaded (recommended)", "electric", "diesel", "natural gas",
                  "flex-fuel (unleaded/E85)", "flex-fuel (premium unleaded recommended/E85)", "flex-fuel (premium unleaded required/E85)", "flex-fuel (unleaded/natural gas)"]

    OptionMenu(insert_window, select_fuel, *
               fuel_types).place(x=530, y=100, width=180)

    # insert hourse power engin
    Label(insert_window, text="< Engin HP >",
          font=("", "14")).place(x=20, y=160)
    engin_hp = Entry(insert_window, font=("", "14"))
    engin_hp.place(x=25, y=200, width=100)

    # insert Engin Cylinders
    Label(insert_window, text="< Cylinders >",
          font=("", "14")).place(x=190, y=160)
    cylinders = Entry(insert_window, font=("", "14"))
    cylinders.place(x=222, y=200, width=50)

    # select Transmission Type
    Label(insert_window, text="Transmission Type",
          font=("", "14")).place(x=350, y=160)

    transmission_select = tk.StringVar()
    transmission_type = ["AUTOMATIC", "AUTOMATIC",
                         "MANUAL", "AUTOMATED_MANUAL", "DIRECT_DRIVE"]

    OptionMenu(insert_window, transmission_select, *
               transmission_type).place(x=350, y=200, width=170)

    # select Driven_Wheels
    Label(insert_window, text="Driven Wheels",
          font=("", "14")).place(x=580, y=160)

    wheels_select = tk.StringVar()
    wheels_type = ["front wheel drive", "front wheel drive",
                   "rear wheel drive", "all wheel drive", "four wheel drive"]

    OptionMenu(insert_window, wheels_select, *
               wheels_type).place(x=580, y=200, width=130)

    # insert number door car
    Label(insert_window, text="< Doors >", font=("", "14")).place(x=25, y=280)
    doors = Entry(insert_window, font=("", "14"))
    doors.place(x=45, y=320, width=50)

    # insert Market Category
    Label(insert_window, text="< Market Category >",
          font=("", "14")).place(x=152.5, y=280)
    market_cat = Entry(insert_window, font=("", "14"))
    market_cat.place(x=150, y=320, width=180)

    # select Vehicle Size
    Label(insert_window, text="Vehicle Size",
          font=("", "14")).place(x=400, y=280)

    size_select = tk.StringVar()
    size_type = ["Compact", "Compact", "Midsize", "Large"]

    OptionMenu(insert_window, size_select, *
               size_type).place(x=390, y=323, width=130)

    # select Vehicle Style
    Label(insert_window, text="Vehicle Style",
          font=("", "14")).place(x=590, y=280)

    style_select = tk.StringVar()
    style_type = ["Coupe", "Coupe", "Convertible", "Sedan",  "Wagon", "4dr Hatchback",  "2dr Hatchback", "4dr SUV",  "Passenger Minivan", "Cargo Minivan",
                  "Crew Cab Pickup", "Regular Cab Pickup",  "Extended Cab Pickup", "2dr SUV",  "Cargo Van", "Convertible SUV", "Passenger Van"]

    OptionMenu(insert_window, style_select, *
               style_type).place(x=580, y=323, width=130)

    # insert highway MPG
    Label(insert_window, text="< highway MPG >",
          font=("", "14")).place(x=55, y=405)
    highway = Entry(insert_window, font=("", "14"))
    highway.place(x=100, y=445, width=60)

    # insert city MPG
    Label(insert_window, text="< city mpg >",
          font=("", "14")).place(x=325, y=405)
    city = Entry(insert_window, font=("", "14"))
    city.place(x=347, y=445, width=60)

    # insert popularity
    Label(insert_window, text="< Popularity >",
          font=("", "14")).place(x=570, y=405)
    popularity = Entry(insert_window, font=("", "14"))
    popularity.place(x=570, y=445, width=120)

    # save insert values
    tk.Button(insert_window, bg='skyblue', text="Save",
              command=save).place(x=200, y=570, width=80, height=40)

    # receive insert all values
    Label(insert_window, text="<<< For Receive all add File",
          font=("", "13")).place(x=540, y=580)
    tk.Button(insert_window, text="Receive", bg='gray',
              command=receive).place(x=460, y=570, width=80, height=40)


# window and remove operations
def main_remove():
    # remove Botton Operation
    def remove():
        result = bk.remove_connect(id=del_id)

        if result == "Successful":
            messagebox.showinfo("Remove", "Product removal was successful")
        elif result == "Not Found":
            messagebox.showwarning("Warning", "id Product Not Found")
        elif result == "ValueError":
            messagebox.showerror("Error", "just Enter Number value!")
        elif result == "Unsuccessful":
            messagebox.showerror(
                "Error", "No products have been imported yet!")
        else:
            messagebox.showerror("Error", "Unknown Error")

    # Receive Botton Operation
    def receive():
        result = bk.receive_connect()

        if result == "Successful":
            messagebox.showinfo(
                "save file", f"Successful \n {Path.home() / "Documents"}")
        else:
            messagebox.showerror("Error", "There is no product")

    remove_window = tk.Toplevel(main_window)
    remove_window.title("delete Car")
    remove_window.geometry('400x250')
    remove_window.maxsize(400, 250)

    # background image for remove main
    remove_window.rm_img = PhotoImage(file="Images/delete_main.png")
    Label(remove_window, image=remove_window.rm_img).place(
        x=0, y=0, relheight=1, relwidth=1)

    # Back Menu Button
    tk.Button(remove_window, bg="darkred", fg="white", text="Back",
              command=remove_window.destroy).place(x=3, y=3)

    # Enter id
    Label(remove_window, font=("", "13"),
          text="Enter id product to delete").place(x=105, y=70)
    del_id = Entry(remove_window, font=("", "13"))
    del_id.place(x=150, y=100, width=100)

    # remove and receive button
    tk.Button(remove_window, bg="salmon", text="Remove",
              command=remove).place(x=90, y=180, width=70, height=30)
    tk.Button(remove_window, bg="gray", text="Receive",
              command=receive).place(x=230, y=180, width=70, height=30)


# window and upload operations
def main_upload():
    # need columns button
    def show_needs():
        # show feature needed
        feature_need = ['Make', "Model", 'Year', 'Engine Fuel Type', 'Engine HP', 'Engine Cylinders', 'Transmission Type', 'Driven_Wheels',
                        'Number of Doors', "Market Category", 'Vehicle Size', 'Vehicle Style', 'highway MPG', 'city mpg', 'Popularity']

        messagebox.showinfo("Need Columns", "\n".join(feature_need))

    def upload():
        # read file user
        file_path = filedialog.askopenfilename(
            title="Select File csv", filetypes=[("CSV Files", "*.csv")])

        # save address file
        if file_path:
            lbl_path.config(text=file_path)   # show address
        else:
            messagebox.showerror("Warning", "No File Selected")

    # save file in data base

    def save():
        path = lbl_path["text"]    # for check select file
        if path:
            result = bk.upload_connect(path)
            if result == "Successful":
                messagebox.showinfo("Result", "Successful registration")
            elif result == "Unsuccessful":
                messagebox.showerror(
                    "Result", "Registration failed, Please Check File")

        else:
            messagebox.showerror("Error", "File Not Found!")

    # create upload window
    upload_window = tk.Toplevel(main_window)
    upload_window.title("upload Cars")
    upload_window.geometry('500x500')
    upload_window.maxsize(500, 500)

    # backgound image
    upload_window.upload_img = tk.PhotoImage(file="Images/up_main.png")
    Label(upload_window, image=upload_window.upload_img).place(x=0, y=0, relheight=1, relwidth=1)

    # Back Menu Button
    tk.Button(upload_window, bg="darkred", fg="white", text="Back",
              command=upload_window.destroy).place(x=3, y=3)

    # show need columns for upload file
    tk.Label(upload_window, bg="silver", text="Required columns for file upload!", font=(
        "", "15")).place(x=110, y=30)
    tk.Button(upload_window, bg="silver", text="Needs",
              command=show_needs).place(x=210, y=70, width=80, height=40)

    # upload file Label and button
    tk.Label(upload_window, bg="silver", text="Click Button To select File >>>", font=(
        "", "17")).place(x=35, y=180)
    tk.Button(upload_window, bg="silver", text="Upload",
              command=upload).place(x=350, y=175, width=80, height=40)
    lbl_path = Label(upload_window, text="")
    lbl_path.place(x=35, y=225)

    # save file
    tk.Label(upload_window, bg="silver", text="Click if the path is correct!", font=(
        "", "16")).place(x=128, y=320)
    tk.Button(upload_window, bg="gray", text="Save", command=save).place(
        x=210, y=360, width=80, height=40)


def main_prediction():
    def predict():
        file_path = Path.home() / "Documnet"
        result = bk.predict_connect(file_name)

        if result == "Successful":
            messagebox.showinfo(
                "Successful", f"Successful prediction! \n {file_path}")
        elif result == "Unsuccessful":
            messagebox.showerror("Error", "not found value")
        elif result == "Not Name":
            messagebox.showerror("Error", "Enter Name For file")

    predict_window = tk.Toplevel(main_window)
    predict_window.title("prediction Cars Price")
    predict_window.geometry('400x400')
    predict_window.maxsize(400, 360)

    # background image
    predict_window.pred_img = PhotoImage(file="Images/predict_main.png")
    Label(predict_window, image=predict_window.pred_img).place(x=0, y=0)

    # predict file name
    Label(predict_window, text="Enter Your File Name>>>",
          font=('', '12')).place(x=10, y=250)
    file_name = Entry(predict_window, font=('', '12'))
    file_name.place(x=190, y=250)

    # Button To Final proccess and predict price
    Button(predict_window, text="Predict", command=predict).place(
        x=160, y=300, width=80, height=40)

    # Back Menu Button
    tk.Button(predict_window, bg="darkred", fg="white", text="Back",
              command=predict_window.destroy).place(x=3, y=3)


# ====================================== Main Window =======================================
# create main window for select operations
main_window = tk.Tk()

main_window.title("Car Price Prediction")
main_window.geometry('700x630')

main_img = tk.PhotoImage(file="Images/car_main.png")
Label(main_window, image=main_img).place(x=0, y=0)

# insert elements
tk.Label(main_window, text="Click to add Car!",
         font=('', 16)).place(x=100, y=405)
Button(main_window, text="Click Here", command=main_insert).place(
    x=130, y=435, width=100, height=40)

# remove elements
Label(main_window, text="Click to delete insert Car!",
      font=('', 16)).place(x=380, y=405)
Button(main_window, text="Click Here", command=main_remove).place(
    x=445, y=435, width=100, height=40)

# import file elements
Label(main_window, text="Click to upload file!",
      font=('', 16)).place(x=90, y=515)
Button(main_window, text="Click Here", command=main_upload).place(
    x=125, y=545, width=100, height=40)

# Prediction machins elements
Label(main_window, text="predict entered values!",
      font=('', 16)).place(x=395, y=515)
Button(main_window, text="Click Here", command=main_prediction).place(
    x=445, y=545, width=100, height=40)

main_window.mainloop()
