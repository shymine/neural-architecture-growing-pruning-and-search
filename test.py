import sys

from torch import nn

import aux_funcs as af
import network_architectures as arcs
import snip
import data
import model_funcs
import torch
import numpy as np
from snip import get_blocs


def main():
    print("test")
    device = af.get_pytorch_device()
    model, param = arcs.create_resnet_iterative(
        "networks/", "dense", "0", (True, [0.8, 0.75, 0.66, 0.6], 128), False
    )

    dataset = data.CIFAR10()
    optimizer, scheduler = af.get_full_optimizer(
        model, (param['learning_rate'], param['weight_decay'], param['momentum'], -1), ([4], [0.1])
    )
    train_params = dict(
        epochs=10,
        epoch_growth=[2, 4, 6],
        epoch_prune=[1, 3, 5, 7, 8],
        prune_batch_size=128,
        prune_type="2",
        reinit=False,
        min_ratio=[0.5, 0.4, 0.3, 0.2],
    )
    params, best_model = model_funcs.iter_training_0(
        model, dataset, train_params, optimizer, scheduler, device
    )

    af.print_sparsity(best_model)


if __name__ == "__main__":
    main()

