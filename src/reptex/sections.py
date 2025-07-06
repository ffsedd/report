from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Section:
    template: str
    context: Dict[str, Any]


def build_sections(cfg: Any = None) -> List[Section]:
    """Construct the list of sections and their rendering context."""

    report_info = {
        "zprava": {
            "nazev": "Průzkum historické omítky",
            "autor1": "Ing. Jan Novak",
            "autor1_adresa": "Fakulta restaurování, Litomyšl 8",
            "autor1_ic": "IČ: 12345678",
            "autor2": "Mgr. Petra Svobodová",
            "autor2_adresa": "Fakulta restaurování, Litomyšl",
            "autor2_ic": "IČ: 87654321",
            "autor_email": "jan.novak@aukpr.cz",
            "autor_web": "www.archeo.cz",
            "cislo": "ZPR-0725",
            "datum": "5. července 2025",
        },
        "objednavka": {
            "nazev": "Kostel sv. Václava",
            "obec": "Libčice nad Vltavou",
            "cast": "centrum",
            "adresa": "Náměstí Svobody 12",
            "vlastnik": "Římskokatolická farnost Libčice",
            "invcislo": "INV-001234",
            "pamkat": "https://pamatkovykatalog.cz/",
            "cislo": "12345/7-6789",
            "material": "Opuka a omítka",
            "rozmer": "Výška fasády cca 12 m",
            "autor": "neznámý stavitel",
            "datace": "konec 17. století",
        },
        "zadavatel": {
            "jmeno": "Město Libčice nad Vltavou",
            "ulice": "Husova 5",
            "psc": "252 66",
            "mesto": "Libčice nad Vltavou",
        },
        "odber": {
            "kdo": "Jan Novák a Petra Svobodová",
            "datum": "24. června 2025",
        },
        "images": {
            "title": "../images/t.jpg",
        },
    }

    strati_context = {
        "vzorek": {
            "cislo": "001",
            "oznaceni_key": "Vzorek:",
            "oznaceni": "A1",
            "popis_key": "Popis:",
            "popis": "Vzorek barvy z trámu.",
            "lokalizace_key": "Místo:",
            "lokalizace": "strop",
        },
        "image": {
            "a": "../images/t.jpg",
            "b": "../images/t.jpg",
            "c": "../images/t.jpg",
            "d": "../images/t.jpg",
        },
        "anotation": {
            "a": "Annotation of A",
            "b": "Annotation B",
            "d": "Annotation D",
        },
        "caption": {
            "a": "Caption A",
            "b": "Caption B",
            "c": "Caption C",
            "d": "Caption D",
        },
        "table": {
            "caption": "Popis vzorku.",
            "tex": r"Place tex table here.",
        },
        "newpage": r"\newpage",
    }

    zaver_context = {
        "section": "Záver",
        "tex": r"Place tex here.",
        "newpage": r"\newpage",
    }

    zadani_context = {
        "section": "Zadání průzkumu",
        "text": "Popis odebraných vzorků a zadání průzkumu jsou uvedeny v následující tabulce.",
        "table": {
            "tex": "",
            "popis": "Popis vzorků.",
        },
        "newpage": r"\newpage",
    }

    metody_context = {"section": "Metody", "tex": r"", "newpage": r"\newpage"}

    return [
        Section(template="aaa-packages.tex", context={}),
        Section(template="aaa-begin.tex.j2", context=report_info),
        Section(template="title.tex.j2", context=report_info),
        Section(template="zadani.tex.j2", context=zadani_context),
        Section(template="metody.tex.j2", context=metody_context),
        Section(template="strati.tex.j2", context=strati_context),
        Section(template="zaver.tex.j2", context=zaver_context),
        Section(template="zzz-end.tex", context={}),
    ]
