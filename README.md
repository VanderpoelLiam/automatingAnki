# In Action
![script running](https://github.com/VanderpoelLiam/automatingAnki/blob/master/images/running.gif)

# Configuration
Before running the script, the following constants must be set depending on your screen size and where you have the Anki application open:

```
FRONT = (1000, 163)
DEFINITION = (1000, 283)
BACK = (1000, 340)
FULL_SENTENCE = (1000, 401)
EXTRA_INFO = (1000, 460)
GET_2_CARDS = (1000, 522)
ADD = (1695, 1055)
HORIZONTAL_MIDPOINT = 960
```
These represent the locations of the various buttons in Anki. I have Anki open on the right half of my screen as such:

![screen setup](https://github.com/VanderpoelLiam/automatingAnki/blob/master/images/ankiLocation.png)

This means I must also set the location the Firefox browser opens. So the window size in the following function should be modified:

```
def setBrowserLocation(driver):
    driver.set_window_position(0, 0)
    driver.set_window_size(960, 1053)
```

To ensure Anki and Firefox are located as such on the screen:
![firefox open](https://github.com/VanderpoelLiam/automatingAnki/blob/master/images/firefoxOpen.png)


To set these values, I obtained the cursor location on Ubuntu by entering in the terminal:

`$ xdotool getmouselocation --shell`



# Running the script
The program takes a German word as input. I use the adjective `mutig` (which means brave) as an example.

To run the program:

`python3 main.py mutig`

Or, copy `mutig` to the clipboard and enter:

`python3 main.py mutig`

The terminal gives instructions, so simply follow the given prompts.
