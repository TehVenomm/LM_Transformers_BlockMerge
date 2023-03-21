from tkinter import *


num_layers = 11
root = Tk()
frame = Frame(root)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="news")
grid = Frame(frame)
grid.grid(sticky="news", column=0, row=7, columnspan=2)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
x = 0
y = 0
layer_sliders = []

#example values
for i in range(num_layers):
    
    slider = Scale(frame, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, length=200)
    slider.grid(column=y, row=(x+1))
    # Create a label for the layer slider
    layer_label = Label(frame, text=f"Layer {i}")
    layer_label.grid(column=y, row=x, sticky='sw')
    #layer_label.place(relx=0.1)
    
    # Create a slider for the merge ratio
    

    #layer_slider = LayerSlider()
    #layer_slider.pack()
    #layer_sliders.append(layer_slider)


    #btn = Button(frame)
    #btn.grid(column=y, row=x, sticky="news")
    y += 1
    if (y % 5 == 0):
        x += 2
        y = 0

frame.columnconfigure(tuple(range(5)), weight=1)
frame.rowconfigure(tuple(range(x+1)), weight=1)

root.mainloop()
