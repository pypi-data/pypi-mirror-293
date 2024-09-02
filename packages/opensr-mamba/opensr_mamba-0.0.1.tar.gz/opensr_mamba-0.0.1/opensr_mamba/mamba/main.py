import torch
from opensr_mamba.mamba.patchify import PatchEmbed, PatchUnEmbed
from opensr_mamba.mamba.upsample import Upsample, UpsampleOneStep
from opensr_mamba.mamba.model import ResidualGroup
from timm.models.layers import trunc_normal_

from typing import Literal


class MambaSR(torch.nn.Module):
    def __init__(
        self,
        img_size=64,
        patch_size=1,
        in_chans=3,
        out_chans=3,
        embed_dim=96,
        depths=(6, 6, 6, 6),
        drop_rate=0.,
        d_state = 16,
        mlp_ratio=2.,
        drop_path_rate=0.1,
        norm_layer=torch.nn.LayerNorm,
        attention_type: Literal['cab', "sigmoid_01", "sigmoid_02", "sigmoid_01_param", "sigmoid_02_param"] = 'cab',
        operation_attention="sum",
        patch_norm=True,
        upscale=2,
        upsampler='',
        resi_connection='1conv'
    ):
        super(MambaSR, self).__init__()
        num_in_ch = in_chans
        num_out_ch = out_chans
        num_feat = 64
        self.upscale = upscale
        self.upsampler = upsampler
        self.mlp_ratio=mlp_ratio

        # 1. shallow feature extraction
        self.conv_first = torch.nn.Conv2d(num_in_ch, embed_dim, 3, 1, 1)

        # 2. deep feature extraction
        self.num_layers = len(depths)
        self.embed_dim = embed_dim
        self.patch_norm = patch_norm
        self.num_features = embed_dim
        self.operation_attention = operation_attention

        # 2.1. transfer 2D feature map into 1D token sequence, pay attention to whether using normalization
        self.patch_embed = PatchEmbed(
            img_size=img_size,
            patch_size=patch_size,
            in_chans=embed_dim,
            embed_dim=embed_dim,
            norm_layer=norm_layer if self.patch_norm else None
        )
        patches_resolution = self.patch_embed.patches_resolution
        self.patches_resolution = patches_resolution

        # 2.2. return 2D feature map from 1D token sequence
        self.patch_unembed = PatchUnEmbed(
            img_size=img_size,
            patch_size=patch_size,
            in_chans=embed_dim,
            embed_dim=embed_dim,
            norm_layer=norm_layer if self.patch_norm else None)
        self.pos_drop = torch.nn.Dropout(p=drop_rate)
        self.is_light_sr = True if self.upsampler=='pixelshuffledirect' else False
        
        # stochastic depth decay rule
        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, sum(depths))]
        
        # build Residual State Space Group (RSSG)
        self.layers = torch.nn.ModuleList()
        for i_layer in range(self.num_layers): # 6-layer
            layer = ResidualGroup(
                dim=embed_dim,
                input_resolution=(patches_resolution[0], patches_resolution[1]),
                depth=depths[i_layer],
                d_state = d_state,
                mlp_ratio=self.mlp_ratio,
                operation=self.operation_attention,
                drop_path=dpr[sum(depths[:i_layer]):sum(depths[:i_layer + 1])],  # no impact on SR results
                norm_layer=norm_layer,
                attention_type=attention_type,
                downsample=None,
                img_size=img_size,
                patch_size=patch_size,
                resi_connection=resi_connection,
                is_light_sr = self.is_light_sr
            )
            self.layers.append(layer)
        self.norm = norm_layer(self.num_features)

        # build the last conv layer in the end of all residual groups
        if resi_connection == '1conv':
            self.conv_after_body = torch.nn.Conv2d(embed_dim, embed_dim, 3, 1, 1)
        elif resi_connection == '3conv':
            # to save parameters and memory
            self.conv_after_body = torch.nn.Sequential(
                torch.nn.Conv2d(embed_dim, embed_dim // 4, 3, 1, 1), torch.nn.LeakyReLU(negative_slope=0.2, inplace=True),
                torch.nn.Conv2d(embed_dim // 4, embed_dim // 4, 1, 1, 0), torch.nn.LeakyReLU(negative_slope=0.2, inplace=True),
                torch.nn.Conv2d(embed_dim // 4, embed_dim, 3, 1, 1))

        # -------------------------3. high-quality image reconstruction ------------------------ #
        if self.upsampler == 'pixelshuffle':
            # for classical SR
            self.conv_before_upsample = torch.nn.Sequential(
                torch.nn.Conv2d(embed_dim, num_feat, 3, 1, 1), torch.nn.LeakyReLU(inplace=True))
            self.upsample = Upsample(upscale, num_feat)
            self.conv_last = torch.nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)
        elif self.upsampler == 'pixelshuffledirect':
            # for lightweight SR (to save parameters)
            self.upsample = UpsampleOneStep(upscale, embed_dim, num_out_ch)

        else:
            # for image denoising
            self.conv_last = torch.nn.Conv2d(embed_dim, num_out_ch, 3, 1, 1)

        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, torch.nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if isinstance(m, torch.nn.Linear) and m.bias is not None:
                torch.nn.init.constant_(m.bias, 0)
        elif isinstance(m, torch.nn.LayerNorm):
            torch.nn.init.constant_(m.bias, 0)
            torch.nn.init.constant_(m.weight, 1.0)

    @torch.jit.ignore
    def no_weight_decay(self):
        return {'absolute_pos_embed'}

    @torch.jit.ignore
    def no_weight_decay_keywords(self):
        return {'relative_position_bias_table'}

    def forward_features(self, x: torch.Tensor, save_attention_maps: bool = False):
        x_size = (x.shape[2], x.shape[3])
        x = self.patch_embed(x) # N,L,C
        x = self.pos_drop(x)
        
        attns = []
        for layer in self.layers:
            x, attn = layer(x, x_size, save_attention_maps)
            attns.append(attn)

        x = self.norm(x)  # b seq_len c
        x = self.patch_unembed(x, x_size)

        return x, attns

    def forward(self, x: torch.Tensor, save_attention_maps: bool = False):
        if self.upsampler == 'pixelshuffle':
            # for classical SR
            x = self.conv_first(x)
            res, attn = self.forward_features(x, save_attention_maps)
            x = self.conv_after_body(res) + x
            x = self.conv_before_upsample(x)
            x = self.conv_last(self.upsample(x))

        elif self.upsampler == 'pixelshuffledirect':
            # for lightweight SR
            x = self.conv_first(x)
            res, attn = self.forward_features(x, save_attention_maps)            
            x = self.conv_after_body(res) + x
            x = self.upsample(x)
        else:
            raise NotImplementedError(
                f'upsampler {self.upsampler} is not implemented'
            )

        if save_attention_maps:
            return x, attn
        else:
            return x

    def flops(self):
        flops = 0
        h, w = self.patches_resolution
        flops += h * w * 3 * self.embed_dim * 9
        flops += self.patch_embed.flops()
        for layer in self.layers:
            flops += layer.flops()
        flops += h * w * 3 * self.embed_dim * self.embed_dim
        flops += self.upsample.flops()
        return flops