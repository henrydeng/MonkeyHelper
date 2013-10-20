#!/usr/bin/python
import onebatch 

#onebatch.phone_id='localhost:5561'
onebatch.install_path_prefix='./'
onebatch.tracefoler='tracefolder'

onebatch.prepare(load_db=False)
onebatch.install_app("test","1.apk")
onebatch.check_warning()

onebatch.start()
onebatch.launch_app("test")
onebatch.finish()

#onebatch.uninstall_app('fb')
onebatch.check_warning()
onebatch.dump(save_db=True)
