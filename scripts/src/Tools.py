class Tools:

    def isConnected(self, a, b, d):
        (x,y)=a
        (z,w)=b
        if (z>=x-d and z<=x+d) and (w>=y-d and w<=y+d):
            return 1
        else:
            return 0
