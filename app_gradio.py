from pathlib import Path
config_path = Path('/content/ljspeech_melgan_forward_transformer/melgan/')
import numpy as np
# import sys

# Load pretrained models
from utils.config_manager import ConfigManager
from utils.audio import Audio

import IPython.display as ipd
import torch
from scipy.io.wavfile import write
sys.path.append('/content/')
from melgan.model.generator import Generator
from melgan.utils.hparams import HParam

config_loader = ConfigManager(str(config_path), model_kind='forward')
audio = Audio(config_loader.config)
model = config_loader.load_model(str(config_path / 'forward_weights/ckpt-179'))

# Synthesize text
sentence = 'Many animals of even complex structure which live parasitically within others are wholly devoid of an alimentary cavity.'
out_normal = model.predict(sentence, speed_regulator=1)

print('FastSpeech: done')


vocoder = torch.load("/content/TransformerTTS/nvidia_tacotron2_LJ11_epoch6400.pt") 
hp = HParam("/content/melgan/config/default.yaml")

vocoder = Generator(hp.audio.n_mel_channels).cuda()
vocoder.load_state_dict(checkpoint["model_g"])
vocoder.eval()

mel = torch.tensor(out_normal['mel'].numpy().T[np.newaxis,:,:])

if torch.cuda.is_available():
    vocoder = vocoder.cuda()
    mel = mel.cuda()

with torch.no_grad():
    audio = vocoder.inference(mel)

print('melgan: done')
output='/content/TransformerTTS/test.wav'
write(, 22050, audio.cpu().numpy())
print('saved audio:', output)
# Display audio
ipd.display(ipd.Audio(audio.cpu().numpy(), rate=22050))