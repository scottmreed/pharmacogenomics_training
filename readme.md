**Websites to Explore / Get to Know**

[Lab Website](https://pharmacogenomics.clas.ucdenver.edu/pharmacogenomics/side-effect/)
     
   •[GTEx](https://gtexportal.org/home/)
   
   •[SIDER](http://sideeffects.embl.de/)
   
   •[ZINC15](https://zinc15.docking.org/substances/)
   
   •[BioTransformer](http://biotransformer.ca/)
   
   •[PHAROS](https://pharos.nih.gov/)
   
   •[ModBase](https://modbase.compbio.ucsf.edu/modbase-cgi/index.cgi)
   
   •[Gnomad](https://gnomad.broadinstitute.org/ )
   

Explore notebooks 1 through 4 (modified from OLCC Cheminformatics course) at your own pace. 
Once comfortable with these, try playing with main.py

1_JupyterNotebookIntro is a Jupyter notebook that shows how the sequence of running blocks of code changes the outcome.

Most everything after main.py requires a server account.

####Directories- where programs are located

Program &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;Lacation 

QuickVina-W &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;/home/boss/qvina

Chimera &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; /home/boss/.local 

LSalign &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; /opt/lsalign 

mgltools &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/opt/mgltools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/ 

jchem cxcalc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/opt/opt/chemaxon/jchemsuite/bin/ 

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

Easier option:
pip install rdkit-pypi

Windows users will use a slightly different command:
C:\> activate my-rdkit-env

In PyCharm go to preferences, Project, Interpreter and:
add select add from the gear box then connect to the
"Existing environment" and find your conda env.

After that, select edit configuration (under Run, e.g.)
Then add that conda env to your configuration for main.py

Then use Sql_connect to query the development mysql server

Finally, try running fpocket or equibind remotely after adding your log in credentials to a .env file

