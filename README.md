# Photogallery

A photo gallery webapp.

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
