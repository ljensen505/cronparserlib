# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# m h dom mon dow usercommand

from cronparser import CronParser
import unittest

cronfile = "cronfile.example"
target_email = "someguy@somecompany.com"


class Tests(unittest.TestCase):
    def setUp(self):
        self.parser = CronParser(cronfile)

    def test_init(self):
        self.assertIsInstance(
            self.parser, CronParser, msg="Error initializing CronParser"
        )

    def test_email(self):
        self.assertEqual(
            self.parser.email_dest, target_email, msg="Emails do not match"
        )


if __name__ == "__main__":
    unittest.main()
