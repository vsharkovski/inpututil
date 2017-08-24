"""Keyboard and Mouse input utility for Windows.
Detects keystrokes and mouse clicks.
Supports binding functions to multiple keys."""
import time
from threading import Thread

_DEFAULT_LOOP_TIME = 0.02
_DEFAULT_HOTKEY_TIMEOUT_TIME = 0.02

class InputUtil:
    """Use this."""
    import collections
    _STATE_NOTSTARTED = 0
    _STATE_RUNNING = 1
    _STATE_PAUSED = 2
    _STATE_STOPPED = 3
    _hotkeys = []
    def __init__(self, loop_time=_DEFAULT_LOOP_TIME):
        """loop_time: time the main input loop sleeps after each cycle"""
        self._state = self._STATE_NOTSTARTED
        self.loop_time = loop_time
    def start(self):
        """Start the main input loop"""
        if self._hotkeys.count == 0:
            raise Exception("No hotkeys set, cannot start main input loop")
        for _, hkey in self._hotkeys:
            hkey.start()
        Thread(target=self._start).start()
    def _start(self):
        import win32api
        # pylint: disable=E1101
        self._state = self._STATE_RUNNING
        while True:
            if self._state == self._STATE_RUNNING:
                for kcodes, hkey in self._hotkeys:
                    all_pressed = True
                    for k in kcodes:
                        if not win32api.GetAsyncKeyState(k):
                            all_pressed = False
                            break
                    if all_pressed:
                        hkey.execute()
            elif self._state == self._STATE_PAUSED:
                pass
            elif self._state == self._STATE_STOPPED:
                break
            time.sleep(self.loop_time)
    def pause(self):
        """Pause the main input loop"""
        self._state = self._STATE_PAUSED
    def unpause(self):
        """Unpause (resume) the main input loop"""
        self._state = self._STATE_RUNNING
    def stop(self):
        """Stop the main input loop, effectively killing the thread"""
        self._state = self._STATE_STOPPED
    def bind_hotkey(self, key_codes, func, args, timeout=_DEFAULT_HOTKEY_TIMEOUT_TIME):
        """key_codes (tuple): key codes for the keys needed to be pressed so func(args) happens
        func (function): the function executed
        args (tuple): arguments to be passed
        timeout (int): time to wait after being able to execute again"""
        if isinstance(key_codes, tuple):
            self._hotkeys.append((list(key_codes), Hotkey(func, args, timeout)))
        else:
            self._hotkeys.append((list((key_codes,)), Hotkey(func, args, timeout)))

class Hotkey():
    """Hotkey Class for InputUtil"""
    _executing = False
    _exec_queued = False
    alive = True
    timeout_idle = 0.02
    def __init__(self, func, args, timeout=_DEFAULT_HOTKEY_TIMEOUT_TIME):
        """i don't need no stinkin docstring!"""
        self.func = func
        self.args = args
        self.timeout = timeout
    def start(self):
        """Start main hotkey loop"""
        Thread(target=self._run).start()
    def _run(self):
        """i don't need no stinkin docstring!"""
        while self.alive:
            if self._exec_queued:
                self._executing = True
                self.func(self.args)
                time.sleep(self.timeout)
                self._exec_queued = False
                self._executing = False
                continue
            time.sleep(self.timeout_idle)
    def execute(self):
        """Execute hotkey"""
        if not self._executing:
            self._exec_queued = True
    def kill(self):
        """Kill main hotkey loop, effectively killing the thread"""
        self.alive = False

VK = {
    'ABNT_C1' : 0xC1,
    'ABNT_C2' : 0xC2,
    'ADD' : 0x6B,
    'ATTN' : 0xF6,
    'BACK' : 0x08,
    'CANCEL' : 0x03,
    'CLEAR' : 0x0C,
    'CRSEL' : 0xF7,
    'DECIMAL' : 0x6E,
    'DIVIDE' : 0x6F,
    'EREOF' : 0xF9,
    'ESCAPE' : 0x1B,
    'EXECUTE' : 0x2B,
    'EXSEL' : 0xF8,
    'ICO_CLEAR' : 0xE6,
    'ICO_HELP' : 0xE3,
    'KEY_0' : 0x30,
    'KEY_1' : 0x31,
    'KEY_2' : 0x32,
    'KEY_3' : 0x33,
    'KEY_4' : 0x34,
    'KEY_5' : 0x35,
    'KEY_6' : 0x36,
    'KEY_7' : 0x37,
    'KEY_8' : 0x38,
    'KEY_9' : 0x39,
    'KEY_A' : 0x41,
    'KEY_B' : 0x42,
    'KEY_C' : 0x43,
    'KEY_D' : 0x44,
    'KEY_E' : 0x45,
    'KEY_F' : 0x46,
    'KEY_G' : 0x47,
    'KEY_H' : 0x48,
    'KEY_I' : 0x49,
    'KEY_J' : 0x4A,
    'KEY_K' : 0x4B,
    'KEY_L' : 0x4C,
    'KEY_M' : 0x4D,
    'KEY_N' : 0x4E,
    'KEY_O' : 0x4F,
    'KEY_P' : 0x50,
    'KEY_Q' : 0x51,
    'KEY_R' : 0x52,
    'KEY_S' : 0x53,
    'KEY_T' : 0x54,
    'KEY_U' : 0x55,
    'KEY_V' : 0x56,
    'KEY_W' : 0x57,
    'KEY_X' : 0x58,
    'KEY_Y' : 0x59,
    'KEY_Z' : 0x5A,
    'MULTIPLY' : 0x6A,
    'NONAME' : 0xFC,
    'NUMPAD0' : 0x60,
    'NUMPAD1' : 0x61,
    'NUMPAD2' : 0x62,
    'NUMPAD3' : 0x63,
    'NUMPAD4' : 0x64,
    'NUMPAD5' : 0x65,
    'NUMPAD6' : 0x66,
    'NUMPAD7' : 0x67,
    'NUMPAD8' : 0x68,
    'NUMPAD9' : 0x69,
    'OEM_1' : 0xBA,
    'OEM_102' : 0xE2,
    'OEM_2' : 0xBF,
    'OEM_3' : 0xC0,
    'OEM_4' : 0xDB,
    'OEM_5' : 0xDC,
    'OEM_6' : 0xDD,
    'OEM_7' : 0xDE,
    'OEM_8' : 0xDF,
    'OEM_ATTN' : 0xF0,
    'OEM_AUTO' : 0xF3,
    'OEM_AX' : 0xE1,
    'OEM_BACKTAB' : 0xF5,
    'OEM_CLEAR' : 0xFE,
    'OEM_COMMA' : 0xBC,
    'OEM_COPY' : 0xF2,
    'OEM_CUSEL' : 0xEF,
    'OEM_ENLW' : 0xF4,
    'OEM_FINISH' : 0xF1,
    'OEM_FJ_LOYA' : 0x95,
    'OEM_FJ_MASSHOU' : 0x93,
    'OEM_FJ_ROYA' : 0x96,
    'OEM_FJ_TOUROKU' : 0x94,
    'OEM_JUMP' : 0xEA,
    'OEM_MINUS' : 0xBD,
    'OEM_PA1' : 0xEB,
    'OEM_PA2' : 0xEC,
    'OEM_PA3' : 0xED,
    'OEM_PERIOD' : 0xBE,
    'OEM_PLUS' : 0xBB,
    'OEM_RESET' : 0xE9,
    'OEM_WSCTRL' : 0xEE,
    'PA1' : 0xFD,
    'PACKET' : 0xE7,
    'PLAY' : 0xFA,
    'PROCESSKEY' : 0xE5,
    'RETURN' : 0x0D,
    'SELECT' : 0x29,
    'SEPARATOR' : 0x6C,
    'SPACE' : 0x20,
    'SUBTRACT' : 0x6D,
    'TAB' : 0x09,
    'ZOOM' : 0xFB,
    '_none_' : 0xFF,
    'ACCEPT' : 0x1E,
    'APPS' : 0x5D,
    'BROWSER_BACK' : 0xA6,
    'BROWSER_FAVORITES' : 0xAB,
    'BROWSER_FORWARD' : 0xA7,
    'BROWSER_HOME' : 0xAC,
    'BROWSER_REFRESH' : 0xA8,
    'BROWSER_SEARCH' : 0xAA,
    'BROWSER_STOP' : 0xA9,
    'CAPITAL' : 0x14,
    'CONVERT' : 0x1C,
    'DELETE' : 0x2E,
    'DOWN' : 0x28,
    'END' : 0x23,
    'F1' : 0x70,
    'F10' : 0x79,
    'F11' : 0x7A,
    'F12' : 0x7B,
    'F13' : 0x7C,
    'F14' : 0x7D,
    'F15' : 0x7E,
    'F16' : 0x7F,
    'F17' : 0x80,
    'F18' : 0x81,
    'F19' : 0x82,
    'F2' : 0x71,
    'F20' : 0x83,
    'F21' : 0x84,
    'F22' : 0x85,
    'F23' : 0x86,
    'F24' : 0x87,
    'F3' : 0x72,
    'F4' : 0x73,
    'F5' : 0x74,
    'F6' : 0x75,
    'F7' : 0x76,
    'F8' : 0x77,
    'F9' : 0x78,
    'FINAL' : 0x18,
    'HELP' : 0x2F,
    'HOME' : 0x24,
    'ICO_00' : 0xE4,
    'INSERT' : 0x2D,
    'JUNJA' : 0x17,
    'KANA' : 0x15,
    'KANJI' : 0x19,
    'LAUNCH_APP1' : 0xB6,
    'LAUNCH_APP2' : 0xB7,
    'LAUNCH_MAIL' : 0xB4,
    'LAUNCH_MEDIA_SELECT' : 0xB5,
    'LBUTTON' : 0x01,
    'LCONTROL' : 0xA2,
    'LEFT' : 0x25,
    'LMENU' : 0xA4,
    'LSHIFT' : 0xA0,
    'LWIN' : 0x5B,
    'MBUTTON' : 0x04,
    'MEDIA_NEXT_TRACK' : 0xB0,
    'MEDIA_PLAY_PAUSE' : 0xB3,
    'MEDIA_PREV_TRACK' : 0xB1,
    'MEDIA_STOP' : 0xB2,
    'MODECHANGE' : 0x1F,
    'NEXT' : 0x22,
    'NONCONVERT' : 0x1D,
    'NUMLOCK' : 0x90,
    'OEM_FJ_JISHO' : 0x92,
    'PAUSE' : 0x13,
    'PRINT' : 0x2A,
    'PRIOR' : 0x21,
    'RBUTTON' : 0x02,
    'RCONTROL' : 0xA3,
    'RIGHT' : 0x27,
    'RMENU' : 0xA5,
    'RSHIFT' : 0xA1,
    'RWIN' : 0x5C,
    'SCROLL' : 0x91,
    'SLEEP' : 0x5F,
    'SNAPSHOT' : 0x2C,
    'UP' : 0x26,
    'VOLUME_DOWN' : 0xAE,
    'VOLUME_MUTE' : 0xAD,
    'VOLUME_UP' : 0xAF,
    'XBUTTON1' : 0x05,
    'XBUTTON2' : 0x06
}
