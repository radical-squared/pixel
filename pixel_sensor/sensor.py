"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from PIL import Image
from math import sqrt
import math


# import webcolors

COLORS = (
    (255,0,0),
    (0, 255, 0),
    (0,0,0),
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([PixelSensor(config)])


class PixelSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, config):
        """Initialize the sensor."""
        self._state = None
        self._name = config['name']
        self._x = config['x']
        self._y = config['y']
        self._image = config['image']
        self._color = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name  

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "lx"

    @property
    def device_class(self):
        """Return the unit of measurement."""
        return "illuminance"

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        img = Image.open(self._image)

        self._attributes['pixel'] = ((self._x,self._y))
        r, g, b = img.getpixel((self._x,self._y))
        self._state = math.floor(0.2126*r + 0.7152*g + 0.0722*b)           
        self._attributes['color'] = self.closest_color((r,g,b))                  

        self._attributes['rgb'] = (r,g,b)
        img.close()


    def closest_color(self, rgb):
        r, g, b = rgb
        color_diffs = []
        color = None
        for color in COLORS:
            cr, cg, cb = color
            color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
            color_diffs.append((color_diff, color))
        
        if min(color_diffs)[1] == (255,0,0):
            color = "Red"
        elif min(color_diffs)[1] == (0,255,0):
            color = "Green"    
        elif min(color_diffs)[1] == (0,0,0):
            color = "Black"
        else:
            color == "Other"
        return color


