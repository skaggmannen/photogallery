# Photogallery

A photo gallery webapp.

## Requirements
You need to have Python (2.7) and PIP installed, and if you're on Linux you need to have `libjpeg-dev` installed in order for the Pillow Python library to be compiled with JPEG support.

Run the following on Ubuntu:

```bash
$ sudo apt-get update && sudo apt-get install python python-pip libjpeg-dev
```

## Setup
Clone the repo and then install using pip:

```bash
$ git clone https://github.com/skaggmannen/photogallery.git
$ cd photogallery
$ pip install -e .
```

Right now you need to manually add the folders you want to scan:

```bash
$ python -m photogallery.parser.add /path/to/folder1 /path/to/folder2
```

After this is done you can start the parser:

```bash
$ python -m photogallery.parser.run
```

Wait for it to complete and then start the server:

```bash
$ python -m photogallery.server
```

Now visit http://localhost:5000/ to view your photogallery.
