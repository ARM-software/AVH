#!/bin/bash
# Version: 1.0
# Date: 2021-07-27
# This bash script generates AVT Documentation:
#
# Pre-requisites:
# - bash shell (for Windows: install git for Windows)
# - doxygen 
# - graphviz
# - plantuml

set -o pipefail

DIRNAME=$(dirname $(readlink -f $0))
DOXYGEN=$(which doxygen 2>/dev/null)
GVDOT=$(which dot 2>/dev/null)
PLANTUML=$(which plantuml 2>/dev/null)
REGEN=0
ALLPARTS=($(find ${DIRNAME} -mindepth 1 -maxdepth 1 -type d -exec basename {} \;))
PARTS=()

if [[ -z "$*" ]]; then
    REGEN=1
else
    for part in "$*"; do
        if [[ " ${ALLPARTS[@]} " =~ " $part " ]]; then
            PARTS+=($part)
        fi
    done
fi

if [[ ! -f "${DOXYGEN}" ]]; then
    echo "Doxygen not found!" >&2
    echo "Did you miss to add it to PATH?"
    exit 1
else
    version=$("${DOXYGEN}" --version | sed -E 's/.*([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
    echo "Doxygen is ${DOXYGEN} at version ${version}"
    if [[ "${version}" != "1.9.1" ]]; then
        echo "Doxygen should be at version 1.9.1!" >&2
        exit 1
    fi
fi

if [[ ! -f "${GVDOT}" ]]; then
    echo "Graphviz/dot not found!" >&2
    echo "Did you miss to add it to PATH?"
    exit 1
else
    version=$("${GVDOT}" -V 2>&1 | sed -E 's/.*version ([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
    echo "Graphviz/dot is ${GVDOT} at version ${version}"
fi

if [[ ! -f "${PLANTUML}" ]]; then
    echo "PlantUML not found!" >&2
    echo "Did you miss to add it to PATH?"
    exit 1
else
    version=$("${PLANTUML}" -version | grep -E 'PlantUML version' | sed -E 's/.*version ([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
    echo "PlantUML is ${PLANTUML} at version ${version}"
fi

function doxygen {
    partname=$(basename $(dirname $1))
    if [[ $REGEN != 0 ]] || [[ " ${PARTS[@]} " =~ " ${partname} " ]]; then
        pushd "$(dirname $1)" > /dev/null
        echo "${DOXYGEN} $1"
        "${DOXYGEN}" $(basename "$1")
        popd > /dev/null
        
        if [[ $2 != 0 ]]; then
            mkdir -p "${DIRNAME}/../Documentation/${partname}/html/search/"
            cp -f "${DIRNAME}/Doxygen_Templates/search.css" "${DIRNAME}/../Documentation/${partname}/html/search/"
        fi
        
        projectName=$(grep -E "PROJECT_NAME\s+=" $1 | sed -r -e 's/[^"]*"([^"]+)".*/\1/')
        projectNumber=$(grep -E "PROJECT_NUMBER\s+=" $1 | sed -r -e 's/[^"]*"([^"]+)".*/\1/')
        datetime=$(date -u +'%a %b %e %Y %H:%M:%S')
        sed -e "s/{datetime}/${datetime}/" "${DIRNAME}/Doxygen_Templates/footer.js" \
          | sed -e "s/{projectName}/${projectName}/" \
          | sed -e "s/{projectNumber}/${projectNumber}/" \
          > "${DIRNAME}/../Documentation/${partname}/html/footer.js"
    fi
}

function plantuml {
    partname=$(basename $1)
    if [[ $REGEN != 0 ]] || [[ " ${PARTS[@]} " =~ " ${partname} " ]]; then
        pushd "$1" > /dev/null
        echo "${PLANTUML} $1/src/*.uml"
        "${PLANTUML}" ./src/*.uml
        mkdir -p $1/src/images/
        cp -f $1/src/*.png $1/src/images/
        popd > /dev/null
    fi
}

if [[ $REGEN != 0 ]]; then
    echo "Cleaning existing documentation ..."
    find "${DIRNAME}/../Documentation/" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
fi

echo "Generating documentation ..."
doxygen "${DIRNAME}/examples/examples.dxy" 1
doxygen "${DIRNAME}/infrastructure/infrastructure.dxy" 1
doxygen "${DIRNAME}/overview/overview.dxy" 1
plantuml "${DIRNAME}/simulation"
doxygen "${DIRNAME}/simulation/simulation.dxy" 1

exit 0
