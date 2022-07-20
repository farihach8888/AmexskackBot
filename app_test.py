import urllib3
from OpenSSL import SSL
from flask import Flask, request, jsonify, Response
import os
import requests
import vaulthelper


import views
import json



from threading import Thread

try:
    print("Reading secrets from the vault ...")
    vault = vaulthelper.VaultHelper()
    vault_values = vault.read_vault()
    CLIENT_ID = vault.get_vault_value('CLIENT_ID')
    CLIENT_SECRET = vault.get_vault_value('CLIENT_SECRET')
    CarId = vault.get_vault_value('CarId')
    PROXY_HOST = vault.get_vault_value('PROXY_HOST')
    SIGNING_SECRET = vault.get_vault_value('SIGNING_SECRET')
    SLACK_APP_ID = vault.get_vault_value('SLACK_APP_ID')
    SLACK_APP_TOKEN = vault.get_vault_value('SLACK_APP_TOKEN')
    SLACK_BOT_TOKEN = vault.get_vault_value('SLACK_BOT_TOKEN')
    SLACK_USER_TOKEN = vault.get_vault_value('SLACK_USER_TOKEN')
    if SLACK_APP_TOKEN == None:
        print("Unable to read secrets from the vault")
        raise ValueError
    else:
        print("Reading secrets from vault complete")
except:
    print("Reading secrets from the local environment f...")
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    CarId = os.environ.get('CarId')
    PROXY_HOST = os.environ.get('PROXY_HOST')
    SIGNING_SECRET = os.environ.get('SIGNING_SECRET')
    SLACK_APP_ID = os.environ.get('SLACK_APP_ID')
    SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    SLACK_USER_TOKEN = os.environ.get('SLACK_USER_TOKEN')

Proxies = {"https": PROXY_HOST,
           "http": PROXY_HOST}

app = Flask(__name__)




@app.route("/")
def hello_world():
    """
    Base endpoint, hit to see message from server.

        ARGS:
            n/a, takes all requests
        RETURNS:
            a single line of text
    """
    return "<p>Hello, Onboarding Slack Team!</p>"


@app.route('/health', methods=["GET", "POST"])  # Check Health
def health():
    """
    Basic endpoint to test server health
        ARGS:
            n/a, POST request
        RETURNS:
            On success: 200 OK
            On failure, 500 Server Error
    """
    if request.method == "POST":
        return (f"{Response(), 200}Post request")
    data = requests.get(url="https://slack.com/api/api.test", proxies=Proxies, verify=False).json()
    return jsonify(data=data)


def find_user_all_channels_helper(user_id):
    """
    Returns all the slack channels of the user.
    The channels returned are only within the workspace the ID and bot is from.

        ARGS:
            user_id: the Slack ID of the requested user. Different for each workspace
        RETURNS:
            On success: returns the list of  channels the user is in
            On failure: return None
    """
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}
    params = {'user': user_id}
    try:
        data = requests.get(url='https://slack.com/api/users.conversations', proxies=Proxies, headers=headers,
                            params=params, verify=False).json()
        if data['ok'] == True:
            return data
    except:
        return None


@app.route('/onboard', methods=['POST'])
def all_channels_modal():
    """
    Main command endpoint to hit.
    Currently, it only contains the functionality of the "invite" subcommand.

    NEXT STEP: Put code in a helper function, add parsing for "getchannels" and "invite"

        ARGS:
            n/a, POST request
        RETURNS:
            On success: Launches a modal whose dropdown is populated with the user's channels,
                        200 Response
            On failure: returns error statement
    """

    if request.method == 'POST':
        data = request.form
        user_id = data.get('user_id')

        if data.get('text'):
            new_hire_username = data.get('text')

            if new_hire_username.count("@") == 1:
                new_hire_id = ''
                if len(new_hire_username) > 1 and '@' in new_hire_username:
                    new_hire_id = data.get('text').split('|')[0].split('@')[1]

                if new_hire_id == user_id:
                    return jsonify(response="You cannot add yourself to your own channels. Please try again."), 200

                headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}
                params = {'user': new_hire_id}

                verify_user = requests.get(url='https://slack.com/api/users.profile.get',headers=headers,params=params,proxies=Proxies,
                                           verify=False).json()
                if verify_user['ok'] == False:
                    return jsonify(response="Could not find the user. Please mention a valid user"), 200

                modal_data = views.create_invite_modal(user_id, new_hire_id)

                try:
                    # getting all the channels of the user
                    all_channels_of_the_user = find_user_all_channels_helper(user_id)

                    if all_channels_of_the_user is not None and all_channels_of_the_user['ok'] == True:
                        channels = all_channels_of_the_user['channels']
                        channel_ids = []
                        channel_names = []

                        for channel in channels:
                            channel_ids.append(channel['id'])
                            channel_names.append(channel['name'])

                    # sending all the channels of the user in a modal view

                    modal_data['blocks'][3]['element']['options'] = views.build_options(channel_names, channel_ids)
                    priv_data = {
                        "new_hire_id": new_hire_id,
                        "channel_requested": data.get('channel_id')
                    }

                    modal_data['private_metadata'] = json.dumps(priv_data)
                    params = {"trigger_id": data.get("trigger_id"), "view": json.dumps(modal_data)}

                    try:
                        api_call_data = requests.post(url='https://slack.com/api/views.open',
                                                      headers=headers, data=params, proxies=Proxies,
                                                      verify=False).json()
                        return '', 200

                    except:
                        return jsonify(response="Error communicating with external server.. Try again"), 200
                except:
                    return jsonify(response="Error communicating with Internal Server. Try again"), 200
                else:
                    return jsonify(response="Please mention a valid user.. Try again"), 200

            elif new_hire_username.count("@") > 1:
                return jsonify(response="Please mention only one user at a time.. Try again"), 200
            else:
                return jsonify(response="Please mention only  username after your command.. Try again"), 200
        else:
            return jsonify(response="You need to mention a user after your slash command"), 200





def add_user_to_channels_async(channels_ids, new_hire_id, chat_channel):
    """
    Asynchronous method to add users to all the provided channels.

        ARGS:
            channels_ids: a list of channel ids to add the user to
            new_hire_id: the user id of the user to be added to the list
            chat_channel: the channel the request was passed from
        RETURNS:
            On success: Returns messages confirming the channels the user was able to be added to,
                        as well as channels they were unable to be added to. 200 Response
            On failure: Return error message.
    """
    user_id = new_hire_id

    headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}
    errors = []

    for channel_id in channels_ids:
        params = {'channel': f'{channel_id}', 'users': f'{user_id}'}
        data = requests.post(url='https://slack.com/api/conversations.invite', proxies=Proxies, headers=headers,
                             params=params, verify=False).json()
        if data['ok'] == False:
            errors.append(data['error'])

    confirmation_data = find_user_all_channels_helper(new_hire_id)

    if confirmation_data is not None:
        new_hire_channels = confirmation_data['channels']
        new_hire_channel_ids = {}

        for channel in new_hire_channels:
            new_hire_channel_ids[channel['id']] = True

        added = [channel for channel in channels_ids if channel in new_hire_channel_ids]
        not_added = [channel for channel in channels_ids if channel not in added]
        errors = [item.replace('not_in_channel',
                               'Add The App to the inviting channels Before using slash command') for item in errors]

        added_message = []
        not_added_message = []

        if len(added) >= 1 and len(not_added) <= 0:
            added_message = views.message_display_channels(f"<@{new_hire_id}> was added to the following channels:")
            added_message[2]['fields'] = views.build_field(added)

        elif len(added) >= 1 and len(not_added) >= 1:
            added_message = views.message_display_channels("<@" + new_hire_id + "> was added to the following channels:")
            added_message[2]['fields'] = views.build_field(added)

            not_added_message = views.message_display_channels(f"<@{new_hire_id}> was NOT added to the following channels:")
            not_added_message[2]['fields'] = views.build_field(not_added)

        else:
            not_added_message = views.message_display_channels(f"<@{new_hire_id} was NOT added to the following channels:")
            not_added_message[2]['fields'] = views.build_field(not_added)

        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}

        if added_message is not None:
            params = {'channel': f'{chat_channel}', 'blocks': json.dumps(added_message)}
            requests.post(
                url='https://slack.com/api/chat.postMessage',
                headers=headers,
                params=params,
                proxies=Proxies,
                verify=False)

        if not_added_message is not None:
            params = {'channel': f'{chat_channel}', 'blocks': json.dumps(not_added_message)}
            requests.post(
                url='https://slack.com/api/chat.postMessage',
                headers=headers,
                params=params,
                proxies=Proxies,
                verify=False)

        return 200

    else:
        return 'Error Communicating with external Server', 200

    return (f'Try Again.Response code :{Response()},The Response is : {data}'), 200




@app.route('/interaction', methods=['POST'])
def interaction_manager():
    """
    Interaction manager for the invite modal.
    Responds to post request, specifically receives data send from Slack Server via POST request.
    Enacted after a modal sends a block_actions or view_submission payload.
        ARGS:
            n/a
        RETURNS:
            200 OK Response
    """

    if request.method == 'POST':
        # immut to dict
        data = request.form.to_dict()
        # only one key and val is string, extracting the string
        data_payload = json.loads(data['payload'])

        if data_payload['view']['callback_id'] == "invite-modal":
            metadata = json.loads(data_payload['view']['private_metadata'])
            new_hire_id = metadata['new_hire_id']
            chat_channel = metadata['channel_requested']

            channel_selection = data_payload['view']['state']['values']['channel_selection']
            selected_options = channel_selection['multi_static_select-action']['selected_options']

            channel_ids = [value['value'] for value in selected_options]

            length = len(channel_ids)
            if length == 0:
                return {
                    "response_action": "errors",
                    "errors": {
                        "channel_selection": "You must select one or more  options from the list."
                    }
                }

            if data_payload['type'] == 'view_submission':
                thr = Thread(target=add_user_to_channels_async, args=[channel_ids, new_hire_id, chat_channel])
                thr.start()

            return Response(), 200





# main driver function
if __name__ == '__main__':
    app.run()
