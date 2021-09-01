# class for setting an managing themes.
class FigBackground:
    def __init__(self, **attrs):
        self.attrs = attrs
        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __str__(self):
        return ";".join([f"{attr.replace('_','-')}:{value}" for attr, value in self.attrs.items()])

    def __repr__(self):
        return "FigUI.widgets.Theme.FigBackground"


class FigTheme:
    def __init__(self, **attrs):
        self.background = FigBackground(**attrs)

    def __str__(self):
        pass

    def __repr__(self):
        return "FigUI.widgets.Theme.FigTheme"

    @classmethod
    def fromFile(cls, filename):
        import json
        json.load(open(filename))
        self = FigTheme()
        
        return self