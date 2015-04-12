#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/usr/bin/python

import argparse
import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

# Parse the command-line arguments (e.g. --noauth_local_webserver)
parser = argparse.ArgumentParser(parents=[argparser])
flags = parser.parse_args()

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'Interstellar-3150d88e64c7.json'

# Check https://developers.google.com/gmail/api/auth/scopes
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run_flow(flow, STORAGE, flags, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# Retrieve a page of threads
threads = gmail_service.users().threads().list(userId='me').execute()

# Print ID for each thread
if threads['threads']:
  for thread in threads['threads']:
    print 'Thread ID: %s' % (thread['id'])