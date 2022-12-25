#Imports
import customtkinter,tkinter
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
scores=[]
#Functions
def set_round(no_teams,scores):
    segment_buttons=[]
    for team in range(no_teams):
        segment_buttons.append(customtkinter.CTkSegmentedButton(rounds_frame,values=scores,command=print))
        segment_buttons[team].place(relx=0.5, rely=(team+1)*.8/no_teams, anchor=tkinter.CENTER)
def round_details(n):
    if rounds_frame.winfo_ismapped():
        rounds_frame.forget()
        for x in rounds_frame.winfo_children():
            x.place_forget()
    rounds_frame.pack(side='right',fill='both',padx=20,pady=20)
    def details():
        dialog1 = customtkinter.CTkInputDialog(text="Number of Teams:", title="Teams")
        no_teams=int(dialog1.get_input())
        dialog2 = customtkinter.CTkInputDialog(text="Score System ('/' seperated):", title="Scores")
        scores=list(map(int,dialog2.get_input().split("/")))
        detBtn.place_forget()
        set_round(no_teams,scores)
    detBtn = customtkinter.CTkButton(rounds_frame, text="Add Round Details", command=details)
    detBtn.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
def add_rounds(event=None):
    for x in sidebar_frame.winfo_children()[1:]:
        x.destroy()
    n=int(sidebar_textbox.get())
    sidebar_textbox.delete(0,"end")
    rounds=[customtkinter.CTkButton(sidebar_frame,text="Round"+str(x),width=width*.05,command=partial(round_details,x)) for x in range(1,n+1)]
    for x in range(n):
        rounds[x].pack(pady=5)
#Elements
sidebar_frame = customtkinter.CTkFrame(app)
sidebar_subframe=customtkinter.CTkFrame(sidebar_frame)
sidebar_label=customtkinter.CTkLabel(sidebar_subframe,text="Enter No of Rounds:")
sidebar_textbox=customtkinter.CTkEntry(sidebar_subframe,width=width*.04)
sidebar_textbox.bind("<Return>",add_rounds)
sidebar_button=customtkinter.CTkButton(sidebar_subframe,text="Go",width=width*.02,command=add_rounds)
rounds_frame=customtkinter.CTkFrame(app,width=width*.8)
#Packing/Griding
sidebar_frame.pack(side="left",fill="y",padx=10,pady=10,ipadx=5)
sidebar_subframe.pack(pady=2,padx=2,ipadx=15,ipady=5)
sidebar_label.pack(pady=10)
sidebar_textbox.pack(side='left')
sidebar_button.pack(side='right')
#MainLoop
app.mainloop()