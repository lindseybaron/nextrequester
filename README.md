# nextrequester (wip)

A hacky bit of python and selenium to navigate the atrociously designed NextRequest public records request websites.

## Requirements
- Linux or OSX
- Python 3.7 or higher
- Pip
- whatever's in the `requirements.txt` file

## Installation

1. Clone the repo
   ```shell script
   git clone git@github.com:lindseybaron/nextrequester.git
   ```
1. Install requirements
   ```shell script
   cd nextrequester
   pip install -r requirements.txt
   ```
1. Set config values in `./config.yaml`

## Use
1. Run like so (but with your own values obvs):
   ```shell script
   python src/nr.py batch [request-id] [account-email] [password]
   ```
1. Fix it when it breaks.

