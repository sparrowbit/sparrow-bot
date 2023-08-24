import os
# Use the package we installed
from slack_bolt import App
# import env keys
from dotenv import load_dotenv


# Load the variables from the .env file
load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"
# check out listeners argument - https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() will send the message where event is triggered
    say(f"Hey there <@{message['user']}>! , How are you doing today?")


# Interactivity events
# 01. First, we’ll send a message that contains an interactive component (in this case a button)
# 02. Next, we’ll listen for the action of a user clicking the button before responding
@app.message("hey")
def message_hey(message, say):
    # say() will send the message to the channel where event was triggered
    say(

        # The value inside of say() is now an object that contains an array of blocks.
        # Blocks are the building components of a Slack message and can range from text to images to
        # datepickers. In this case, your app will respond with a section block that includes a button as
        # an accessory. Since were using blocks, the text is a fallback for notifications and accessibility.

        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }

            }
        ],
        text=f"Hey there, <@{message['user']}>!"
    )


# Let’s add a handler to send a followup message when someone clicks the button, it need the "action_id" from accessories above
@app.action("button_click")
def button_click_action(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}>clicked this button.")

# LISTENING TO MESSAGES
# listen to messages that arent type of messages like an emoji
@app.message(":wave")
def react_to_wave_emoji(message, say):
  user = message['user']
  say(f"hello there 👋 <@{user}>")
  
# LISTENING TO EVENTS

# Start your app
# this http server is using a built in development adapter which is reponsible for handling
# and parsing events from slack
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
