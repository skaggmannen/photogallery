import hashlib
import logging
import sys

log = logging.getLogger(__name__)

from photogallery.common import init, models

if __name__ == "__main__":
    init()
    
    session = models.Session()
    
    for path in sys.argv[1:]:
        log.info("Adding folder %s...", path)
        f = models.Folder()
        f.path = path
        f.hash = hashlib.md5(f.path).hexdigest()
        session.add(f)
    
    session.commit()
