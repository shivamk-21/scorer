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
master_team_scores=[]
#Functions
def set_round(no_teams,scores):
    segment_buttons=[]
    team_scores=[0]*no_teams
    scoreTab=customtkinter.CTkEntry(rounds_frame,state='readonly',width=width*.4)
    scoreTab.place(relx=0.4,rely=.95,anchor=tkinter.CENTER)
    switch_var = customtkinter.StringVar(value="on")
    def switch_event():
        if switch_var.get()=="off":
            scoreTab.configure(state="normal")
        else:
            s=scoreTab.get().split(":")
            s=[int(x.split()[0]) for x in s[1:]]
            for x in range(len(s)):
                team_scores[x]=s[x]
            scoreTab.configure(state="readonly")
    switch = customtkinter.CTkSwitch(rounds_frame, text="Admin LOCK", command=switch_event,variable=switch_var, onvalue="on", offvalue="off")
    switch.place(relx=0.9,rely=.95,anchor=tkinter.CENTER)
    def add_points(team_no,val):
        team_scores[team_no]+=val
        scoreTab.configure(state="normal")
        s=" ".join(["Team "+str(x+1)+" : "+str(team_scores[x]) for x in range(len(team_scores))])
        scoreTab.delete(0,'end')
        scoreTab.insert(0,s)
        scoreTab.configure(state="readonly")
        segment_buttons[team_no].set("unset")
    for team in range(no_teams):
        segment_buttons.append(customtkinter.CTkSegmentedButton(rounds_frame,values=scores,command=partial(add_points,team)))
        segment_buttons[team].place(relx=0.5, rely=.05+(team+1)*.8/no_teams, anchor=tkinter.CENTER)
        customtkinter.CTkLabel(rounds_frame,text="Team "+str(team+1)).place(relx=0.3, rely=.05+(team+1)*.8/no_teams, anchor=tkinter.CENTER)
    
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