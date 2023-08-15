https://github.com/steven2358/awesome-generative-ai#text

# Overview

Parent: “I want a story for my child that …” 

This prototype will generate a static interview given to parents for this purpose.

Personalization is accomplished by collecting “seeds” (aka tags or images or sounds).

Parents select suitable seeds:
Child life events 
Birthday / First day of school / End of school year
Moving / Funeral / Wedding / new siblings
Difficulty child is having
Fears of things / lack of caution
bed wetting

# Task

Build a prototype able to create parent interviews that collect information about a child, their child’s favorite things that entertain them and the lesson the parent wants the child to learn from the personalized story.

Ideally the prototype will be a python function:

```make_interview(story_seed_db) => url_to_interview_twine```

Such that:

```parent + interview_twine => interview_data```

The input story_seed_db is a dictionary that will contain text descriptions of 
* things children often like vs dislike
* significant events / milestones in life of a child
* significant people in the life of a child
* problems children often have
* feelings children experience 
* lessons / morals parents may want to teach children
* reminders children should not forget

The output `interview_data` is a dictionary that 
* will contain information collected during interview 
* it may be a subset story_seed_db that parent selected

This prototype 
* must use the story_seed_db to create new interviews (generative AI)
* can leverage existing LLMs via APIs or running locally.

Subtasks

Prototype an AI way for parents to pick story elements
Recommendation AI: “Which elements go together?”
For inspiration see https://pcpartpicker.com/list/ 

Twine to assemble narrative, pictures, music, sound effects
* Twine https://twinery.org/ 
* DEMO: https://crowscrowscrows.itch.io/the-temple-of-no   
* https://twine2.neocities.org/#introduction_three-fundamentals-of-harlowe 
Open source / Browser based / Well supported 
