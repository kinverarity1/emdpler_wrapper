EM-induction
============

Python tools for electromagnetic (EM) induction forward modelling.

Basically at this stage it's a simple Python wrapper for running Emdpler, which is a Fortan 77 program for forward modelling the EM fields due to a vertical or horizontal magnetic dipole, published in this paper:

Singh, N. P., and Toru Mogi. "EMDPLER: A F77 program for modeling the EM response of dipolar sources over the non-magnetic layer earth models." Computers & Geosciences 36, no. 4 (2010): 430-440.

Available at: http://dx.doi.org/10.1016/j.cageo.2009.08.009

Examples
--------

 - [VMD example #1 - 2-layer model](http://nbviewer.ipython.org/github/kinverarity1/em-induction/blob/master/examples/VMD%20example%20%231%20-%202-layer%20model.ipynb)
 - [VMD example #2 - varying overburden resistivity in 2 layer model](http://nbviewer.ipython.org/github/kinverarity1/em-induction/blob/master/examples/VMD%20example%20%232%20-%20varying%20overburden%20resistivity%20in%202%20layer%20model.ipynb)

Requirements
------------

 - Python 2.6
 - Numpy
 - Fortranformat
 - Emdpler source code
 - gfortran (for automatic compilation of Emdpler)
 - matplotlib (optional, for graphing)

Install
-------

Make sure the requirements are installed:

    $ pip install numpy 
    $ pip install fortranformat

Download the contents of this Git repository here or directly:

    $ git clone https://github.com/kinverarity1/em-induction

Also download the supplementary material from the above paper and copy the file ``Emdpler.for`` into the ``em-induction\eminduction`` folder.

Then open a shell and go to the folder containing ``setup.py`` and run ``python setup.py develop``:

    PS D:\personal\code\em-induction> python setup.py develop
    INFO:__main__:About to compile emdpler...
    DEBUG:__main__:  object_path=emdpler.exe
    DEBUG:__main__:  source_path=Emdpler.for
    DEBUG:__main__:  working_dir=eminduction
    DEBUG:__main__:Compiler finished
    DEBUG:__main__:D:\personal\code\em-induction\eminduction\emdpler.exe
    INFO:__main__:Created D:\personal\code\em-induction\eminduction\emdpler.exe
    running develop
    running egg_info
    writing eminduction.egg-info\PKG-INFO
    writing top-level names to eminduction.egg-info\top_level.txt
    writing dependency_links to eminduction.egg-info\dependency_links.txt
    writing entry points to eminduction.egg-info\entry_points.txt
    reading manifest file 'eminduction.egg-info\SOURCES.txt'
    writing manifest file 'eminduction.egg-info\SOURCES.txt'
    running build_ext
    Creating c:\users\kent\anaconda\lib\site-packages\eminduction.egg-link (link to .)
    Adding eminduction 0.0.0 to easy-install.pth file

    Installed d:\personal\code\em-induction
    Processing dependencies for eminduction==0.0.0
    Finished processing dependencies for eminduction==0.0.0

See the docstrings in ``emdpler.py`` for information on how to call the forward modelling program. It's intended to be simpler than doing it by hand: during the installation it compiles ``emdpler`` using ``gfortran`` and then when you call the forward modelling routine from Python it runs ``emdpler`` in a temporary directory, creating the input files and reading in the output files, and then deleting them all automatically.
