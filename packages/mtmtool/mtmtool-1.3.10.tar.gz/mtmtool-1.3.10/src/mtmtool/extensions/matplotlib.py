from cycler import cycler

from matplotlib.figure import Figure
from matplotlib.layout_engine import ConstrainedLayoutEngine


def get_scientific_style_context(
    fontname: str = "Arial",
    fontsize_large: float = 10.5,
    fontsize_medium: float = 9,
    setxytick: bool = True,
    setcolorcycle: bool = True,
) -> dict:
    """
    获取科学绘图风格的一般参数设置，包括字体、字号、布局等。
        :param fontname: str, 字体名称，默认None，使用Arial
        :param fontsize_large: float, 大字体大小，默认10.5
        :param fontsize_medium: float, 中字体大小，默认9
        :param setxytick: bool, 是否修改xy刻度，默认True
        :param setcolorcycle: bool, 是否修改颜色循环，默认True
        :return: dict, 参数设置
    """
    # 通用设置，包括字体、字号、布局等
    common_params = {
        # 字体设置，期刊大多要求Arial字体
        "font.family": "sans-serif",
        "font.sans-serif": fontname,
        "font.weight": "normal",
        "mathtext.fontset": "stix",
        # 字体大小设置，小四号字体为12pt, 五号字体为10.5pt, 小五号字体为9pt
        "font.size": fontsize_medium,
        "axes.labelsize": fontsize_large,
        "axes.titlesize": fontsize_large,
        "figure.titlesize": fontsize_large,
        "figure.labelsize": fontsize_large,
        "legend.fontsize": fontsize_medium,
        "legend.title_fontsize": fontsize_large,
        "xtick.labelsize": fontsize_medium,
        "ytick.labelsize": fontsize_medium,
        # 布局设置
        "figure.constrained_layout.use": True,
        "figure.dpi": 500,
    }
    # x和y刻度设置
    xy_tick_params = {
        "xtick.direction": "in",
        "xtick.major.size": 3,
        "xtick.major.width": 0.5,
        "xtick.minor.size": 1.5,
        "xtick.minor.width": 0.5,
        "xtick.minor.visible": True,
        "xtick.top": True,
        "ytick.direction": "in",
        "ytick.major.size": 3,
        "ytick.major.width": 0.5,
        "ytick.minor.size": 1.5,
        "ytick.minor.width": 0.5,
        "ytick.minor.visible": True,
        "ytick.right": True,
    }
    # 颜色循环设置
    # 方案来源 [论文配色：跟着顶刊学配色（Nature篇）](https://blog.csdn.net/2301_77413856/article/details/140200971)
    color_cycle_params = {
        "axes.prop_cycle": cycler(
            "color",
            [
                "#227980",
                "#68BF69",
                "#D2DC38",
                "#F5B16E",
                "#F38F3C",
                "#CE9FCA",
                "#707070",
                "#A9CCDE",
                "#734E9C",
                "#F7D1E3",
                "#415C42",
                "#FAE93B",
            ],
        ),
    }
    # 返回设置
    return_params = common_params.copy()
    if setxytick:
        return_params.update(xy_tick_params)
    if setcolorcycle:
        return_params.update(color_cycle_params)
    return return_params


def savefig_with_fixed_edgesize(
    fig: Figure, path: str, fixed: str = "width", threshold: float = 2 / 72, renderer=None, **kwargs
) -> None:
    """
    bbox_inches参数固定为tight。在保存图片时自动调整fig大小, 确保图片具有指定宽度或高度。
        :param fig: Figure
        :param path: str, 保存路径
        :param fixed: str, 保持的边，可选"width"或"height"
        :param threshold: float, 保持的阈值范围
        :param renderer: Renderer, 渲染器
        :param kwargs: dict, 其它保存参数, 请查阅 matplotlib.pyplot.savefig
        :return: None
    """
    # 检查参数
    if fixed not in ["width", "height"]:
        raise ValueError("fixed param must be 'width' or 'height'")
    # 设置默认参数
    kwargs["bbox_inches"] = "tight"  # 保存时自动裁剪白边
    if kwargs.get("pad_inches") is None:  # 保存时白边大小
        kwargs["pad_inches"] = 1 / 72
    pad_inches = kwargs["pad_inches"]  # 白边大小
    # 获取原始fig大小
    orig_width, orig_height = fig.get_size_inches()

    # 设置figure边距参数
    layout_engine = fig.get_layout_engine()
    if layout_engine is None:
        fig.subplots_adjust(left=pad_inches, bottom=pad_inches, right=1 - pad_inches, top=1 - pad_inches)
        layout_pad_h, layout_pad_w = pad_inches, pad_inches
    if isinstance(layout_engine, ConstrainedLayoutEngine):
        layout_params = layout_engine.get()
        layout_pad_h, layout_pad_w = layout_params["h_pad"], layout_params["w_pad"]

    # 计算当前边距
    diff_pad_w = 0 if pad_inches >= layout_pad_w else layout_pad_w - pad_inches  # 缺少的宽度
    diff_pad_h = 0 if pad_inches >= layout_pad_h else layout_pad_h - pad_inches  # 缺少的高度
    obj_save_width = orig_width + 2 * diff_pad_w  # 实际保存时应设置的宽度
    obj_save_height = orig_height + 2 * diff_pad_h  # 实际保存时应设置的高度
    obj_ttbox_width = orig_width - 2 * pad_inches  # 实际保存时tightbbox的宽度
    obj_ttbox_height = orig_height - 2 * pad_inches  # 实际保存时tightbbox的高度
    fig.set_size_inches(obj_save_width, obj_save_height)  # 重新设置fig大小

    # 计算缩放比例
    for _ in range(5):
        # 计算当前宽度和高度
        if renderer is not None:
            fig.draw(renderer)
            now_ttbox_width, now_ttbox_height = fig.get_tightbbox(renderer).size
        else:
            fig.draw_without_rendering()
            now_ttbox_width, now_ttbox_height = fig.get_tightbbox().size
        step_scale_ratio = 1.5  # 步长增加的比例
        if fixed == "width":
            now_save_width = now_ttbox_width + 2 * (pad_inches)  # 当前实际保存时的宽度
            # 计算tightbbox的高度差值
            diff_ttbox_height = now_ttbox_height / now_ttbox_width * (obj_ttbox_width - now_ttbox_width)
            # 如果当前宽度高于给定阈值范围，退出循环
            if now_save_width >= orig_width - threshold:
                break
            # 增加高度，并根据layout的pad参数调整宽度
            fig.set_size_inches(obj_save_width, now_ttbox_height + diff_ttbox_height * step_scale_ratio)
        if fixed == "height":
            now_save_height = now_ttbox_height + 2 * (pad_inches)
            # 计算tightbbox的宽度差值
            diff_ttbox_width = now_ttbox_width / now_ttbox_height * (obj_ttbox_height - now_ttbox_height)
            # 如果当前高度高于给定阈值范围，退出循环
            if now_save_height >= orig_height - threshold:
                break
            # 增加宽度，并根据layout的pad参数调整高度
            fig.set_size_inches(now_ttbox_width + diff_ttbox_width * step_scale_ratio, obj_save_height)
    # 保存图片
    fig.savefig(path, **kwargs)
