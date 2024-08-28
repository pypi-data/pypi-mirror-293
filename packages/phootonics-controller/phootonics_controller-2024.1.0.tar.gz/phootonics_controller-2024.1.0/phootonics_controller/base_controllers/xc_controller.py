
# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import logging
import time
import requests
from requests.auth import HTTPBasicAuth

from phootonics_controller.base_controllers.config import configuration_dictionary, TEMP_STAB_TIMEOUT_SEC
from phootonics_controller.utils.vcm_resources.base_controller import BaseController


logger = logging.getLogger(__name__)


target_wavelength = 1000


class ECController(BaseController):
    RESPONDING = 'RESPONDING'
    NOT_RESPONDING = 'NOT_RESPONDING'
    READY = 'READY'
    NOT_READY = 'NOT_READY'

    def __init__(self, ec_url, index, monitor_interval):
        super(ECController, self).__init__(monitor_interval=monitor_interval)
        self._driver = None
        self.index = index
        self.s2params = configuration_dictionary[self.index]['s2params']
        self.temperature = configuration_dictionary[self.index]['temperature_setpoint']
        self._device_status = None
        self._ec_client_url = ec_url
        self._stage_responsive = None
        self._stage_status = None
        self._pulser_responsive = None
        self._pulser_status = None
        self._tc_responsive = None
        self._tc_status = None

    def _connected_status(self):
        if self._stage_responsive and self._pulser_responsive and self._tc_responsive:
            return ECController.RESPONDING
        else:
            return ECController.NOT_RESPONDING

    def _check_connection(self):
        try:
            info_xc = self._driver.info_xc()
            self._pulser_status = info_xc['response']['data']['pulser']['status']
            self._tc_status = info_xc['response']['data']['tc']['status']
            self._stage_status = info_xc['response']['data']['stage']['status']
            if self._pulser_status == -1 or self._pulser_status == 2000 or self._pulser_status == 2001:
                self._pulser_responsive = False
                logging.error('pulser unresponsive: {}'.format(self._pulser_status))
            if self._tc_status == -1 or self._tc_status == 4002:
                self._tc_responsive = False
                logging.error('tc unresponsive: {}'.format(self._tc_status))
            if self._stage_status == -1 or self._stage_status == 3000 or self._stage_status == 3003 or self._stage_status == 3004:
                self._stage_responsive = False
                logging.error('stage unresponsive: {}'.format(self._stage_status))
            if self._pulser_responsive == False or self._stage_responsive == False or self._tc_responsive == False:
                logging.error('Some devices failed the connection check')
                raise
        except Exception as e:
            logging.error('connection error {}'.format(e))
            raise
        self._pulser_responsive = True
        self._tc_responsive = True
        self._stage_responsive = True
        return True

    def _connect(self):
        if self._driver is None:
            self._driver = ECClient(base_url=self._ec_client_url)

    def _disconnect(self):
        self._driver = None

    def xc_ready_to_action(self):
        try:
            if self._pulser_status in [2003, 2004] and self._tc_status in [4000, 4003] and self._stage_status == 3001:
                return ECController.READY
            else:
                return ECController.NOT_READY
        except Exception as e:
            logging.exception(e)
            return ECController.NOT_READY

    def get_absolute_position(self, rel_position):
        return configuration_dictionary[self.index]['x_position'] + rel_position

    def get_absolute_position_y(self, rel_position):
        return configuration_dictionary[self.index]['y_position'] + rel_position

    def get_rel_position(self, abs_position):
        return abs_position - configuration_dictionary[self.index]['x_position']

    def get_rel_position_y(self, abs_position):
        return abs_position - configuration_dictionary[self.index]['y_position']

    def shutdown(self):
        try:
            self._driver.shutdown_xc()
        except Exception as e:
            logging.exception('shutdown error {}'.format(e))

    def system_info(self):
        return self._driver.info_xc()

    def stop_pulsing(self):
        try:
            self._driver.shut_down_s2()
        except Exception as e:
            logging.error('could not turn pulsing OFF {}'.format(e))

    def get_wavelength(self):
        try:
            return self._driver.get_wavelength()
        except Exception as e:
            logging.error('Cannot read wavelength {}'.format(e))

    def set_temperature_sync(self):
        logging.info('Stabilizing temperature {}'.format(self.temperature))
        self._driver.set_controlled_temperature(self.temperature)

    def activate_s2(self):
        try:
            self.set_temperature_sync()
            logging.info('Set S-2 settings {}'.format(self.s2params))
            self._driver.s2_set_settings(self.s2params)
        except Exception as e:
            logging.error('Error in activating S2 {}'.format(e))

    def move_to_wavelength(self, wl, timeout=0):
        self._driver.move_to_wavelength(wl, timeout)


class MockECController(BaseController):

    RESPONDING = 'RESPONDING'
    NOT_RESPONDING = 'NOT_RESPONDING'
    READY = 'READY'
    NOT_READY = 'NOT_READY'

    def __init__(self, index, monitor_interval):
        super(MockECController, self).__init__(monitor_interval=monitor_interval)
        self._driver = None
        self.index = index
        self.s2params = configuration_dictionary[self.index]['s2params']
        self.temperature = configuration_dictionary[self.index]['temperature_setpoint']
        self._device_status = None
        self._stage_responsive = None
        self._stage_status = None
        self._pulser_responsive = None
        self._pulser_status = None
        self._tc_responsive = None
        self._tc_status = None

    def _connected_status(self):
        return ECController.RESPONDING

    def _check_connection(self):
        self._pulser_responsive = True
        self._tc_responsive = True
        self._stage_responsive = True
        return True

    def _connect(self):
        pass

    def _disconnect(self):
        pass

    def xc_ready_to_action(self):
        return ECController.READY

    def get_absolute_position(self, rel_position):
        return 0.0

    def get_absolute_position_y(self, rel_position):
        return 0.0

    def get_rel_position(self, abs_position):
        return 0.0

    def get_rel_position_y(self, abs_position):
        return 0.0

    def shutdown(self):
        pass

    def system_info(self):
        return {'response': {'data': {}}}

    def stop_pulsing(self):
        pass

    def get_wavelength(self):
        return 1.0

    def activate_s2(self):
        pass

    def move_to_wavelength(self, wl, timeout=20):
        pass

    def set_temperature_sync(self):
        pass


class MotorStabilizationTimeout(Exception):
    pass


class TemperatureStabilizationTimeout(Exception):
    pass


class ECClient:
    def __init__(self, base_url,
                 temperature_tolerance=0.5,
                 temperature_stab_time=10.0,
                 temperature_stab_timeout=TEMP_STAB_TIMEOUT_SEC):
        self.baseUrl = base_url
        self.auth = HTTPBasicAuth(username='admin1',
                                  password='12345')
        self.requestTimeout = 10
        self.wlTolerance = 0.1
        self.tempTol = temperature_tolerance
        self.stabTime = temperature_stab_time
        self.stabTimeout = temperature_stab_timeout

    def _get(self, path, params=None, timeout=None):
        rsp = requests.get(self.baseUrl + path, params=params, auth=self.auth, timeout=timeout or self.requestTimeout)
        rsp.raise_for_status()
        return rsp.json()

    def _post(self, path, params=None, timeout=None, success_code=0):
        rsp = requests.post(self.baseUrl + path, json=params, auth=self.auth, timeout=timeout or self.requestTimeout)
        rsp.raise_for_status()
        response = rsp.json()['response']
        if not response['code'] == success_code:
            raise Exception(response)
        return rsp.json()

    def _is_wl_within_tolerance(self, wl_target, wl_now):
        return abs(wl_now - wl_target) < self.wlTolerance

    def move_to_wavelength(self, wl, timeout=0):
        self._post('/stage/wavelength', params={'wavelength': wl}, success_code=3011)
        if timeout == 0:
            return
        start_time = time.time()
        while True:
            status = self._get('/stage/status')['response']['code']
            if status == 3001:
                break
            if time.time() - start_time > timeout:
                raise MotorStabilizationTimeout
            time.sleep(max(timeout/100.0, 0.05))

    def s2_set_settings(self, settings):
        pp = settings
        if 'pulsing_mode' in settings:
            pp['pulse_mode'] = settings['pulsing_mode']
        if 'applied_voltage' in settings:
            pp['output_voltage'] = settings['applied_voltage']
        self._post('/driver/settings', params=pp)


    def s2_get_settings(self):
        return

    def s2_measure(self):
        v = self._get('/driver/voltage')['response']['data']
        c = self._get('/driver/current')['response']['data']
        return {'measured_current': c['output_current'],
                'measured_voltage': v['output_voltage']}

    def wait_instrument_ready(self, timeout):
        time.sleep(timeout)

    def shut_down_s2(self):
        self.s2_set_settings(dict(applied_voltage=0.0, pulsing_mode='off'))

    def get_temperature(self):
        rsp = self._get('/tc/temperature')['response']['data']
        return rsp['temperature']

    def get_wavelength(self):
        wl_now = self._get('/stage/wavelength')['response']['data']['wavelength']
        return wl_now

    def set_temperature(self, temp):
        self._post('/tc/temperature', params=dict(temperature=temp))

    def set_controlled_temperature(self, temperature):
        self.set_temperature(temperature)
        self.check_temperature_stable(temperature)

    def check_temperature_stable(self, temperature):
        self._stopCheckTempStable = False
        start = time.time()
        timeout = self.stabTimeout


        read_time_step = self.stabTime / 10.0
        stab_time_start = time.time()
        while True:
            if self._stopCheckTempStable:
                return
            if abs(self.get_temperature() - temperature) < self.tempTol:
                stab_time = time.time()
            else:
                stab_time_start = time.time()
                stab_time = time.time()
            if stab_time - stab_time_start > self.stabTime:
                info_xc = self.info_xc()
                tc_stable = info_xc['response']['data']['tc']['stability']
                if tc_stable == 'True':
                    return
                else:
                    logger.info('Temperature actually not yet stable: {}'.format(tc_stable))
            if time.time() - start > timeout:
                raise TemperatureStabilizationTimeout
            time.sleep(read_time_step)

    def info_xc(self):
        return self._get('/system/all')




if __name__ == '__main__':
    controller = ECController('http://0.0.0.0:5001/ec/api/v1.0', monitor_interval=1)
    controller.start()
    time.sleep(1)
    try:
        print(controller.system_info())
    except Exception as e:
        print(e)
    finally:
        controller.stop()






