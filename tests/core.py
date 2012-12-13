"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from octogit.core import get_single_issue

class UTF8Support(unittest.TestCase):

    def assertNotRaises(self, exception_type, called_func, kwargs):
        try:
            called_func(**kwargs)
        except Exception as e:
            if isinstance(e, exception_type):
                self.fail(e)
            else:
                pass

    def test_assert_not_raises_UnicodeDecodeError(self):
        self.assertNotRaises(UnicodeEncodeError, get_single_issue,
            kwargs={'user':'cesarFrias', 'repo':'pomodoro4linux',
            'number':2})


if __name__ == '__main__':
    unittest.main()
