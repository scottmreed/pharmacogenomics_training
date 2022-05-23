From this starting point, try downloading the structure of a 
few drug molecules and calculating their logp and saving a figure.

Create a branch and commit your output to a branch with your name when done.

To run this script you will need rdkit installed using the following instructions:

How to install RDKit with Conda
Creating a new conda environment with the RDKit installed requires one single command similar to the following::
$ conda create -c conda-forge -n my-rdkit-env rdkit
Finally, the new environment must be activated so that the corresponding python interpreter becomes available in the same shell:
$ conda activate my-rdkit-env
If for some reason this does not work, try:
$ cd [anaconda folder]/bin
$ source activate my-rdkit-env
Windows users will use a slightly different command:
C:\> activate my-rdkit-env

In PyCharm go to preferences, Project, Interpreter and:
add select add from the gear box then connect to the
"Existing environment" and find your conda env.

After that, select edit configuration (under Run, e.g.)
Then add that conda env to your configuration for main.py
