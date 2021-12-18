# Ubuntu utilities and wrappers.
try:
    import FigUI.api.Ubuntu.App
    import FigUI.api.Ubuntu.Thumbnailer
except ImportError: 
    import App
    import Thumbnailer