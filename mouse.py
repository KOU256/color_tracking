import cv2


class Mouse:
    def __init__(self, window_name):
        self.mouseEvent = {"x": None, "y": None, "event": None, "flags": None}
        cv2.setMouseCallback(window_name, self.__CallBack__, None)

    def __CallBack__(self, event_type, x, y, flags, userdata):
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = event_type
        self.mouseEvent["flags"] = flags

    def getData(self):
        return self.mouseEvent

    def getEvent(self):
        return self.mouseEvent["event"]

    def getFlags(self):
        return self.mouseEvent["flags"]

    def getX(self):
        return self.mouseEvent["x"]

    def getY(self):
        return self.mouseEvent["y"]

    def getPos(self):
        return self.mouseEvent["x"], self.mouseEvent["y"]