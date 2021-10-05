@echo off

REM ====================================================================================
REM Batch file for generating
REM
REM Author  :
REM Date    : 13th July 2021
REM Version : 0.1
REM Company : ARM
REM
REM
REM Command syntax: genDoc.bat
REM
REM  REM  Version: 0.1 Initial Version.
REM ====================================================================================

SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM -- Specify path to plantuml.jar here ---------------------
SET PLANTUML=C:\Program Files\PlantUML\plantuml.jar

REM -- Delete previous generated HTML files ---------------------
  ECHO.
  ECHO Delete previous generated HTML files

REM -- Remove existing documentation ---------------------
PUSHD ..\Documentation
FOR %%A IN (overview) DO IF EXIST %%A (RMDIR /S /Q %%A)
FOR %%A IN (simulation) DO IF EXIST %%A (RMDIR /S /Q %%A)
FOR %%A IN (infrastructure) DO IF EXIST %%A (RMDIR /S /Q %%A)
FOR %%A IN (examples) DO IF EXIST %%A (RMDIR /S /Q %%A)
POPD

REM -- Generate New HTML Files ---------------------
  ECHO.
  ECHO Generate New HTML Files

pushd overview
CALL doxygen_overview.bat
popd

pushd simulation
CALL doxygen_simulation.bat
popd

pushd infrastructure
CALL doxygen_infra.bat
popd

pushd examples
CALL doxygen_examples.bat
popd

REM -- Copy search style sheet ---------------------
  ECHO.
  ECHO Copy search style sheets
copy /Y Doxygen_Templates\search.css ..\Documentation\overview\html\search\.
copy /Y Doxygen_Templates\search.css ..\Documentation\simulation\html\search\.
copy /Y Doxygen_Templates\search.css ..\Documentation\infrastructure\html\search\.
copy /Y Doxygen_Templates\search.css ..\Documentation\examples\html\search\.


:END
  ECHO.
REM done
