Deconstruct drum sample into noise and tone based parameters, allowing user to adjust the tonal component (stuff like pitch up or down) without changing the pitch of noise component.

The current tools that allow working with drum samples would change the pitch of the noise component along with the tonal component on repitching. A lot of the drum sound character is in its noise component, our attempt is to build a tool (synthesiser) that allows us to retain the original noise component during repitching

Our approach involves the following stages -

### Extracting the harmonic and residual components

1. Identify the top n (around 3 to 5) frequencies for the tonal component, which would be picked based on a measure that reflects their cumulative energy across the sample length.
2. Similarly identify the top m (around 6-8) frequency bands (NOT frequencies) for the residual component, based on their cumulative energy across the sample length.
3. For these frequencies (and bands), take their time varying magnitude spectrum envelope. 

### Fitting ADSR curves for time varying sounds

1. These time varying envelopes would be very noisy, we capture their essence by modelling them as ADSR curves, which is similar to their shape in time domain for some drum sounds we observed.
2. These best fit ADSR curve values are obtained using genetic algorithms right now, the chromosomes would be length 4 vectors.
3. The evaluation function for this ADSR curve would simply be the L1 or L2 error between the predicted curve and the original time varying envelope. The genetic algorithm would pick the chromosome that minimises this error.

### Synthesising the sound

1. For each curve obtained from stage 1, we get 4 values as ADSR.
2. Thus for each curve, we can provide 4 knobs that could be modified by the user to adjust the amplitude envelope of the drum sound.
3. Many more parameters can be thought of in terms of this representation. 
