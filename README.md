# cronparserlib

A python library for parsing a crontab file and determining when a job will next be run

## How it works

cronparserlib is separated into two logical sections: cronparser and cronjob. The CronParser class is fairly straightforward and attempts to read the crontab file in chunks. Each chunk is divided by comments in the file itself. Use of a buffer here probably isn't necessary, but a very large crontab file might make use of it.

CronJob does most of the heavy lifting
