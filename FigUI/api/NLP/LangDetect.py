import enum
import json

class FigLang(enum.Enum):
    ISO = 1
    TUP = 2
    JSON = 3
    NATIVE = 4


class FigLangDetectEngine(enum.Enum):
    CLD3 = 1
    LANGID = 2
    LINGUA = 3
    FASTEXT = 4


class CLD3tect():
    def __init__(self):
        import cld3
        self._backend = cld3

    def __call__(self, text: str, dtype=FigLang.JSON):
        pred = self._backend.get_language(text)
        if dtype == FigLang.JSON:
            return {
                "lang": pred.language,
                "prob": pred.probability,
                "is_reliable": pred.is_reliable,
                "proportion": pred.proportion,
            }
        elif dtype == FigLang.TUP:
            return (
                pred.language,
                pred.probability,
                pred.is_reliable,
                pred.proportion,
            )
        elif dtype == FigLang.NATIVE:
            return pred 
        elif dtype == FigLang.ISO:
            return pred.language


class LangIDetect:
    def __init__(self):
        from langid.langid import model, LanguageIdentifier
        self._backend = LanguageIdentifier.from_modelstring(
            model, norm_probs=True
        )

    def __call__(self, text: str, dtype=FigLang.JSON):
        pred = self._backend.classify(text)
        if dtype == FigLang.JSON:
            return {
                "lang": pred[0],
                "prob": pred[1],
            }
        elif dtype == FigLang.TUP:
            return pred
        elif dtype == FigLang.NATIVE:
            return pred
        elif dtype == FigLang.ISO:
            return pred[0]


class FigLangDetector:
    def __init__(self, backend=FigLangDetectEngine.LANGID):
        if backend == FigLangDetectEngine.LANGID or backend == "langid":
            self._backend = LangIDetect()
        elif backend == FigLangDetectEngine.CLD3 or backend == "cld3":
            self._backend = CLD3tect()
        else:
            raise TypeError(f"No backend found for {backend}")

    def __call__(self, text: str, dtype=FigLang.JSON):
        return self._backend(text, dtype=dtype)