import matplotlib.pyplot as plt


__all__ = [
    'make_pretty',
]
    

def make_pretty(styler):
    # styler.hide()
    styler.background_gradient(cmap=plt.cm.PiYG, vmin=-2, vmax=3, axis=None)
    styler.format(precision=0)
    return styler
