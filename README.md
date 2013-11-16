MonkeyHelper
============

MonkeyHelper is a wrapper for MonkeyRunner, the automated start-to-finsih Android testing framework. MonkeyHelper extends MonkeyRunner by providing python functions to use various Android Development Tools (adb, aapt, etc)

## Get started
* We use Ecplise PyDev for running scripts with MonkeyHelper. You can skip any of the following subsections if you feel you have finished the steps before.

### Instal Java, Eclipse, PyDev, Android SDK.
* Add `<android_sdk>/tools/` to your system PATH. Remember, as long as PATH changes,  Eclipse need to be restarted.
* Make sure Eclipse works well with PyDev.

### Install jython 2.5.3
* Download the jython-2.5.3-installer.jar and run it with `java -jar`. The GUI installer will guide you to install the jython interpreter.
* Add jython folder to the system PATH. (e.g. on Windows 7, jython is installed at `c:\jython2.5.3\` by default)
* Configure Eclipse to use jython. Goto `Window->Preferences->PyDev->Interpreter-Jython`. Click auto config, which should be able to find the jython interpreter. If not, please check your PATH.

### Configure MonkeyRunner for jython
* Following last step, in the jython interpereter setup window. Click "New Jar/Zip(s)" to add the MonkeyRunner. The `monkeyrunner.jar` is located at `<android_sdk>/tools/lib/`.

### Import the project
* Import the PyDev project of MonkeyHelper.
* The project should be using the default jython interpreter. After a while, you should see all symbols in the source code are resolved.
* The project has embedded the run configuration (monkeyrunner.launch). Make sure this configuration is imported to Eclipse too.
* DO NOT click the RUN button to test MonkeyHelper in Eclipse. Click the `Run with external tools` button (which should be next to the big run button).

### Create your own scripts with MonkeyHelper
* If you have used MonkeyRunner before, MonkeyHelper will be a straightforward helper. To begin with, take a look at the test.py. The few important lines of code in the very beginning ensure that your MonkeyRunner script can find MonkeyHelper properly.
* `test.py` is in the same folder of `MonkeyHelper.py`. However, jython did not include this. So we add a small hack `module_path()` to return the folder for test.py. Then, we append that to the `sys.path` to make jython find `MonkeyHelper.py`.

### APIs
* MonkeyHelper mainly provides two classess `EMonkeyDevice` and `MonkeyHelper`.
* `MonkeyHelper` defines a bunch of static methods to invoke other Android SKD tools (for details, look into its doc).
* `EMonkeyDevice` wraps `MonkeyDevice` and extends a lot of easier functionalities such as sliding left, right, etc.
* `EMonkeyDevice` is 99% compatible with `MonkeyDevice`. The only difference is that instead of using `device = MonkeyRunner.waitForConnection()`, now you use `device = EMonkeyDevice()`.
* `EmonkeyDevice` contains all the functions supported by `MonkeyDevice`. They behave as usual. For extended functions, take a look at the `EMonkeyDevice` doc.

### Tips
* Keep in mind that your are using jython 2.5.3, which support python syntax 2.5 (so no `with` statement, etc). Hope one day we can use 2.7.
