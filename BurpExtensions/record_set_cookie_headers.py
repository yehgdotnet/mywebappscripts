from burp import IBurpExtender
from burp import IHttpListener
from burp import IProxyListener
import re
import os
import sys

urls_in_scope=['stg.one.sony-europe.com']
#Adding directory to the path where Python searches for modules
module_folder = os.path.dirname('/media/truecrypt2/Sony_2014-04_OneSony/screenshots/BurpExtensions/modules/')
sys.path.insert(0, module_folder)
import webcommon

class BurpExtender(IBurpExtender, IHttpListener, IProxyListener):
  def registerExtenderCallbacks(self,callbacks):
    # Get a reference to the Burp helpers object
    self._helpers = callbacks.getHelpers()

    # set our extension name
    callbacks.setExtensionName("Record Set Cookie Headers")

    # register ourselves as an HTTP listener
    callbacks.registerHttpListener(self)

    # register ourselves as a Proxy listener
    callbacks.registerProxyListener(self)

  def processProxyMessage(self,messageIsRequest,message):
    request_byte_array=message.getMessageInfo().getRequest()
    requestInfo = self._helpers.analyzeRequest(request_byte_array)
    setcookie_header=BurpExtender.record_setcookie_headers(self,messageIsRequest,message)

  def record_setcookie_headers(self,messageIsRequest,message):
    if not messageIsRequest:
      response_byte_array=message.getMessageInfo().getResponse()
      responseInfo = self._helpers.analyzeResponse(response_byte_array)
      setcookie_header=webcommon.get_setcookie_from_header(self,responseInfo)
      if setcookie_header:
        for cookie in setcookie_header:
          print cookie
