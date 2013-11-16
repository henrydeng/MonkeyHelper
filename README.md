MonkeyHelper
============

MonkeyHelper is a wrapper for MonkeyRunner, the automated start-to-finsih Android testing framework. MonkeyHelper extends MonkeyRunner by providing python functions to use various Android Development Tools (adb, aapt, etc)

## For contributors
* We use Ecplise PyDev to code MonkeyHelper and the commandline tool provided by Android SDK to test.
* To begin with, you need Java, Eclipse, PyDev and Android SDK. Make sure Eclipse works well with PyDev.
* Install jython 2.5.3. Download the jython-2.5.3-installer.jar and run it with `java -jar`. The GUI installer will guide you to install the jython interpreter.
* Add jython folder to the system PATH. (e.g. on Windows 7, jython is installed at `c:\jython2.5.3\` by default)
* Configure Eclipse to use jython. Goto `Window->Preferences->PyDev->Interpreter-Jython`. Click auto config, which should be able to find the jython interpreter. If not, please check your PATH.
* Following last step, in the jython interpereter setup window. Click "New Jar/Zip(s)" to add the MonkeyRunner. The `monkeyrunner.jar` is located at `<android_sdk>/tools/lib/`.
* The tool chain it ready, now import the pydev project for MonkeyHelper. The project should be using the default jython interpreter. After a while, you should see all symbols in the source code are resolved.
* DO NOT click the RUN button to test MonkeyHelper in Eclipse. Use the commandline tool: `<android_sdk>/tools/monkeyrunner.bat test.py`.
