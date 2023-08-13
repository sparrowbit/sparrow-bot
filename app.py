import os
# Use the package we installed
from slack_bolt import App
# import env keys
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

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


# Add functionality here
# @app.event("app_home_opened") etc
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This is Sparrow Bot Developed by Team Sparrow Bit"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Hello there, this is Sparrow Bot. "
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Say Hello"
                }
              }
            ]
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")


# Start your app
# this http server is using a built in development adapter which is reponsible for handling
# and parsing events from slack
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
