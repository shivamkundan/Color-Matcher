# Color Matcher
 Matches input RGB values to closest color in the stored database. 
 
Developed for use in my tricorder project with its photo-spectrometer (AS7411) providing the input.

## Database
Color names and values acquired from the following sources:
* https://web.njit.edu/~walsh/rgb.html
* https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F
* https://en.wikipedia.org/wiki/List_of_colors:_G%E2%80%93M
* https://en.wikipedia.org/wiki/List_of_colors:_N%E2%80%93Z

## Screen Recording
A sample using random RGB inputs. Colors with average RGB distance of < 10 seem to match pretty closely. However, some colors still look quite different even with < 10 difference. Probably a subjective thing depending upon the monitor and the viewers vision.

<img src="example.gif"  width="100%" height="100%">
