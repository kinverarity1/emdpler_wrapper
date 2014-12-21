# Use the setuptools package if it is available. It's preferred 
# because it creates an exe file on Windows for Python scripts.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


suffix = ""
if os.name == "nt":
    suffix = ".exe"

object_path = "emdpler" + suffix
source_path = "Emdpler.for" 
working_dir = os.path.join(os.path.dirname(__file__), "eminduction")

logger.info("About to compile emdpler...")
logger.debug("\t object_path=" + object_path)
logger.debug("\t source_path=" + source_path)
logger.debug("\t working_dir=" + working_dir)

output = subprocess.check_output(["gfortran", "-o%s" % object_path, source_path], cwd=working_dir, shell=True)
if output:
    logger.debug("Compiler output:\n%s"% output)
else:
    logger.debug("Compiler finished")
exe_path = os.path.join(os.path.abspath(working_dir), object_path)
logger.debug(exe_path)
if os.path.isfile(exe_path):
    logger.info("Created " + exe_path)
else:
    logger.error("Failed to create an executable.")

# Set up Python package

setup(name='eminduction',
      entry_points={'console_scripts': [ 
      #     'EXECUTABLE_NAME = package_name.scripts.script_module_name:entry_function_name'
            ]
      }) 