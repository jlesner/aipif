# Overview

Child: “A story just for me?! It lets me decide? Wow!”

# Task

Build a prototype that transforms parent interview_data into a personalized child suitable “choose your way” twine (see https://twinery.org/ ) 

The prototype will be a python function:

```make_narrative(interview_data) => url_to_narative_twine```

The input `interview_data` is a dictionary described in the previous task.

The output `url_to_narative_twine` will be the personalized experience the child interacts with.

This prototype 
* must use interview_data to create personalized twines (generative AI)
* can leverage existing AI generation tools via APIs or running locally

Possible Subtasks
* Investigate child narrative generation with LLMs (ChatGPT, WizardLLM, ...)
* Investigate building datasets to “fine tune” LLMs for children’s narrative 

Datasets
* Child story collections (ebooks?)
** Dr. Suess / P. D. Eastman / Rolad Dahl / Mo Williams
* Child shows (scripts? speech-to-text?)
** Bear in the Big Blue House 
** Sesame Street / “Arthur” / Dora
