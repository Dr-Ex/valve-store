from flask import Flask
website = Flask(__name__)

import public.datamanager
import public.routes