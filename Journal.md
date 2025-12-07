# My Journal

This is the journal where I created a project with Arduino.

## So how much time did I spend on that?

In total, I spent about over 13 hours on it...

## My worst hangups

- I couldn't even put the leds in the holes, so I had to grind it all down.
- The RTC module was also giving me weird dates, but I fixed that.
- I made a few coding mistakes.

## Timeline

I thought I would create a system that would monitor temperature and humidity using Arduino and then send the information to Gmail. First I drew everything and started working on it:

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjAyNjUsInB1ciI6ImJsb2JfaWQifX0=--dffa209d73b1ee9702b165cc5bfb55d8af426307/20251206_232301.jpg)

Next, I started creating a GitHub repo and created folders. I also found all the parts so I could put it together. I thought for a while about using RTC, but I got over it and used it.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjAyNjksInB1ciI6ImJsb2JfaWQifX0=--26df50ea322c39e8572847a904ec84c32617bfd4/20251206_211413.jpg)

I started testing all the components to see if they worked. The LCD worked, the Buzzer too... But I forgot to set the RTC, so it told me that today is the year 2087 😭

This: 2087-31-12 03:27:00

I solved the problem by resetting the RTC and I was able to continue building.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjAyNzgsInB1ciI6ImJsb2JfaWQifX0=--a04d52a3db24e6e35ee671c8d80c5bf942d74d31/Sn%C3%ADmek%20obrazovky%202025-12-06%20234423.png)

After testing the components, I jumped into making the 3D case. I took all my measurements and started modeling the bottom part. I gave each piece a small tolerance so it would fit nicely. When I had the bottom finished, I just tried it out to see if everything fit and it did! So I moved on to the top part, which was easy to model.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjAyODQsInB1ciI6ImJsb2JfaWQifX0=--bef9c54564db1dea05fe1de42e0e033b6463797f/Sn%C3%ADmek%20obrazovky%202025-12-06%20225556.png)

When I had the 3D case ready, I started connecting the components. A few times some of the cables fell out, but that was probably the worst problem.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjAyOTIsInB1ciI6ImJsb2JfaWQifX0=--4403a50cff6c159ad2781d506906e7a2f7d729ea/20251206_235604.jpg)

Unfortunately I found a minor problem that I hadn't noticed before. The DHT11 connection is completely extruded, so I had to adjust a few things on the bottom and it should be good now.

After editing the 3D case, I jumped into coding the Arduino. I just wanted the basic logic for the system to send information to the serial monitor, which would then be taken over by the python code, which would then do more things.
I experimented with libraries a few times, but after a while I decided to use the ones in the picture now.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjA0OTUsInB1ciI6ImJsb2JfaWQifX0=--ae09a4bcf0c3bcf21d92a6c3f5cbf4ffdea23df9/image.png)

Once I had the code without errors (hopefully), I could start testing if everything is working properly. I tested if the RTC is showing a good date, and it is. I also tested the sensor to see if it is sending good information and it seems that everything is working perfectly so far!
In the meantime, I printed the bottom part so it would be finished as soon as possible.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjA1MDIsInB1ciI6ImJsb2JfaWQifX0=--0881ee4a249f33221a8a82cb5bc4ca060f90d1eb/20251207_101758.jpg)

Meanwhile, while the bottom part was printing, I started creating python code that would take values ​​from the Arduino and then send emails using Google Code. At first I didn't know how to do it, but then I added things gradually and it became a working code.

When the bottom part was printed, I took it off the printer and prepared a breadboard and components so I could put them inside. It all worked out, but there were a few problems...
The holes for the LEDs were too small, so I had to grind them down and they ended up getting in there. I also kept disconnecting the cables from the components, but I fixed that. Then I had it all ready and tested to see if everything worked. And it did!
Just print the top part, tweak a few things, set the code and everything should hopefully work.

![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjA1NjksInB1ciI6ImJsb2JfaWQifX0=--7a43bf670677a8b683d7a46163506395cc815aa2/20251207_132256.jpg)

I already printed the top part. I put it on top of it and it fit perfectly. I saved the Python code and created a code in Google settings so I could send emails.I was looking for that setting for a while, but after some time I found it.

After about 13 hours of work, I finished this project. Everything works and fits.
I'm very glad it works!
