# Language Model Transformer Block Merge
Image Diffusion block merging technique applied to transformers based Language Models.

## Usage:
### Start the script via the command
```bash
python ./LM_BlockMerge.py
```

### The script will then prompt you for three folders:

1. The first model
   - The first model will be used as a base for the transformers configuration, and will be used as reference when handling the layers and weights.
2. The second model
   - The second model will only be used for providing the secondary layers for the merge.
3. The output folder
   - The resulting model will be saved inside the selected directory, in a folder called `"./this/is/your/chosen_path/"` + `"/converted_model"`
 
The script will then load the weights in memory, according to the precision (32/16 bit) chosen in the configuration header, and will subsequently prompt the user with a popup GUI listing all of the layers available in the selected models.
 
### The user will be able to merge layers according to any strategy, ranging from:
  - Creating the output_model by completely replacing N layers at will;
  - Creating the output_model by chosing an individual mix ratio on N layers;
  - Any mix of the two strategies on N chosen layers.

The layers will be merged according to the individual choices per layer, and the resulting model weights will be saved onto the output folder, alongside the first model's `config.json` file.

### Available output settings:
```Python
fp16 = False                # Perform operations in fp16. Saves memory, but CPU inference will not be possible.
always_output_fp16 = True   # If true, will output fp16 even if operating in fp32
max_shard_size = "2000MiB"  # Set output shard size
verbose_info = True         # Will show model information when loading
force_cpu = True            # Only use cpu
```

Notes:
 - Performing the operation in FP16 mode halves the memory requirements, but will massively slow down the process of loading up the models on memory;
 - Always outputting in fp16 is preferable to save in storage space, especially if the original weights were quantized down to 16bit already. But if your original models are using 31bit precision, then be sure whether you wish to halve the precision of the resulting file or not.

 
# Credits:
 - Co-wrote current  LM block merge implementation:
 
      https://github/digitous
 - Original script implementation (Average weights merge):
 
      https://github.com/LostRuins
