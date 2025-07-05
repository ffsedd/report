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
            "Nazev": "Kostel sv. Václava",
            "Obec": "Libčice nad Vltavou",
            "Cast": "centrum",
            "Adresa": "Náměstí Svobody 12",
            "Vlastnik": "Římskokatolická farnost Libčice",
            "InvCislo": "INV-001234",
            "Pamkat": "https://pamatkovykatalog.cz/",
            "Cislo": "12345/7-6789",
            "Material": "Opuka a omítka",
            "Rozmer": "Výška fasády cca 12 m",
            "Autor": "neznámý stavitel",
            "Datace": "konec 17. století",
        },
        "zadavatel": {
            "Jmeno": "Město Libčice nad Vltavou",
            "Ulice": "Husova 5",
            "Psc": "252 66",
            "Mesto": "Libčice nad Vltavou",
        },
        "odber": {
            "Kdo": "Jan Novák a Petra Svobodová",
            "Datum": "24. června 2025",
        },
        "images": {
            "title": "images/t.jpg",
        },
    }

    strati_context = {
        "cislo": "001",
        "oznaceni": "A1",
        "popis": "This is a sample description.",
        "lokalizace": "Prague, Czechia",
        "image": {
            "a": "images/t.jpg",
            "b": "images/t.jpg",
            "c": "images/t.jpg",
            "d": "images/t.jpg",
        },
        "anot": {
            "a": "Annotation of A",
            "b": "Annotation B",
            "d": "Annotation D",
        },
        "tex_table_popis": {
            "strati": "This is stratigraphy description text in LaTeX.",
        },
        "dic": {
            "zprava": {
                "vzorek_name": "Sample2",
            }
        },
    }
    strati_context2 = {
        "cislo": "002",
        "oznaceni": "A2",
        "popis": "Omítka.",
        "lokalizace": "Hlavice",
        "image": {
            "a": "images/t.jpg",
            "b": "images/t.jpg",
            "c": "images/t.jpg",
            "d": "images/t.jpg",
        },
        "anot": {
            "a": "Annotation of A",
            "b": "Annotation B",
            "d": "Annotation D",
        },
        "tex_table_popis": {
            "strati": "This is stratigraphy description text in LaTeX.",
        },
        "dic": {
            "zprava": {
                "vzorek_name": "Sample2",
            }
        },
    }

    zaver_context = {
        "zprava": {
            "vzorek_name": "Sample",
        }
    }

    return [
        Section(template="aaa-packages.tex", context={}),
        Section(template="aaa-begin.tex.j2", context=report_info),
        Section(template="title.tex.j2", context=report_info),
        Section(template="strati.tex.j2", context=strati_context),
        Section(template="strati.tex.j2", context=strati_context2),
        Section(template="zaver.tex.j2", context=zaver_context),
        Section(template="zzz-end.tex", context={}),
    ]
