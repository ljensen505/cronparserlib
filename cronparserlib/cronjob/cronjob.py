from datetime import datetime
import calendar


class CronJob:
    """
    Representation of a cron job. Contains all the core logic for finding the next run time.
    """

    def __init__(self, job: list[str], now: datetime):
        self.job: list[str] = job
        self.minute = job[0]
        self.hour = job[1]
        self.dom = job[2]
        self.month = job[3]
        self.dow = job[4]
        self.lang = job[5]
        self.cmd = job[6:]
        self.now: datetime = now
        self.job_time: datetime = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day,
            hour=self.now.hour,
            minute=self.now.minute,
        )

        self._inc_minute()

        if self.dow == "7":
            self.dow = "0"
            self.job[4] = "0"

    def __repr__(self) -> str:
        return f"{self._job_name()}: {self.job[:5]}\n\tnext run @ {self._next_run()}\n"

    def _job_name(self) -> str:
        """
        Returns the name of the job, as found in the last argument of the cron job.
        """
        return self.cmd[-1].split("/")[-1].split(".")[0]

    def _next_run(self) -> str:
        """
        Calculates the next run time of the job.
        May be called recursively if the next run time is not valid.
        """
        self._calc_min()
        self._calc_hour()
        self._calc_dom()
        self._calc_month()
        self._check_dow()
        return self.job_time.strftime("%Y-%m-%d %H:%M")

    def _check_dow(self) -> None:
        """
        Checks if the next run time is valid for the day of the week.
        If not, increments the minute and commences recursion.
        """
        dow_set: set[int] = self._calc_dow_set()
        is_valid_dow = (self.job_time.weekday() + 1) % 7 in dow_set
        if not is_valid_dow:
            self._inc_minute()
            self._next_run()

    def _calc_dom_set(self) -> set[int]:
        """
        Calculates and returns the set of days of the month that the job is allowed to run on.
        """
        dom_set: set[int] = set()
        if self.dom == "*":
            dom_set.update(
                range(
                    1,
                    calendar.monthrange(self.job_time.year, self.job_time.month)[1] + 1,
                )
            )
        elif self.dom.isdigit():
            dom_set.add(int(self.dom))
        elif "," in self.dom:
            for num_range in self.dom.split(","):
                self._process_range(dom_set, num_range)
        elif "-" in self.dom:
            self._process_range(dom_set, self.dom)
        elif "/" in self.dom:
            interval = int(self.dom.split("/")[-1])
            dom_set = set(
                [
                    num
                    for num in range(
                        1,
                        calendar.monthrange(self.job_time.year, self.job_time.month)[1]
                        + 1,
                    )
                    if num % interval == 0
                ]
            )
        return dom_set

    def _calc_dow_set(self) -> set[int]:
        """
        Calculates and returns the set of days of the week that the job is allowed to run on.
        """
        dow_set: set[int] = set()
        if self.dow == "*":
            dow_set.update(range(0, 7))
        elif self.dow.isdigit():
            dow_set.add(int(self.dow))
        elif "," in self.dow:
            for num_range in self.dow.split(","):
                self._process_range(dow_set, num_range)
        elif "-" in self.dow:
            self._process_range(dow_set, self.dow)
        elif "/" in self.dow:
            interval = int(self.dow.split("/")[-1])
            dow_set = set([num for num in range(0, 7) if num % interval == 0])
        return dow_set

    def _calc_month(self) -> None:
        """
        Calculates the month of the next run.
        """
        if self.month == "*":
            return

        elif self.month.isdigit():
            while self.job_time.month != int(self.month):
                self._inc_month()

        elif "/" in self.month:
            interval = int(self.month.split("/")[-1])
            while self.job_time.month % interval != 0:
                self._inc_month()

        elif "-" in self.month:
            permitted = set()
            ranges = self.month.split(",")
            for num_range in ranges:
                start, end = num_range.split("-")
                permitted.update(range(int(start), int(end) + 1))
            while self.job_time.month not in permitted:
                self._inc_month()

    def _calc_dom(self) -> None:
        """
        Calculates the day of the month of the next run.
        """
        dom_set: set[int] = self._calc_dom_set()

        while self.job_time.day not in dom_set:
            self._inc_dom()

    def _process_range(self, day_set: set[int], num_range: str) -> None:
        """
        Processes a range of days of the month or week and adds them to a set.
        """
        if num_range.isdigit():
            day_set.add(int(num_range))
            return
        start, end = num_range.split("-")
        day_set.update(range(int(start), int(end) + 1))

    def _calc_hour(self) -> None:
        """
        Calculates the hour of the next run.
        """
        if self.hour == "*":
            return

        elif self.hour.isdigit():
            while self.job_time.hour != int(self.hour):
                self._inc_hour()

        elif "/" in self.hour:
            interval = int(self.hour.split("/")[-1])
            while self.job_time.hour % interval != 0:
                self._inc_hour()

        elif "-" in self.hour:
            permitted = set()
            ranges = self.hour.split(",")
            for num_range in ranges:
                start, end = num_range.split("-")
                permitted.update(range(int(start), int(end) + 1))
            while self.job_time.hour not in permitted:
                self._inc_hour()

    def _calc_min(self) -> None:
        """
        Calculates the minute of the next run.
        """
        if self.minute == "*":
            return

        if self.minute.isdigit():
            while self.job_time.minute != int(self.minute):
                self._inc_minute()
            return

        if "/" in self.minute:
            interval = int(self.minute.split("/")[-1])
            while self.job_time.minute % interval != 0:
                self._inc_minute()
            return

    def _inc_minute(self) -> None:
        """
        Increments the minute of the job time.
        """
        minutes = self.job_time.minute + 1
        if minutes > 59:
            minutes = 0
            self._inc_hour()

        self.job_time = self.job_time.replace(minute=minutes)

    def _inc_hour(self) -> None:
        """
        Increments the hour of the job time.
        """
        hours = int(self.job_time.hour) + 1
        if hours > 23:
            hours = 0
            self._inc_dom()

        self.job_time = self.job_time.replace(hour=hours)

    def _inc_dom(self) -> None:
        """
        Increments the day of the month of the job time.
        """
        dom = int(self.job_time.day) + 1
        year = self.job_time.year
        month = self.job_time.month

        # Check for leap year and adjust February days
        if month == 2 and calendar.isleap(year):
            max_days = 29
        else:
            max_days = calendar.monthrange(year, month)[1]

        if dom > max_days:
            dom = 1
            self._inc_month()

        self.job_time = self.job_time.replace(day=dom)

    def _inc_month(self) -> None:
        """
        Increments the month of the job time.
        """
        month = int(self.job_time.month) + 1
        if month > 12:
            month = 1
            self._inc_year()

        self.job_time = self.job_time.replace(month=month)

    def _inc_year(self) -> None:
        """
        Increments the year of the job time.
        """
        self.job_time = self.job_time.replace(year=self.job_time.year + 1)
