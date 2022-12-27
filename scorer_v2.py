#Imports
import customtkinter,tkinter
from functools import partial
#Setting App Appreance
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
#App Class
class Scorer(customtkinter.CTk):
    #Main App Definitions
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("Inquizitive_Scoring_App")
        self.w=self.winfo_width()
        self.h=self.winfo_height()
        #Main App Elements
        sidebar_frame = customtkinter.CTkFrame(self)
        scores_frame=customtkinter.CTkFrame(self,height=50,width=self.w*.8)
        self.sidebar_subframe2=customtkinter.CTkFrame(sidebar_frame)
        sidebar_subframe3=customtkinter.CTkFrame(sidebar_frame)
        self.rounds_frame=customtkinter.CTkFrame(self,width=self.w*.8)
        self.main_button=customtkinter.CTkButton(sidebar_subframe3,text="Start",command=self.Toplevel)
        appearance_mode_label = customtkinter.CTkLabel(sidebar_subframe3, text="Appearance Mode:", anchor="w")
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_subframe3, values=["Dark", "Light", "System"],
                                                                        command=self.change_appearance_mode_event)
        scaling_label = customtkinter.CTkLabel(sidebar_subframe3, text="UI Scaling:", anchor="w")
        scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_subframe3, values=["50%","60%","80%", "90%", "100%", "110%", "120%"],
                                                                    command=self.change_scaling_event)
        scaling_optionemenu.set("100%")
        scores_label=customtkinter.CTkLabel(scores_frame,text="Last Round Scores: ")
        self.scores_textbox=customtkinter.CTkEntry(scores_frame,width=self.w*.45,state='readonly')
        #Packing/Griding
        sidebar_frame.pack(side="left",fill="y",padx=10,pady=10,ipadx=5)
        sidebar_subframe3.pack(side='bottom',pady=5,padx=5,ipadx=10)
        scores_frame.pack(fill='y',padx=20,pady=20)
        scaling_optionemenu.pack(side='bottom',padx=10,pady=10)
        scaling_label.pack(side='bottom')
        appearance_mode_optionemenu.pack(side='bottom')
        appearance_mode_label.pack(side='bottom')
        self.main_button.pack(side='bottom',padx=10,pady=10)
        scores_label.place(relx=0.07,rely=0.5, anchor=tkinter.CENTER)
        self.scores_textbox.place(relx=0.55,rely=0.5, anchor=tkinter.CENTER)
    #Function that creates TopLevel Window
    def Toplevel(self):
        self.window =customtkinter.CTkToplevel(self)
        self.window.geometry(str(self.w//2)+"x"+str(self.h//2)+"+"+str(self.w)+"x"+str(self.h))
        self.window.title("Set Quiz Details")
        self.window.protocol("WM_DELETE_WINDOW", self.setup)
        #TopLevel Window ELements
        label=customtkinter.CTkLabel(self.window,text="Enter No of Rounds:")
        self.textbox=customtkinter.CTkEntry(self.window)  #Declaring self as may be reuired later
        self.textbox.bind("<Return>",self.add_rounds)
        button=customtkinter.CTkButton(self.window,text="Go")
        #Placing elements on self.window
        label.place(relx=0.3,rely=0.05)
        self.textbox.place(relx=0.5,rely=0.05,width=self.w*.04)
        button.place(relx=0.6,rely=0.05)
        if self.rounds_frame.winfo_ismapped():
            self.rounds_frame.forget()
    #Function that adds rounds and corresponding buttons to add details in self.window
    def add_rounds(self,event=None):
        #Overriding previous rounds if any
        for x in self.window.winfo_children()[3:]:
            x.destroy()
        #Attaining No of rounds 
        self.n=int(self.textbox.get())
        self.textbox.delete(0,"end")
        rounds=[customtkinter.CTkLabel(self.window,text="Round"+str(x)) for x in range(1,self.n+1)]
        #Creating self.detBtns as it will store future data as well
        self.detBtns =[customtkinter.CTkButton(self.window,text="Add Round Details", command=partial(self.details,x)) for x in range(self.n)]
        for x in range(self.n):
            rounds[x].place(relx=0.3,rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)
            self.detBtns[x].place(relx=0.6, rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)
    #Function that is linked to buttons to take each round inputs
    def details(self,x):
        #If it is first round then take the number of initial teams
        if x==0:
            dialog1 = customtkinter.CTkInputDialog(text="Number of Teams:", title="Teams")
            no_teams=int(dialog1.get_input())
        #If not first round then no is teams is the number of previous round qualifiers
        else:
            no_teams=int(self.detBtns[x-1][0].cget("text").split("=")[-1])
        #Dialogs to take inputs
        dialog2 = customtkinter.CTkInputDialog(text="Score System ( '/' seperated):", title="Scores")
        scores=list(map(int,dialog2.get_input().split("/")))
        dialog3 = customtkinter.CTkInputDialog(text="No of Qualifying Teams:", title="Qualifying Criteria")
        no_q_teams=int(dialog3.get_input())
        #Removing Add details button and placing a Label with all data.
        #Also adding relevant round detials in the self.detBtns
        self.detBtns[x].place_forget()
        self.detBtns[x]=[customtkinter.CTkLabel(self.window,
            text="Number of teams="+str(no_teams)+"  Scores for this round="+str(scores)+"  Qualifying Teams="+str(no_q_teams))
            ,no_teams,scores,no_q_teams]
        self.detBtns[x][0].place(relx=0.6, rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)
    #Function adding points 
    def add_points(self,x,val):
        self.team_scores[x]+=val
        self.scoreTab.configure(state="normal")
        s=" ".join(["Team "+str(x+1)+" : "+str(self.team_scores[x]) for x in range(len(self.team_scores))])
        self.scoreTab.delete(0,'end')
        self.scoreTab.insert(0,s)
        self.scoreTab.configure(state="readonly")
        self.segment_buttons[x].set("unset")
    #FUnction creating the layout round
    def round(self,round_no):
        #Initailising if team_scores do not exist
        if round_no==0:
            self.team_scores=[0]*self.detBtns[round_no][0]
        #Selecting top teams from last round
        else:
            s=" ".join(["Team "+str(x+1)+" : "+str(self.team_scores[x]) for x in range(len(self.team_scores))])
            self.scores_textbox.configure(state="normal")
            self.scores_textbox.delete(0,'end')
            self.scores_textbox.insert(0,s)
            self.scores_textbox.configure(state="readonly")
            self.team_scores.sort()
            self.team_scores.reverse()
            self.team_scores=self.team_scores[:self.detBtns[round_no][0]]
            if self.team_scores.count(self.team_scores[-1])!=1:
                tkinter.messagebox.showwarning("Warning","A Tie has occured")
        #Removing layout of last round if any
        if self.rounds_frame.winfo_ismapped():
            self.rounds_frame.forget()
        for x in self.rounds_frame.winfo_children():
            x.place_forget()
        #Packing an empty Rounds Frame 
        self.rounds_frame.pack(side='right',fill='both',padx=20,pady=20)
        #Subfunction which add functionality to Switch 
        switch_var = customtkinter.StringVar(value="on") #Variable for the Switch
        def switch_event():
            if switch_var.get()=="off":
                self.scoreTab.configure(state="normal")
            else:
                s=self.scoreTab.get().split(":")
                s=[int(x.split()[0]) for x in s[1:]]
                for x in range(len(s)):
                    self.team_scores[x]=s[x]
                self.scoreTab.configure(state="readonly")
        #ScoreTab and Switch elements
        self.scoreTab=customtkinter.CTkEntry(self.rounds_frame,state='readonly',width=self.w*.4)
        self.scoreTab.place(relx=0.4,rely=.95,anchor=tkinter.CENTER)
        switch = customtkinter.CTkSwitch(self.rounds_frame, text="Admin LOCK", command=switch_event,variable=switch_var, onvalue="on", offvalue="off")
        switch.place(relx=0.9,rely=.95,anchor=tkinter.CENTER)
        #Segment Button for adding scores | Linked with add_points
        self.segment_buttons=[]
        for team in range(self.detBtns[round_no][0]):
            self.segment_buttons.append(customtkinter.CTkSegmentedButton(self.rounds_frame,values=self.detBtns[round_no][1],command=partial(self.add_points,team)))
            self.segment_buttons[team].place(relx=0.6, rely=(team+1)*.8/self.detBtns[round_no][0], anchor=tkinter.CENTER)
            #Label for each Segment Button
            customtkinter.CTkLabel(self.rounds_frame,text="Team "+str(team+1)).place(relx=0.4, rely=(team+1)*.8/self.detBtns[round_no][0], anchor=tkinter.CENTER)
        self.add_points(0,0)
    #Function to print all Inputs
    def setup(self):
        #Closing TopLevel Window
        self.window.destroy()
        for x in range(len(self.detBtns)):
            self.detBtns[x]=self.detBtns[x][1:]
        #Changing Main button text to Restart
        self.main_button.configure(text="Restart")
        #Packing when required
        self.sidebar_subframe2.pack(pady=5,padx=5,ipadx=10)
        #Destroying previous elements
        for x in self.sidebar_subframe2.winfo_children():
            x.destroy()
        #Adding Round BUttons
        for x in range(self.n):
            customtkinter.CTkButton(self.sidebar_subframe2,text="Round "+str(x+1),command=partial(self.round,x)).pack(padx=10,pady=10)
    #Function to change Appearance
    def change_appearance_mode_event(self,new_appearance_mode):
            customtkinter.set_appearance_mode(new_appearance_mode)
    #Function to change Scaling
    def change_scaling_event(self,new_scaling):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
    
#App Object
app=Scorer()  
#MainLoop
app.mainloop()