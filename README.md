WebDomo
=======

A platform based on a set of REST web services that allows seamless access to every 
domotic resources like lelylan does but it is intended to use in a home network.

Use cases
---------

Let's suppose we already have an actuator and a WebDomo server running at 
http://webdomoserver.local and we want to know if bedroom lights are turned on, 
the following http get request will return the state of all the lights inside 
the bedroom

	GET http://webdomoserver.local/light/bedroom/
	
Or if we want to see what lights are on we can simple do this:

	GET http://webdomoserver.local/light/?state=on

Now if we want to turn on a light we can simply do an http put request like this:

	PUT http://webdomoserver.local/light/bedroom/?state=on

If we want to turn off all lights we can do it in the following way

	PUT http://webdomoserver.local/light/?state=off
	
There are also server specific calls with let you know the server status, for example:

	GET http://webdomoserver.local/server/active-actuators

Return a list of currently active actuators

Basic structure
---------------

* WebDomo Server -- Base Server, it can have multiple actuators associated to it
* Actuators -- Used to comunicate between server and domotic appliances
* Appliance -- Base block, it can have a type, subtypes and custom properties

Defining new actuator
---------------------

To define your own actuator you have to subclass the DomoActuator class, the put method has to be absolutely overwrited:

* put(*subtypes, **parameters) -- this method is used in put calls it modify the appliance state

Optionally you can also overwrite the following method;

* get(*subtypes, **parameters) -- this method is used in get calls to retrive the current appliance status

an actuator structure and his appliances are described from xml files for example:


	<?xml version="1.0" standalone="yes" ?>
	<actuator type="test" class="ArduinoActuator">
		<!--Actuator Variables -->
		<var name="port" value="/dev/ttyACM0" />

		<!--Subtypes and Appliances -->
		<subtype name="test">
			<appliance name="luce1">
				<var name="pin" value="13" />
				<var name="state" value="off" />
			</appliance>
		</subtype>
	</actuator>
	