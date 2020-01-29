#!/bin/bash

echo Script instalación complementos NLP

echo Instalación de varios paquetes

  sleep 1s

  cd /home/

  sudo apt-get update
  
  sudo apt-get install python3-pip
  pip3 install virtualenv
  pip install jupyterlab

  sudo apt-get upgrade
