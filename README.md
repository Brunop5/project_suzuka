# Tutorial
1. to setup the whole project, you need to run the posting/setup.sh file first by:
    - opening terminal in the project_suzuka-main/ directory
    - once in the directory, run : "sudo chmod +x posting/setup.sh", and when prompted, input password
    - then run: "bash posting/setup.sh"
    - this will install all the dependencies and create executables.
2. once it is ran, two executables will show up in the project_suzuka-main/ directory:
    - run_post.sh (runs the main app for posting)
    - setup_env.sh (runs the app for setting up api keys)
3. to run either of them, right click on them and choose "run as a program"

- to gather information on working with the apps and gathering api keys, you can check the tutorials in "project_suzuka-main/posting/tutorials/" directory


# Current State
  - automatic running through crone is ready(not needed for now)
  - python enviroment is set up
  - ## SETUP
    - shows a window that inputs api keys and tokens
    - you can test them
    - you can save them as enviroment variables(stays within the computer, is safe)
    - you can change already existing ones(by saving a new one under the same name)
    - platforms easily implementable
    - DISCORD, REDDIT, PATREON

  - ## POST APP
    - python app that has title and text input field
    - simply edits text to short posts from a premium post
    - checkboxes for where you want to send and what form, and logs
    - DISCORD, REDDIT
  
# TODO
## Bruno
  - finish patreon posting
    - update script to work with multiple browsers(safari too)
  - twitter posting (api)
  - look into linkedin
  - write tutorial for post app

## Ashley
  - create discord account for code updates(optional but great)
  - set up all accounts for api intergration based on tutorial
