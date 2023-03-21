# Language Model Transformer Block Merge
Image Diffusion block merging technique applied to transformers based Language Models.

## Usage:
###Start the script via the command
```bash
python ./LM_BlockMerge.py
```

###The script will then prompt you for three folders:

 - The first model
 
   The first model will be used as a base for the transformers configuration, and will be used as reference when handling the layers and weigts.
 
 - The second model
 
   The second model will only be used for providing the secondary layers for the selected merge.
 
 - The output folder
 
   The resulting merged layers will be saved inside the selected directory, in a folder called `"./chosen_path/"` + '"/converted_model"'
 
###The script will then load the weights in memory, according to the precision (32/16 bit) chosen in the configuration header, and will subsequently prompt the user with a popup GUI listing all of the layers available in the selected models.
 
###The user will be able to merge layers according to any strategy, ranging from 
  - Creating the output_model by completely replacing N layers at will;
  - Creating the output_model by chosing an individual mix ratio on N layers at will
  - Any mix of the two strategies on N chosen layers.
 
# Credits:
 - Co-wrote current block merge implementation:
https://github/digitous
 - Original script implementation (Average weights merge):
https://github.com/LostRuins
