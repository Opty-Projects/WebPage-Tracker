# WebPage-Tracker

<img src="./Pictures/WebPage-Tracker-Icon.png" alt="WebPage-Tracker-Icon" width="200">

This Program detects Modifications to WebPages and, as a result, sends E-Mail Notifications to its Listeners.

### Setup

You **need** to Setup the Program by filling in [Config.json](./Config.json):

- `WebPages` Param: List of WebPages you wanna Track, its size is up to you.
- `SMTP`:`To` Param: List of E-Mails you wanna Notify whenever a WebPage is Modified.

### To Run

Commands:
- `pipenv install`
- `pipenv run python Main.py`

### Extra: Screen Sessions

You're able to Create Screen Sessions to keep a Program running on a Remote Machine, even after Disconnecting:

- To Create a Session: `screen -S <Session-Name>`
- To Detach from Session: `Ctrl + A D`
- To Reattach to Session: `screen -r <Session-Name>`
- To Kill a Session: `screen -S <Session-Name> -X quit`

---

| Name | University | Email |
| ---- | ---- | ---- |
| Ricardo Grade | Técnico Lisboa | ricardo.grade@tecnico.ulisboa.pt |
