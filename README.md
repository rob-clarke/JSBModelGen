# JSBSim MXS2 Model

The files here implement a JSBSim version of the MXS2 model via JSBSim's Python bindings. Along with the JSBSim Python
bindings, the model also has a requirement on `xacro`. It is used to generate the actual the XML file used by JSBSim
from an initial file to allow for code re-use. `xacro` allows for macros to be used to programatically generate XML
from within an XML file, rather than generating the entire file.

# Makefile targets:

- `install`: Install the two Python requirements from the `requirements.txt` file
- `xacro`: Generate the actual aircraft XML from the `.xacro` version
- `test`: Run the test script (`mxs2_jsb.py`)

Running 
