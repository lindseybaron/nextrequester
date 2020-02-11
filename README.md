# nextrequester (wip)

A hacky bit of python and selenium to navigate the atrociously designed NextRequest public records request websites.

## Requirements
- Linux or OSX
- Python 3.7 or higher
- Pip
- whatever's in the `requirements.txt` file

## Installation

1. Clone the repo:
   ```shell script
   git clone git@github.com:lindseybaron/nextrequester.git
   ```
1. Install requirements:
   ```shell script
   cd nextrequester
   pip install -r requirements.txt
   ```
1. Set config values in `./config.yaml`
1. Copy `./secret_example.yaml` and add your login credentials:
   ```shell script
   cp secret_example.yaml secret.yaml
   ```

## Use

### Single Request
To download all the files for a single records request, use the request ID from the url.
   ```shell script
   python src/nr.py req [request-id]
   ```

### All Files From 'Documents'
To download all the files from https://lacity.nextrequest.com/documents:
   ```shell script
   python src/nr.py alldocs
   ```
It'll take a long time. As of the time of writing this, there are 4489 of them.

### All Requests
To fetch all the requests from the 'All Requests' section:
   ```shell script
   python src/nr.py allreqs
   ```
It'll take a long time. As of the time of writing this, there are 4489 of them.