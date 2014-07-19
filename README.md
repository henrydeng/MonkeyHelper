MonkeyHelper
============

MonkeyHelper offers recording, replaying, manipulcation and data mining capabilities for Android usage traces. It also provides wrappers for common Android Development Tools (adb, aapt, etc). All in Python. 

## Get started
* We use Ecplise PyDev for running scripts with MonkeyHelper. You can skip any of the following subsections if you feel you have finished the steps before.

### Use cases
We highlight some use cases that could be useful for different purposes.
* Record a trace from an Android box and replay it. This could be useful for debugging and testing apps. The trace can be stored as a simple text file, essentially everywhere.
* Record, manipulate and then replay a trace. The manipulation functionality allows one to change a small fraction of the trace (e.g. add a swipe, etc).
* Fusion multiple traces. Pick a gesture from one trace and paste it to another.
* Implement data mining algorithm to mine values from some collected trace, via our mining APIs.

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


## Get involved

### Component-based architecture
To be explained.

### Device control APIs
* MonkeyHelper mainly provides two classess `EMonkeyDevice` and `MonkeyHelper` for controlling an Android box.
* `MonkeyHelper` defines a bunch of static methods to invoke other Android SDK tools (for details, look into its doc).
* `EMonkeyDevice` wraps `MonkeyDevice` and extends a lot of easier functionalities such as sliding left, right, etc.
* `EMonkeyDevice` is 99% compatible with `MonkeyDevice`. The only difference is that instead of using `device = MonkeyRunner.waitForConnection()`, now you use `device = EMonkeyDevice()`.
* `EMonkeyDevice` contains all the functions supported by `MonkeyDevice`. They behave as usual. For extended functions, take a look at the `EMonkeyDevice` doc.

### Recording APIs
* Currently, the raw trace can be simply recored by the `getevent` utility of Android. Check the [Android doc](https://source.android.com/devices/tech/input/getevent.html) for details. We need traces produced from `getevent -lt <dev>`.

### Trace manipulation
* In current version, we are working out a simple web visualization tool for the traces, as found in `visualizer/trail_visualizer.html`. More user-friendly web interfaces would be developed later.


### Data mining interfaces
* We discover the potential of analyzing the traces. We are working out a unified interface for data mining the trace.
* We will give out some preliminary data mining case studies before we roll out the interfaces.

### Tips
* The current stable jython is 2.5.3, which is python 2.5 syntax (most notable no `with` statement, etc). Jython 2.7* are release candidates right now.
