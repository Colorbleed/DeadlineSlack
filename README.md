# DeadlineSlack

Post your [Thinkbox Deadline](http://deadline.thinkboxsoftware.com) events to a [Slack](http://www.slack.com) channel

![deadlineslack_message](https://cloud.githubusercontent.com/assets/2439881/19310499/a48ee002-908a-11e6-9f87-aa50854aeae0.jpg)

## Features

- Connect Thinkbox Deadline events to Slack
- Post the render messages as a custom BOT user.
- Format messages the way you want!


## Installation

1. Copy the `DeadlineSlack` folder into your Deadline repository, e.g.: `DeadlineRepository8/custom/events`
2. Ensure Deadline synchronized the event plug-in: `Tools > Synchronize Scripts and Plugins` 
3. Configure the settings through `Tools > Configure Event Plugins > DeadlineSlack`

![deadlineslack_configuration](https://cloud.githubusercontent.com/assets/2439881/19310480/908322a8-908a-11e6-97c2-28a6ff9e0c8b.jpg)

### Dependencies

This package has dependencies to *[slacker](https://github.com/os/slacker)* which requires *[requests](https://pypi.python.org/pypi/requests)*.
As such ensure you have both on your PYTHONPATH for the events to process correctly.

You can add an additional Python search paths to Deadline using:

`Tools > Configure Repository Options > Python Settings > Add Path`

_Note that these changes may take some time (up to 10 minutes) to be in effect_