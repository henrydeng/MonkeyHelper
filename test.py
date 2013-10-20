#!/usr/bin/python
import onebatch 

#onebatch.phone_id='localhost:5561'
onebatch.install_path_prefix='../../apks/'
onebatch.tracefoler='tracefolder'

onebatch.prepare(load_db=True)
#onebatch.install_app("fb","Facebook v2.0.apk")
onebatch.install_app("skype","Skype_2.9.0.315.apk")
onebatch.install_app("cutrope","Cut the Rope FULL FREE v2.0.3.apk")
onebatch.install_app('tom','Talking_Tom_Cat_2_2.0.3.apk')
onebatch.install_app('weather','AccuWeather for Android v2.1.8.apk')
onebatch.install_app('yahoo','Yahoo!_0.9.7.apk')
onebatch.install_app('sogou','sogou.apk')
onebatch.install_app('360','360_3.7.0.apk')
onebatch.install_app('pinyin','Google Pinyin IME2.1.0 (33864729).apk')
onebatch.install_app('renren','renren_5.6.3.apk')
onebatch.install_app('weibo','Weibo1.0.apk')
onebatch.install_app('rss','Feedly. Google Reader News RSS13.0.7.apk')
onebatch.install_app('pris','pris2.1.0.apk')
onebatch.install_app('wechat','WeChat4.5.apk')
onebatch.install_app('pinterest','Pinterest v1.2.2.apk')
onebatch.install_app('twitter','Twitter v3.6.0.apk')
onebatch.check_warning()

onebatch.start()
#onebatch.launch_app("fb")
#onebatch.stall(8)
#onebatch.launch_app('cutrope')
#onebatch.stall(10)
#onebatch.launch_app('skype')
#onebatch.stall(10)
#onebatch.launch_app('tom')
#onebatch.stall(10)
#onebatch.launch_app('weather')
#onebatch.launch_app('yahoo')
onebatch.finish()

#onebatch.uninstall_app('fb')
onebatch.check_warning()
onebatch.dump(save_db=True)
