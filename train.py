# Copyright 2020 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import argparse
import logging

import gan_pytorch.models as models
from gan_pytorch.utils import create_folder
from trainer import Trainer

model_names = sorted(name for name in models.__dict__
                     if name.islower() and not name.startswith("__")
                     and callable(models.__dict__[name]))

logger = logging.getLogger(__name__)
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research and application of GAN based super resolution "
                                                 "technology for pathological microscopic images.")
    # basic parameters
    parser.add_argument("--dataset", type=str, required=True,
                        help="mnist | fashion-mnist | cifar10 |.")
    parser.add_argument("--dataroot", type=str, default="data",
                        help="Path to dataset. (default: ``data``).")
    parser.add_argument("-j", "--workers", default=4, type=int, metavar="N",
                        help="Number of data loading workers. (default:4)")
    parser.add_argument("--manualSeed", type=int, default=1111,
                        help="Seed for initializing training. (default:1111)")
    parser.add_argument("--device", default="",
                        help="device id i.e. `0` or `0,1` or `cpu`. (default: ````).")

    # log parameters
    parser.add_argument("-p", "--save-freq", default=50, type=int,
                        metavar="N", help="Save frequency. (default: 50).")

    # model parameters
    parser.add_argument("-a", "--arch", metavar="ARCH", default="mnist",
                        choices=model_names,
                        help="model architecture: " +
                             " | ".join(model_names) +
                             " (default: mnist)")
    parser.add_argument("--model-path", default="", type=str, metavar="PATH",
                        help="Path to latest checkpoint for model. (default: ````).")
    parser.add_argument("--pretrained", dest="pretrained", action="store_true",
                        help="Use pre-trained model.")
    parser.add_argument("--netD", default="", type=str, metavar="PATH",
                        help="Path to latest discriminator checkpoint. (default: ````).")
    parser.add_argument("--netG", default="", type=str, metavar="PATH",
                        help="Path to latest generator checkpoint. (default: ````).")

    # training parameters
    parser.add_argument("--start-epoch", default=0, type=int, metavar="N",
                        help="manual epoch number (useful on restarts)")
    parser.add_argument("--iters", default=1e5, type=int, metavar="N",
                        help="The number of iterations is needed in the training of PSNR model. (default: 1e5)")
    parser.add_argument("-b", "--batch-size", default=64, type=int, metavar="N",
                        help="mini-batch size (default: 64), this is the total "
                             "batch size of all GPUs on the current node when "
                             "using Data Parallel or Distributed Data Parallel.")
    parser.add_argument("--image-size", type=int, default=28,
                        help="The height / width of the input image to network. (default: 28).")
    parser.add_argument("--channels", type=int, default=1,
                        help="The number of channels of the image. (default: 1).")
    parser.add_argument("--lr", type=float, default=3e-4,
                        help="Learning rate. (default:3e-4)")
    args = parser.parse_args()

    print("##################################################\n")
    print("Run Training Engine.\n")
    print(args)

    create_folder("output")
    create_folder("weights")

    logger.info("TrainingEngine:")
    print("\tAPI version .......... 0.1.0")
    print("\tBuild ................ 2020.11.30-1116-0c5adc7e")

    logger.info("Creating Training Engine")
    trainer = Trainer(args)

    logger.info("Staring training model")
    trainer.run()
    print("##################################################\n")

    logger.info("All training has been completed successfully.\n")
