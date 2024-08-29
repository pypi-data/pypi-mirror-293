import argparse


def parse_args():
    """
    Parses command line arguments
    :return: Namespace object with arguments as fields
    """
    parser = argparse.ArgumentParser(
        description="Belief-PPG: Belief Propagation framework for uncertainty-aware PPG-based Heart Rate estimation."
    )
    # SETUP
    parser.add_argument(
        "--data_dir",
        type=str,
        default="Data",
        help="Path to data directory",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="dalia",
        choices=["dalia", "wesad", "bami", "bami-1", "bami-2", "ieee", "all"],
        help="Dataset to train/evaluate on",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default="Output",
        help="Where to save predictions",
    )
    parser.add_argument(
        "--n_frames",
        type=int,
        default=7,
        help="Number of consecutive frames to feed models. (Time-domain is concatenated without overlap)",
    )
    parser.add_argument(
        "--freq",
        type=int,
        default=64,
        help="Frequency to resample time-domain signal to in Hz",
    )
    parser.add_argument(
        "--filter_highcut",
        type=float,
        default=18,
        help="Upper cutoff frequency for Butterworth bandpass filtering of time-domain features.",
    )
    parser.add_argument(
        "--filter_lowcut",
        type=float,
        default=0.1,
        help="Lower cutoff frequency for Butterworth bandpass filtering of time-domain features.",
    )

    parser.add_argument(
        "--min_hz",
        type=float,
        default=0.5,
        help="Minimal predictable frequency in Hz",
    )
    parser.add_argument(
        "--max_hz",
        type=float,
        default=3.5,
        help="Maximal predictable frequency in Hz",
    )
    parser.add_argument(
        "--n_bins",
        type=int,
        default=64,
        choices=[64, 256],
        help="Number of bins to subdivide HR space into",
    )
    parser.add_argument(
        "--sigma_y",
        type=float,
        default=1.5,
        help="Standard deviation for label smoothing.",
    )
    parser.add_argument(
        "--no_time_backbone",
        action="store_false",
        dest="use_time_backbone",
        help="Deactivate time-domain backbone",
    )
    parser.add_argument(
        "--init_lr",
        type=float,
        default=0.00025,
        help="Initial learning rate",
    )
    parser.add_argument(
        "--augmentations",
        type=bool,
        default=True,
        help="Whether to use train-time augmentations",
    )
    parser.add_argument(
        "--prior",
        type=str,
        default="gauss",
        choices=[
            "gauss",
            "laplace",
        ],
        help="Prior for belief propagation",
    )
    parser.add_argument(
        "--uncertainty",
        type=str,
        default="entropy",
        choices=["entropy", "std"],
        help="Metric for predictive uncertainty",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=128,
        help="Batch size for training & inference",
    )
    parser.add_argument(
        "--cache_pipeline",
        type=bool,
        default=True,
        help="Whether to cache the windowed tf.data pipeline in memory. Speeds up training greatly but crashes if not enough memory available.",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=50,
        help="Patience for early stopping",
    )
    parser.add_argument(
        "--use_wandb",
        action="store_true",
        help="Whether to use Weights & Biases. Make sure to login before usage",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=12,
        help="Seed for full determinism.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="loso",
        choices=["loso", "train"],
        help="Specifies the validation scheme. 'loso' performs a leave-one-subject-out validation, while 'train' uses a single training fold where one session from each dataset is reserved for validation and testing."
    )

    return parser.parse_args()
