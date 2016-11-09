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

![modules](https://docs.google.com/drawings/d/1A56i6HXJhikkHOtVfNO4qoF10zZ_d4SD5ztqsPuY-EA/pub?w=1094&h=1026)

## Preprocessing

We built a preprocessing tool for extracting raw data from the various media files that were provided. The tool outputs CSV files into a *features* folder which can be accessed for statistical analysis. The CSV files that we can extract are the following:

- **metadata**
    - `features.csv`: filename, duration, explicit, licence, size, title, uploader_id, uploader_login
    - `tf_description.csv`: term frequencies for the video description

## Notebooks



## Traitement en minibatchs

![minibatchs](https://docs.google.com/drawings/d/1iAOM0KxzRnVMzs1XhLfxYdepDBjDmu3OimwHH7BBO5I/pub?w=960&h=846)
