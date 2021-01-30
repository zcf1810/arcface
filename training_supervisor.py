"""This module provides the implementation of training supervisor."""

import os

import tensorflow as tf
from tqdm import tqdm


class TrainingSupervisor(object):
    """A training supervisor will organize and monitor the training process."""

    def __init__(self, model, optimizer, loss, metrics, training_dir) -> None:
        """Training supervisor organizes and monitors the training process.

        Args:
            model: the Keras model to be trained.
            optimizer: a Keras optimizer used for training.
            loss: a Keras loss function.
            metrics: List of metrics to be evaluated during training.
            training_dir: the directory to save the training files.
        """
        super().__init__()
        # Track the objects used for training.
        self.model = model
        self.optimizer = optimizer
        self.loss_fun = loss
        self.metrics = metrics

        # Training schedule tracks the training progress. The training
        # supervisor uses this object to make training arrangement. The schedule
        # is saved in the checkpoint and maintained by the manager.
        self.schedule = {}

        # Both the model and the training status shall be tracked. A TensorFlow
        # checkpoint is the best option to fullfill this job.
        self.checkpoint = tf.train.Checkpoint(
            model=model,
            schedule=self.schedule)

        # A model manager is responsible for saving the current training
        # schedule and the model weights.
        self.manager = tf.train.CheckpointManager(
            self.checkpoint,
            os.path.join(training_dir, 'checkpoints'),
            max_to_keep=2)

        # A model scout watches and saves the best model according to the
        # monitor value.
        self.scout = tf.train.CheckpointManager(
            self.checkpoint,
            os.path.join(training_dir, 'model_scout'),
            max_to_keep=1)

        # A clerk writes the training logs to the TensorBoard.
        self.clerk = tf.summary.create_file_writer(
            os.path.join(training_dir, 'logs'))
