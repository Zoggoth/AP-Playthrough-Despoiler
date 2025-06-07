# Archipelago Playthrough Despoiler

A program for finding the available progress in Archipelago, without revealing too much information.

Takes the full playthrough from an Archipelago spoiler file, and removes already found progress using a sphere tracker. Both files should be linked in settings.yaml

Can be configured to reveal the 1 check at a time (slowest, but minumum spoilers), 1 sphere at a time (gives multiple options without spoilers) or the whole playthrough (most info & most spoilers)

Can also be configured to hide item names (minimize spoilers) or show them (lets you prioritize important items)

# To Do

Improve event detection. Events appear in the playthrough, but not in the sphere tracker, so it's impossible to detect which events have been done. This results in early spheres being full of events that have to be scrolled through to find the actual progression.

There are 2 possible solutions. One is to collect a full list of events to remove. This is currently in events.txt, but will have to be expanded to more games. It cannot deal with new games without manual work & can never deal with checks that cannot be identified by name (e.g "777 Score" can be a check or an event in Yacht Dice depending on settings). Improving this requires updating events.txt

The other solution is use the individual game trackers instead of the sphere tracker. This includes a list of unchecked locations without events, so anything not in the tracker can be removed. This should work perfectly, but does require opening multiple trackers, which has been difficult to deal with in [another project](https://github.com/Zoggoth/Zoggoths-Archipelago-Multitracker). However, it's possible that once you reach enough webpages for that to be a problem, the sphere tracker *also* becomes difficult to open. Perhaps it should be another setting