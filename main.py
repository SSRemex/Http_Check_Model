from check import one_package_check

package = "GET /?bid=ca5990264a164e1f9b3ea391deedac95&id=1+union+select+current+schema+from+sysibm.sysdummy1 HTTP/1.1             " \
          "rm-pro-time:1670575793282             " \
          "x-forwarded-for:42.187.174.228             " \
          "x-scheme:https             " \
          "x-real-ip:42.187.174.228             " \
          "accept-encoding:gzip,deflate             " \
          "host:appseccheck.58.com             " \
          "x-forwarded-proto:https             " \
          "https-tag:HTTPS             " \
          "rm-pro-token:             " \
          "rm-pro-businessid:ca5990264a164e1f9b3ea391deedac95             " \
          "x-remote-port:54067             " \
          "user-agent:curl/7.83.1"


one_package_check(package=package, mode="str")

