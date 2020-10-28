from json import load
from hashlib import sha1
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from requests import session
from Lib.Driver import doLogin


def main(conf):
    while True:
        for wp in conf["WebPages"]:
            s = session()
            if "Login" in wp:
                doLogin(s, wp["Login"])
            for trg in wp["Targets"]:
                if checkWP(s, trg):
                    try:
                        notify(conf["EmailNotifications"], trg)
                    except SMTPException as e:
                        print("Error: '{}'".format(e))
            sleep(conf["SecsTillReplay"])


def checkWP(s, trg):
    r = s.get(trg["Link"])
    if r:
        h = sha1(r.text.encode("UTF-8")).hexdigest()
        try:
            if trg["Hash"] != h:
                trg["Hash"] = h
                return True
        except KeyError:
            trg["Hash"] = h
    return False


def notify(ntf, trg):
    m = MIMEMultipart()
    m["From"] = ntf["Notifier"]["Credentials"]["Email"]
    m["To"] = ','.join(ntf["Subscribers"])
    m["Subject"] = ntf["Content"]["Subject"].format(Name=trg["Name"])
    con = ntf["Content"]["Body"].format(Name=trg["Name"])
    con += "\nCheck it <a href='{Link}'>Here</a>!".format(Link=trg["Link"])
    m.attach(MIMEText(con, "html"))

    with SMTP(ntf["SMTPServer"]["Host"], ntf["SMTPServer"]["Port"]) as s:
        s.starttls()
        s.login(ntf["Notifier"]["Credentials"]["Email"], ntf["Notifier"]["Credentials"]["Password"])
        s.sendmail(ntf["Notifier"]["Credentials"]["Email"], ntf["Subscribers"], m.as_string())


if __name__ == "__main__":
    main(load(open("MyConfig.json", 'r')))
