# PYtibiaAutoHeal
A healing bot made for a game named "Tibia" but can be used for other purposes

A python script inspired by cnmoro's outdated healer. Checks pixels on your screen and presses a button on 0.5 second intervals until the color turns to original. More than 1 pixel can be tracked


How to use:
1.Install needed python libraries in the code if needed

Add pixel creates a row in which you can choose a certain pixel on your screen to record it's position and original color. (Example can be on healthbar where at which point you want a healing spell or potion to go off)
  A prompt comes up when "select" is pressed. After which you need to move your cursor onto the pixel you want to select and press enter twice.
  First enter closes the prompt but second enter determines the pixel you are choosing

You can then select which button is pressed when said pixel changes colors on dropdown menu

You can then assign priority to each row. (Lower number means higher priority)
  Do note that rows with higher priority (lower number) override the lower priority (they dont work)
  If higher priority pixel is in it's original color then next higher priority is functional (if the color is different)

You can bypass priority order with always check checkbox
  Any row with always check box marked is functional regardless of priority.
  Multiple pixel checks can occur at the same time if the box is marked. Otherwise only the highest prio is active.

Once you set up your pixels you can then press "start monitoring" to activate the checks.
You can pause the monitoring with "stop monitoring" button

You can add more rows with add pixel and pause each individual row at will.
  You need to STOP MONITORING first before you pause individual rows

I am not responsible for any bans/in game deaths etc. as I reckon the script can easily be detected with anticheat programs 
I am using this script for my personal private server.
Again, DO NOT RUN THIS ON OFFICIAL TIBIA SERVERS, YOU'LL MOST LIKELY GET BANNED
No promises of program working bug free but as far as I'm concerned it is useful. Test it yourself before running.
The only reason for this is on github is to provide to those who just want to chill playing Tibia OTS out of feeling nostalgia
Feel free to contact me on github or make an issue thread for anything you wanna know
