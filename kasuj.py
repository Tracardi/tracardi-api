from device_detector import DeviceDetector

ua = 'Mozilla/5.0 (Linux; Android 4.3; C5502 Build/10.4.1.B.0.101) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.136 Mobile Safari/537.36'

# Parse UA string and load data to dict of 'os', 'client', 'device' keys
detector = DeviceDetector(ua, skip_bot_detection=True)
device = detector.parse()

response = {
    "device": {
        "model": {
            "name": device.device_model(),
            "brand": {
                "name": device.device_brand_name(),
            },
            "type": device.device_type()
        },
        "os": {
            "name": device.os_name(),
            "version": device.os_version(),
        },
        "client": {
            "type": device.client_type(),
            "name": device.client_name(),
            "version": device.secondary_client_version(),
            "engine": device.engine(),
        },
        "type": {
            "mobile": device.is_mobile(),
            "desktop": device.is_desktop(),
            "bot": device.is_bot(),
            "tv": device.is_television(),
        }

    }
}
print(response)
exit()
device.is_bot()  # >>> False
device.is_desktop()
device.os_name()  # >>> Android
device.os_version()  # >>> 4.3
device.engine()  # >>> WebKit

device.device_brand_name()  # >>> Sony
device.device_brand()  # >>> SO
device.device_model()  # >>> Xperia ZR
device.device_type()  # >>> smartphone

# For much faster performance, skip Bot and Device Hardware Detection
# and extract get OS / App details only.
from device_detector import SoftwareDetector

ua = 'Mozilla/5.0 (Linux; Android 6.0; 4Good Light A103 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'
device = SoftwareDetector(ua).parse()
print(device.all_details)
device.client_name()  # >>> Chrome Mobile
device.client_short_name()  # >>> CM
device.client_type()  # >>> browser
device.client_version()  # >>> 58.0.3029.83

device.os_name()  # >>> Android
device.os_version()  # >>> 6.0
device.engine()  # >>> WebKit

device.device_brand_name()  # >>> ''
device.device_brand()  # >>> ''
device.device_model()  # >>> ''
device.device_type()  # >>> ''

# Many mobile browser UA strings contain the app info of the APP that's using the browser
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 EtsyInc/5.22 rv:52200.62.0'
device = DeviceDetector(ua).parse()

device.secondary_client_name()  # >>> EtsyInc
device.secondary_client_type()  # >>> generic
device.secondary_client_version()  # >>> 5.22
