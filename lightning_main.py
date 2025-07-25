import torch
import lightning as L
import config as cf
import os

from model import ChessCNN, ChessDualDatasetNew
from torch.utils.data import DataLoader
from lightning_model import LitCNN, ChessDM
from preprocess import get_dataloader



# train_loader, test_loader = get_dataloader(K=1)

# train_ds = ChessDualDatasetNew(train=True, K=0)
# test_ds = ChessDualDatasetNew(train=False, K=0)

# train_loader = DataLoader(dataset=train_ds, batch_size=cf.BATCH_SIZE, shuffle=True)
# test_loader = DataLoader(dataset=test_ds, batch_size=cf.BATCH_SIZE, shuffle=False)

input_size = 28*28
hidden_size = 100
num_classes = 10
num_epochs = cf.NUM_EPOCHS
batch_size = cf.BATCH_SIZE
learning_rate = cf.LEARNING_RATE

torch.manual_seed(cf.SEED)
torch.set_float32_matmul_precision('medium')

if __name__ == "__main__":
    
    dm = ChessDM(batch_size=cf.BATCH_SIZE)
    pytorchModel = ChessCNN()
    model = LitCNN(model=pytorchModel, lr=learning_rate)
    
    for iterations in range(1):
        print(f"\n---- ITERATION: {iterations} ----")
        trainer = L.Trainer(
            max_epochs=num_epochs,
            accelerator="auto",
            devices="auto",
            reload_dataloaders_every_n_epochs=1
        )
        
        # trainer.fit(
        #     model=model,
        #     train_dataloaders=train_loader,  
        # )
        trainer.fit(
            model=model,
            datamodule=dm
        )

        test_acc = trainer.test(model=model, dataloaders=dm.train_dataloader())[0]['accuracy']
        train_acc = trainer.test(model=model, dataloaders=dm.test_dataloader())[0]['accuracy']
        print(f"Test accuracy: {test_acc} | Train accuracy: {train_acc}")
        
        FILE_NAME = os.path.join("lightning_check",f"train2_it_{iterations}_epoch_{cf.NUM_EPOCHS}_lr_{cf.LEARNING_RATE}.ckpt")
        trainer.save_checkpoint(FILE_NAME)
        