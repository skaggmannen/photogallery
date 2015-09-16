# Photogallery

A photo gallery webapp.

## Setup
Clone the repo and then install using pip:

```bash
$ git clone https://github.com/skaggmannen/photogallery.git
$ cd photogallery
$ pip install -e .
```

Right now you need to manually add the folders you want to scan from the Python console:

```python
import hashlib
from photogallery.common import models, init

init()

f = models.Folder()
f.path = "/path/to/photos"
f.hash = hashlib.md5(f.path).hexdigest()

session = models.Session()
session.add(f)
session.commit()
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
