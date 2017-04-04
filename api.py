import subprocess
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('command')
parser.add_argument('station_code')


class StationNotFoundException(Exception):
    pass


class Radio:
    stations = [
        {'station_code': 'radio_rock', 'station': 'Radio Rock',
         'url': 'http://icelive0.80692-icelive0.cdn.qbrick.com/10565/80692_RadioRock.mp3'}
    ]

    @classmethod
    def get_url(cls, station_code):
        for station in cls.stations:
            if station['station_code'] == station_code:
                return station['url']
        raise StationNotFoundException('{} not found'.format(station_code))

    @classmethod
    def get_stations(cls):
        return cls.stations


class RadioAPI(Resource):

    def get(self):
        return Radio.get_stations()

    def post(self):
        args = parser.parse_args()
        command = args['command']
        station_code = args['station_code']

        if command == 'start':
            print("Starting {}".format(station_code))
            print(subprocess.Popen(["mplayer", Radio.get_url(station_code)]))
            print("Success")
        if command == 'stop':
            print("Stopping {}".format(station_code))
            print(subprocess.call(["killall", "mplayer"]))
            print("Success")


api.add_resource(RadioAPI, '/')

if __name__ == '__main__':
    app.run(debug=True)
