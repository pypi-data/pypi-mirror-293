from torch.nn import Module, Sequential, Conv2d, MaxPool2d, ReLU, Flatten,AdaptiveAvgPool2d, Dropout, Linear

class ANet7(Module):
    def __init__(self,classes=10):
        super(ANet7, self).__init__()

        self.block1 = Sequential(
          Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
          ReLU(inplace=True),
          MaxPool2d(kernel_size=2, stride=2, padding=0),
        )

        self.block2 = Sequential(
          Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
          ReLU(inplace=True),
          Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
          ReLU(inplace=True),
          MaxPool2d(kernel_size=2, stride=2, padding=0),
        )

        self.block3 = Sequential(
          Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
          ReLU(inplace=True),
          Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1),
          ReLU(inplace=True),
          MaxPool2d(kernel_size=2, stride=2, padding=0),
          AdaptiveAvgPool2d((6, 6))
        )

        self.classification = Sequential(
          Flatten(),
          Dropout(p=0.5),
          Linear(512*6*6,1024),
          Dropout(p=0.5),
          Linear(1024, classes)
        )


    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.classification(x)
        return x