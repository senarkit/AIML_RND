import torch
from safetensors.torch import save_file, load_file

def convert_bin_to_safetensors(bin_path: str, safetensors_path: str):
    print(f"Converting {bin_path} → {safetensors_path}")

    # Load PyTorch bin (allow objects, safe if from Hugging Face)
    state_dict = torch.load(bin_path, map_location="cpu", weights_only=False)

    # If checkpoint has a 'state_dict' wrapper, unwrap it
    if isinstance(state_dict, dict) and "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]

    # Save only tensors
    save_file(state_dict, safetensors_path)
    print(f"Saved: {safetensors_path}")


# Convert to Safetensor - Paths
convert_bin_to_safetensors("./embedding/pytorch_model.bin", "./embedding/model.safetensors")
convert_bin_to_safetensors("./segmentation/pytorch_model.bin", "./segmentation/model.safetensors")