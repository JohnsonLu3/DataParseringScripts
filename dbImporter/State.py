class state:
    stateFid = None
    stateName = None
    polygon = None
    year = None
    clickCount = None

    def state(self, stateFid, stateName, polygon, year, clickCount):
        self.stateFid = stateFid
        self.stateName = stateName
        self.polygon = polygon
        self.year = year
        self.clickCount = clickCount

    def setstateFid(self, stateFid):
        self.stateFid = stateFid

    def setstateName(self, stateName):
        self.stateName = stateName

    def setpolygon(self, polygon):
        self.polygon = polygon

    def setyear(self, year):
        self.year = year

    def setclickCount(self, clickCount):
        self.clickCount = clickCount
