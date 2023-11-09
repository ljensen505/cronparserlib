# cronparserlib

A python library for parsing a crontab file and determining when a job will next be run. This library isn't published, but we can pretend. Maybe someday we can install it with pip and then use the syntax in `main.py` to use it after installing.

## How it works

cronparserlib is separated into two logical sections: cronparser and cronjob. The CronParser class is fairly straightforward and attempts to read the crontab text file in chunks. Each chunk is divided by comments in the file itself (for example, `# minutely` or `# daily`). Use of a buffer here probably isn't necessary, but a very large crontab file might make use of it.

With the exception of storing MAILTO, all lines which have been commented out will be ignored. (this includes job13 of the sample file)

CronJob does most of the heavy lifting. A CronJob is instantiated by the cronparser and is passed the start time of the job, and details about the indivdual job as arguments. A CronJob will take an optimistic approach to figuring out when it will next be run by essentially taking a sliding window and moving through minutes, hours, days of the month, and the month. As a last check, it will validate the day of the week. If that check fails, the sliding window will have its minute incremented and the process begins again. This continues recursively until a solution is found, or maximum recursion depth is found.

This optimistic approach may not be the most ideal - a more clever approach may exist. However, this algorithm is still very fast. I exceeded the limitations of datetime's year value before encountering any noticeable lag during testing.

A CronJob does not expose its anticipated run time, but instead includes that data in its repr dunder method. That repr method is used by the CronParser and the information is directed to stdout.

## Development

This was developed with python3.11 on Pop!\_OS 22.04 LTS x86_64. There is nothing here which should be platform dependent, but nonetheless, all testing was done in Pop!\_OS. Some type hints may require use of python3.11

## Reasoning

The approach described above was not my first instinct, but did ultimately prove to make the most sense. Initially, I tried to validate and mutate the final datetime object from left to right. This proved challenging because of, for example, hours overflowing and bumping the day which had already been handled. For this reason, processing is done from right to left, starting with minutes. There is a private method to increment each part of the final datetime object, and overflows are handled automatically.

Similarily, my initial naive approach to handling dom and dow by validating them at the same time did not work. My initial reasoning was that handling all "day" logic at once would simplify things. But again, an overflow of the month or year would cause the dow validation to be offset and likely incorrect. Therefore, I went with the aforementioned optimistic approach of calculating everything except dow validation first, and then recursively continuing the cycle until a valid dow was found (with a datetime which has been otherwise verified at this point in the algorithm).

While the resolution of cron jobs is in minutes rather than seconds, seconds still have to minorly be accounted for. A job cannot be run in the same minute as this library is called, and therefore one of the first things the CronJob does is increment the minute. If the job is run every minute, then the algorithm is done.

CronJob includes no method for directly extracting its anticipated run time because this is a cron-parser-library, not a cron-job-library. The user should only use CronParser, and can handle stdout as they see fit.

Python sets are used extensively by CronJob. This is mainly because I like using them, but I also initially expected to want to need the intersection of valid_dom and valid_dow. This didn't pan out, and refactoring to remove use of sets didn't seem worthwhile.

## Usage

```python
from cronparserlib import CronParser

crontab = "cronfile.example"
parser = CronParser(crontab)
parser.parse()
```

```bash
> python main.py

Job started @ 2023-11-08 18:48
job1: ['*/1', '*', '*', '*', '*']
        next run @ 2023-11-08 18:49

job2: ['*/1', '15-23,0-5', '*', '*', '*']
        next run @ 2023-11-08 18:49

job3: ['*/2', '*', '*', '*', '*']
        next run @ 2023-11-08 18:50
[...]
```

## Limitations

As mentioned on the spec sheet, crontabs come in many shapes and sizes. This library certainly is not comprehensive. While I've made a best-effort to also aligh with the crontab man page, some syntax is not supported.

For example, the man page states:

> For example, ``0-23/2'' can be used in the hours field to specify command execution every other hour

The syntax of `0-23/2` is not supported, but everything on the example crontab file is.
