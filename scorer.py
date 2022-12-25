#Imports
import customtkinter
from functools import partial
#App Definition
app = customtkinter.CTk()
app.state("zoomed")
app.title("CTk example")
width=app.winfo_width()
height=app.winfo_height()
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
#Varibales
rounds=[]
#Functions
def round(n):
    print(n)
def add_rounds(event=None):
    for x in sidebar_frame.winfo_children()[1:]:
        x.destroy()
    n=int(sidebar_textbox.get())
    sidebar_textbox.delete(0,"end")
    rounds=[customtkinter.CTkButton(sidebar_frame,text="Round"+str(x),width=width*.05,command=partial(round,x)) for x in range(1,n+1)]
    for x in range(n):
        rounds[x].pack(pady=5)
#Elements
sidebar_frame = customtkinter.CTkFrame(app,corner_radius=0)
sidebar_subframe=customtkinter.CTkFrame(sidebar_frame,corner_radius=0)
sidebar_label=customtkinter.CTkLabel(sidebar_subframe,text="Enter No of Rounds:")
sidebar_textbox=customtkinter.CTkEntry(sidebar_subframe,width=width*.04)
sidebar_textbox.bind("<Return>",add_rounds)
sidebar_button=customtkinter.CTkButton(sidebar_subframe,text="Go",width=width*.02,command=add_rounds)
#Packing/Griding
sidebar_frame.pack(side="left",fill="y")
sidebar_subframe.pack()
sidebar_label.grid(row=0,column=0,columnspan=2,ipady=5)
sidebar_textbox.grid(row=1,column=0)
sidebar_button.grid(row=1,column=1)
#MainLoop
app.mainloop()