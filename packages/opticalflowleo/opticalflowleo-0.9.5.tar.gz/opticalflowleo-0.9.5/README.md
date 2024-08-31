# windflow_leo
A package for deriving atmospheric winds from two overlapping granules of satellites in a LEO (low earth orbit)
train formation, using optical flow of CrIS retrievals of specific humidity (JPSS) or AVHRR imagery (MetOp). Author: T.Rink

This package runs inference on a pre-trained model based on WindFlow: Dense feature tracking of atmospheric winds with deep optical flow:

Vandal, T., Duffy, K., McCarty, W., Sewnath, A., & Nemani, R. (2022). Dense feature tracking of atmospheric winds with deep optical flow, Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining.


To install and run:  
First, you must have Python, Conda and Pip installed. Miniconda is convenient as it comes with Python and Pip:

`conda env create -f opticalflowleo.yml`  
`conda activate opticalflowleo`  
`pip install opticalflowleo`  
`python runner.py`

If you want to clone this project, use this command:

`git clone --recursive https://gitlab.ssec.wisc.edu/rink/windflow_leo.git`

Note: the --recursive flag is needed as this project uses git submodules.
