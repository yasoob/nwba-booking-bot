# Northwest Badminton Academy Bot

This repository contains the code for automating the timeslot booking process for Northwest Badminton Academy. The academy uses Zen planner so the code should theoretically be able to automate the booking for most other websites as well that rely on zen planner with little to no modification.

You need to install Selenium before you can use it:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install selenium
```

You might also have to download chrome webdriver and adjust the path on line 36 appropriately.