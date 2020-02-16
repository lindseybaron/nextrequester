# nextrequester

A hacky bit of python to download responsive files from the atrociously designed NextRequest public records request websites.

Currently hard-coded for Los Angeles, but you should be able to just change the value of `BASE_URL` to whatever you want. 

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
   python src/nr.py batch [request-id]
   ```

### All Files From 'Documents'
To download all the files from https://lacity.nextrequest.com/documents:
   ```shell script
   python src/nr.py alldocs
   ```