
import torch
import torch.nn as nn
import torch.nn.functional as F

class PartialConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, bn=True, bias=False, sample="none-3", activation="relu"):
        super().__init__()
        self.bn = bn
        self.activation_type = activation

        if sample == "down-7":
            self.input_conv = nn.Conv2d(in_channels, out_channels, 7, 2, 3, bias=bias)
            self.mask_conv = nn.Conv2d(in_channels, out_channels, 7, 2, 3, bias=False)
        elif sample == "down-5":
            self.input_conv = nn.Conv2d(in_channels, out_channels, 5, 2, 2, bias=bias)
            self.mask_conv = nn.Conv2d(in_channels, out_channels, 5, 2, 2, bias=False)
        elif sample == "down-3":
            self.input_conv = nn.Conv2d(in_channels, out_channels, 3, 2, 1, bias=bias)
            self.mask_conv = nn.Conv2d(in_channels, out_channels, 3, 2, 1, bias=False)
        else:
            self.input_conv = nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=bias)
            self.mask_conv = nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False)

        nn.init.constant_(self.mask_conv.weight, 1.0)
        nn.init.kaiming_normal_(self.input_conv.weight, a=0, mode="fan_in")

        for param in self.mask_conv.parameters():
            param.requires_grad = False

        if bn:
            self.batch_normalization = nn.BatchNorm2d(out_channels)

        if activation == "relu":
            self.activation = nn.ReLU()
        elif activation == "leaky_relu":
            self.activation = nn.LeakyReLU(negative_slope=0.2)
        else:
            self.activation = None

    def forward(self, input_x, mask):
        output = self.input_conv(input_x * mask)
        with torch.no_grad():
            output_mask = self.mask_conv(mask)

        if self.input_conv.bias is not None:
            output_bias = self.input_conv.bias.view(1, -1, 1, 1).expand_as(output)
        else:
            output_bias = torch.zeros_like(output)

        mask_is_zero = (output_mask == 0)
        mask_sum = output_mask.masked_fill(mask_is_zero, 1.0)

        output = (output - output_bias) / mask_sum + output_bias
        output = output.masked_fill(mask_is_zero, 0.0)

        new_mask = torch.ones_like(output).masked_fill(mask_is_zero, 0.0)

        if self.bn:
            output = self.batch_normalization(output)
        if self.activation:
            output = self.activation(output)

        return output, new_mask


class PartialConvUNet(nn.Module):
    def __init__(self, input_size=256, layers=7):
        super().__init__()
        assert 2**(layers + 1) == input_size, "Input size must be 2^(layers + 1)"
        self.freeze_enc_bn = False
        self.layers = layers

        self.encoder_1 = PartialConvLayer(3, 64, bn=False, sample="down-7")
        self.encoder_2 = PartialConvLayer(64, 128, sample="down-5")
        self.encoder_3 = PartialConvLayer(128, 256, sample="down-3")
        self.encoder_4 = PartialConvLayer(256, 512, sample="down-3")

        for i in range(5, layers + 1):
            setattr(self, f"encoder_{i}", PartialConvLayer(512, 512, sample="down-3"))

        for i in range(5, layers + 1):
            setattr(self, f"decoder_{i}", PartialConvLayer(512 + 512, 512, activation="leaky_relu"))

        self.decoder_4 = PartialConvLayer(512 + 256, 256, activation="leaky_relu")
        self.decoder_3 = PartialConvLayer(256 + 128, 128, activation="leaky_relu")
        self.decoder_2 = PartialConvLayer(128 + 64, 64, activation="leaky_relu")
        self.decoder_1 = PartialConvLayer(64 + 3, 3, bn=False, activation="", bias=True)

    def forward(self, input_x, mask):
        encoder_dict = {"h_0": input_x}
        mask_dict = {"h_0": mask}
        key_prev = "h_0"

        for i in range(1, self.layers + 1):
            layer = getattr(self, f"encoder_{i}")
            key = f"h_{i}"
            encoder_dict[key], mask_dict[key] = layer(encoder_dict[key_prev], mask_dict[key_prev])
            key_prev = key

        out_data, out_mask = encoder_dict[f"h_{self.layers}"], mask_dict[f"h_{self.layers}"]

        for i in range(self.layers, 0, -1):
            enc_key = f"h_{i - 1}"
            dec_layer = getattr(self, f"decoder_{i}")
            out_data = F.interpolate(out_data, scale_factor=2)
            out_mask = F.interpolate(out_mask, scale_factor=2)
            out_data = torch.cat([out_data, encoder_dict[enc_key]], dim=1)
            out_mask = torch.cat([out_mask, mask_dict[enc_key]], dim=1)
            out_data, out_mask = dec_layer(out_data, out_mask)

        return out_data

    def train(self, mode=True):
        super().train(mode)
        if self.freeze_enc_bn:
            for name, module in self.named_modules():
                if isinstance(module, nn.BatchNorm2d) and "enc" in name:
                    module.eval()
