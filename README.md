# alfred-google-search

Inline google search in alfred powered by Python.
Best for quick lookup on google.

## Features

1. Inline search of google showing the first page results

## Requirements

- Python 3
- [requests-html](https://github.com/psf/requests-html.git)

To install requests-html, run this in command line

```
pip3 install requests-html
```

Or

```
pip install requests-html
```

## Installations

Download the workflow file and import to alfred.

## Setup

You might need to change the python3 executable path in the setting of Script
Filter of the alfred workflow according to your settings.

The current setting is "/usr/local/opt/python@3.8/bin/python3". You should run
"which python3" in terminal to check your python3 executable path.

## Usage

Enter "gg" to trigger the workflow and enter the keywords. The first page of
google results will be shown. Press enter on the result will open it in
your browser. You can preview in alfred by pressing **shift**.

Holding **shift** will copy the url to clipboard.
