emdpler_wrapper
===============

Python wrapper for Emdpler, which is a Fortan 77 program for forward modelling the EM fields due to a vertical or horizontal magnetic dipole, published in this paper:

[Singh, N. P., and Toru Mogi. "EMDPLER: A F77 program for modeling the EM response of dipolar sources over the non-magnetic layer earth models." **Computers & Geosciences** 36, no. 4 (2010): 430-440.](http://dx.doi.org/10.1016/j.cageo.2009.08.009)

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

Download the contents of this Git repository.

Copy the supplementary material from the above paper into the ``emdpler_wrapper`` folder.

Then open a shell and go to the folder containing ``setup.py`` and run:

    PS D:\personal\code\emdpler_wrapper> python setup.py develop
    INFO:__main__:About to compile emdpler...
    DEBUG:__main__:  object_path=emdpler.exe
    DEBUG:__main__:  source_path=Emdpler.for
    DEBUG:__main__:  working_dir=emdpler_wrapper
    DEBUG:__main__:Compiler finished
    DEBUG:__main__:D:\personal\code\emdpler_wrapper\emdpler_wrapper\emdpler.exe
    INFO:__main__:Created D:\personal\code\emdpler_wrapper\emdpler_wrapper\emdpler.exe
    running develop
    running egg_info
    creating emdpler_wrapper.egg-info
    writing emdpler_wrapper.egg-info\PKG-INFO
    writing top-level names to emdpler_wrapper.egg-info\top_level.txt
    writing dependency_links to emdpler_wrapper.egg-info\dependency_links.txt
    writing entry points to emdpler_wrapper.egg-info\entry_points.txt
    writing manifest file 'emdpler_wrapper.egg-info\SOURCES.txt'
    reading manifest file 'emdpler_wrapper.egg-info\SOURCES.txt'
    writing manifest file 'emdpler_wrapper.egg-info\SOURCES.txt'
    running build_ext
    Creating c:\users\kent\anaconda\lib\site-packages\emdpler-wrapper.egg-link (link to .)
    Adding emdpler-wrapper 0.0.0 to easy-install.pth file

    Installed d:\personal\code\emdpler_wrapper
    Processing dependencies for emdpler-wrapper==0.0.0
    Finished processing dependencies for emdpler-wrapper==0.0.0
    PS D:\personal\code\emdpler_wrapper>

Then call the function ``emdpler_wrapper.emdpler.vmd``. See the examples above for more.
