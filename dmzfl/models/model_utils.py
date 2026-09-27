def build_model(name, input_dim=None, num_classes=10):
    if name == 'CNN2':
        from .cnn2 import CNN2; return CNN2(num_classes)
    if name == 'MLP3':
        from .mlp3 import MLP3; return MLP3(input_dim, num_classes)
    raise ValueError(name)