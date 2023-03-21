import os
import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

#mixer output settings

fp16 = False                 #perform operations in fp16. Saves memory, but CPU inference will not be possible.
always_output_fp16 = True   #if true, will output fp16 even if operating in fp32
max_shard_size = "2000MiB"  #set output shard size
verbose_info = True        #will show model information when loading
force_cpu = True            #only use cpu

# Create a GUI for selecting the first and second models, and save path for merged model
root = tk.Tk()
#root.withdraw()

# Ask user to select the first model
print("Opening file dialog, please select FIRST model directory...")
first_model_path = filedialog.askdirectory(title="Select the first model")

# Ask user to select the second model
print("Opening file dialog, please select SECOND model directory...")
second_model_path = filedialog.askdirectory(title="Select the second model")

# Ask user to select the save path for the merged model
print("Opening file dialog, please select OUTPUT model directory...")
merged_model_path = filedialog.askdirectory(title="Select where to save the merged model")

if not first_model_path or not second_model_path:
    print("\nYou must select two directories containing models to merge and one output directory. Exiting.")
    exit()

with torch.no_grad(): 
    if fp16:
        torch.set_default_dtype(torch.float16)
    else:
        torch.set_default_dtype(torch.float32)

    device = torch.device("cuda") if (torch.cuda.is_available() and not force_cpu) else torch.device("cpu")
    print(device)
    
    # Load the first and second models
    print("Loading Model 1...")
    first_model = AutoModelForCausalLM.from_pretrained(first_model_path)
    first_model = first_model.to(device)
    first_model.eval()
    print("Model 1 Loaded. Dtype: " + str(first_model.dtype))
    
    print("Loading Model 2...")
    second_model = AutoModelForCausalLM.from_pretrained(second_model_path)
    second_model = second_model.to(device)
    second_model.eval()
    print("Model 2 Loaded. Dtype: " + str(second_model.dtype))
    
    # Determine the number of layers in the first model
    num_layers = first_model.config.num_hidden_layers
    #num_layers = len(first_model.transformer.h)
    #model.transformer.h
    #num_layers = len(first_model.encoder.layer)

    # Create a GUI for selecting merge ratios for each layer
    class LayerSlider(tk.Frame):
        def __init__(self, parent, layer_num):
            super().__init__(parent)
            
            self.layer_num = layer_num
            
            # Create a label for the layer slider
            self.layer_label = tk.Label(self, text=f"Layer {layer_num}")
            self.layer_label.grid(row=0, column=0)
            
            # Create a slider for the merge ratio
            self.slider = tk.Scale(self, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)
            self.slider.grid(row=0, column=1)
            
    # Create a window with sliders for each layer
    layer_sliders = []
    for i in range(num_layers):
        layer_slider = LayerSlider(root, i)
        layer_slider.pack()
        layer_sliders.append(layer_slider)

# Create a "commit and merge" button
def merge_models():
    with torch.no_grad(): 
        # Read the merge ratios from the sliders
        merge_ratios = [layer_slider.slider.get() for layer_slider in layer_sliders]
        
        #    # Check that the merge ratios add up to 1
        #    if sum(merge_ratios) != 1:
        #        messagebox.showerror("Error", "Merge ratios must add up to 1")
        #        return
        
        # Merge the models using the merge ratios
        for i in range(num_layers):
            # Determine how much of each layer to use from each model
            first_ratio = merge_ratios[i]
            second_ratio = 1 - first_ratio
            
            # Merge the layer from the two models
            merged_layer = (first_model.transformer.h[i].state_dict(), second_model.transformer.h[i].state_dict())        
            for key in merged_layer[0].keys():
                merged_layer[0][key] = first_ratio * merged_layer[0][key] + second_ratio * merged_layer[1][key]
                
            if verbose_info:
               print("Merging tensor "+str(i))
            pass
            
            # Create the merged model by replacing the layers in the second model with the merged layers
            second_model.transformer.h[i].load_state_dict(merged_layer[0])
            if verbose_info:
               print("Migrating tensor "+str(i))
            pass
        
        # Save the merged model to the specified path
        if merged_model_path:
            print("Saving new model...")
            newsavedpath = merged_model_path+"/converted_model"
            
            if always_output_fp16 and not fp16:
                second_model.half()
                
            second_model.save_pretrained(newsavedpath, max_shard_size=max_shard_size)
            print("\nSaved to: " + newsavedpath)
        else:
            print("\nOutput model was not saved as no output path was selected.")
        
        # Close the GUI
        root.destroy()

commit_button = tk.Button(root, text="Commit and Merge", command=merge_models)
commit_button.pack()

# Run the GUI
root.mainloop()
