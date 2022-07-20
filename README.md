OnBoarding Buddy

Onboarding Buddy is a headless Slack app to assist teams and hiring leaders to easily integrate new hires into the Slack workspace & ecosystems using simple slack slash commands.

Project Status: Active

FEATURES

Scalable: This app can be scaled in cloud by changing the number of pods available to it. Since no associated date is stored, we do not need to worry about scaling databases.

Can be adapted for other front-ends: e.g. RtO app, WebEx plugin, any webpage, etc. – basically anything that can consume this API.

ADVANTAGES

Saves time and effort by adding new hires for all selected channels with a single command, in a consolidated view, for the user to choose from.

Shows all public channels you (slash command invoking user) are part of in a multi select menu.

There is no limit on the number of channels you can request for adding a user to. Adding newhires to multiple channels is a tedious process manually, this slack app solves this issue and automates this process with a simple slash command.

Can be used to add any slack user to any of your channels in a workspace where this app is installed.

Installation You can pull the latest release of this application by cloning the repository.

Usage Simply invoke the following command in a slack workspace this slack app is a part of : /onboard @newhire

In (1.), tag individual user/newhire (replace @user1 with slack handle)

This will pop up a list of all the channels that you are part of , and from there you can choose as many channels as you like to add the new hire.

Tools and Technologies

This app is using various slack web APIs, these APIs are being consumed by the app's own API endpoint. The backend server is built with Flask. Here are some important links for reference ->

For a quick overview, visit our confluence page, Click here

Jenkins, Click here

XL release Template, Click here.

E1 Server, Click here.

Postman Collection(API Documentation), Click here

Contributors

Custodians Lead Maintainers: Team Kronos
