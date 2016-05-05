# Poser

Generate placeholder Verilog modules for early stage physical design layout, etc. before real RTL is complete. Poser parses a Verilog file, extracting pertinent module IO and parameter information, then generates a poser module with the same IO footprint but with randomly generated internal logic. Poser modules of different sizes can be created through estimated flop counts and relative size based on IO count.

# Usage

```
usage: poser.py [-h] -f FLOPS -s {xs,s,m,l,xl,xxl,xxxl} -v FILE -i INPUT_PINS -o OUTPUT_PINS

Create a verilog module based on flop and size estimates.

optional arguments:
  -h, --help                                               show this help message and exit
  -f FLOPS, --flops FLOPS
                                                           estimated number of flops.
  -s {xs,s,m,l,xl,xxl,xxxl}, --size {xs,s,m,l,xl,xxl,xxxl}
                                                           relative size estimate.
  -v FILE, --verilog FILE
                                                           path to the verilog file with an existing module
                                                           definition.
  -i INPUT_PINS, --inputs INPUT_PINS
                                                           Total number of input pins.
  -o OUTPUT_PINS, --outputs OUTPUT_PINS
                                                           Total number of output pins.
```

# Examples 

For a relatively large Verilog module in module.v with approximately 128 flops, a total of 38 input pins and 41 output pins:
```
python3 bin/poser.py --flops 128 --size l --verilog module.v --inputs 38 --outputs 41 > poserModule.v
```
The poser module is written to STDOUT (or poserModule.v with the redirect). It can be included in place of the real module.v for synthesis, etc. Note: the poserModule.v requires verilog/poserCell.v and verilog/PoserMux.v (these are structures used to build the internals of the poser module).

# Contact

neil.johnson@agilesoc.com
