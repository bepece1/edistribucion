import logging
from homeassistant.const import POWER_KILO_WATT
from homeassistant.helpers.entity import Entity
from .backend.EdistribucionAPI import Edistribucion
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)

def setup_platform(hass, config, add_entities, discovery_info=None):

    """Set up the sensor platform."""
    add_entities([EDSSensor(config)])

class EDSSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, config):
        """Initialize the sensor."""
        self._state = None
        self._attributes = {}
        self._usr=config['username']
        self._pw=config['password']
        if 'cups' in config:
            self._cups = config['cups']

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'EDS Power Consumption'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return POWER_KILO_WATT

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        edis = Edistribucion(self._usr,self._pw)
        edis.login()
        r = edis.get_cups()

        try:
            for c in r['data']['lstCups']:
                if c['Name'] == self._cups:
                    cups_id = c['Id']
        except AttributeError:
            cups_id = r['data']['lstCups'][0]['Id']
            self._cups = r['data']['lstCups'][0]['Name']
        
        _LOGGER.debug(f'Fetching data for CUPS={self._cups} with Id={cups_id}')
        meter = edis.get_meter(cups_id)
        _LOGGER.debug(meter)
        _LOGGER.debug(meter['data']['potenciaActual'])
        attributes = {}
        attributes['Estado ICP'] = meter['data']['estadoICP']
        attributes['Totalizador'] = str(meter['data']['totalizador']) + ' kWh'
        attributes['Porcentaje actual'] = meter['data']['percent']
        attributes['Potencia Contratada'] = str(meter['data']['potenciaContratada']) + ' kW'
        self._state = meter['data']['potenciaActual']
        self._attributes = attributes
