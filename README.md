# VisualCliffBehaviouralTest
Automatic video processing software for analysis of visual cliff behavioural tests - University Third Year Dissertation Project (2018).

1. Project description

This project consists of two main aims. One of which is analytical and involves biology understanding and the other comprises of visual processing methods and programming.

The first is understanding and analysis of deficiency in stereoscopic vision. Stereoscopic vision is where both eyes are used to get similar but overlapping images in order to achieve depth perception. The inability to perceive depth perception is often hard to detect as it gets confuses as clumsiness. A test used in preclinical behavioural neuroscience to detect this deficiency is visual cliff. This is where a transparent plexiglass surface is supported above the floor and immediately under one side is a patterned material and on the other side the same material is placed some distance below the surface, hence giving an impression of a cliff drop. Healthy subjects, who have depth perception, will see there is a ‘cliff’ and will therefore spend more time on the shallow side in comparison to impaired subjects. Analysis can be carried out by collecting, calculating and comparing parameters such as percentage of time spent on shallow side, movement trajectory, total distance moved and velocity profile.

The second aim is to deliver a working automated video processing software for analysis of visual cliff behavioural tests. It should be able to detect the test subject on the video with a complex background and track its position over time. Methods such as thresholding of the colour red will be used to detect the ears and tail of the mouse and hence be able to track its position over time. On top of this, modelling techniques will be used such as Kalman filter which uses an algorithm to allow the software to predict the motion of the mouse even when it cannot be seen. The data can be collected continuously and in batches, and additional parameters can be calculated from the obtained trajectory in order to be statistically analysed. Additionally, other information for example head angle can be detected. Key parameters will be discussed with biologists later in the project. By the end, there should be a software application with a graphical user interface that will allow data and calculated statistics to be exported to excel.


2.	Literature survey

A similar pre-existing research project was carried out by Jack Saunders in the summer. In his visual behavioural experiment, mice were in a rotating drum with vertical stripes of different dimensions. Depending on how long mice were following the rotation gave information about their deficiencies. Although this project consists of a different experiment, Jack created a video processing software using python to detect the mouse’s trajectory and head angle. In order to detect the mouse, he used thresholding. He managed to track the angle of the mouse’s head by finding the pink ears and taking the centre point. This was done by using the python library OpenCV. [1]

[1] J. Saunders, Y. Hicks, I. Erchova. “Image processing software for automatic scoring of visual acuity tests in preclinical research models”. CUROP Project, Dept. Eng., Cardiff Univ., Cardiff, 2018

OpenCV contains tutorials on different image processing techniques that they offer. For example, they give python tutorials on simple thresholding, adaptive thresholding and Otsu’s thresholding. Due to the nature of my project involving computer programming, there already exists many methods that I could find online and implement into my project. [2]

[2] OpenCV. Open Source Computer Vision. Image Thresholding. (2018) [Online]. Available at:https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html Accessed on: Oct. 17, 2018. 

A study of the same visual cliff test for visual perception in mice has already been completed and analysed. In this article, the test was used to investigate the depth perception in five strains of mice. It showed that four strains of mice were healthy as the mice chose to walk on the ‘safe’ side and avoided the cliff drop. The last strain of mice which had retinal degeneration did not avoid the drop and seemed to show an even split, and hence they did not seem to have depth perception. This test contains useful data and statistics and shows how visual cliff can be used as an effective way to detect deficiency in stereovision. [3]

[3] M.W.Fox. “The visual cliff test for the study of visual depth perception in the mouse” Animal Behaviour., vol.13, no. 2-3, pp. 232-233, April-July 1965.
