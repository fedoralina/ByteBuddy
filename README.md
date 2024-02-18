# ByteBuddy
ByteBuddy is planned to be a multimodal game in the field of computer science education with the goal to teach elementary school students programming concepts. Here, speech, touch gesture and facial features are used to solve the levels of mazes.

ByteBuddy B, the personal robot of the player walking through the mazes, will be supporting the player to learn the concepts of programming.

## Face
Use of [Openface 2.0](https://github.com/TadasBaltrusaitis/OpenFace?tab=readme-ov-file) for the extraction of Action Units (AUs) and landmarks for further processing.

## Gesture
Code based on the `$Q` implementation from https://github.com/shakyaprashant/qdollar .

## UI Prototype with Figma

The prototype can be tried out [here](https://www.figma.com/file/Qrn9PIKYjyVjBp93YwEBZ5/ByteBuddy?type=design&node-id=0%3A1&mode=design&t=g1R6L5dZluDlRgto-1).

For now, only the Start Screen, the Intro and the Intro to Level 1 are included to show the functionality of how the player gets information to play the game. 

## Future Work
+ include speech
+ evaluate with real users which face feature is the most robust to use (or mixture of both)
+ Action Units: currently only the smiling AUs are checked for activation against a threshold. It may make sense to check which other AUs are activated as well &rightarrow; if other AUs are activated over a certain time window as well, it may not be a smile.

