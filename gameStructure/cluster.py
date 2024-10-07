

class Cluster:
    def __init__(self, initialTile):
        self.tileCluster = [initialTile]

    def collect(self):
        sum = 0
        for tile in self.tileCluster:
            sum += tile.collect()

        return sum

    def addTile(self, Tile):
        self.tileCluster.append(Tile)

    def transferTilesToNewCluster(self, newCluster):
        for tile in self.tileCluster:
            tile.setCluster(newCluster)
            newCluster.addTile(tile)

    def transferTilesFromCluster(self, oldCluster):
        for tile in oldCluster:
            tile.setCluster(self)
            self.addTile(tile)

