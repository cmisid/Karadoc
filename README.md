# Karadoc :hamburger:

:movie_camera: :sound: :page_facing_up: TOOL USED TO TAG SOME VIDEOS OF MEDIAEVAL CHALLENGE

<p align="center">
  <a href="https://travis-ci.org/cmisid/Karadoc">
    <img alt="Build Status" src="https://travis-ci.org/cmisid/Karadoc.svg?branch=master">
  </a>
</p>

<p align="center">
	<img alt="cover" src="img/cover.png">
</p>

# Installation

## Updating to the latest version of Anaconda

1. Install the release version of [`Anaconda`](https://www.continuum.io/downloads).
2. Follow the instructions below.

Create a new virtual environment:
```
conda create -n karadoc python=3
```
Then, launch it with:
```
# Linux and Mac OS X
source activate karadoc
# Windows
activate karadoc
```

## Dependencies

Install python dependencies with:
```
pip install -r requirements.txt
```

# Architecture

## Modules

![modules](https://docs.google.com/drawings/d/1A56i6HXJhikkHOtVfNO4qoF10zZ_d4SD5ztqsPuY-EA/pub?w=1094&h=1026)

1. :green_heart: **Module de preprocessing**. A partir des différents jeux de données, on extrait plusieurs matrices contenant des features.
2. :yellow_heart: **Module d'apprentissage**. A partir des matrices de features, on entraîne des classifieurs qu'on sauvegarde par la suite.
3. :blue_heart: **Module de classification**. On peut classifier des nouveaux documents en utilisant le module de preprocessing puis en faisant appel aux classifieurs sauvegardés.

## Traitement en minibatchs

![minibatchs](https://docs.google.com/drawings/d/1iAOM0KxzRnVMzs1XhLfxYdepDBjDmu3OimwHH7BBO5I/pub?w=960&h=846)
