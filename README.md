# inpututil
Keyboard and Mouse input utility for Windows.

Detects the state of all keyboard and mouse keys through their Virtual Key (VK) codes. This is done through an input loop.

Can be paused and resumed.

Supports binding functions to individual keys or key combinations (**bind_hotkey** function). Every hotkey is executed through a separate thread.

You can bind a pause hotkey through the function **bind_pause_hotkey**; the main input loop will pause or resume when you press that key.

You can make it only work when a specific window is selected ie. it can automatically pause and resume itself to reduce CPU usage.
