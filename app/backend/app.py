import connexion

from flask_cors import CORS

from config.db_initializer import init_db
from config.error_handler import init_error_handler
from routes.static_route import init_route

app = connexion.App(__name__, specification_dir='resources/')
app.add_api('swagger.yaml', resolver=connexion.resolver.RestyResolver('api'))
app.app.static_folder = './resources/client/static'
app.app.template_folder = './resources/client'

CORS(app.app)

init_db(app.app)
init_route(app)
init_error_handler(app.app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
