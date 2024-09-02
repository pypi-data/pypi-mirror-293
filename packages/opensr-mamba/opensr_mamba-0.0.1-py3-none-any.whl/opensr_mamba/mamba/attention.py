import torch
from typing import Literal

class ChannelAttention(torch.nn.Module):
    """
    Channel Attention Module to enhance channel-wise feature representation.
    
    This module applies channel-wise attention to the input tensor by first squeezing
    the feature maps through adaptive pooling and two convolutional layers, followed by
    a sigmoid activation to generate attention weights.

    Args:
        num_feat (int): Number of input features (channels).
        squeeze_factor (int, optional): Factor to reduce the number of channels in the 
            intermediate layer. Default is 16.
    """
    def __init__(self, num_feat: int, squeeze_factor: int = 16) -> None:
        super(ChannelAttention, self).__init__()
        self.attention = torch.nn.Sequential(
            torch.nn.AdaptiveAvgPool2d(1),  # Global average pooling to a single pixel
            torch.nn.Conv2d(num_feat, num_feat // squeeze_factor, 1, padding=0),  # Reduction in channels
            torch.nn.ReLU(inplace=True),  # Non-linearity
            torch.nn.Conv2d(num_feat // squeeze_factor, num_feat, 1, padding=0),  # Restoration of channels
            torch.nn.Sigmoid()  # Output between 0 and 1 for attention weights
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the Channel Attention module.

        Args:
            x (torch.Tensor): Input tensor of shape (N, C, H, W), where N is batch size, C is number of channels,
                              H is height, and W is width.
        
        Returns:
            torch.Tensor: Tensor after applying channel attention.
        """
        y = self.attention(x)  # Generate attention weights
        return x * y  # Apply attention weights to the input tensor


class CAB(torch.nn.Module):
    """
    Convolutional Attention Block (CAB) with channel attention and convolutions.

    This module consists of two convolutional layers with GELU activation in between,
    followed by a Channel Attention module. It enhances the feature maps and applies
    channel-wise attention for improved representation.

    Args:
        num_feat (int): Number of input features (channels).
        is_light_sr (bool, optional): Flag to use a lighter compression ratio for 
            super-resolution tasks. Default is False.
        compress_ratio (int, optional): Ratio to reduce the number of channels in
            the convolutional layers. Default is 3.
        squeeze_factor (int, optional): Factor for channel attention module. Default
            is 30.
    """
    def __init__(self, num_feat: int, is_light_sr: bool = False, compress_ratio: int = 3, squeeze_factor: int = 30) -> None:
        super(CAB, self).__init__()
        if is_light_sr:
            compress_ratio = 6  # Use lighter compression ratio for super-resolution tasks
        
        self.cab = torch.nn.Sequential(
            torch.nn.Conv2d(num_feat, num_feat // compress_ratio, 3, 1, 1),  # Convolutional layer with padding
            torch.nn.GELU(),  # Activation function
            torch.nn.Conv2d(num_feat // compress_ratio, num_feat, 3, 1, 1),  # Convolutional layer to restore channels
            ChannelAttention(num_feat, squeeze_factor)  # Apply channel attention
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the Convolutional Attention Block (CAB).

        Args:
            x (torch.Tensor): Input tensor of shape (N, C, H, W), where N is batch size, C is number 
                of channels, H is height, and W is width.
        
        Returns:
            torch.Tensor: Output tensor after applying convolutions and channel attention.
        """
        return self.cab(x)


class ParameterFreeAttention(torch.nn.Module):
    """
    Parameter-Free Attention Module to enhance feature representation.

    This module applies attention to the input tensor using the global average pooling
    and max pooling to generate attention weights. The attention weights are applied to
    the input tensor to enhance the feature representation.

    Args:
        num_feat (int): Number of input features (channels).
    """
    def __init__(self, method: Literal["sigmoid_01", "sigmoid_02", "sigmoid_01_param", "sigmoid_02_param"] = "sigmoid_02") -> None:
        super(ParameterFreeAttention, self).__init__()
        self.attention = torch.nn.Sigmoid()
        self.a_parameter = torch.nn.Parameter(torch.randn(1))
        self.b_parameter = torch.nn.Parameter(torch.randn(1))
        self.method = method

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the Parameter-Free Attention module.

        Args:
            x (torch.Tensor): Input tensor of shape (N, C, H, W), where 
                N is batch size, C is number of channels, H is height, 
                and W is width.
        """

        # Compute the sigmoid
        if self.method == "sigmoid_01":
            attention_map = self.attention(x)
        elif self.method == "sigmoid_02":
            attention_map = self.attention(x) - 0.5
        elif self.method == "sigmoid_01_param":
            attention_map = self.attention(x * self.a_parameter) - 0.5
        elif self.method == "sigmoid_02_param":
            attention_map = self.attention(x * self.a_parameter) * self.b_parameter - 0.5
        else:
            raise ValueError("Invalid method. Choose from 'sigmoid_01', 'sigmoid_02', 'sigmoid_01_param', 'sigmoid_02_param'.")
        
        return attention_map
    

if __name__ == "__main__":

    # Example usage:

    # Define input tensor
    input_tensor = torch.randn(1, 64, 32, 32)  # Example tensor with batch size=1, 64 channels, 32x32 spatial dimensions

    # Initialize and use ChannelAttention
    ca = ChannelAttention(num_feat=64, squeeze_factor=16)
    output_ca = ca(input_tensor)
    print("Output of ChannelAttention:", output_ca.shape)

    # Initialize and use CAB
    cab = CAB(num_feat=64, is_light_sr=False, compress_ratio=3, squeeze_factor=30)
    output_cab = cab(input_tensor)
    print("Output of CAB:", output_cab.shape)

    # Initialize and use ParameterFreeAttention
    pfa = ParameterFreeAttention(method="sigmoid_02")
    output_pfa = pfa(input_tensor)
    print("Output of ParameterFreeAttention:", output_pfa.shape)
    