import os
from base.base_trainer import BaseTrain
from keras.callbacks import ModelCheckpoint, TensorBoard

class LSTMChemTrainer(BaseTrain):
    def __init__(self, model, data, config):
        super(LSTMChemTrainer, self).__init__(model, data, config)
        self.callbacks = []
        self.loss = []
        self.val_loss = []
        self.init_callbacks()

    def init_callbacks(self):
        self.callbacks.append(
                ModelCheckpoint(
                    filepath=os.path.join(self.config.checkpoint_dir, '%s-{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp_name),
                    monitor=self.config.checkpoint_monitor,
                    mode=self.config.checkpoint_mode,
                    save_best_only=self.config.checkpoint_save_best_only,
                    save_weights_only=self.config.checkpoint_save_weights_only,
                    verbose=self.config.checkpoint_verbose,
                    )
                )
        self.callbacks.append(
                TensorBoard(
                    log_dir=self.config.tensorboard_log_dir,
                    write_graph=self.config.tensorboard_write_graph,
                    )
                )

    def train(self, in_batch = False):
        if not in_batch:
            self.data = self.data.get_train_data()
            history = self.model.fit(
                self.data[0], self.data[1],
                epochs=self.config.num_epochs,
                verbose=self.config.verbose_training,
                batch_size=self.config.batch_size,
                validation_split=self.config.validation_split,
                callbacks=self.callbacks,
                )
        else:
            history = self.model.fit_generator(
                self.data.get_batch_train_data(batch_size = self.config.data_length),
                epochs=self.config.num_epochs,
                verbose=self.config.verbose_training,
                batch_size=self.config.batch_size,
                validation_split=self.config.validation_split,
                callbacks=self.callbacks,
                )
        self.loss.extend(history.history['loss'])
        self.val_loss.extend(history.history['val_loss'])

