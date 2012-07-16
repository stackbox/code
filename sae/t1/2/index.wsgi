import sae
from test import app
application = sae.create_wsgi_app(app.wsgifunc())
