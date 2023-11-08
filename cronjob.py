from pprint import pprint


class CronJob:
    def __init__(self, job: list[str]):
        self.job: list[str] = job
        self.minute = job[0]
        self.hour = job[1]
        self.dom = job[2]
        self.month = job[3]
        self.dow = job[4]
        self.lang = job[5]
        self.cmd = job[6:]
        self.name = self._get_job_name()

    def __repr__(self) -> str:
        return f"{self.name}: {self.job}"

    def _get_job_name(self) -> str:
        return self.cmd[-1].split("/")[-1].split(".")[0]
