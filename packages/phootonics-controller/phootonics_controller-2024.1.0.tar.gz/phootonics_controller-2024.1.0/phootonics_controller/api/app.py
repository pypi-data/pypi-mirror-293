__author__ = 'olgare'
__copyright__ = "Copyright 2021, Alpes Lasers SA"

import logging

logging.basicConfig(level=logging.INFO)

import argparse
import os
import sys
from time import sleep

from flask import Flask
from flask.json import jsonify
from flask_restful import Api, Resource, abort
from flask_restful.reqparse import RequestParser

from phootonics_controller.base_controllers.config import WL_INCREMENT
from phootonics_controller.base_controllers.main_controller import MainController, AlreadyScanningException, \
    ControllerNotReady


logger = logging.getLogger(__name__)




def argsbool(value):
    if value == 't':
        return True
    elif value == 'f':
        return False
    else:
        raise ValueError('undefined value {}'.format(value))


app = Flask(__name__)

api = Api(app)


class ControllerResource(Resource):

    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        super(ControllerResource, self).__init__(*args, **kwargs)


class Info(ControllerResource):

    def get(self):
        monitoring_info = self.controller.get_monitoring_data()
        return jsonify({'monitoring': monitoring_info,
                        'scan_running': self.controller.is_scan_command_running(),
                        'scan': self.controller.get_results()})


def _pos_parser(x):
    return list(x)


scan_post_parser = RequestParser()
scan_post_parser.add_argument('positions', type=_pos_parser, required=True,
                              action='append',
                              help='list of (x, y) positions, example [(0.0, 0.0), (1.0, 0.0), ...]',
                              location=['json'])
scan_post_parser.add_argument('wl_step', type=float, required=False,
                              location=['json'],
                              default=WL_INCREMENT)
scan_post_parser.add_argument('wavelength', type=float, required=False,
                              location=['json'])


class ScanStart(ControllerResource):

    def post(self):
        args = scan_post_parser.parse_args()
        if self.controller.is_scan_command_running():
            abort(403, message='scan command already running')
        try:
            self.controller.start_scan(positions=args.positions, wl_step=args.wl_step,
                                       wavelength=args.wavelength)
        except AlreadyScanningException:
            abort(403, message='scan command already running')
        except ControllerNotReady:
            abort(403, message='controller not ready. Are all subsystems initialized?')


fast_scan_post_parser = RequestParser()
fast_scan_post_parser.add_argument('wl_step', type=float, required=False,
                                   location=['json'],
                                   default=WL_INCREMENT)
fast_scan_post_parser.add_argument('amplitude_x', type=float, required=False,
                                   location=['json'],
                                   default=1)
fast_scan_post_parser.add_argument('amplitude_y', type=float, required=False,
                                   location=['json'],
                                   default=1)


class FastScanStart(ControllerResource):

    def post(self):
        args = fast_scan_post_parser.parse_args()
        if self.controller.is_scan_command_running():
            abort(403, message='scan command already running')
        try:
            self.controller.start_fast_scan(wl_step=args.wl_step, amplitude_x=args.amplitude_x,
                                            amplitude_y=args.amplitude_y)
        except AlreadyScanningException:
            abort(403, message='scan command already running')
        except ControllerNotReady:
            abort(403, message='controller not ready. Are all subsystems initialized?')




class ScanStop(ControllerResource):

    def post(self):
        self.controller.stop_scan()


test_mode = (os.environ.get('PHOOTC_TEST_MODE', False) == 'MOCK')

controller = MainController(test_mode=test_mode)

try:
    controller.start()
except Exception as e:
    controller.shutdown_all_systems()
    raise


api.add_resource(Info, '/info',
                 resource_class_kwargs={'controller': controller})
api.add_resource(ScanStart, '/scan/start/default',
                 resource_class_kwargs={'controller': controller})
api.add_resource(FastScanStart, '/scan/start/fast',
                 resource_class_kwargs={'controller': controller})
api.add_resource(ScanStop, '/scan/stop',
                 resource_class_kwargs={'controller': controller})


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=5555)
    args = parser.parse_args()
    try:
        app.run(host='0.0.0.0', port=args.p)
    finally:
        controller.shutdown_all_systems()


if __name__ == '__main__':
    run()