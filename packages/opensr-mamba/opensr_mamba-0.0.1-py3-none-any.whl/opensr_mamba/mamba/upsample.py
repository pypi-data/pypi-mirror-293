import torch
import math

class Upsample(torch.nn.Sequential):
    """Upsample module.

    Args:
        scale (int): Scale factor. Supported scales: 2^n and 3.
        num_feat (int): Channel number of intermediate features.
    """

    def __init__(self, scale, num_feat):
        m = []
        if (scale & (scale - 1)) == 0:  # scale = 2^n
            for _ in range(int(math.log(scale, 2))):
                m.append(torch.nn.Conv2d(num_feat, 4 * num_feat, 3, 1, 1))
                m.append(torch.nn.PixelShuffle(2))
        elif scale == 3:
            m.append(torch.nn.Conv2d(num_feat, 9 * num_feat, 3, 1, 1))
            m.append(torch.nn.PixelShuffle(3))
        else:
            raise ValueError(f'scale {scale} is not supported. Supported scales: 2^n and 3.')
        super(Upsample, self).__init__(*m)


class UpsampleOneStep(torch.nn.Sequential):
    """UpsampleOneStep module (the difference with Upsample is that it always only has 1conv + 1pixelshuffle)
       Used in lightweight SR to save parameters.

    Args:
        scale (int): Scale factor. Supported scales: 2^n and 3.
        num_feat (int): Channel number of intermediate features.
    """

    def __init__(self, scale, num_feat, num_out_ch):
        self.num_feat = num_feat
        m = []
        m.append(torch.nn.Conv2d(num_feat, (scale**2) * num_out_ch, 3, 1, 1))
        m.append(torch.nn.PixelShuffle(scale))
        super(UpsampleOneStep, self).__init__(*m)

