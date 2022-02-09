# Step Response Plots
In this expiriment, our lab group used multitasking in order to simultaneously perform step responses on two seperate motors. The two motors were each ran through different distances in order to show their performance. Another abjective of this task was to vary the period for one of the motors and see how this affected the step response. However, our group had issues when it came to plotting values over 20 ms. The way our system was set up consited of three main tasks, one that checks for keyboard input, one that runs a step response and collects data, and one that sends data to the frontend via serial communication. The tasks for keyboard input and sending data were both run at 10 ms. at values of over 20ms for our step respoinse task, data would fail to be sent to the front end for plotting. With that being said, of the values we were able to test, we found that 20 ms overshot the reference value and and didn't correct itself. the best reponse seemed to come when the period was 12ms. At this rate, there was a slight overshoot, but the motor then corrected itself to be near the reference value. This sould indicate that the system would be able to take some slight disturbance and not be severelly affected.
![Step response p=12](https://github.com/cvsantan/Lab-3/blob/main/period%2012.png)

FIGURE 1. Step response produced by motor task running at a period of 12ms

![Step response p=20](https://github.com/cvsantan/Lab-3/blob/main/period%2020.png)

FIGURE 2. Step response plot produced by motor task running at a period of 20ms
