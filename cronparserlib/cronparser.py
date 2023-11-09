from datetime import datetime
from os import path
from cronparserlib.cronjob import CronJob


class CronParser:
    """
    CronParserLib is a library for parsing cron files and determining when jobs will next run.
    """

    def __init__(self, cronfile: str):
        self.cronfile: str = cronfile
        self.email_dest: str = ""
        self.buffer: list[CronJob] = []
        self.buffer_count = 0  # only used when debugging
        self.now = datetime.now()

        if not path.exists(self.cronfile):
            raise FileNotFoundError(f"{self.cronfile} not found")

    def parse(self) -> None:
        """
        Parses the cronfile and prints the results to stdout.
        """
        print(f"Job run @ {self.now.strftime('%Y-%m-%d %H:%M')}")
        self._read_file()

    def _read_file(self) -> None:
        """
        Reads the cronfile line by line, building up a buffer of CronJob objects.
        """
        with open(self.cronfile, "r") as f:
            for line in f.readlines():
                self._read_line(line)
            self._read_buffer()

    def _read_line(self, line: str) -> None:
        """
        Reads a line from the cronfile.
        If the line is blank, the buffer is reset.
        """
        if line == "\n":
            self._read_buffer()
            self.buffer = []
            return

        if line[0] == "#":
            comment = line
            if "MAILTO" in comment:
                self._set_email(line)
            return
        self.now = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day,
            hour=self.now.hour,
            minute=self.now.minute,
        )
        self.buffer.append(CronJob([arg for arg in line.split(" ") if arg], self.now))

    def _read_buffer(self) -> None:
        """
        Reads the buffer of CronJob objects.
        Used for debugging.
        """
        if self.buffer:
            for job in self.buffer:
                print(job)
            self.buffer_count += 1
            self.buffer = []

    def _set_email(self, line: str) -> None:
        """
        Sets the email destination based on comment in crontab.
        """
        self.email_dest = line.split("=")[1].strip().strip('"')
