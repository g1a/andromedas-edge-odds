#!/bin/bash

for defender_targeting in 5 4 3 2 1 ; do
	for attacker_targeting in 5 4 3 2 1 ; do
		mkdir -p two-combatants/${attacker_targeting}-targeting-v-${defender_targeting}-targeting
		python3 combat-odds.py $attacker_targeting $defender_targeting --html > two-combatants/${attacker_targeting}-targeting-v-${defender_targeting}-targeting/index.html
	done
done
