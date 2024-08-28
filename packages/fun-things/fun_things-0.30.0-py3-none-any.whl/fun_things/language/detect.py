import unicodedata
import pycld2
import langdetect
import regex

from .payload import Payload
import pycountry

RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")


def _remove_bad_chars(text):
    text = "".join(
        [
            l
            for l in text
            if unicodedata.category(str(l))[0]
            not in (
                "S",
                "M",
                "C",
            )
        ]
    )
    return RE_BAD_CHARS.sub("", text)


def _parse_pycld2(text: str):
    try:
        isReliable, textBytesFound, details, vectors = pycld2.detect(
            text, returnVectors=True
        )

        for info in details:
            name, code, percent, score = info

            if name != "Unknown" and percent > 0:
                yield Payload(
                    name=name,
                    code=code,
                    percent=percent / 100,
                    source="pycld2",
                )

    except:
        pass


def _parse_langdetect(text: str):
    langs = langdetect.detect_langs(text)

    for lang in langs:
        pycountry_lang = pycountry.languages.get(
            alpha_2=lang.lang,
        )

        if pycountry_lang == None:
            continue

        yield Payload(
            name=pycountry_lang.name.upper(),
            code=lang.lang,
            percent=lang.prob,
            source="langdetect",
        )


def detect(text: str):
    if text == None:
        return []

    text = _remove_bad_chars(text)

    from_pycld2 = list(_parse_pycld2(text))

    if any(from_pycld2):
        return from_pycld2

    return list(_parse_langdetect(text))
