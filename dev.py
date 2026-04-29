import tkinter as tk

root = tk.Tk()
root.title("We Knead Bread")
root.geometry("1920x1080")
root.resizable(True, False)
root.config(background="skyblue")

#main container
main_frame = tk.Frame(root, bg="skyblue")
main_frame.pack(fill="both", expand=True)

#left column
gray_baker_frame = tk.Frame(main_frame, width=640, bg="tomato")
gray_baker_frame.pack(side=tk.LEFT, fill="y", padx=(10, 0), pady=10)

stray_baker_frame = tk.Frame(main_frame, width=640, bg="tomato")
stray_baker_frame.pack(side=tk.RIGHT, fill="y", padx=(0,10), pady=10)

#middle column
middle_frame = tk.Frame(main_frame, bg="skyblue")
middle_frame.pack(padx=10, pady=10)

#top middle box
bread_count_frame = tk.Frame(middle_frame, width=640, height=400, bg="tomato")
bread_count_frame.pack(pady=(0,0))

#bottom middle box
gumbie_frame = tk.Frame(middle_frame, width=640, height=660, bg="tomato")
gumbie_frame.pack(pady=(10,0))


root.mainloop()

