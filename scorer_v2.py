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
        #MAin App Elements
        sidebar_frame = customtkinter.CTkFrame(self)
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
        #Packing/Griding
        sidebar_frame.pack(side="left",fill="y",padx=10,pady=10,ipadx=5)
        sidebar_subframe3.pack(side='bottom',pady=5,padx=5,ipadx=10)
        scaling_optionemenu.pack(side='bottom')
        scaling_label.pack(side='bottom')
        appearance_mode_optionemenu.pack(side='bottom')
        appearance_mode_label.pack(side='bottom')
        self.main_button.pack(side='bottom')
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
            customtkinter.CTkButton(self.sidebar_subframe2,text="Round "+str(x+1)).pack(padx=10,pady=10)
    #Function to change Appearance
    def change_appearance_mode_event(self,new_appearance_mode):
            customtkinter.set_appearance_mode(new_appearance_mode)
    #Function to change Scaling
    def change_scaling_event(self,new_scaling):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
    #Function that creates TopLevel Window
    def Toplevel(self):
        self.window =customtkinter.CTkToplevel(self)
        self.window.geometry(str(self.w//2)+"x"+str(self.h//2))
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
            rounds[x].place(relx=0.2,rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)
            self.detBtns[x].place(relx=0.5, rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)
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

#App Object
app=Scorer()  
#MainLoop
app.mainloop()