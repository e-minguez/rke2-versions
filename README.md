<div align="center">

# RKE2 versions

<p align="center">
  <img alt="RKE2 Logo" src="https://raw.githubusercontent.com/cncf/artwork/main/projects/rke2/icon/color/rke2-icon-color.svg" height="140" />
  <h3 align="center">RKE2 versions</h3>
</p>

| :warning: **This is an unofficial and unsupported repository. See the [official documentation](https://docs.rke2.io/).** |
| ----------------------------------------------------------------------------------------------------------------------- |

</div>

This repo generates a website that shows the different RKE2 versions at a glance.

See it [live](https://www.eduardominguez.es/rke2-versions/)!

> :warning: This is an unofficial tool, don't blame us!

## Background

Finding which is the latest stable release of RKE2 is not an easy process. Currently folks need to go to [https://github.com/rke2-io/rke2/releases](https://github.com/rke2-io/rke2/releases) and browse over the releases. There you can find pre-releases, old releases being updated, etc.

There is also the RKE2 docs site [https://docs.rke2.io/release-notes/v1.28.X](https://docs.rke2.io/release-notes/v1.28.X) where you can find the release but as of today, current stable version according to [https://update.rke2.io/v1-release/channels](https://update.rke2.io/v1-release/channels) is v1.28.4+rke22 while the release notes doc shows the latest v1.28 is v1.28.3+rke2.

The idea for the project is to automate it and make it hands-free leveraging github actions to be built when there are changes.

## How it works

There are two main parts for this project:

- Data collection
- Data visualization

## Data collection

For the data collection, a simple python script is used that collects the data from various sources:

- [https://update.rke2.io/v1-release/channels](https://update.rke2.io/v1-release/channels)
- [https://github.com/rke2-io/rke2/releases](https://github.com/rke2-io/rke2/releases)

And then, it generates a json file with all the required data and metadata to be able to visualize it in a later step. It looks like:

```
{
  "date": "12/12/2023 10:55:44",
  "rke2-versions": [
	{
  	"all-versions": [
    	{
      	"github-release-link": "https://github.com/rke2-io/rke2/releases/tag/v1.28.4+rke22",
      	"prerelease": false,
      	"released": "06/12/2023 22:35:52",
      	"version": "v1.28.4+rke22"
    	},
    	{
      	"github-release-link": "https://github.com/rke2-io/rke2/releases/tag/v1.28.4-rc1+rke22",
      	"prerelease": true,
      	"released": "06/12/2023 21:22:11",
      	"version": "v1.28.4-rc1+rke22"
    	},
...
  	"github-release-link": "https://github.com/rke2-io/rke2/releases/tag/v1.28.4+rke22",
  	"name": "stable",
  	"version": "v1.28.4+rke22"
	},
```

It also includes the release link and it flags it as prerelease if it is so. For each release, it gets the release notes in markdown format as they will be shown as well.

To avoid getting all the data everytime, it checks first if the data from the release channels [has changed since last time](https://github.com/e-minguez/rke2-versions/blob/main/rke2-versions.py#L49) by storing the last one and checking the differences. If it is the same, it fails gracefully, otherwise it runs the process to completion.

## Data visualization

The data is presented as a static website which is regenerated and deployed every time the data is updated. The main page displays list of RKE2 versions showing the name and latest patch version for each. Each version has a 'View Details' button which reveals side panel with Markdown formatted release notes for the specific version. Clicking the dropdown caret opens a list of all existing patch versions linking to the respective release on GitHub.

<img width="330" alt="Screenshot 2023-12-12 at 12 29 43" src="https://github.com/e-minguez/rke2-versions/assets/1121740/113b7a81-8d66-4248-82fe-c348b88af44a"> <img width="330" alt="Screenshot 2023-12-12 at 12 30 05" src="https://github.com/e-minguez/rke2-versions/assets/1121740/487abc8c-f9e8-46b8-aabd-0cdac1849fed"> <img width="330" alt="Screenshot 2023-12-12 at 12 29 55" src="https://github.com/e-minguez/rke2-versions/assets/1121740/c42147cc-e826-4e90-9228-a67c2d43104b">

Since the main project requirement was to keep it light weight and leverage the GitHub actions and have it published in server less environment on GitHub pages, we've decided to use static site created with [Gatsby framework](https://www.gatsbyjs.com/). Gatsby provides an easy way to build static sites using Javascript and React to define site pages and components and easily access data from various sources using Graphql queries.

## Automation

The script leverages GitHub Actions and it is executed every hour. Some things to highlight:

- There are two independent jobs, the `build-json` one that runs the data collection procedure and the `build-ui` one that renders the json file using Gatsby. The json file is shared between jobs using GitHub artifacts if they changed.
- It makes a good use of GitHub cache to store a few assets to reduce the build time, such as the versions.json file so it doesn't update the site if there are no changes as well as the python pip packages
- The build-ui job that renders the json file it is only executed if the content changed or if there are changes in the UI code (aka the frontend/ folder)

## Next steps

We are tracking the next steps as [issues](https://github.com/e-minguez/rke2-versions/issues)
