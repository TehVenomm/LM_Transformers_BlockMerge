# Language Model Transformer Block Merge
Image Diffusion block merging technique applied to transformers based Language Models.

## Dependencies:
```bash
A basic python install with Transformers and Pytorch.
```
## Usage:
### Start the script via the command
```bash
[On Linux] python ./LM_BlockMerge.py
[On Windows] python LM_BlockMerge.py
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

From the first selected model's folder copy special_tokens_map.json, tokenizer_config.json, vocab.json, and merges.txt into the new model's folder and it's ready to be used in any HF model text generation interface such as KoboldAI or Text-Generation-WebUI.

### Available output settings:
```Python
fp16 = False                # Perform operations in fp16. Saves memory, but CPU inference will not be possible.
always_output_fp16 = True   # If true, will output fp16 even if operating in fp32
max_shard_size = "2000MiB"  # Set output shard size
verbose_info = True         # Will show model information when loading
force_cpu = True            # Only use cpu
```

Supported Models:
 - GPT-J, Opt, Llama

Pseudo-Supported Models:
 - GPT-Neox & Pythia (may work with models smaller than 6b, larger models cause errors while merging), BERT (testing required to validate implementation)

Notes:
 - Performing the operation in FP16 mode halves the memory requirements, but will massively slow down the process of loading up the models on memory;
 - Always outputting in fp16 is preferable to save in storage space, especially if the original weights were quantized down to 16bit already. But if your original models are using 32bit precision, then be sure whether you wish to halve the precision of the resulting file or not.
 - Model loading is automatic; the script determines the model type and adjusts accordingly, no special command-line flags required.
 - Current GPT-NeoX support is sketchy, it tends to have an error mid-merge; it might work on GPT-NeoX and Pythia models of a smaller size 6b or lower for now until a solution is implemented.

To Do:
 - ✔ GUI fix; current User Interface lists layer sliders vertically in a window with no scrollbar, it will be changed to have multiple columns and scrollbars as          necessary.
 - Make LM_BlockMerge.py auto-copy the first selected model's special_tokens_map.json, tokenizer_config.json, vocab.json, and merges.txt into the merged model's folder    upon merge completion.
 - Research GPT-NeoX documentation for special considerations when handling GPT-NeoX layers, adjust GPT-NeoX implementation to support larger GPT-NeoX models.
 - GUI Enhancement; looking into allowing manual entry for layer merge ratios for those who want precise numbers or don't prefer sliders.
 - GUI-less Mode; considering adding support for GUI-less mode for those in a commandline-only environment, ideally the script will open the selected model, generate a template text document with all available layers and let the params be modified in there and the script read/execute the text merge config. (This feature may not be implemented but will look into it.)

 
# Credits:
 - Co-wrote current  LM block merge implementation:
 
      https://github/digitous
 - Original script implementation (Average weights merge):
 
      https://github.com/LostRuins
