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
#MainLoop
app.mainloop()