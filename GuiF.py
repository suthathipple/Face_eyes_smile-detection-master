from tkinter import *
#
def on_click():
    height_m = height_cm.get()/100
    height_m_sq = height_m**2
    bmi = weigh_kg.get() / height_m_sq
    bmi_val.set(f'{bmi:.2f} BMI')


root = Tk()
root.title("โปรแกรมคำนวณดัชนีมวลกาย")
root.option_add("*Font","Tahoma 16")

weigh_kg = DoubleVar()
height_cm = DoubleVar()
bmi_val = StringVar()

photo = PhotoImage(file="bmi-mahidol.png")
Label(root,image=photo).pack()

Label(root,text="น้ำหนักตัว หน่วยเป็น กิโลกรัม",fg='red').pack()
ent_kg = Entry(root,textvariable = weigh_kg,width = 23).pack(pady = 10)

Label(root,text="ส่วนสูง หน่วยเป็น เซ็นติเมตร",fg='navy').pack()
ent_cm = Entry(root,textvariable = height_cm,width = 23).pack(pady = 10)

btn1 = Button(root,command=on_click,text = " คำนวณค่า BMI ", width= 21, borderwidth=1, bg='deep sky blue').pack()

Label(root,text="\nค่าดัชนีมวลกาย เท่ากับ").pack()
Label(root,textvariable = bmi_val).pack(pady = 20)

photo2 = PhotoImage(file="bmi-scale.png")
Label(root,image=photo2).pack()

root.mainloop()