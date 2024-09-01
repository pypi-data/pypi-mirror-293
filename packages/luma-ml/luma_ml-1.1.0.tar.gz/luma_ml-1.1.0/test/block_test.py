import luma
import numpy as np

from luma.neural.block import MobileNetBlock

X = np.random.randn(100, 32, 24, 24)
dX = np.random.randn(100, 64, 24, 24)

se = MobileNetBlock.InvertedRes_SE(32, 64)

out = se.forward(X)
print("forward out:", out.shape)

d_out = se.backward(dX)
print("backward out:", d_out.shape)
