#!/usr/bin/env python3

import json
import os
import requests
import sys
import re
import jinja2

from datetime import datetime

from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = None
if "GITHUB_TOKEN" in os.environ:
	auth = Auth.Token(os.environ["GITHUB_TOKEN"])

URL = "https://update.rke2.io/v1-release/channels"
HEADERS = {"accept": "application/json"}
FILE = "rke2-versions.json"
REPO = "rancher/rke2"
GITHUBRELEASES = f"https://github.com/{REPO}/releases/tag/"

OUTPUTFILE = "data/rke2.json"

def main():
	# Open the previous json data
	try:
		with open(FILE) as json_file:
				previous = json.load(json_file)
	except Exception:
			previous = {}

	# Get the URL
	try:
		page = requests.get(URL, headers=HEADERS)
		page.raise_for_status()
	except requests.exceptions.HTTPError as err:
		raise SystemExit(err)
	
	# Convert it to a dict directly as it is json
	try:
		data = page.json()
	except requests.exceptions.JSONDecodeError as err:
		raise SystemExit(err)
	
	# If the data didn't changed, exit soon
	if data == previous:
		print("CHANGED=false")
		sys.exit(0)
	# Otherwise, save it for the future
	else:
		print("CHANGED=true")
		with open(FILE, "w") as json_file:
			json_file.write(json.dumps(data, sort_keys=True))

	rke2versions = {"rke2-versions": [], "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

	g = Github(auth=auth)
	repo = g.get_repo(REPO)
	releases=repo.get_releases()

def get_ordered_data(data):
	# Separate special channels from versioned channels
	special_channels = []
	versioned_channels = []
	special_channel_names = ["stable", "latest", "testing"]

	for item in data:
		if item['name'] in special_channel_names:
			special_channels.append(item)
		else:
			versioned_channels.append(item)

	# Sort special channels according to the predefined list
	special_channels.sort(key=lambda d: special_channel_names.index(d['name']))

	# Sort versioned channels semantically (e.g., v1.10 > v1.2)
	versioned_channels.sort(key=lambda d: [int(p) for p in d['name'].lstrip('v').split('.')], reverse=True)

	return special_channels + versioned_channels

def main():
	# Open the previous json data
	try:
		with open(FILE) as json_file:
				previous = json.load(json_file)
	except Exception:
			previous = {}

	# Get the URL
	try:
		page = requests.get(URL, headers=HEADERS)
		page.raise_for_status()
	except requests.exceptions.HTTPError as err:
		raise SystemExit(err)

	# Convert it to a dict directly as it is json
	try:
		data = page.json()
	except requests.exceptions.JSONDecodeError as err:
		raise SystemExit(err)

	# If the data didn't changed, exit soon
	if data == previous:
		print("CHANGED=false")
		sys.exit(0)
	# Otherwise, save it for the future
	else:
		print("CHANGED=true")
		with open(FILE, "w") as json_file:
			json_file.write(json.dumps(data, sort_keys=True))

	rke2versions = {"rke2-versions": [], "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

	g = Github(auth=auth)
	repo = g.get_repo(REPO)
	releases=repo.get_releases()

	ordereddata = get_ordered_data(data["data"])

	for key in ordereddata:
		# Some releases (k3s 1.16-testing & 1.17-testing don't have a latest version, skipping them
		if 'latest' in key:
			previous = []
			for i in list(filter(lambda r: re.match(key['latest'][:6], r.title),releases)):
				previous.append({"version": i.title,
											"github-release-link": f"{GITHUBRELEASES}{i.title}",
											"prerelease": i.prerelease,
											"released": i.published_at.strftime("%d/%m/%Y %H:%M:%S")})
			version = {"name": key['name'],
							"version": key['latest'],
							"github-release-link": f"{GITHUBRELEASES}{key['latest']}",
							"all-versions": previous }
			rke2versions['rke2-versions'].append(version)

			release = repo.get_release(key['latest'])

			with open("data/"+key['latest']+".md", "w") as releasefile:
				releasefile.writelines(["---\n",
											f"version: {key['latest']}\n",
											f"releaseDate: {release.published_at.strftime('%d/%m/%Y %H:%M:%S')}\n",
											"---\n"])
				releasefile.write(release.body or '')

	g.close()

	with open(OUTPUTFILE, "w") as json_file:
		json_file.write(json.dumps(rke2versions, sort_keys=True))

if __name__ == "__main__":
    main()