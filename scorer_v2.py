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
        self.Toplevel()  #Callinf TopLevel to take Inputs
    #Function to print all Inputs
    def run(self):
        self.window.destroy()
        for x in range(len(self.detBtns)):
            self.detBtns[x]=self.detBtns[x][1:]
            print(self.detBtns[x])
    #Function that creates TopLevel Window
    def Toplevel(self):
        self.window =customtkinter.CTkToplevel(self)
        self.window.geometry(str(self.w//2)+"x"+str(self.h//2))
        self.window.title("Set Quiz Details")
        self.window.protocol("WM_DELETE_WINDOW", self.run)
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
            text="Number of teams="+str(no_teams)+"Scores for this round="+str(scores)+" Qualifying Teams="+str(no_q_teams))
            ,no_teams,scores,no_q_teams]
        self.detBtns[x][0].place(relx=0.6, rely=0.1+(x+1)*.8/(self.n),anchor=tkinter.CENTER)

#App Object
app=Scorer()  
#MainLoop
app.mainloop()