# Author: Lihao Wang

def dlph(v, k="root", indent=0, is_DC=False):   # v: value, k: key
    if isinstance(v, dict):
        if is_DC:
            print(" " * indent + f"|-- {k} (DC)")
        else:
            print(" " * indent + f"|-- {k}")
        sub_indent = indent + 4
        for sub_k, sub_v in v.items():
            dlph(sub_v, sub_k, sub_indent)
    elif type(v).__name__ == "DataContainer":    # mmcv DataContainer
        dlph(v.data, k, indent, is_DC=True)
    elif isinstance(v, list) or isinstance(v, tuple):
        if is_DC:
            print(" " * indent + f"|-- {k} (DC): {type(v).__name__} of len {len(v)}")
        else:
            print(" " * indent + f"|-- {k}: {type(v).__name__} of len {len(v)}")
        sub_indent = indent + 4
        for i, ele in enumerate(v):
            dlph(ele, str(i), sub_indent)
    elif type(v).__name__ == "ndarray" or type(v).__name__ == "Tensor":  # numpy.ndarray & torch.Tensor
        if is_DC:
            print(" " * indent + f"|-- {k} (DC): {type(v).__name__} of shape {list(v.shape)}, "
                                 f"dtype {v.dtype}, min {v.min():.2f}, max {v.max():.2f}")
        else:
            print(" " * indent + f"|-- {k}: {type(v).__name__} of shape {list(v.shape)}, "
                                 f"dtype {v.dtype}, min {v.min():.2f}, max {v.max():.2f}")
    else:
        if is_DC:
            print(" " * indent + f"|-- {k} (DC): {v}")
        else:
            print(" " * indent + f"|-- {k}: {v}")

