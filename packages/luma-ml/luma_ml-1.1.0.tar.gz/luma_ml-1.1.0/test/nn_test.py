import luma
from luma.neural import model

nn = model.MobileNet_V2()
nn.summarize(in_shape=(-1, 3, 224, 224), n_lines=None)
