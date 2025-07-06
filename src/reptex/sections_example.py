from pathlib import Path
from typing import List

from reptex.section import Section


def build_sections(template_dir: Path) -> List[Section]:
    """Construct the list of sections and their rendering context."""
    sections: List[Section] = [
        Section(
            template=template_dir / "aaa-packages.tex.j2",
            context={"template": "aaa-packages.tex.j2"},
        ),
        Section(
            template=template_dir / "aaa-begin.tex.j2",
            context={
                "template": "aaa-begin.tex.j2",
                "format": {"line_height": 1.5},
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
            },
        ),
        Section(
            template=template_dir / "title.tex.j2",
            context={
                "template": "title.tex.j2",
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
                "images": {"title": "../images/example.png"},
            },
        ),
        Section(
            template=template_dir / "zadani.tex.j2",
            context={
                "template": "zadani.tex.j2",
                "section": "Zadání průzkumu",
                "text": "Popis odebraných vzorků a zadání průzkumu jsou uvedeny v následující tabulce.",
                "table": {"tex": "", "popis": "Popis vzorků."},
                "newpage": r"\newpage",
            },
        ),
        Section(
            template=template_dir / "metody.tex.j2",
            context={
                "template": "metody.tex.j2",
                "section": "Metody",
                "tex": r"",
                "newpage": r"\newpage",
            },
        ),
        Section(
            template=template_dir / "strati.tex.j2",
            context={
                "template": "strati.tex.j2",
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
                    "a": "../images/example.png",
                    "b": "../images/example.png",
                    "c": "../images/example.png",
                    "d": "../images/example.png",
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
            },
        ),
        Section(
            template=template_dir / "zaver.tex.j2",
            context={
                "template": "zaver.tex.j2",
                "section": "Záver",
                "tex": r"Place tex here.",
                "newpage": r"\newpage",
            },
        ),
        Section(template=template_dir / "zzz-end.tex.j2", context={"template": "zzz-end.tex.j2"}),
    ]

    return sections
