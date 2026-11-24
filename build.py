import re, os
D = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(D, 'img')

R = [
 ('kalisz', 3, 'Żłobek Miejski „Szuwarek”', 'Kalisz Pomorski, woj. zachodniopomorskie', 'Otwarty 1 października 2022 r., budowa trwała <b>9 miesięcy</b>. Inwestycja wygrała konkurs na najlepszą zakończoną inwestycję.', 'projekt budynku i zagospodarowania terenu'),
 ('pniewo', 3, 'Muzeum Fortyfikacji i Nietoperzy', 'Pniewo, gmina Międzyrzecz', 'Przebudowa i rozbudowa budynku z nowym holem i salą ekspozycyjną, <b>632,56 m²</b> powierzchni użytkowej.', 'projekt'),
 ('drezdenko', 2, 'Żłobek i przedszkole z placem zabaw', 'Drezdenko, powiat strzelecko-drezdenecki', 'Dwukondygnacyjny budynek w kształcie odwróconej litery C, <b>3244 m²</b> powierzchni użytkowej.', 'projekt'),
 ('raclaw', 3, 'Centrum Opiekuńczo-Mieszkalne', 'Racław, gmina Bogdaniec', 'Budynek dostosowany do osób z niepełnosprawnościami, <b>499,54 m²</b> powierzchni zabudowy.', 'projekt w formule „zaprojektuj i wybuduj”'),
 ('gremagor', 2, 'Dom jednorodzinny GreMagor', 'dom szkieletowy drewniany', 'Prosta bryła ze stalowymi łącznikami i drewnianymi detalami, <b>145 m²</b> powierzchni użytkowej.', 'projekt i budowa'),
 ('illingen', 7, 'Dom dwulokalowy pod Illingen', 'Niemcy', 'Konstrukcja szkieletowa GreMagor, <b>180 m²</b> powierzchni użytkowej. W galerii cała budowa, od szkieletu po elewację.', 'budowa'),
 ('merchweiler', 6, 'Dom jednorodzinny w Merchweiler', 'Niemcy', 'Lekka konstrukcja szkieletowa w systemie GreMagor, <b>145 m²</b> powierzchni zabudowy.', 'budowa'),
 ('wiata', 4, 'Wiata garażowa z pomieszczeniem gospodarczym', 'okolice Gorzowa Wielkopolskiego', 'Drewniana konstrukcja w klasycznym stylu.', 'wykonanie i montaż'),
]
P = [
 ('p-woda', 'Dom na wodzie', 'Koncepcja: szkielet drewniany GreMagor na stalowym pontonie.'),
 ('p-letni', 'Domek letniskowy całoroczny', '40 m² powierzchni użytkowej, salon z aneksem, łazienka i antresola.'),
 ('p-wielo', 'Domy wielorodzinne', 'Trzykondygnacyjne budynki, na każdej kondygnacji trzy mieszkania.'),
 ('p-t1', 'Dom parterowy T-1', 'Przestronny dom energooszczędny z wyraźnym podziałem na strefę dzienną i nocną.'),
 ('p-d5', 'Dom parterowy D-5', 'Otwarty salon z jadalnią, kuchnia ze spiżarnią.'),
 ('p-d4', 'Dom z poddaszem D-4', 'Dom energooszczędny z poddaszem użytkowym.'),
 ('p-d3', 'Dom z poddaszem D-3', 'Energooszczędny i ekonomiczny w budowie.'),
 ('p-d2', 'Niewielki dom parterowy D-2', 'Funkcjonalny układ na małej powierzchni.'),
 ('p-d1', 'Budynek rekreacji indywidualnej D-1', 'Energooszczędny dom do wypoczynku.'),
]

def jest(n): return os.path.exists(os.path.join(IMG, n))

def zdj(k, i, pierwszy, alt):
    b = f'img/{k}-{i}'
    ss = ', '.join(f'{b}-{w}.webp {w}w' for w in (600, 800) if jest(f'{k}-{i}-{w}.webp'))
    duze = f'{b}-1600.webp' if jest(f'{k}-{i}-1600.webp') else (f'{b}-800.webp' if jest(f'{k}-{i}-800.webp') else f'{b}-600.webp')
    sz = '(max-width:760px) 86vw, (max-width:1280px) 44vw, (max-width:1700px) 31vw, 450px'
    if pierwszy:
        return f'<img src="{b}-600.webp" srcset="{ss}" sizes="{sz}" width="600" height="450" loading="lazy" decoding="async" alt="{alt}" data-duze="{duze}" draggable="false">'
    return f'<img data-src="{b}-600.webp" data-srcset="{ss}" sizes="{sz}" width="600" height="450" decoding="async" alt="{alt}, zdjęcie {i}" data-duze="{duze}" draggable="false">'

def fot(k, n, tyt):
    imgs = ''.join(zdj(k, i, i == 1, tyt) for i in range(1, n + 1))
    nav = ''
    if n > 1:
        nav = ('<button class="pv" aria-label="Poprzednie zdjęcie"><svg><use href="#sl"/></svg></button>'
               '<button class="nx" aria-label="Następne zdjęcie"><svg><use href="#sp"/></svg></button>'
               f'<span class="lic">1 / {n}</span>')
    t = re.sub('<[^>]+>', '', tyt)
    return f'<div class="fot" data-tytul="{t}"><div class="fot-tor">{imgs}</div>{nav}</div>'

kr = '\n'.join(f'<article class="karta">{fot(k, n, t)}<h3>{t}</h3><p class="gdzie">{g}</p><p class="fakt">{f}</p><span class="tag">{tag}</span></article>' for k, n, t, g, f, tag in R)
kp = '\n'.join(f'<article class="karta">{fot(k, 1, t)}<h3>{t}</h3><p class="fakt">{f}</p></article>' for k, t, f in P)

s = open(os.path.join(D, 'src.html'), encoding='utf-8').read()
s = s.replace('{{KARTY_R}}', kr).replace('{{KARTY_P}}', kp)
s = s.replace('{{BADGE_STYLE}}', open(os.path.join(D, 'badge_style.part'), encoding='utf-8').read().replace('<style>', '').replace('</style>', '').strip())
s = s.replace('{{BADGE_LINK}}', open(os.path.join(D, 'badge_link.part'), encoding='utf-8').read().strip().replace('utm_source=amdinwestycje.pl', 'utm_source=ecotekhome.pl'))
assert '{{' not in s and 'amdinwestycje' not in s and '—' not in s
a = s.find('<body>')
def fix(m): return re.sub(r'(?<=[\s>(])([aiouwzAIOUWZ]|we|ze|na|do|od|po) (?=\S)', lambda k: k.group(1) + '&nbsp;', m.group(0))
b = s.find('<script>', a)
s = s[:a] + re.sub(r'>[^<]+<', fix, s[a:b]) + s[b:]
open(os.path.join(D, 'index.html'), 'w', encoding='utf-8').write(s)
print('ok', len(s))
