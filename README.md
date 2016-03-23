# Software Development
Deliberately bad code providing the basis for a module in Software Development

#Repository Contents
The game is run from:

- `cardgame.py` : the debug output level can be adjusted in this file

The settings are configured in:

- `config.py` : containing a dictionary of game parameters

Other relevant files for the running of the game:

- `test.py` : unit tests for the base classes and settings
- `game_engine.py` : contains the `game()` class that instantiates players from `actors.py`
- `actors.py` : The classes for the players and central deck
- `common.py` : Common routines inherited by the player and deck classes
- `logs.py` : Logging routines
- `game_art.py` : Game art including an alternative welcome message
- `logging_colorer.py` : Colouring parameters for the logger
- `logging_formatter.py` : Formatting for the logger

Other folders in this directory:

- docs/modifiedcode : Modified code flow diagrams and dependencies
- docs/originalcode : Original code flow diagrams
- docs/usertests : User feedback summary and response sheets


#Code Relationships / Code Structure
!["File Relationships"](https://github.com/flipdazed/SoftwareDevelopment/blob/master/docs/modifiedcode/relationships.png "File Relationships")

##Assessed Criteria: Improvement and Reflection
The main part of this submission should be a new version of the code, implementing the changes you proposed in Planning and Risks. Your submission should include any required files such as build and/or test files. The submitted code must be runnable and be able to be used to play games. 

**Note** The code submission should be a link/reference to a source code control system such as GIT or SVN. 
The repository should contain everything needed to compile the code - including build files which get any required dependencies. Non-working or non-compiling code will be marked down accordingly.

Please note that your code (and any supplied tests) must satisfy the following:

 - It must be possible to build and run your code and tests on the Physics Computational Lab machines.
 - If your code or tests requires additional packages or software to build or test that are not already available on the Physics Computational Lab machines then you should document what these packages or software are and how to set them up - this should include installation and run scripts which will create the required environment for the code to run.

To accompany the code a **short report** is required which should contain a **summary of the changes to the code** that you have made and the **benefits they give to the code**. The report should also contain your **personal reflection on the whole process**, including **how your actual work compared with the plan you created at the start** and did you encounter **any risks you had not considered**.

The short report should include a **future enhancement** you think would improve or add value to the code - you should **summarise the purpose of your proposal** and **highlight any risks or impact** that it may have on the existing code.

The final submission should contain:

 - Improved Code
 - Summary of Changes
 - Reflection on Process
 - Future Enhancement

This component of the submission is worth 40 marks out of 100 marks total for the course.
