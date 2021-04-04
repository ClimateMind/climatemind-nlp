# ClimateMind NLP

Contains the code & data that powers ClimateMind's NLP efforts

## Getting Started

## Folder Structure 
- `data/` : When applicable, relases of the data we used can be found in this directory
- `notebooks/` : Contains the jupyter notebooks used by the team during development
- `tools/` : Any data annotation tools, or helper code used during development can be found here
- `src/` : Production code can be found here

## Dev Practices 

### Issues
Avaible issues & tickets can be found in our internal Jira.

### Pull Requests
Pull Requests require 1 approving review from a team member before being merged, we also use Github's CodeQL for the Python code security checks.

### Documentation

### Package Manager
=======
This repo uses Miniconda3 to manage the python version and package dependencies.

If you have a macOS, you can install Miniconda from homebrew simply by runing `brew install --cask miniconda`.
If you are using Linux or Windows, you can follow the installation guide for Linux [https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html] and for Windows [https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html].

Type `conda` in your terminal to confirm installation success.

***Change the directory to your cloned version of this NLP repo, then follow the instructions below.***

Install the conda environment by doing:
```
conda env create -f environment.yml
```

Once installed, activate the environment by doing:
```
conda activate nlp_env
```

If you are having problem with the conda activate command, you might want to take a look at this stackoverflow thread.
https://stackoverflow.com/questions/47246350/conda-activate-not-working

If the code dependencies in this repo have changed or update, you will need to update your conda environment by doing:
```
conda env update -f environment.yml
``` 


Adding Conda to Jupyter Notebook
Unfortunately, installing miniconda on your terminal does not mean it will be working in Jupyter Notebook.
To be able to select a conda environment as the kernel in Jupyter, you need to install `ipykernel` in that environment.

```
conda activate condaenv
conda install ipykernel
python3 -m ipykernel install --user --name nlp_env --display-name "nlp_env"
```

Once you have done this, you could start up the notebook by using the `jupyter notebook` command and then open any .ipynb notebook. 
Inside that notebook, select the menu Kernel > Change kernel > nlp_env to activate the conda environment kernel.



To remove Conda environments from the cache to free up RAM space, run:
```
conda clean --all
```

How to run the Climate Mind NLP scripts:
1. Install and activate the Conda environment following the instructions in the above sections of this readme.
2. Run any if the python scripts in the activated Conda environment.
