class Connections:
    def __init__(self, d):
        self.d=d

    def isConnected(self, a, b):
        (x,y)=a
        (z,w)=b
        if (z>=x-self.d and z<=x+self.d) and (w>=y-self.d and w<=y+self.d):
            return 1
        else:
            return 0

    def isConnectedFromRow(self,row):
        return (row["z"] >= row["x"] - self.d and row["z"] <= row["x"] + self.d) and (
                row["w"] >= row["y"] - self.d and row["w"] <= row["y"] + self.d)