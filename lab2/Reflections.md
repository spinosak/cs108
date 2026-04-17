### Reflection/Observations Reaction Diffusion

Run the simulation and let it develop for at least 30 seconds before interacting.

**1. Describe what you see during the first 10 seconds. How does the pattern change over time?**

The animation starts out as a sqaure and then starts spreading. The corners start to stretch. It reminds me of a kaleidescope painitng app my mom used to have on her iPad when I was younger. The gow spreads at the corners, but it also gets darker.

**2. Click and drag on the canvas. What happens where you paint? Does the pattern respond differently in areas that are already patterned versus empty areas?**

When you paint in an empty area it reacts similarly to the square that starts out in the middle it starts spreading. When you paint over an already patterned area it creates more blank space where you painted.

### Exploration
Try each parameter set below. Let each run for ~30 seconds. Write one word describing each pattern.

| F     | k     | Your description |
|-------|-------|-----------------|
| 0.035 | 0.065 | Instead of lines,  start seeing dots appear. Reminded me of the inside of a cheese grater.|
| 0.012 | 0.050 | Spreads much faster than the previous two and changes faster. It was interesting to watch|
| 0.025 | 0.055 | Also spreads faster. definetly more yellow. It reminds me of a ripple effect.|


**Which combination (F, k, colormap) do you find most visually interesting? Why?**  
I thought (0.012, 0.050, binary) was visually interesting in the sense that watching the animation play out was entertaining. But it also reminded me of those scenes in movies where they'll have somoene stare at a screen and they end up hypnotized. I could definetly see them using an animation like this one for that purpose.

### Reflection/Observations Particle Life

**1. Without changing anything, describe the overall behavior after ~20 seconds. Do the colors cluster? Scatter? Chase each other?**

The colors look like they're boucing off each other. Green seems to cluster together and blue seems to join in. Orange and red seeem to stay away from the blue and green. It's entertaining. 

**2. Run the script again (a new random attraction matrix is generated each time). How different is this run from the last? What does that tell you about the role of the attraction matrix?**

It's really random, but looks like the orange and red are starting to cluster. I think the attraction matrix is in charge of the "attraction" rules like which color is attracted to which and which color wanst to form clusters and which colors stay spread out. 

### Reflection/Observations Double Pendulum

**1. For the first several seconds, the trails stay close together. Then they diverge. Approximately how long does it take before the trails look completely different from each other?**  

It takes about 20-30 seconds for the image to become more "stable".

**2. Try changing `base_angle` to `np.pi * 0.2` (a small, low-energy swing). Do the trails diverge as quickly? Why do you think that is?**  

The image becomes more stable faster. At first, it seems that it's doign to be slower. but then it seems to build from the bottom up really quickly. 

### Reflection/Observations Generative Galaxy

**1. Run the script twice without changing anything. Describe how the two galaxies differ. What is the source of that variation?**
The position of the stars and how much they glow changes. It's hard to tell since there is a lot of stars, but the stars are not in the same position. I think this variation comes from mathmatical noise and the spiral formula probably helps with the variations. 


**2. Change `NUM_ARMS` to `2`, then `6`. How does the visual feel change?**

When NUM_ARMS is changed to '2' if feels less busy. There is a lot more going on when it is set to 6. It's like how much of the stars you can see when there's light pollution. 