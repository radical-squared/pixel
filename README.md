# Home Assistant Pixel Sensor (custom component)

Custom sensor for Home Assistant that returns pixel info of a given image. Useful for monitoring status lights of home appliances with a camera. The sensor reports approximate pixel brightness as state and pixel color as state attributes e.g:
```
  pixel: 100, 200
  color: Black
  rgb: 18, 17, 15
  unit_of_measurement: lx
  friendly_name: viessman
  device_class: illuminance


### HA Setup:

Copy pixel_sensor to your custom_components folder. Then add the following to your HA configuration files:

```
sensor:
  - platform: pixel_sensor
    name: 'viessmann'
    x: 100
    y: 200
    image: '/share/viessmann_snapshot.jpg'
    
automation:
  - id: '23fds234'
    alias: Take camera snapshot
    initial_state: true
    trigger:
    - platform: time_pattern
      seconds: "/10"
    action:  
    - service: camera.snapshot
      data:
        entity_id: camera.viessman
        filename: '/share/viessmann_snapshot.jpg'
    
