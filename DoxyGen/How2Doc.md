# Rules for API Function documentation
This document describes how to generate Doxygen-style documentation.

## Required setup (Windows):

- Install Doxygen (verified to work with v1.9.6) - https://www.doxygen.nl/download.html
- Install Graphiz (verified to work with v4.73) - http://www.graphviz.org/download/
- Install bash shell (for example git bash for Windows)
- Download PlantUML compiled Jar under Apache license (verified to work with v1.2021.8):
  - download link:  http://sourceforge.net/projects/plantuml/files/plantuml-jar-asl-1.2021.8.zip/download
  - PlantUML page: https://plantuml.com/
  - extract downloaded .zip file
  - add path to plantuml.jar file extracted above to the environment PATH
  - additional PlantUML documentation: https://plantuml-documentation.readthedocs.io/en/latest/index.html

## Build documentation
To generate documentation execute ./gen_doc.sh in bash shell.

## Folder structure

Directory      | Description
:--------------|:--------------------------------------------------
.\Doxygen\                        | Doxygen documentation of Arm Virtual Targets
.\Doxygen\gen_doc.sh              | Script for building documentation
.\Doxygen\Doxygen_Templates\      | Additional files defining styles and appearance
.\Doxygen\\&lt;<i>component</i>&gt;\\&lt;<i>component&gt;</i>.dxy | Doxygen configuration for <i>&lt;component</i>&gt;
.\Doxygen\\&lt;<i>component</i>&gt;\\src\        | Text files describing the <i>&lt;component</i>&gt;
.\Doxygen\\&lt;<i>component</i>&gt;\\src\images\ | Graphic files used by *.txt files
.\Documentation\                  | Documentation output folder
