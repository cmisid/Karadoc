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

```sh
conda create -n karadoc numpy scipy scikit-learn matplotlib python=3
```

Then, launch it with:

```sh
# Linux and Mac OS X
$ source activate karadoc
# Windows
$ activate karadoc
```


## Dependencies

Install python dependencies with:

```sh
$ pip install -r requirements.txt
```


## Install OpenCV3

Since you are inside the virtual env, you can install OpenCV (Open Source library for Computer Vision):

```sh
$ conda install -c https://conda.binstar.org/menpo opencv3
```

You can then test if `opencv3` is correctly by typing the following command:

```sh
$ python -c "import cv2; print(cv2.__version__)"
>>> 3.1.0
```


## Install required NLTK corpuses

First, make sure NLTK is correctly installed.

```sh
$ python -c "import nltk; print(nltk.__version__)"
>>> 3.1
```

For certain tasks, NLTK requires extra data (ie. stop words). Running the following command will install the necessary data for lemmatization:

```sh
python -m nltk.downloader wordnet
```

# Architecture

![modules](https://docs.google.com/drawings/d/1A56i6HXJhikkHOtVfNO4qoF10zZ_d4SD5ztqsPuY-EA/pub?w=1094&h=1026)

## Preprocessing

We built a preprocessing tool for extracting raw data from the various media files that are available. The tool outputs CSV files into a *features/* folder which can be accessed for statistical analysis. The CSV files that we can extract are the following:

- **metadata**
    - `features.csv`: filename, duration, explicit, licence, size, title, uploader_id, uploader_login
    - `tf_description.csv`: term frequencies for the video descriptions
    - `tf_keywords.csv`: term frequencies for the video keywords
    - `tf_titles.csv`: term frequencies for the video titles
- **shots**
- **trans**
- **videos**

## Notebooks

Some analytics notebooks are available in the `notebooks` directory. To edit them, you just need to do:

```sh
$ jupyter notebook notebooks/
```

## Traitement en minibatchs

![minibatchs](https://docs.google.com/drawings/d/1iAOM0KxzRnVMzs1XhLfxYdepDBjDmu3OimwHH7BBO5I/pub?w=960&h=846)
