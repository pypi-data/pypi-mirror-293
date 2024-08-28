from .DataPipe import DataPipe
from .BatchMap import BatchMap
from .ShuffleMap import ShuffleMap
from .PreloadPipe import PreloadPipe


class DataLoader:
    @staticmethod
    def build(
        data: DataPipe,
        batchSize=1,
        onlyFullBatches=False,
        preload=True,
        preloadCount=1,
        shuffle=False,
        shuffleSeed=None,
        mapBatchToXY=True,
        torch=False,
        torchCuda=False,
    ):
        if shuffle:
            data = ShuffleMap(data, seed=shuffleSeed)

        if batchSize > 1:
            data = BatchMap(data, batchSize, onlyFullBatches, toXY=mapBatchToXY)

        if torch:
            from .TorchMap import TorchMap

            data = TorchMap(data, cuda=torchCuda)

        if preload:
            data = PreloadPipe(data, preloadCount=preloadCount)

        return data
