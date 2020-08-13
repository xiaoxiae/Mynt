# a script that watches for changes in the configuration file
# when one is noticed things should happen
# just pseudocode atm

while true
	inotifywait -e close_write /home/pi/mynt/config.yaml

	sleep 0.5

	# run stuff
end
