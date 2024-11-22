"""
@Author: Conghao Wong
@Date: 2024-10-31 20:03:29
@LastEditors: Ziqian Zou
@LastEditTime: 2024-11-04 16:55:34
@Github: https://cocoon2wong.github.io
@Copyright 2024 Conghao Wong, All Rights Reserved.
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch

from qpid.model import Model
from qpid.mods import vis
from qpid.utils import dir_check, get_mask

COLOR_HIGH = np.array([0xe7, 0xe7, 0x71], np.float32)
# COLOR_MID = np.array([0x1e, 0x9e, 0xee], np.float32)
COLOR_LOW = np.array([0xf8, 0x77, 0x61], np.float32)

ROOT_DIR = './temp_files/gp'

v = None


def draw(model: Model, clip: str,
         obs: torch.Tensor,
         nei: torch.Tensor,
         f_re_meta: torch.Tensor,
         w_max=0.2,
         w_min=0.05):

    global v
    if v is None:
        v = vis.Visualization(manager=model.manager,
                              dataset=model.args.dataset,
                              clip=clip)

    nei_count = int(torch.sum(get_mask(torch.sum(nei, dim=[-1, -2]))))
    _nei = nei[0, :nei_count]
    _obs = obs[0]

    l = torch.norm(_obs[-1] - _obs[0], dim=-1)
    r_max = w_max * l
    r_min = w_min * l

    plt.close()
    plt.figure()
    v._visualization_plt(None, obs=_obs, neighbor=_nei)

    text_delta = r_min.numpy()

    # Compute radiuses
    r_re_real = torch.sum(f_re_meta ** 1, dim=-1)[0, :nei_count]
    r = (r_re_real/torch.max(r_re_real))

    for index, (_nei_p, _r) in enumerate(zip(_nei[..., -1, :], r)):

        _radius = (r_min + (r_max - r_min) * _r).numpy()
        _color = COLOR_LOW + (COLOR_HIGH - COLOR_LOW) * _r.numpy()
        _pos = (float(_nei_p[0]), float(_nei_p[1]))

        _circle = plt.Circle(_pos, _radius,
                             fill=True, color=list(_color/255), alpha=0.6)
        plt.gca().add_artist(_circle)

        plt.text(_pos[0] + text_delta, _pos[1] + text_delta, str(index),
                 color='white',
                 bbox=dict(boxstyle='round', alpha=0.5))

    plt.show()


def draw_spectrums(nei: torch.Tensor,
                   Tlayer: torch.nn.Module,
                   length_gain=50):

    nei_count = int(torch.sum(get_mask(torch.sum(nei, dim=[-1, -2]))))
    nei_spec = Tlayer(nei[0, :nei_count] - nei[0, :nei_count, -1:, :])

    # Compute new shape (after resize)
    shape = nei_spec[0].shape
    new_shape = (shape[0] * length_gain,
                 shape[1] * length_gain)

    # Batch normalize -> (0, 1)
    nei_spec = (nei_spec - nei_spec.min()) / (nei_spec.max() - nei_spec.min())

    r = dir_check(ROOT_DIR)
    for index, _spec in enumerate(nei_spec):
        p = os.path.join(r, f'{index}.png')

        _spec = (255 * _spec).numpy().astype(np.uint8)
        _spec = cv2.resize(_spec, new_shape, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(p, _spec)
