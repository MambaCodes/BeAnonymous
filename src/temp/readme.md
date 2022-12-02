# What Happens Here?

## Step by Step Explaination : 

-  	After the Script is inputted, a Simple Plain tts is Generated 
	with the Help of pyttsx3. --> normal_tts.mp3

- 	Then Using `normal_tts.mp3` a new mp3 is created
	which is --> `final_tts.mp3` , 
	also the previous `normal_tts.mp3` will be removed in this
	step.

- 	Now with the help of Video Generator a new video is Generated using 
	- 	`final_tts.mp3` 
	- 	`Background Video`
	- 	`Background Audio`
	- 	`Anonymous Intro` (*optional)
- 	`output_video.mp4` is obtained at Desired Destination.


