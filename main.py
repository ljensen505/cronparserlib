from cronparserlib import CronParser

crontab = "cronfile.example"

if __name__ == "__main__":
    parser = CronParser(crontab)
    parser.parse()
