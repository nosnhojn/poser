# Poser

Generate placeholder Verilog modules for early stage physical design layout, etc. before real RTL is complete. Poser parses a Verilog file, extracting pertinent module IO and parameters information, then generates a poser module with the same IO footprint but with randomly generated internal logic. Poser modules of different sizes can be created by estimating flop counts and relative size based on IO count.

# Usage

'''usage: poser.py [-h] -f FLOPS -s {xs,s,m,l,xl,xxl,xxxl} -v file -i input width
                -o output width

Create a verilog module based on flop and size estimates.

optional arguments:
  -h, --help            show this help message and exit
  -f FLOPS, --flops FLOPS
                        estimated number of flops.
  -s {xs,s,m,l,xl,xxl,xxxl}, --size {xs,s,m,l,xl,xxl,xxxl}
                        relative size estimate.
  -v file, --verilog file
                        path to the verilog file with an existing moduel
                        definition.
  -i input width, --inputs input width
                        Minimum effective input width (i.e. if all inputs were
                        concatentated into 1 vector)
  -o output width, --outputs output width
                        Minimum effective output width (i.e. if all outputs
                        were concatentated into 1 vector)'''

# Examples 

For a large Verilog module in myFile.v with approximately 128 flops, 38 input pins and 41 output pins:

>python3 poser.py -f 128 -s l -v myFile.v -i 38 -o 41
