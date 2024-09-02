import torch
import importlib.resources
from opensr_mamba.mamba.main import MambaSR
from typing import Tuple

def load_models(img_size: int = 128) -> Tuple[MambaSR, MambaSR, MambaSR]:

    # Load the weights
    internal_path = importlib.resources.files("opensr_mamba.mamba.weights")
    
    # SR model from 10m to 2.5m
    sr_model_path = internal_path / "srmodel.pth"
    sr_model_params = {
            "img_size": img_size, "in_chans": 3, "embed_dim": 60,
            "depths": [2, 2, 2, 2], "d_state": 16, "mlp_ratio": 1.5,
            "upscale": 4, "attention_type": "sigmoid_02",
            "upsampler": "pixelshuffledirect",
            "resi_connection": "1conv", "operation_attention": "sum"
    }

    # Fusion model from 20m to 10m
    fusion_model01_path = internal_path / "fusionmodel01.pth"
    fusion_model01_params = {
        "img_size": img_size, "in_chans": 10, "out_chans": 6,
        "embed_dim": 60, "depths": [2, 2, 2, 2], "d_state": 16, "mlp_ratio": 1.5,
        "upscale": 1, "attention_type": "sigmoid_02",
        "upsampler": "pixelshuffledirect",
        "resi_connection": "1conv", "operation_attention": "prod"
    }

    # Fusion model from 10m to 2.5m
    fusion_model02_path = internal_path / "fusionmodel02.pth"
    fusion_model02_params = {
        "img_size": img_size, "in_chans": 10, "out_chans": 7,
        "embed_dim": 60, "depths": [2, 2, 2, 2], "d_state": 16, "mlp_ratio": 1.5,
        "upscale": 1, "attention_type": "sigmoid_02",
        "upsampler": "pixelshuffledirect",
        "resi_connection": "1conv", "operation_attention": "sum"
    }

    # Create the models
    sr_model, fusion_model01, fusion_model02 =(
        MambaSR(**sr_model_params),
        MambaSR(**fusion_model01_params),
        MambaSR(**fusion_model02_params)
    )

    # Copy the weights
    sr_model.load_state_dict(torch.load(sr_model_path, map_location="cpu", weights_only=True))
    fusion_model01.load_state_dict(torch.load(fusion_model01_path, map_location="cpu", weights_only=True))
    fusion_model02.load_state_dict(torch.load(fusion_model02_path, map_location="cpu", weights_only=True))

    # Set the models to evaluation mode
    sr_model.eval().cuda()
    fusion_model01.eval().cuda()
    fusion_model02.eval().cuda()

    # Remove the gradients
    for model in [sr_model, fusion_model01, fusion_model02]:
        for param in model.parameters():
            param.requires_grad = False 

    return sr_model, fusion_model01, fusion_model02


def predict(tensor: torch.Tensor, models = None) -> torch.Tensor:
    
    # Load model if not provided
    if models is None:
        sr_model, fusion_model01, fusion_model02 = load_models()

    # if tensor is no in cuda, move it
    if not tensor.is_cuda:
        tensor = tensor.cuda()

    # Select bands
    rgb_bands = tensor[[2, 1, 0]][None]
    bands_10m = tensor[[0, 1, 2, 6]][None]
    bands_20m = tensor[[3, 4, 5, 7, 8, 9]][None]

    # From 10m to 20m and then to 10m again
    bands_20m_ready = torch.nn.functional.interpolate(bands_20m, scale_factor=1/2, mode="nearest")
    bands_20m_ready = torch.nn.functional.interpolate(bands_20m_ready, scale_factor=2, mode="bilinear", antialias=True)
    
    # Perform SR from 10m to 2.5m - RETURN B2-B3-B4
    sr_tensor = sr_model(rgb_bands, save_attention_maps=True)[0]

    # Perform fusion (20m to 10m) - RETURN B5-B6-B7-B8A-B11-B12
    fs_tensor01 = fusion_model01(torch.cat((bands_20m_ready, bands_10m), 1), save_attention_maps=True)[0]
    
    # Concatenate the 10 meters bands - RETURN B2-B3-B4-B8 - B5-B6-B7-B8A-B11-B12
    all_bands_10m = torch.cat([bands_10m, fs_tensor01], dim=1)
    all_bands_10m_512 = torch.nn.functional.interpolate(all_bands_10m, scale_factor=4, mode="bilinear", antialias=True)
    all_bands_10m_512[:, [2, 1, 0]] = sr_tensor
    
    # Perform fusion (10m to 2.5m) - RETURN B2-B3-B4-B8 - B5-B6-B7-B8A-B11-B12
    fs_tensor02 = fusion_model02(all_bands_10m_512, save_attention_maps=True)[0].cpu().squeeze()
    all_bands_10m_512[:, 3:10] = fs_tensor02

    # Concatenate all bands in the original order
    final_tensor = torch.concatenate([
        all_bands_10m_512[0, 0][None],
        all_bands_10m_512[0, 1][None],
        all_bands_10m_512[0, 2][None],
        all_bands_10m_512[0, 4][None],
        all_bands_10m_512[0, 5][None],
        all_bands_10m_512[0, 6][None],
        all_bands_10m_512[0, 3][None],
        all_bands_10m_512[0, 7][None],
        all_bands_10m_512[0, 8][None],
        all_bands_10m_512[0, 9][None]
    ], dim=0)
    return final_tensor.cpu().numpy()