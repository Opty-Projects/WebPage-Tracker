from json import load
from requests import get
from hashlib import sha1
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep


def main(conf):
    while True:
        for wp in conf["WebPages"]:
            if checkWP(wp):
                try:
                    notify(conf["SMTP"], wp["Name"])
                except SMTPException as e:
                    print("Error: '{}'".format(e))
        sleep(conf["SecsTillReplay"])


def checkWP(wp):
    r = get(wp["URL"])
    if r:
        h = sha1(r.text.encode("UTF-8")).hexdigest()
        try:
            if wp["Hash"] != h:
                wp["Hash"] = h
                return True
        except KeyError:
            wp["Hash"] = h
    return False


def notify(smtp, name):
    m = MIMEMultipart()
    m["From"] = smtp["Notifier"]["User"]
    m["To"] = ','.join(smtp["To"])
    m["Subject"] = smtp["Content"]["Subject"].format(Name=name)
    m.attach(MIMEText(smtp["Content"]["Body"].format(Name=name), "plain"))

    with SMTP(smtp["Server"]["Host"], smtp["Server"]["Port"]) as s:
        s.starttls()
        s.login(smtp["Notifier"]["User"], smtp["Notifier"]["Password"])
        s.sendmail(smtp["Notifier"]["User"], smtp["To"], m.as_string())


if __name__ == "__main__":
    main(load(open("Config.json", 'r')))

