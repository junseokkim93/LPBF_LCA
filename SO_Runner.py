import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.font import Font

def browse_file_func(entry, ext):
    file_path = filedialog.askopenfilename(filetypes=[("{} files".format(ext), "*.{}".format(ext)), ("All files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    
def browse_dir_func(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)
        
class Frame(tk.Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        self.parent = master
       
       
class App(tk.Tk):

    def __init__(self):
    
        super().__init__()
        self.window_setup()
        self.create_frames()
        
    def quit_me(self):
        self.quit()
        self.destroy() 
        print("\nWindow closed.")
        
    def window_setup(self):
        self.title("SO Runner")
        self.iconbitmap("fraunhofer.ico")
        self.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.geometry("800x600+50+50")       
        
    def create_frames(self):
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.upper_frame = Upper_Frame(self, bg="green", bd=5)
        self.upper_frame.grid(row=0, column=0, sticky="nsew")
        
        self.mid_frame = Mid_Frame(self, bg="blue", bd=5)
        self.mid_frame.grid(row=1, column=0, sticky="nsew")
        
        self.lower_frame = Lower_Frame(self, bg="red", bd=5)
        self.lower_frame.grid(row=2, column=0, sticky="nsew")
        # lower_frame.pack_propagate(False)
        
        
class Upper_Frame(Frame):

    def __init__(self, container, **kwargs):
    
        super().__init__(container, **kwargs)
        self.create_frames()
        
    def create_frames(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        
        self.u_left_frame = U_left_Frame(self, bg="yellow")
        self.u_left_frame.grid(row=0, column=0, sticky="nswe")
        
        self.u_right_frame = U_right_Frame(self, bg="black")
        self.u_right_frame.grid(row=0, column=1, sticky="nswe")
        
        
class U_left_Frame(Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        
        self.wk_dir_lbl = tk.Label(self, text="Working directory")
        self.wk_dir_lbl.grid(row=0, column=0, pady=5)
        self.tcl_lbl = tk.Label(self, text="Optimization script")
        self.tcl_lbl.grid(row=1, column=0, pady=5)
        self.eco_lbl = tk.Label(self, text="Ecoinvent dataset directory")
        self.eco_lbl.grid(row=2, column=0, pady=5)
        self.py_lbl = tk.Label(self, text="Python script")
        self.py_lbl.grid(row=3, column=0, pady=5)
        
        
class U_right_Frame(Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        
        self.wk_dir_ent = tk.Entry(self, width=50)
        self.wk_dir_ent.grid(row=0, column=0, pady=5, padx=5)
        self.browse_Btn1 = tk.Button(self, text = "Browse", command=lambda: browse_dir_func(self.wk_dir_ent))
        self.browse_Btn1.grid(row=0, column=1, pady=5)
        
        self.tcl_ent = tk.Entry(self, width=50)
        self.tcl_ent.grid(row=1, column=0, pady=5, padx=5)
        self.browse_Btn2 = tk.Button(self, text = "Browse", command=lambda: browse_file_func(self.tcl_ent, "tcl"))
        self.browse_Btn2.grid(row=1, column=1, pady=5)
        
        self.eco_ent = tk.Entry(self, width=50)
        self.eco_ent.grid(row=2, column=0, pady=5, padx=5)
        self.browse_Btn3 = tk.Button(self, text = "Browse", command=lambda: browse_dir_func(self.eco_ent))
        self.browse_Btn3.grid(row=2, column=1, pady=5)
        
        self.py_ent = tk.Entry(self, width=50)
        self.py_ent.grid(row=3, column=0, pady=5, padx=5)
        self.browse_Btn4 = tk.Button(self, text = "Browse", command=lambda: browse_file_func(self.py_ent, "py"))
        self.browse_Btn4.grid(row=3, column=1, pady=5)        


class Lower_Frame(Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        
        self.start_Btn = tk.Button(self, text = "Run", command=self.start)
        self.start_Btn.pack()
        
    def start(self):
        tcl_file_path = self.parent.mid_frame.L3_frame.tcl_file_path
        tcl = tk.Tcl()
        tcl.eval("source {}".format(tcl_file_path))
        
        
class Mid_Frame(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master = master, **kwargs)
        self.create_frames()
        
    def create_frames(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.M_left_Frame = M_left_Frame(self, relief=tk.RIDGE, bd=5)
        self.M_left_Frame.grid(row=0, column=0, sticky="nsew")
        
        self.M_mid_Frame = M_mid_Frame(self,  relief=tk.RIDGE, bd=5)
        self.M_mid_Frame.grid(row=0, column=1, sticky="nsew")
        
        self.M_right_Frame = M_right_Frame(self,  relief=tk.RIDGE, bd=5)
        self.M_right_Frame.grid(row=0, column=2, sticky="nsew")


class M_left_Frame(Frame):

    def __init__(self, master, **kwargs):
        
        super().__init__(master = master, **kwargs)
        
        self.to_lbl = tk.Label(self, text="Std. Topology Optimization")
        self.to_lbl.grid(row=0, column=0)
        
        self.input_model_lbl = tk.Label(self, text="Input Model")
        self.input_model_lbl.grid(row=1, column=0)
        self.input_model_ent = tk.Entry(self)
        self.input_model_ent.grid(row=1, column=1)
        self.input_model_btn = tk.Button(self, text = "Browse", command=lambda: browse_dir_func(self.input_model_ent))
        self.input_model_btn.grid(row=1, column=2)
        
        self.discrete_factor_lbl = tk.Label(self, text="Discrete factor")
        self.discrete_factor_lbl.grid(row=2, column=0)
        self.discrete_factor_Var = tk.IntVar(value=0)
        self.discrete_factor_spinbox = tk.Spinbox(self, from_=0, to=5, width=5, textvariable=self.discrete_factor_Var, wrap=True,
            # font=Font(family='Helvetica', size=10)
        )
        self.discrete_factor_spinbox.grid(row=2, column=1)
        
        self.volumeFraction_lbl = tk.Label(self, text="Volume fraction")
        self.volumeFraction_lbl.grid(row=3, column=0)
        self.volumeFraction_scale = tk.Scale(self, orient=tk.HORIZONTAL, length=200, from_=0.0, to=1.0, resolution=0.05)
        self.volumeFraction_scale.grid(row=3, column=1)
        
        self.param_study_lbl = tk.Label(self, text="Parameter Study")
        self.param_study_lbl.grid(row=4, column=0)
        
        self.param_lbl = tk.Label(self, text="Parameter")
        self.param_lbl.grid(row=5, column=0)
        algo_var = tk.StringVar()
        self.param_combobox = tk.Combobox
        
        self.algo_combobox = ttk.Combobox(self, textvariable=algo_var)
        
        self.interval_lbl = tk.Label(self, text="Interval")
        self.interval_lbl.grid(row=6, column=0)
        
        self.stepsize_lbl = tk.Label(self, text="Stepsize")
        self.stepsize_lbl.grid(row=7, column=0)
        
class M_mid_Frame(Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        
        
class M_right_Frame(Frame):

    def __init__(self, master, **kwargs):
    
        super().__init__(master = master, **kwargs)
        self.dir1 = tk.Entry(self, width=50)
        self.dir1.grid(row=0, column=0, padx=5)
        self.browse_Btn = tk.Button(self, text = "Browse", command=self.browse_func)
        self.browse_Btn.grid(row=0, column=1)
        

    def browse_func(self):
        self.tcl_file_path = filedialog.askopenfilename(filetypes=[("tcl files", "*.tcl"), ("All files", "*.*")])
        self.dir1.insert(0, self.tcl_file_path)
        
        
def main():
 
    app = App()
    app.mainloop()
    print("\nProgram ended.")
    
if __name__ == "__main__":
    main()
    