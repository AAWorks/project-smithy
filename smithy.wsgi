#!/usr/bin/python
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/smithy/")

from smithy import app as application
application.secret_key = os.urandom(32)