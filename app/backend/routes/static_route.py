from flask import send_from_directory
import os


def init_route(app):

    @app.route('/')
    def main():
        return send_from_directory('resources/client', 'index.html')

    @app.route('/<path:filename>')
    def main_icons(filename):
        return send_from_directory('resources/client', filename)
