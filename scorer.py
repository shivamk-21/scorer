#Imports
import customtkinter,tkinter
from functools import partial
#App Definition
app = customtkinter.CTk()
app.state("zoomed")
app.title("Inquizitive_Scoring_App")
width=app.winfo_width()
height=app.winfo_height()
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
#Varibales

#Functions
#Function to Save the scores in upper Tab
def save_master(score):
    s=" ".join(["Team "+str(x+1)+" : "+str(score[x]) for x in range(len(score))])
    scores_textbox.configure(state="normal")
    scores_textbox.delete(0,'end')
    scores_textbox.insert(0,s)
    scores_textbox.configure(state="readonly")
#Function which designs the Round's Frame
def set_round(no_teams,scores,iniScores):
    segment_buttons=[] #List of all segment buttons
    switch_var = customtkinter.StringVar(value="on") #Variable for the Switch
    if iniScores==['']:  #If Initial scores were left blank for setting all scores zero
        iniScores=[0]*no_teams
    else:              #Converting Values to Integer
        iniScores=list(map(int,iniScores))
    team_scores=iniScores  #Initial Scores of teams
    scores_button.configure(command=partial(save_master,team_scores)) #Adding functionality to Save Button
    #Subfunction which add functionality to Switch 
    def switch_event():
        if switch_var.get()=="off":
            scoreTab.configure(state="normal")
        else:
            s=scoreTab.get().split(":")
            s=[int(x.split()[0]) for x in s[1:]]
            for x in range(len(s)):
                team_scores[x]=s[x]
            scoreTab.configure(state="readonly")
    #Subfunction which adds functionality to the Segment Buttons
    def add_points(team_no,val):
        team_scores[team_no]+=val
        scoreTab.configure(state="normal")
        s=" ".join(["Team "+str(x+1)+" : "+str(team_scores[x]) for x in range(len(team_scores))])
        scoreTab.delete(0,'end')
        scoreTab.insert(0,s)
        scoreTab.configure(state="readonly")
        segment_buttons[team_no].set("unset")
    #ScoreTab and Switch elements
    scoreTab=customtkinter.CTkEntry(rounds_frame,state='readonly',width=width*.4)
    scoreTab.place(relx=0.4,rely=.95,anchor=tkinter.CENTER)
    switch = customtkinter.CTkSwitch(rounds_frame, text="Admin LOCK", command=switch_event,variable=switch_var, onvalue="on", offvalue="off")
    switch.place(relx=0.9,rely=.95,anchor=tkinter.CENTER)
    #Creation of segment Buttons and addition in the segment_buttons list
    for team in range(no_teams):
        segment_buttons.append(customtkinter.CTkSegmentedButton(rounds_frame,values=scores,command=partial(add_points,team)))
        segment_buttons[team].place(relx=0.6, rely=.05+(team+1)*.8/no_teams, anchor=tkinter.CENTER)
        #Label for each Segment Button
        customtkinter.CTkLabel(rounds_frame,text="Team "+str(team+1)).place(relx=0.4, rely=.05+(team+1)*.8/no_teams, anchor=tkinter.CENTER)
    add_points(0,0)  #PseudoUpdating the ScoreaTab
#Function to set Each Round Details
def round_details():
    #Removing Elements of Previous Round if they Exist
    if rounds_frame.winfo_ismapped():
        rounds_frame.forget()
        for x in rounds_frame.winfo_children():
            x.place_forget()
    #Packing an empty Rounds Frame 
    rounds_frame.pack(side='right',fill='both',padx=20,pady=20)
    #Functions Handling Round Creation via Dialog Boxes
    def details():
        #Taking Relevant Details
        dialog1 = customtkinter.CTkInputDialog(text="Number of Teams:", title="Teams")
        no_teams=int(dialog1.get_input())
        dialog2 = customtkinter.CTkInputDialog(text="Score System ( '/' seperated):", title="Scores")
        scores=list(map(int,dialog2.get_input().split("/")))
        dialog3 = customtkinter.CTkInputDialog(text="Initial Team Scores ( ',' seperated)\n Leave Blank for all Zero:", title="Initial Scores")
        ini_scores=dialog3.get_input().split(",")
        detBtn.place_forget()
        #Remapping to finally create and place elements on Round's Frame
        set_round(no_teams,scores,ini_scores)
    #Button which opens dialogs to set Round Options
    detBtn = customtkinter.CTkButton(rounds_frame, text="Add Round Details", command=details)
    detBtn.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
#Function to add Rounds in the SideBar 
def add_rounds(event=None):
    sidebar_subframe2.pack(pady=5,padx=5,fill='y',ipadx=5,ipady=5)  #Packing Frame when required
    #Removing Rounds if they exist
    for x in sidebar_subframe2.winfo_children():
        x.destroy()
    #Creating Buttons for Each Round
    n=int(sidebar_textbox.get())
    sidebar_textbox.delete(0,"end")
    rounds=[customtkinter.CTkButton(sidebar_subframe2,text="Round"+str(x),width=width*.05,command=round_details) for x in range(1,n+1)]
    #Packing all Round's Button in Sidebar
    for x in range(n):
        rounds[x].pack(pady=5)
#Function to change Appearance
def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
#Function to change Scaling
def change_scaling_event(new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
#Elements
sidebar_frame = customtkinter.CTkFrame(app)
sidebar_subframe1=customtkinter.CTkFrame(sidebar_frame)
sidebar_subframe2=customtkinter.CTkFrame(sidebar_frame)
sidebar_subframe3=customtkinter.CTkFrame(sidebar_frame)
scores_frame=customtkinter.CTkFrame(app,height=50,width=width*.8)
rounds_frame=customtkinter.CTkFrame(app,width=width*.8)
scores_label=customtkinter.CTkLabel(scores_frame,text="Saved Scores: ")
scores_button=customtkinter.CTkButton(scores_frame,text="Save",width=width*.02)
scores_textbox=customtkinter.CTkEntry(scores_frame,width=width*.45,state='readonly')
sidebar_label=customtkinter.CTkLabel(sidebar_subframe1,text="Enter No of Rounds:")
sidebar_textbox=customtkinter.CTkEntry(sidebar_subframe1,width=width*.04)
sidebar_textbox.bind("<Return>",add_rounds)
sidebar_button=customtkinter.CTkButton(sidebar_subframe1,text="Go",width=width*.02,command=add_rounds)
appearance_mode_label = customtkinter.CTkLabel(sidebar_subframe3, text="Appearance Mode:", anchor="w")
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_subframe3, values=["Dark", "Light", "System"],
                                                                       command=change_appearance_mode_event)
scaling_label = customtkinter.CTkLabel(sidebar_subframe3, text="UI Scaling:", anchor="w")
scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_subframe3, values=["50%","60%","80%", "90%", "100%", "110%", "120%"],
                                                               command=change_scaling_event)
scaling_optionemenu.set("100%")
#Packing/Griding
sidebar_frame.pack(side="left",fill="y",padx=10,pady=10,ipadx=5)
sidebar_subframe1.pack(pady=5,padx=5,ipadx=5,ipady=5)
sidebar_subframe3.pack(side='bottom',pady=5,padx=5,ipadx=10)
sidebar_label.pack(pady=10)
sidebar_textbox.pack(side='left',padx=5,pady=5)
sidebar_button.pack(side='right',padx=5,pady=5)
scores_frame.pack(fill='y',padx=20,pady=20)
scores_label.place(relx=0.05,rely=0.5, anchor=tkinter.CENTER)
scores_button.place(relx=.97,rely=0.5, anchor=tkinter.CENTER)
scores_textbox.place(relx=0.52,rely=0.5, anchor=tkinter.CENTER)
scaling_optionemenu.pack(side='bottom')
scaling_label.pack(side='bottom')
appearance_mode_optionemenu.pack(side='bottom')
appearance_mode_label.pack(side='bottom')
#MainLoop
app.mainloop()