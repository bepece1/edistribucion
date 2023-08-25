# edistribucion
Este es un proyecto apra poder consumir la API de e-distribución (Endesa distribución) y exponerla como un sensor dentro de Home Assistant. 
Actualmente está usando como backend el crawler de trocotronic (versiones >= 0.7.0). Por defecto está configurado para hacer update de nuestro contrador de edistribución cada 10 minutos. Esto es configurable en el configuration.yml no obstante no es recomendable dado que puede dar lugar a baneos por parte de la distribuidora. 

Como instalarlo:

Simplemente copia el contenido de este repositorio en la carpeta custom components y añade al configuration.yml el siguiente contenido:

``` yaml
  
sensor:
  - platform: edistribucion
    username: "username sin comillas"
    password: "password sin comillas"
    #scan_interval: 60 #This is in seconds. Mejor no usar para evitar baneos
    #cups: XXXXX #Establecer cuando se tienen varios CUPS para selecionar de cual de ellos obtener los datos
```

Es importante no poner un tiempo muy bajo para que no nos encontremos con cortes en las mediciones. Esto será así hasta que edistribución presente una api. 

![image](https://user-images.githubusercontent.com/1789503/133009041-8b99f7d9-5768-425f-8b04-09bbdefd031e.png)

 
# ¿Se pueden crear sensores con los atributos? 
Sí, se pueden crear de esta forma:

``` yaml
platform: template
sensors:
porcentaje_consumo_maximo:
friendly_name: "Porcentaje Consumo Máximo"
entity_id: sensor.eds_power_consumption
unit_of_measurement: '%'
value_template: "{{ state_attr('sensor.eds_power_consumption','Porcentaje actual')|replace(',','.')|replace('%','')|float }}"
```

# ¿Se pueden crear sensores para el panel de energía con los atributos? 
Sí, se pueden crear de esta forma:

```
template:
  - sensor:
      - name: "eds_meter_reading"
        unit_of_measurement: "kWh"
        state_class: total_increasing
        device_class: "energy"
        state: >
          {% if state_attr('sensor.eds_power_consumption','Totalizador') is not none %}
          {{ state_attr('sensor.eds_power_consumption','Totalizador')|replace('.','')|replace(' kWh','')|float }}
          {% else %}
          unknown
          {% endif %}
        attributes:
          last_reset: '1970-01-01T00:00:00+00:00'
```

TODO
=======
* Integrar el backend como dependencia pip
* Implementar la reconexion del ICP en cuanto el backend lo soporte. 

Agradecimientos
=======
Agradecer a @trocotronic el trabajo de implementar el crwler para extraer los datos desde eds y a @jagalindo por usar como plantilla su trabajo para anteriores versiones del backend de trocotronic
