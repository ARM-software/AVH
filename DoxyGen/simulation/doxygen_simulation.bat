java -jar "%PLANTUML%" ./src/*.uml
xcopy .\src\*.png .\src\images\*.* /Y
doxygen simulation.dxy
