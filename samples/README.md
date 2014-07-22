This folder contains several example traces that could be used to test the toolchain. We collect traces from a Samsung Galaxy S phone with 4.1.2 Android, an Asus Transformer TF201 with the same Android and the Android emulator. All traces are collected with `getevent -lt /dev/input1` (`getevent` is the standard Android Linux-layer tool to capture user inputs).

## Emulator traces
* ./Emulator/emulator-drag.txt
* ./Emulator/emulator-openPeople.txt
* ./Emulator/emulator-PeopleAddContact.txt
* ./Emulator/emulator-single-touch.txt
* ./Emulator/emulator-three-touches.txt

## Phone traces
* ./Phone/galaxys-paint.txt: the painting app, demo at http://www.youtube.com/watch?v=4j8VpAO4XCg
* ./Phone/phone-CalenderaddEvent.txt
* ./Phone/phone-openCalender.txt
* ./Phone/phone-playAngryBirdsLevel1.txt
* ./Phone/phone-single-drag.txt
* ./Phone/phone-single-touch.txt
* ./Phone/phone-three-touches.txt
* ./Phone/phone-two-finger-drag.txt

## Tablet traces
* ./Tablet/tablet-AngryBirdsMultipleLevels.txt: play the angry birds and pass several levels, demo at http://www.youtube.com/watch?v=vYlO0UrhRR8
* ./Tablet/tablet-CalenderaddEvent.txt
* ./Tablet/tablet-openAngryBirds-drag-tap-tap.txt
* ./Tablet/tablet-openCalender-drag-tap-tap.txt
* ./Tablet/tablet-playAngryBirdsLevel1.txt
* ./Tablet/tablet-single-drag.txt
* ./Tablet/tablet-single-touch.txt
* ./Tablet/tablet-three-touches.txt
* ./Tablet/tablet-two-finger-drag.txt


