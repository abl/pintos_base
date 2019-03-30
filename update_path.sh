#!/bin/bash

# Bash strict mode
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# Changes directory to the actual location of the script.
cd "$(dirname "$(realpath "$0")")";

PINTOS_HOME="$(pwd)"

if [ -f "${HOME}/.pintosrc" ] && ! grep -Fxq "export PINTOS_HOME=\"${PINTOS_HOME}\"" "${HOME}/.pintosrc"
then
  rm "${HOME}/.pintosrc"
fi

if [ ! -f "${HOME}/.pintosrc" ]
then
cat <<EOF > "${HOME}/.pintosrc"
export PINTOS_HOME="${PINTOS_HOME}"
export PATH=\${PATH}:"\${PINTOS_HOME}/pintos/src/utils"
EOF
echo "[INFO] .pintosrc updated; start a new shell or \"source ~/.pintosrc\" before continuing."
fi

SOURCE_PINTOSRC="source \"\${HOME}/.pintosrc\""

if [ -f "${HOME}/.bashrc" ] && ! grep -Fxq "${SOURCE_PINTOSRC}" "${HOME}/.bashrc"
then
  echo "${SOURCE_PINTOSRC}" >> "${HOME}/.bashrc"
  echo "[INFO] .bashrc updated; start a new shell or \"source ~/.pintosrc\" before continuing."
fi

if [ -f "${HOME}/.zshrc" ] && ! grep -Fxq "${SOURCE_PINTOSRC}" "${HOME}/.zshrc"
then
  echo "${SOURCE_PINTOSRC}" >> "${HOME}/.zshrc"
  echo "[INFO] .zshrc updated; start a new shell or \"source ~/.pintosrc\" before continuing."
fi
