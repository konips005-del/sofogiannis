#!/usr/bin/env python3
"""Static site generator για το Γραφείο Τελετών Σοφογιάννης (Βύρωνας).

Τρέξε:  python3 tools/build.py   (από τον φάκελο website/)
Παράγει όλα τα HTML, sitemap.xml και robots.txt. Για αλλαγή domain άλλαξε μόνο το SITE.
"""
import hashlib
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://teletessofogiannisvyronas.gr"
TODAY = date.today().isoformat()

BIZ = {
    "name": "Γραφείο Τελετών Σοφογιάννης · Βύρωνας",
    "brand": "Σοφογιάννης",
    "legal": "Γραφείο Τελετών Σοφογιάννης",
    "owner": "Νικόλαος Ι. Σοφογιάννης",
    "phone": "210 7600 900",
    "phone_tel": "+302107600900",
    "phone2": "210 7600 907",
    "phone2_tel": "+302107600907",
    "fax": "210 7600 908",
    "mobile": "6944 14 58 44",
    "mobile_tel": "+306944145844",
    "email": "nikossofogiannis@gmail.com",
    "street": "Φορμίωνος 233",
    "city": "Βύρωνας",
    "region": "Αττική",
    "since": 2003,
}
YEARS = date.today().year - BIZ["since"]
EXP_YEARS = date.today().year - 1990  # στον χώρο από το 1990 (36 χρόνια το 2026)
MAPS_Q = "Φορμίωνος 233, Βύρωνας"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + MAPS_Q.replace(" ", "+")
MAPS_EMBED = "https://www.google.com/maps?q=" + MAPS_Q.replace(" ", "+") + "&output=embed"

LOGO_V = hashlib.md5(open(os.path.join(ROOT, "images/logo-emblem.webp"), "rb").read()).hexdigest()[:8]
ASSET_V = hashlib.md5(b"".join(open(os.path.join(ROOT, f), "rb").read()
                              for f in ("css/style.css", "js/main.js"))).hexdigest()[:8]

AREAS_MAIN = "Βύρωνας"
AREAS = ["Καισαριανή", "Παγκράτι", "Υμηττός", "Ζωγράφου", "Ηλιούπολη", "Δάφνη", "Άγιος Δημήτριος",
         "Νέα Σμύρνη", "Μετς", "Αθήνα", "Όλη η Αττική", "Όλη η Ελλάδα", "Εξωτερικό"]

# ----------------------------------------------------------------- icons
def svg(inner, stroke=1.6):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (stroke, inner))

I = {
    "phone": svg('<path d="M5 3.5h3.2l1.6 4.2-2.1 1.4a11.5 11.5 0 0 0 7.2 7.2l1.4-2.1 4.2 1.6V19a1.8 1.8 0 0 1-2 1.8A16.5 16.5 0 0 1 3.2 5.5 1.8 1.8 0 0 1 5 3.5z"/>'),
    "mobile": svg('<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    "fax": svg('<path d="M7 8V3.5h8l2 2V8"/><rect x="3.5" y="8" width="17" height="9" rx="2"/><path d="M7 14h10v6.5H7z"/><circle cx="17" cy="11" r=".8"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>'),
    "pin": svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>'),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "chev": svg('<path d="m6 9 6 6 6-6"/>', 2),
    "check": svg('<circle cx="12" cy="12" r="9"/><path d="m8.2 12.2 2.6 2.6 5-5.2"/>'),
    "info": svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/>', 1.8),
    "cross": svg('<path d="M12 2.8v18.4M7.2 8h9.6"/><path d="M8.5 21.2h7"/>'),
    "urn": svg('<path d="M9 3.5h6M10 3.5v2.2c0 .6-.4 1-.9 1.3C6.8 8.4 5.5 10.6 5.5 13.2c0 3.4 2.4 6 5.2 6.8h2.6c2.8-.8 5.2-3.4 5.2-6.8 0-2.6-1.3-4.8-3.6-6.2-.5-.3-.9-.7-.9-1.3V3.5"/><path d="M8.5 20.5h7M7 12h10"/>'),
    "candle": svg('<path d="M12 2.5c1.5 1.8 2.3 3 2.3 4.2a2.3 2.3 0 0 1-4.6 0c0-1.2.8-2.4 2.3-4.2z"/><rect x="9" y="10.5" width="6" height="11" rx="1"/><path d="M6.5 21.5h11"/>'),
    "plane": svg('<path d="M21 4.5 3.5 11.2l6 2.3 2.3 6L21 4.5z"/><path d="m9.5 13.5 4.2-4.2"/>'),
    "doc": svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 16.5h5"/>'),
    "heart": svg('<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.2a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20z"/>'),
    "shield": svg('<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>'),
    "map": svg('<path d="m9 4-5.5 2v14L9 18l6 2 5.5-2V4L15 6z"/><path d="M9 4v14M15 6v14"/>'),
    "hands": svg('<path d="M7 11V6.5a1.5 1.5 0 0 1 3 0V10m0-3.5v-1a1.5 1.5 0 0 1 3 0V10m0-3a1.5 1.5 0 0 1 3 0v3m0-1.5a1.5 1.5 0 0 1 3 0v5.5a6.5 6.5 0 0 1-6.5 6.5h-1A6.5 6.5 0 0 1 5 16l-1.6-3.2a1.5 1.5 0 0 1 2.6-1.5L7 13"/>'),
    "flower": svg('<circle cx="12" cy="9" r="2.2"/><path d="M12 6.8c0-2.4 1.6-3.8 1.6-3.8s1.9 1.6 1.2 3.9M14.2 9c2.2-.8 4.2.2 4.2.2s-.6 2.4-3 2.6M13.6 11c1.4 1.9 1 4 1 4s-2.4-.3-3-2.6M10.4 11c-1.4 1.9-1 4-1 4M9.8 9c-2.2-.8-4.2.2-4.2.2s.6 2.4 3 2.6M12 6.8C12 4.4 10.4 3 10.4 3s-1.9 1.6-1.2 3.9"/><path d="M12 11.2V21"/>'),
    "car": svg('<path d="M2.5 15.5V12l2.2-4.5h11l3.8 3.5 2 .8v3.7z"/><circle cx="7" cy="16" r="2"/><circle cx="17" cy="16" r="2"/><path d="M4.7 11h14"/>'),
    "coffee": svg('<path d="M4 9h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 10.5h1.5a2.5 2.5 0 0 1 0 5H16M7 3.5c0 1.2 1 1.2 1 2.4M11 3.5c0 1.2 1 1.2 1 2.4"/>'),
    "news": svg('<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M7 8.5h10M7 12h10M7 15.5h6"/>'),
    "globe": svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9S14.5 18.5 12 21c-2.5-2.5-3.8-5.5-3.8-9S9.5 5.5 12 3z"/>'),
    "hospital": svg('<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M12 7.5v6M9 10.5h6M9 20.5v-3h6v3"/>'),
    "user": svg('<circle cx="12" cy="8" r="3.6"/><path d="M4.5 20.5c.8-4 3.8-6.5 7.5-6.5s6.7 2.5 7.5 6.5"/>'),
}

# Κλαδί ελιάς: διακοσμητικό διαχωριστικό τίτλων
LEAF = ('<svg class="leaf" viewBox="0 0 64 16" aria-hidden="true"><path d="M2 8h60" stroke="currentColor" stroke-width="1"/>'
        '<path d="M32 8c-5-6-11-6-15-4 4 4 10 5 15 4zM32 8c5-6 11-6 15-4-4 4-10 5-15 4zM32 8c-5 6-11 6-15 4 4-4 10-5 15-4zM32 8c5 6 11 6 15 4-4-4-10-5-15-4z" fill="currentColor" opacity=".9"/></svg>')

# ----------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "kideies", "icon": "cross", "title": "Κηδείες",
        "nav": "Οργάνωση κηδείας από την αρχή ως το τέλος",
        "card": "Αναλαμβάνουμε κάθε λεπτομέρεια της τελετής, ώστε η οικογένεια να σταθεί δίπλα στον άνθρωπό της με αξιοπρέπεια.",
        "seo_title": "Κηδείες στον Βύρωνα · Οργάνωση Κηδείας · Σοφογιάννης",
        "h1": "Οργάνωση κηδείας",
        "desc": "Πλήρης οργάνωση κηδείας στον Βύρωνα και τις γύρω περιοχές από το Γραφείο Τελετών Σοφογιάννης. Παραλαβή σορού, ναός, κοιμητήριο, στολισμός, αγγελτήρια. Τηλ. 210 7600 900.",
        "lead": "Από την πρώτη τηλεφωνική επικοινωνία μέχρι την ολοκλήρωση της εξόδιας ακολουθίας, αναλαμβάνουμε κάθε βήμα με διακριτικότητα, ώστε εσείς να μπορείτε να αφοσιωθείτε στον αποχαιρετισμό.",
    },
    {
        "slug": "apotefroseis", "icon": "urn", "title": "Αποτεφρώσεις",
        "nav": "Οργάνωση αποτέφρωσης & τεφροδόχοι",
        "card": "Οργανώνουμε την αποτέφρωση σύμφωνα με την ισχύουσα νομοθεσία, με ή χωρίς θρησκευτική τελετή, και φροντίζουμε για την παράδοση της τεφροδόχου.",
        "seo_title": "Αποτέφρωση Νεκρών · Γραφείο Τελετών Βύρωνας · Σοφογιάννης",
        "h1": "Αποτέφρωση",
        "desc": "Οργάνωση αποτέφρωσης από το Γραφείο Τελετών Σοφογιάννης στον Βύρωνα. Δικαιολογητικά, μεταφορά στο κέντρο αποτέφρωσης, τελετή, τεφροδόχος. Τηλ. 210 7600 900.",
        "lead": "Η αποτέφρωση είναι μια επιλογή που όλο και περισσότερες οικογένειες εξετάζουν. Σας εξηγούμε με σαφήνεια τι προβλέπεται, αναλαμβάνουμε τα δικαιολογητικά και οργανώνουμε τα πάντα με τον ίδιο σεβασμό μιας παραδοσιακής τελετής.",
    },
    {
        "slug": "mnimosyna", "icon": "candle", "title": "Μνημόσυνα",
        "nav": "Τρισάγια, 40ήμερα, ετήσια μνημόσυνα",
        "card": "Οργανώνουμε μνημόσυνα και τρισάγια: συνεννόηση με τον ναό, κόλλυβα, αγγελίες και χώρο για τον καφέ της παρηγοριάς.",
        "img": "mnimosyno-naos.jpg",
        "seo_title": "Μνημόσυνα Βύρωνας · Κόλλυβα, 40ήμερα, Ετήσια · Σοφογιάννης",
        "h1": "Μνημόσυνα",
        "desc": "Οργάνωση μνημοσύνων στον Βύρωνα: 9ήμερα, 40ήμερα, εξάμηνα, ετήσια. Κόλλυβα, ναός, αγγελίες, καφές παρηγοριάς. Γραφείο Τελετών Σοφογιάννης, 210 7600 900.",
        "lead": "Το μνημόσυνο είναι η στιγμή που η οικογένεια και οι φίλοι ξανασυναντιούνται για να θυμηθούν. Φροντίζουμε ώστε κάθε λεπτομέρεια να είναι έτοιμη, όπως ακριβώς τη θέλετε.",
    },
    {
        "slug": "anthostolismos", "icon": "flower", "title": "Ανθοστολισμός",
        "nav": "Στολισμός ναού, φερέτρου & στεφάνια",
        "card": "Στολισμός ναού και φερέτρου, στεφάνια και ανθοσυνθέσεις με λουλούδια της επιλογής σας, για έναν αποχαιρετισμό με φροντίδα και αξιοπρέπεια.",
        "seo_title": "Ανθοστολισμός Κηδείας · Στεφάνια & Στολισμός Ναού · Βύρωνας",
        "h1": "Ανθοστολισμός",
        "desc": "Ανθοστολισμός κηδείας και μνημοσύνου: στολισμός ναού και φερέτρου, στεφάνια, ανθοσυνθέσεις. Γραφείο Τελετών Σοφογιάννης, Βύρωνας. Τηλ. 210 7600 900.",
        "lead": "Τα λουλούδια είναι ένας από τους πιο τρυφερούς τρόπους να εκφράσουμε αγάπη και σεβασμό. Φροντίζουμε τον στολισμό του ναού, του φερέτρου και τα στεφάνια, ώστε ο αποχαιρετισμός να έχει την ομορφιά που του αξίζει.",
    },
    {
        "slug": "metafora-sorou", "icon": "plane", "title": "Μεταφορά σορού",
        "nav": "Σε όλη την Ελλάδα & επαναπατρισμός",
        "card": "Μεταφορά σορού σε κάθε πόλη ή χωριό της Ελλάδας, καθώς και από και προς το εξωτερικό, με όλα τα απαραίτητα έγγραφα.",
        "seo_title": "Μεταφορά Σορού & Επαναπατρισμός · Γραφείο Τελετών Βύρωνας",
        "h1": "Μεταφορά σορού και επαναπατρισμός",
        "desc": "Μεταφορά σορού σε όλη την Ελλάδα και επαναπατρισμός από το εξωτερικό. Έγγραφα, προξενεία, αεροπορική μεταφορά. Γραφείο Τελετών Σοφογιάννης, Βύρωνας, 210 7600 900.",
        "lead": "Όταν ο άνθρωπός σας θα ήθελε να αναπαυθεί στον τόπο του, ή όταν η απώλεια συμβαίνει μακριά από το σπίτι, αναλαμβάνουμε τη μεταφορά από άκρη σε άκρη, με συνέπεια και διαρκή ενημέρωση της οικογένειας.",
    },
    {
        "slug": "diadikasies", "icon": "doc", "title": "Γραφειοκρατικές διαδικασίες",
        "nav": "Δικαιολογητικά, ληξιαρχείο, ασφαλιστικά",
        "card": "Διεκπεραιώνουμε τα έγγραφα που απαιτούνται μετά από μια απώλεια και σας καθοδηγούμε σε όσα ακολουθούν.",
        "seo_title": "Διαδικασίες μετά τον Θάνατο · Ληξιαρχική Πράξη, Έξοδα Κηδείας",
        "h1": "Γραφειοκρατικές διαδικασίες",
        "desc": "Διεκπεραίωση διαδικασιών μετά από θάνατο: ληξιαρχική πράξη θανάτου, άδεια ταφής, έξοδα κηδείας από τον e-ΕΦΚΑ. Γραφείο Τελετών Σοφογιάννης, Βύρωνας, 210 7600 900.",
        "lead": "Τις πρώτες ημέρες μετά από μια απώλεια, η τελευταία σκέψη που πρέπει να σας απασχολεί είναι τα χαρτιά. Αναλαμβάνουμε τα έγγραφα της κηδείας και σας εξηγούμε απλά τι χρειάζεται να γίνει στη συνέχεια.",
    },
]

# ----------------------------------------------------------------- layout helpers
def url(path):
    return SITE + path

def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def business_ld():
    return {
        "@type": ["FuneralHome", "LocalBusiness"],
        "@id": url("/#funeralhome"),
        "name": BIZ["name"],
        "alternateName": ["Γραφείο Τελετών Σοφογιάννης", "Σοφογιάννης Γραφείο Τελετών", "Γραφείο Τελετών Βύρωνας Σοφογιάννης", "Sofogiannis Funeral Home"],
        "description": "Γραφείο τελετών στον Βύρωνα από το 2003, Φορμίωνος 233. Κηδείες, αποτεφρώσεις, μνημόσυνα, ανθοστολισμός, μεταφορά σορού και διεκπεραίωση γραφειοκρατικών διαδικασιών, 24 ώρες το 24ωρο.",
        "url": url("/"),
        "image": [url("/og-image.png"), url("/images/grafeio-vyronas.jpg"), url("/images/nikolaos-sofogiannis.jpg")],
        "logo": url("/logo.png"),
        "telephone": [BIZ["phone_tel"], BIZ["phone2_tel"], BIZ["mobile_tel"]],
        "faxNumber": "+302107600908",
        "email": BIZ["email"],
        "founder": {"@type": "Person", "name": "Νικόλαος Σοφογιάννης"},
        "foundingDate": str(BIZ["since"]),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "addressLocality": BIZ["city"],
            "addressRegion": BIZ["region"],
            "addressCountry": "GR",
        },
        "hasMap": MAPS_LINK,
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": BIZ["phone_tel"], "contactType": "customer service", "availableLanguage": ["el"]},
            {"@type": "ContactPoint", "telephone": BIZ["mobile_tel"], "contactType": "emergency", "availableLanguage": ["el"],
             "hoursAvailable": {"@type": "OpeningHoursSpecification", "opens": "00:00", "closes": "23:59", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}},
        ],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        },
        "areaServed": [{"@type": "Place", "name": a} for a in [AREAS_MAIN] + AREAS[:-3]] + [{"@type": "AdministrativeArea", "name": "Αττική"}, {"@type": "Country", "name": "Ελλάδα"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Υπηρεσίες γραφείου τελετών",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"], "url": url("/ypiresies/%s/" % s["slug"])}} for s in SERVICES],
        },
    }

def graph(path, title, desc, crumbs, extra=None):
    nodes = [
        {"@type": "WebSite", "@id": url("/#website"), "url": url("/"), "name": BIZ["name"], "inLanguage": "el", "publisher": {"@id": url("/#funeralhome")}},
        business_ld(),
        {"@type": "WebPage", "@id": url(path) + "#webpage", "url": url(path), "name": title, "description": desc, "inLanguage": "el",
         "isPartOf": {"@id": url("/#website")}, "about": {"@id": url("/#funeralhome")}},
    ]
    if crumbs:
        nodes.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(crumbs)]})
    nodes += extra or []
    return json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False, indent=2)

NAV = [("Αρχική", "/"), ("Το Γραφείο", "/to-grafeio/"), ("Υπηρεσίες", "/ypiresies/"), ("Εκθεσιακός Χώρος", "/ekthesiakos-xoros/"), ("Τι κάνω τώρα", "/ti-kano-tora/"), ("Επικοινωνία", "/epikoinonia/")]

def head(path, title, desc, ld):
    return f"""<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#2f7d46">
  <link rel="canonical" href="{url(path)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="el_GR">
  <meta property="og:site_name" content="{esc(BIZ['name'])}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url(path)}">
  <meta property="og:image" content="{url('/og-image.png')}?v={LOGO_V}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Γραφείο Τελετών Σοφογιάννης · Βύρωνας">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{url('/og-image.png')}?v={LOGO_V}">
  <meta name="format-detection" content="telephone=no">
  <link rel="icon" href="/favicon.ico?v={LOGO_V}" sizes="48x48">
  <link rel="icon" href="/favicon-96.png?v={LOGO_V}" sizes="96x96" type="image/png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v={LOGO_V}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bona+Nova:ital,wght@0,400;0,700;1,400&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css?v={ASSET_V}">
  <script>document.documentElement.classList.add("js")</script>
  <script type="application/ld+json">
{ld}
  </script>
</head>
"""

def brand(light=False):
    return f"""<a class="brand{' light' if light else ''}" href="/" aria-label="{esc(BIZ['name'])}, αρχική σελίδα">
        <img class="brand-mark" src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="58" height="58">
        <span class="brand-text"><span class="brand-name">Σοφογιάννης</span><span class="brand-sub">Γραφείο Τελετών · Βύρωνας</span></span>
      </a>"""

def header(active):
    dd_items = "".join(
        f'<a href="/ypiresies/{s["slug"]}/"><span class="ic">{I[s["icon"]]}</span><span><strong>{s["title"]}</strong><small>{s["nav"]}</small></span></a>'
        for s in SERVICES)
    links = []
    for name, href in NAV:
        cur = ' aria-current="page"' if active == href else ""
        if href == "/ypiresies/":
            act = " active" if active.startswith("/ypiresies/") else ""
            links.append(f"""<div class="dd{act}">
          <button type="button" aria-expanded="false" aria-haspopup="true">Υπηρεσίες {I['chev']}</button>
          <div class="dd-menu">{dd_items}<a class="all" href="/ypiresies/">Όλες οι υπηρεσίες {I['arrow']}</a></div>
        </div>""")
        else:
            links.append(f'<a href="{href}"{cur}>{name}</a>')
    m_sub = "".join(f'<a href="/ypiresies/{s["slug"]}/">{s["title"]}</a>' for s in SERVICES)
    m_links = []
    for name, href in NAV:
        m_links.append(f'<a href="{href}">{name}</a>')
        if href == "/ypiresies/":
            m_links.append(f'<div class="sub">{m_sub}</div>')
    return f"""<body>
<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a>
<div class="topbar">
  <div class="wrap">
    <div class="tb-left"><span><span class="dot"></span>Δίπλα σας 24 ώρες το 24ωρο</span><a class="hide-sm" href="{MAPS_LINK}" target="_blank" rel="noopener">{I['pin']}{BIZ['street']}, {BIZ['city']}</a></div>
    <div class="tb-right"><a href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone']}</a><a class="hide-sm" href="tel:{BIZ['phone2_tel']}">{BIZ['phone2']}</a><a href="tel:{BIZ['mobile_tel']}">{I['mobile']}{BIZ['mobile']}</a></div>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    {brand()}
    <nav class="nav" aria-label="Κύρια πλοήγηση">
      {''.join(links)}
    </nav>
    <div class="header-cta">
      <a class="btn btn-primary" href="tel:{BIZ['phone_tel']}">{I['phone']}<span>{BIZ['phone']}</span></a>
      <button class="menu-toggle" type="button" aria-label="Μενού" aria-expanded="false" aria-controls="mobile-nav"><span></span></button>
    </div>
  </div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Πλοήγηση κινητού">
  {''.join(m_links)}
  <div class="m-contact">
    <a class="btn btn-primary" href="tel:{BIZ['phone_tel']}">{I['phone']}Κλήση {BIZ['phone']}</a>
    <a class="btn btn-ghost" href="tel:{BIZ['mobile_tel']}">{I['mobile']}Κινητό {BIZ['mobile']}</a>
  </div>
</nav>
<main id="main">
"""

def footer():
    svc = "".join(f'<li><a href="/ypiresies/{s["slug"]}/">{s["title"]}</a></li>' for s in SERVICES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="f-about">
      {brand(light=True)}
      <p>Γραφείο τελετών στον Βύρωνα από το 2003, στη Φορμίωνος 233. Με σεβασμό, αξιοπρέπεια και διακριτικότητα, δίπλα σας στις πιο δύσκολες στιγμές.</p>
    </div>
    <div>
      <h4>Υπηρεσίες</h4>
      <ul>{svc}</ul>
    </div>
    <div>
      <h4>Πλοήγηση</h4>
      <ul>
        <li><a href="/">Αρχική</a></li>
        <li><a href="/to-grafeio/">Το Γραφείο</a></li>
        <li><a href="/ypiresies/">Υπηρεσίες</a></li>
        <li><a href="/ekthesiakos-xoros/">Εκθεσιακός Χώρος</a></li>
        <li><a href="/ti-kano-tora/">Τι κάνω τώρα</a></li>
        <li><a href="/epikoinonia/">Επικοινωνία</a></li>
      </ul>
    </div>
    <div>
      <h4>Επικοινωνία</h4>
      <ul class="f-contact">
        <li>{I['phone']}<span><a href="tel:{BIZ['phone_tel']}"><strong>{BIZ['phone']}</strong></a> · <a href="tel:{BIZ['phone2_tel']}"><strong>{BIZ['phone2']}</strong></a></span></li>
        <li>{I['mobile']}<a href="tel:{BIZ['mobile_tel']}"><strong>{BIZ['mobile']}</strong></a></li>
        <li>{I['fax']}<span>Fax {BIZ['fax']}</span></li>
        <li>{I['mail']}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
        <li>{I['pin']}<a href="{MAPS_LINK}" target="_blank" rel="noopener">{BIZ['street']}, {BIZ['city']}</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="wrap">
      <span>© <span id="year">{date.today().year}</span> {BIZ['legal']} · {BIZ['owner']}</span>
      <a class="credit" href="https://digitalroast.gr" target="_blank" rel="noopener">Made by <strong>Digital Roast</strong></a>
    </div>
  </div>
</footer>
<div class="call-bar" aria-label="Γρήγορη κλήση">
  <a class="primary" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone']}</a>
  <a href="tel:{BIZ['mobile_tel']}">{I['mobile']}Κινητό</a>
</div>
<script src="/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

def sec_title(text, center=False, light=False):
    return f'<div class="sec-title{" center" if center else ""}{" light" if light else ""}">{LEAF}<h2>{text}</h2></div>'

def page_hero(crumbs, h1, lead, actions=True):
    bc = []
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            bc.append(f'<span aria-current="page">{n}</span>')
        else:
            bc.append(f'<a href="{p}">{n}</a><span aria-hidden="true">/</span>')
    act = f"""<div class="hero-actions">
        <a class="btn btn-primary" href="tel:{BIZ['phone_tel']}">{I['phone']}Κλήση · {BIZ['phone']}</a>
        <a class="btn btn-ghost" href="tel:{BIZ['mobile_tel']}">{I['mobile']}{BIZ['mobile']}</a>
      </div>""" if actions else ""
    return f"""<section class="page-hero">
  <div class="wrap">
    <div class="bevel">
      <div class="panel">
        <img class="panel-art" src="/images/monastery.svg" alt="" aria-hidden="true">
        <nav class="breadcrumbs" aria-label="Διαδρομή">{''.join(bc)}</nav>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        {act}
      </div>
    </div>
  </div>
</section>
"""

def cta_band(title="Είμαστε εδώ, όποια ώρα κι αν μας χρειαστείτε.",
             text="Μιλήστε απευθείας μαζί μας, ημέρα ή νύχτα, Σαββατοκύριακα και αργίες. Θα σας εξηγήσουμε με ηρεμία τα επόμενα βήματα."):
    return f"""<section class="cta-wrap">
  <div class="wrap">
    <div class="cta-band">
      <img class="cta-emblem" src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="120" height="120">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="actions">
        <a class="btn btn-light" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone']}</a>
        <a class="btn btn-outline-light" href="tel:{BIZ['mobile_tel']}">{I['mobile']}{BIZ['mobile']}</a>
      </div>
    </div>
  </div>
</section>
"""

def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>'
        for q, a in items) + "</div>"

def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def service_cards(items=None):
    out = []
    for i, s in enumerate(items or SERVICES):
        out.append(f"""<a class="service-card" href="/ypiresies/{s['slug']}/">
          <span class="num">{i + 1:02d}</span>
          <span class="ic">{I[s['icon']]}</span>
          <h3>{s['title']}</h3>
          <p>{s['card']}</p>
          <span class="more">Περισσότερα {I['arrow']}</span>
        </a>""")
    return '<div class="services-grid">' + "".join(out) + "</div>"

def check_list(items, two=False):
    return f'<ul class="check-list{" two" if two else ""}">' + "".join(f"<li>{I['check']}<span>{t}</span></li>" for t in items) + "</ul>"

def contact_card():
    """Αντίγραφο της πίσω όψης της επαγγελματικής κάρτας."""
    return f"""<div class="bizcard" aria-label="Στοιχεία επικοινωνίας">
      <div class="bevel">
        <div class="panel">
          <p class="bc-name">Σοφογιάννης</p>
          <p class="bc-sub">Γραφείο Τελετών</p>
          <p class="bc-owner">{BIZ['owner']}</p>
          <a class="bc-addr" href="{MAPS_LINK}" target="_blank" rel="noopener">{BIZ['street']} · {BIZ['city']}</a>
          <dl class="bc-grid">
            <div><dt>Τηλ.</dt><dd><a href="tel:{BIZ['phone_tel']}">{BIZ['phone']}</a><a href="tel:{BIZ['phone2_tel']}">{BIZ['phone2']}</a></dd></div>
            <div><dt>Κιν.</dt><dd><a href="tel:{BIZ['mobile_tel']}">{BIZ['mobile']}</a></dd></div>
            <div><dt>Fax</dt><dd><span>{BIZ['fax']}</span></dd></div>
          </dl>
          <a class="bc-mail" href="mailto:{BIZ['email']}">{BIZ['email']}</a>
        </div>
      </div>
    </div>"""

def write(path, html):
    rel = path.strip("/")
    if rel.endswith(".html"):
        fn = os.path.join(ROOT, rel)
    else:
        out_dir = os.path.join(ROOT, rel) if rel else ROOT
        os.makedirs(out_dir, exist_ok=True)
        fn = os.path.join(out_dir, "index.html")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(html)

def build_page(path, title, desc, crumbs, body, extra_ld=None, active=None):
    ld = graph(path, title, desc, crumbs, extra_ld)
    write(path, head(path, title, desc, ld) + header(active or path) + body + footer())

PAGES = []  # για sitemap

# ================================================================= HOME
HOME_FAQ = [
    ("Τι κάνω αμέσως μόλις συμβεί ένας θάνατος;",
     f"Καλέστε μας στο <a href=\"tel:{BIZ['phone_tel']}\">{BIZ['phone']}</a> ή στο κινητό <a href=\"tel:{BIZ['mobile_tel']}\">{BIZ['mobile']}</a>, οποιαδήποτε ώρα. Αν ο θάνατος συνέβη στο σπίτι, χρειάζεται ιατρός για τη βεβαίωση θανάτου, ενώ αν συνέβη σε νοσοκομείο, η βεβαίωση εκδίδεται εκεί. Από εκεί και πέρα αναλαμβάνουμε εμείς. Δείτε αναλυτικά τον οδηγό <a href=\"/ti-kano-tora/\">«Τι κάνω τώρα»</a>."),
    ("Εξυπηρετείτε και εκτός Βύρωνα;",
     "Ναι. Το γραφείο μας βρίσκεται στον Βύρωνα, αλλά εξυπηρετούμε όλες τις περιοχές της Αττικής, από τα γύρω προάστια όπως Καισαριανή, Παγκράτι, Υμηττό και Ζωγράφου μέχρι κάθε άλλη γειτονιά, ενώ οργανώνουμε μεταφορές σορού σε όλη την Ελλάδα και το εξωτερικό."),
    ("Είστε διαθέσιμοι Σαββατοκύριακα και αργίες;",
     f"Ναι. Στο κινητό <a href=\"tel:{BIZ['mobile_tel']}\">{BIZ['mobile']}</a> μπορείτε να μας βρείτε 24 ώρες το 24ωρο, κάθε ημέρα του χρόνου, και θα μιλήσετε απευθείας με τον υπεύθυνο του γραφείου."),
    ("Πόσο κοστίζει μια κηδεία;",
     "Το κόστος εξαρτάται από τις επιλογές της οικογένειας (φέρετρο, στολισμός, στεφάνια, κοιμητήριο, μεταφορές κ.λπ.). Σας δίνουμε από την αρχή σαφή και αναλυτική ενημέρωση, χωρίς κρυφές χρεώσεις, και σας ενημερώνουμε για το επίδομα εξόδων κηδείας που μπορεί να δικαιούστε από τον ασφαλιστικό φορέα."),
    ("Αναλαμβάνετε και τα χαρτιά;",
     "Ναι. Διεκπεραιώνουμε τα έγγραφα που απαιτούνται για την κηδεία, όπως η ληξιαρχική πράξη θανάτου και η άδεια ταφής, και σας καθοδηγούμε για όσα ακολουθούν. Δείτε τις <a href=\"/ypiresies/diadikasies/\">γραφειοκρατικές διαδικασίες</a>."),
]

home_body = f"""<section class="hero">
  <div class="hero-bg"><img src="/images/prosopsi-2.jpg" alt="" width="765" height="1020" fetchpriority="high"></div>
  <div class="wrap hero-grid">
    <figure class="hero-shot"><img src="/images/prosopsi-2.jpg" alt="Η πρόσοψη του Γραφείου Τελετών Σοφογιάννης, Φορμίωνος 233, Βύρωνας" width="765" height="1020"></figure>
    <div class="bevel">
      <div class="panel hero-panel">
        <div class="hero-text">
          <h1><span class="h1-script">Σοφογιάννης</span><span class="h1-sub">Γραφείο Τελετών στον Βύρωνα</span></h1>
          <p class="lead">Οργανώνουμε κηδείες, αποτεφρώσεις και μνημόσυνα με σεβασμό και διακριτικότητα, και αναλαμβάνουμε όλα τα διαδικαστικά, ώστε εσείς να σταθείτε δίπλα στους δικούς σας.</p>
          <div class="hero-rows">
            <div class="row-owner">{I['user']}<span>{BIZ['owner']}</span><em class="since">από το 2003</em></div>
            <a class="row-addr" href="{MAPS_LINK}" target="_blank" rel="noopener">{I['pin']}<span>{BIZ['street']} · {BIZ['city']}</span></a>
          </div>
          <div class="hero-actions">
            <a class="btn btn-primary" href="tel:{BIZ['phone_tel']}">{I['phone']}Κλήση {BIZ['phone']}</a>
            <a class="btn btn-purple" href="tel:{BIZ['mobile_tel']}">{I['mobile']}24/7 · {BIZ['mobile']}</a>
            <a class="btn btn-link" href="/ti-kano-tora/">Τι κάνω τώρα; {I['arrow']}</a>
          </div>
        </div>
        <div class="hero-seal">
          <img src="/images/logo-emblem.webp?v={LOGO_V}" alt="Το έμβλημα του Γραφείου Τελετών Σοφογιάννης" width="150" height="150">
        </div>
      </div>
    </div>
  </div>
</section>

<section class="trust" aria-label="Γιατί να μας εμπιστευτείτε">
  <div class="wrap">
    <div class="trust-item"><span class="ic">{I['clock']}</span><div><strong>24 ώρες το 24ωρο</strong><span>Και σε αργίες, και τη νύχτα</span></div></div>
    <div class="trust-item"><span class="ic">{I['shield']}</span><div><strong>{EXP_YEARS} χρόνια στον χώρο</strong><span>Με δικό του γραφείο από το 2003</span></div></div>
    <div class="trust-item"><span class="ic">{I['user']}</span><div><strong>Προσωπική φροντίδα</strong><span>Μιλάτε απευθείας με τον υπεύθυνο</span></div></div>
    <div class="trust-item"><span class="ic">{I['doc']}</span><div><strong>Όλα τα διαδικαστικά</strong><span>Εμείς τα χαρτιά, εσείς η οικογένεια</span></div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      {sec_title("Οι υπηρεσίες μας")}
      <p class="lead">Από την οργάνωση της κηδείας μέχρι το μνημόσυνο και τα έγγραφα, αναλαμβάνουμε τα πάντα, ώστε να μη χρειαστεί να τρέξετε πουθενά.</p>
    </div>
    {service_cards()}
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <figure class="portrait">
      <div class="portrait-frame"><img src="/images/nikolaos-sofogiannis.jpg" alt="Ο Νικόλαος Ι. Σοφογιάννης, υπεύθυνος του Γραφείου Τελετών Σοφογιάννης στον Βύρωνα" width="640" height="643" loading="lazy" decoding="async"></div>
      <figcaption><img src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="56" height="56"><span><strong>{BIZ['owner']}</strong><small>Υπεύθυνος γραφείου</small></span></figcaption>
    </figure>
    <div>
      {sec_title("Λίγα λόγια για εμάς")}
      <p class="quote">«Κάθε οικογένεια που μας εμπιστεύεται τον αποχαιρετισμό ενός αγαπημένου της προσώπου αξίζει την ίδια φροντίδα που θα θέλαμε κι εμείς για τους δικούς μας ανθρώπους.»</p>
      <p>Ο Νικόλαος Σοφογιάννης βρίσκεται στον χώρο των τελετών εδώ και {EXP_YEARS} χρόνια. Το 2003, με την εμπειρία που είχε ήδη αποκτήσει, άνοιξε το πρώτο του γραφείο και το έχτισε από το μηδέν, με προσωπική δουλειά και την εμπιστοσύνη των οικογενειών που εξυπηρέτησε. Σήμερα, στη Φορμίωνος 233 στον Βύρωνα, αναλαμβάνει ο ίδιος κάθε τελετή, από την πρώτη επικοινωνία μέχρι το τελευταίο αντίο. Γνωρίζει ότι καμία οικογένεια δεν είναι ίδια, γι’ αυτό ακούει, προτείνει και σέβεται κάθε επιθυμία.</p>
      {check_list(["Προσωπική επικοινωνία με τον υπεύθυνο, όποια ώρα κι αν καλέσετε", "Σαφής ενημέρωση για το κόστος από την αρχή", "Διακριτικότητα σε κάθε στάδιο της διαδικασίας"])}
      <a class="btn btn-ghost" href="/to-grafeio/">Γνωρίστε μας {I['arrow']}</a>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="section-head">
      {sec_title("Πώς λειτουργούμε", light=True)}
      <p class="lead">Μόλις μας καλέσετε, αναλαμβάνουμε την ευθύνη της διαδικασίας και σας κρατάμε ενήμερους σε κάθε στάδιο.</p>
    </div>
    <ol class="steps">
      <li class="step"><span class="n">1</span><h3>Μας καλείτε</h3><p>Στο {BIZ['phone']} ή στο κινητό {BIZ['mobile']}, ημέρα ή νύχτα. Σας ακούμε και σας λέμε τι χρειάζεται άμεσα.</p></li>
      <li class="step"><span class="n">2</span><h3>Ερχόμαστε</h3><p>Παραλαμβάνουμε με σεβασμό τον εκλιπόντα από το σπίτι ή το νοσοκομείο και ερχόμαστε σε επαφή μαζί σας.</p></li>
      <li class="step"><span class="n">3</span><h3>Οργανώνουμε</h3><p>Μαζί αποφασίζουμε για ναό, κοιμητήριο, στολισμό και αγγελτήρια. Εμείς φροντίζουμε τα υπόλοιπα.</p></li>
      <li class="step"><span class="n">4</span><h3>Διεκπεραιώνουμε</h3><p>Αναλαμβάνουμε τα έγγραφα και την τελετή, ώστε εσείς να σταθείτε δίπλα στους δικούς σας.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      {sec_title("Περιοχές που εξυπηρετούμε")}
      <p class="lead">Το γραφείο μας βρίσκεται στη Φορμίωνος 233 στον Βύρωνα και εξυπηρετούμε σε όλη την Αττική και αναλαμβάνουμε τελετές σε όλη την Ελλάδα και μεταφορές από το εξωτερικό.</p>
    </div>
    <div class="map">
      <iframe src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Χάρτης: {BIZ['name']}"></iframe>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap narrow">
    <div class="section-head center">
      {sec_title("Συχνές ερωτήσεις", center=True)}
    </div>
    {faq_html(HOME_FAQ)}
  </div>
</section>
{cta_band()}
"""
HOME_TITLE = "Γραφείο Τελετών Βύρωνας · Σοφογιάννης · 210 7600 900"
HOME_DESC = "Γραφείο Τελετών Σοφογιάννης στον Βύρωνα από το 2003, Φορμίωνος 233. Κηδείες, αποτεφρώσεις, μνημόσυνα, μεταφορά σορού, διαδικαστικά. 24 ώρες το 24ωρο: 210 7600 900, 6944 14 58 44."
build_page("/", HOME_TITLE, HOME_DESC, None, home_body, [faq_ld(HOME_FAQ)])
PAGES.append(("/", "1.0"))

# ================================================================= ABOUT
about_body = page_hero([("Αρχική", "/"), ("Το Γραφείο", "/to-grafeio/")],
    "Το γραφείο",
    f"Από το 2003 στον Βύρωνα, με έναν άνθρωπο υπεύθυνο για κάθε οικογένεια. Αυτό που μας οδηγεί είναι απλό: σεβασμός στον άνθρωπο που φεύγει και στήριξη σε όσους μένουν.") + f"""
<section class="section">
  <div class="wrap split">
    <figure class="portrait">
      <div class="portrait-frame"><img src="/images/grafeio-vyronas.jpg" alt="Η πρόσοψη του Γραφείου Τελετών Σοφογιάννης στη Φορμίωνος 233, Βύρωνας" width="977" height="1200" loading="lazy" decoding="async" style="object-position:center 100%"></div>
      <figcaption><img src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="56" height="56"><span><strong>Το γραφείο μας</strong><small>{BIZ['street']} · {BIZ['city']}</small></span></figcaption>
    </figure>
    <div>
      {sec_title("Η ιστορία μας")}
      <p class="quote">«Αναλαμβάνουμε την οργάνωση και τη διεκπεραίωση κάθε τελετής, προσφέροντας στήριξη σε εσάς και την οικογένειά σας.»</p>
      <p>Ο Νικόλαος Ι. Σοφογιάννης ξεκίνησε το 2003, χωρίς οικογενειακή «κληρονομιά» στον χώρο, και έχτισε το γραφείο του βήμα βήμα, με δουλειά, συνέπεια και τη σύσταση από οικογένεια σε οικογένεια. Σήμερα, μετά από {YEARS} χρόνια, το Γραφείο Τελετών Σοφογιάννης στη Φορμίωνος 233 στον Βύρωνα συνεχίζει με τον ίδιο τρόπο. Από την πρώτη ημέρα, η φιλοσοφία μας ήταν απλή: κάθε οικογένεια που μας εμπιστεύεται τον αποχαιρετισμό ενός αγαπημένου της προσώπου αξίζει την ίδια φροντίδα που θα θέλαμε κι εμείς για τους δικούς μας ανθρώπους.</p>
      <p>Οργανώνουμε κάθε είδους τελετή: από μια απλή, ήσυχη εξόδιο ακολουθία μέχρι αποτεφρώσεις και μεταφορές σορού σε άλλη πόλη ή από το εξωτερικό. Ο υπεύθυνος του γραφείου είναι πάντα διαθέσιμος στο κινητό, 24 ώρες το 24ωρο.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head center">
      {sec_title("Πώς δουλεύουμε", center=True)}
    </div>
    <div class="values">
      <div class="value"><span class="ic">{I['heart']}</span><h3>Σεβασμός</h3><p>Στον άνθρωπο που έφυγε, στην πίστη και τις παραδόσεις της οικογένειας, στις επιθυμίες του καθενός.</p></div>
      <div class="value"><span class="ic">{I['shield']}</span><h3>Αξιοπρέπεια</h3><p>Κάθε τελετή οργανώνεται με την ίδια φροντίδα, ανεξάρτητα από το μέγεθος ή τον προϋπολογισμό.</p></div>
      <div class="value"><span class="ic">{I['hands']}</span><h3>Διακριτικότητα</h3><p>Είμαστε παρόντες όπου μας χρειάζεστε και αθόρυβοι όπου πρέπει. Η οικογένεια έρχεται πάντα πρώτη.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      {sec_title("Γιατί να μας επιλέξετε")}
      {check_list([f"{EXP_YEARS} χρόνια εμπειρίας στον χώρο, με δικό του γραφείο από το 2003", "Άμεση ανταπόκριση 24/7, ακόμη και σε αργίες", "Ένας υπεύθυνος για όλη τη διαδικασία, χωρίς μεσάζοντες", "Διαφάνεια στο κόστος και αναλυτική ενημέρωση", "Διεκπεραίωση όλων των εγγράφων της κηδείας", "Αποτεφρώσεις και μεταφορές σορού σε Ελλάδα και εξωτερικό", "Γνώση των ναών και των κοιμητηρίων της περιοχής"])}
      <div class="hero-actions">
        <a class="btn btn-primary" href="/ypiresies/">Οι υπηρεσίες μας {I['arrow']}</a>
        <a class="btn btn-ghost" href="/epikoinonia/">Επικοινωνία</a>
      </div>
    </div>
    {contact_card()}
  </div>
</section>
{cta_band()}
"""
build_page("/to-grafeio/", "Το Γραφείο · Γραφείο Τελετών Σοφογιάννης, Βύρωνας",
           "Γνωρίστε το Γραφείο Τελετών Σοφογιάννης στον Βύρωνα από το 2003, Φορμίωνος 233. Υπεύθυνος ο Νικόλαος Ι. Σοφογιάννης. Με σεβασμό και διακριτικότητα, 24 ώρες το 24ωρο.",
           [("Αρχική", "/"), ("Το Γραφείο", "/to-grafeio/")], about_body,
           [{"@type": "AboutPage", "url": url("/to-grafeio/"), "mainEntity": {"@id": url("/#funeralhome")}}])
PAGES.append(("/to-grafeio/", "0.8"))

# ================================================================= ΕΚΘΕΣΙΑΚΟΣ ΧΩΡΟΣ
# Φέρετρα ns-01 … ns-29: Τογρίδης ΛΤ1–ΛΤ6, ΛΤ30–ΛΤ52 (ns-XX-b.jpg = εικόνα λεπτομέρειας για hover)
COFFINS = sorted(f for f in os.listdir(os.path.join(ROOT, "images", "feretra")) if f.startswith("ns-") and not f.endswith("-b.jpg"))
def fimg(f):
    v = hashlib.md5(open(os.path.join(ROOT, "images", "feretra", f), "rb").read()).hexdigest()[:8]
    return f"/images/feretra/{f}?v={v}"
def coffin_card(n, f):
    b = f.replace(".jpg", "-b.jpg")
    alt = (f'<img class="alt" src="{fimg(b)}" alt="" width="800" height="600" loading="lazy" decoding="async">'
           if os.path.exists(os.path.join(ROOT, "images", "feretra", b)) else "")
    return f"""<figure class="coffin{' has-alt' if alt else ''}">
        <div class="coffin-img"><img src="{fimg(f)}" alt="Φέρετρο ΝΣ{n}" width="800" height="600" loading="lazy" decoding="async">{alt}</div>
        <figcaption><span>Φέρετρο</span><span class="ns-code"><img src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="26" height="26">ΝΣ{n}</span></figcaption>
      </figure>"""
showroom_body = page_hero([("Αρχική", "/"), ("Εκθεσιακός Χώρος", "/ekthesiakos-xoros/")],
    "Εκθεσιακός χώρος",
    "Δείτε τα φέρετρα που διαθέτουμε. Επιλέξτε το μοντέλο που σας ταιριάζει, καλέστε μας με τον κωδικό του και θα σας βοηθήσουμε να επιλέξετε με ηρεμία.") + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      {sec_title("Φέρετρα")}
      <p class="lead">Για κάθε μοντέλο ρωτήστε μας με τον κωδικό του (π.χ. ΝΣ1) για διαθεσιμότητα και τιμή.</p>
    </div>
    <div class="coffins">{"".join(coffin_card(n, f) for n, f in enumerate(COFFINS, 1))}
    </div>
  </div>
</section>
{cta_band("Σας ενδιαφέρει κάποιο μοντέλο;", "Καλέστε μας με τον κωδικό του φερέτρου. Θα σας ενημερώσουμε για διαθεσιμότητα και τιμή και θα σας εξηγήσουμε όλες τις επιλογές με ηρεμία.")}
"""
build_page("/ekthesiakos-xoros/", "Εκθεσιακός Χώρος · Φέρετρα · Γραφείο Τελετών Σοφογιάννης, Βύρωνας",
           "Δείτε τα φέρετρα του Γραφείου Τελετών Σοφογιάννης στον Βύρωνα. Μεγάλη γκάμα σε ξύλο και αποχρώσεις, με σαφή ενημέρωση για διαθεσιμότητα και τιμή. Τηλ. 210 7600 900.",
           [("Αρχική", "/"), ("Εκθεσιακός Χώρος", "/ekthesiakos-xoros/")], showroom_body,
           [{"@type": "CollectionPage", "url": url("/ekthesiakos-xoros/"), "about": {"@id": url("/#funeralhome")}}])
PAGES.append(("/ekthesiakos-xoros/", "0.8"))

# ================================================================= SERVICES INDEX
svc_index_body = page_hero([("Αρχική", "/"), ("Υπηρεσίες", "/ypiresies/")],
    "Υπηρεσίες",
    "Κηδείες, αποτεφρώσεις, μνημόσυνα, μεταφορά σορού και διεκπεραίωση της γραφειοκρατίας. Ό,τι χρειαστεί η οικογένεια, το αναλαμβάνουμε με συνέπεια και σεβασμό.") + f"""
<section class="section">
  <div class="wrap">
    {service_cards()}
  </div>
</section>
<section class="section alt">
  <div class="wrap split">
    <div>
      {sec_title("Τι μπορούμε να αναλάβουμε")}
      <p class="lead">Κάθε τελετή προσαρμόζεται στις επιθυμίες της οικογένειας. Ενδεικτικά, μπορούμε να αναλάβουμε:</p>
    </div>
    <div>
      {check_list(["Παραλαβή σορού 24/7", "Φέρετρα & στολισμός", "Στεφάνια & ανθοστολισμοί", "Αγγελτήρια & αγγελίες", "Συνεννόηση με ναό & ιερέα", "Κοιμητήρια & ταφή", "Νεκροφόρα & μεταφορές", "Καφές παρηγοριάς", "Κόλλυβα & μνημόσυνα", "Όλα τα έγγραφα"], two=True)}
    </div>
  </div>
</section>
{cta_band()}
"""
build_page("/ypiresies/", "Υπηρεσίες Γραφείου Τελετών · Κηδείες, Αποτεφρώσεις, Μνημόσυνα · Βύρωνας",
           "Υπηρεσίες του Γραφείου Τελετών Σοφογιάννης στον Βύρωνα: κηδείες, αποτεφρώσεις, μνημόσυνα, ανθοστολισμός, μεταφορά σορού, διαδικασίες. Τηλ. 210 7600 900.",
           [("Αρχική", "/"), ("Υπηρεσίες", "/ypiresies/")], svc_index_body,
           [{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["title"], "url": url("/ypiresies/%s/" % s["slug"])} for i, s in enumerate(SERVICES)]}],
           active="/ypiresies/")
PAGES.append(("/ypiresies/", "0.9"))

# ================================================================= SERVICE PAGES
def features(items):
    return '<div class="feature-grid">' + "".join(
        f'<div class="feature"><span class="ic">{I[ic]}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in items) + "</div>"

def photo(src, alt, w, h, pos="center"):
    return (f'<figure class="photo"><img src="/images/{src}" alt="{esc(alt)}" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" style="object-position:{pos}"></figure>')

def carousel(items, label):
    """Slider φωτογραφιών με βελάκια (scroll-snap, χωρίς βιβλιοθήκες)."""
    slides = "".join(
        f'<figure class="slide"><img src="/images/{src}?v=2" alt="{esc(alt)}" loading="lazy" decoding="async"></figure>'
        for src, alt in items)
    return f"""<div class="carousel" role="region" aria-roledescription="carousel" aria-label="{esc(label)}">
  <div class="car-track" tabindex="0">{slides}</div>
  <button class="car-btn prev" type="button" aria-label="Προηγούμενη φωτογραφία"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
  <button class="car-btn next" type="button" aria-label="Επόμενη φωτογραφία"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
  <div class="car-dots" aria-hidden="true"></div>
</div>"""

STEFANIA = [
    ("stefani-1.jpg", "Στεφάνι με λευκά τριαντάφυλλα, λίλιουμ και πράσινο φύλλωμα"),
    ("stefani-2.jpg", "Στρογγυλό στεφάνι από λευκά χρυσάνθεμα και τριαντάφυλλα"),
    ("stefani-3.jpg", "Δύο στρογγυλά στεφάνια με λευκά τριαντάφυλλα"),
    ("stefani-4.jpg", "Στεφάνι με λευκά τριαντάφυλλα και κορδέλα συλλυπητηρίων"),
    ("stefani-5.jpg", "Στεφάνι σε σχήμα καρδιάς από λευκά τριαντάφυλλα"),
    ("stefani-6.jpg", "Ανθοσύνθεση με λευκά τριαντάφυλλα πάνω στο φέρετρο"),
    ("stefani-7.jpg", "Στεφάνι καρδιά με λευκά τριαντάφυλλα και γυψοφίλη σε ναό"),
]

def note(html):
    return f'<div class="note">{I["info"]}<p>{html}</p></div>'

SVC_CONTENT = {}

SVC_CONTENT["kideies"] = {
    "body": f"""
<h2>Τι αναλαμβάνουμε</h2>
<p>Η οργάνωση μιας κηδείας περιλαμβάνει πολλές αποφάσεις και πρακτικά ζητήματα που πρέπει να διευθετηθούν σε λίγες ώρες. Σας καθοδηγούμε με ηρεμία και αναλαμβάνουμε την εκτέλεση, ώστε να μην χρειαστεί να ασχοληθείτε με τίποτα άλλο.</p>
{features([
    ("car", "Παραλαβή σορού", "Από οικία, νοσοκομείο ή κλινική, οποιαδήποτε ώρα, με σεβασμό και διακριτικότητα."),
    ("cross", "Ναός & ιερέας", "Συνεννόηση με την ενορία για την ώρα της εξοδίου ακολουθίας, τους ιερείς και τους ψάλτες."),
    ("map", "Κοιμητήριο", "Επικοινωνία με το κοιμητήριο, κράτηση ή χρήση οικογενειακού τάφου, οργάνωση ταφής."),
    ("flower", "Φέρετρο & στολισμός", "Μεγάλη γκάμα φερέτρων (δείτε τον <a href='/ekthesiakos-xoros/'>εκθεσιακό χώρο</a>) και στολισμός ναού και φερέτρου με λουλούδια της επιλογής σας."),
    ("news", "Αγγελτήρια", "Εκτύπωση και τοποθέτηση κηδειόχαρτων, καθώς και καταχώριση αγγελίας σε εφημερίδα."),
    ("coffee", "Καφές παρηγοριάς", "Οργάνωση του καφέ της παρηγοριάς μετά την τελετή, σε χώρο κοντά στον ναό."),
])}
<h2>Πώς οργανώνεται μια κηδεία</h2>
<p>Αμέσως μόλις μας καλέσετε, ερχόμαστε σε επαφή μαζί σας και κανονίζουμε την παραλαβή. Στη συνέχεια συναντιόμαστε, στο γραφείο μας στον Βύρωνα ή όπου σας εξυπηρετεί, για να συζητήσουμε τις επιθυμίες σας: τον ναό, το κοιμητήριο, το φέρετρο, τον στολισμό και τα αγγελτήρια.</p>
<p>Σας δίνουμε από την αρχή μια σαφή εικόνα του κόστους, χωρίς εκπλήξεις. Από εκεί και πέρα αναλαμβάνουμε εμείς τον συντονισμό με τον ναό, το κοιμητήριο, τους ανθοπώλες και τις υπηρεσίες, και διεκπεραιώνουμε τα <a href="/ypiresies/diadikasies/">απαραίτητα έγγραφα</a>.</p>
<h2>Κηδεία σε άλλη πόλη ή στο χωριό</h2>
<p>Πολλές οικογένειες επιθυμούν η ταφή να γίνει στον τόπο καταγωγής. Αναλαμβάνουμε τη <a href="/ypiresies/metafora-sorou/">μεταφορά της σορού</a> σε οποιοδήποτε σημείο της Ελλάδας και τον συντονισμό με την τοπική ενορία και το κοιμητήριο.</p>
{note("Αν ο θάνατος συνέβη στο σπίτι, χρειάζεται πρώτα ιατρός για να εκδώσει την ιατρική βεβαίωση θανάτου. Αν δεν γνωρίζετε ποιον να καλέσετε, τηλεφωνήστε μας και θα σας καθοδηγήσουμε.")}
""",
    "faq": [
        ("Πόσο γρήγορα μπορεί να γίνει η κηδεία;", "Συνήθως η κηδεία πραγματοποιείται εντός μίας έως τριών ημερών, ανάλογα με τη διαθεσιμότητα του ναού και του κοιμητηρίου και τις επιθυμίες της οικογένειας. Σας ενημερώνουμε αμέσως για τις διαθέσιμες επιλογές."),
        ("Μπορώ να επιλέξω ναό και κοιμητήριο;", "Ναι, εσείς επιλέγετε. Εμείς επικοινωνούμε με την ενορία και το κοιμητήριο και κανονίζουμε ημέρα και ώρα."),
        ("Πώς γίνεται η πληρωμή;", "Σας δίνουμε αναλυτική προσφορά πριν από οποιαδήποτε δέσμευση. Σας ενημερώνουμε επίσης για το επίδομα εξόδων κηδείας από τον ασφαλιστικό φορέα, για το οποίο σας βοηθάμε με τα δικαιολογητικά."),
        ("Οργανώνετε κηδείες και για άλλα δόγματα;", "Επικοινωνήστε μαζί μας για να συζητήσουμε τις ανάγκες σας. Σεβόμαστε τις θρησκευτικές πεποιθήσεις κάθε οικογένειας και οργανώνουμε και πολιτικές τελετές."),
    ],
}

SVC_CONTENT["apotefroseis"] = {
    "body": f"""
<h2>Η αποτέφρωση στην Ελλάδα</h2>
<p>Η αποτέφρωση νεκρών προβλέπεται από την ελληνική νομοθεσία και πραγματοποιείται σε αδειοδοτημένο κέντρο αποτέφρωσης. Μπορεί να γίνει εφόσον το είχε επιθυμήσει ο ίδιος ο εκλιπών ή, σε κάθε άλλη περίπτωση, κατόπιν επιλογής των οικείων του, όπως ορίζει ο νόμος.</p>
<p>Πριν από την αποτέφρωση μπορεί να τελεστεί κανονικά θρησκευτική ή πολιτική τελετή αποχαιρετισμού, ώστε η οικογένεια και οι φίλοι να έχουν την ευκαιρία να πουν το τελευταίο αντίο.</p>
{features([
    ("doc", "Δικαιολογητικά", "Συγκεντρώνουμε και υποβάλλουμε τα έγγραφα που απαιτούνται για την αποτέφρωση."),
    ("cross", "Τελετή αποχαιρετισμού", "Οργάνωση θρησκευτικής ή πολιτικής τελετής πριν από την αποτέφρωση."),
    ("car", "Μεταφορά", "Μεταφορά της σορού στο κέντρο αποτέφρωσης με ειδικό όχημα."),
    ("urn", "Τεφροδόχος", "Επιλογή τεφροδόχου και παράδοσή της στην οικογένεια ή στον χώρο φύλαξης."),
])}
<h2>Πώς ξεκινάμε</h2>
<p>Καλέστε μας και θα σας εξηγήσουμε τα βήματα και τα δικαιολογητικά που χρειάζονται για τη δική σας περίπτωση. Αναλαμβάνουμε την επικοινωνία με το κέντρο αποτέφρωσης, τον προγραμματισμό και τη μεταφορά, και σας ενημερώνουμε σε κάθε στάδιο.</p>
{note("Αν ο εκλιπών είχε εκφράσει γραπτώς την επιθυμία του για αποτέφρωση, φέρτε μαζί σας το σχετικό έγγραφο. Αν όχι, δεν πειράζει: θα σας εξηγήσουμε τι προβλέπεται.")}
""",
    "faq": [
        ("Επιτρέπεται θρησκευτική τελετή πριν από την αποτέφρωση;", "Ναι. Μπορεί να πραγματοποιηθεί τελετή αποχαιρετισμού πριν από τη μεταφορά στο κέντρο αποτέφρωσης. Σας βοηθάμε να βρείτε την κατάλληλη λύση για την οικογένειά σας."),
        ("Τι γίνεται με την τεφροδόχο;", "Η τεφροδόχος παραδίδεται στην οικογένεια ή τοποθετείται σε χώρο φύλαξης, σύμφωνα με τις επιθυμίες σας και όσα προβλέπονται. Διαθέτουμε τεφροδόχους σε διάφορα σχέδια."),
        ("Πόσο χρόνο χρειάζεται η διαδικασία;", "Ο χρόνος εξαρτάται από τα δικαιολογητικά και τη διαθεσιμότητα του κέντρου αποτέφρωσης. Θα σας δώσουμε ακριβές χρονοδιάγραμμα μόλις επικοινωνήσουμε."),
    ],
}

SVC_CONTENT["mnimosyna"] = {
    "body": f"""
<h2>Μνημόσυνα και τρισάγια</h2>
<p>Κατά την ορθόδοξη παράδοση, η μνήμη του εκλιπόντος τιμάται με μνημόσυνα σε συγκεκριμένες ημέρες: το τριήμερο, τα εννιάμερα, τα σαράντα, τους τρεις και τους έξι μήνες και τα ετήσια. Οργανώνουμε κάθε μνημόσυνο με την ίδια φροντίδα που οργανώσαμε και την κηδεία.</p>
{features([
    ("cross", "Συνεννόηση με τον ναό", "Κλείνουμε ημέρα και ώρα με την ενορία της επιλογής σας."),
    ("flower", "Κόλλυβα", "Παραδοσιακά κόλλυβα, σε δίσκο και σε ατομικά σακουλάκια, στολισμένα όπως επιθυμείτε."),
    ("news", "Αγγελίες & προσκλήσεις", "Εκτύπωση προσκλήσεων και καταχώριση αγγελίας μνημοσύνου."),
    ("coffee", "Κέρασμα & καφές", "Οργάνωση κεράσματος ή καφέ μετά το μνημόσυνο."),
])}
{photo("mnimosyno-naos.jpg", "Ναός στολισμένος για μνημόσυνο με συνθέσεις από λευκά τριαντάφυλλα και κεριά", 1400, 1050)}
<h2>Οργάνωση με μία μόνο κλήση</h2>
<p>Μας λέτε την ημερομηνία και τον ναό, και αναλαμβάνουμε τα υπόλοιπα: από τα κόλλυβα και τα κεριά μέχρι τις αγγελίες και τον χώρο για τον καφέ. Μπορούμε επίσης να σας υπενθυμίσουμε τις ημερομηνίες των επόμενων μνημοσύνων.</p>
""",
    "faq": [
        ("Πότε γίνονται τα μνημόσυνα;", "Συνήθως στις 3 και 9 ημέρες, στις 40 ημέρες, στους 3 και 6 μήνες, και στον 1 χρόνο από τον θάνατο. Τα μνημόσυνα τελούνται συνήθως Σάββατο ή Κυριακή μετά τη Θεία Λειτουργία."),
        ("Μπορείτε να αναλάβετε μόνο τα κόλλυβα;", "Ναι. Μπορείτε να μας αναθέσετε όλη την οργάνωση ή μόνο όσα χρειάζεστε, όπως τα κόλλυβα ή την αγγελία."),
        ("Οργανώνετε μνημόσυνα σε ναούς εκτός Βύρωνα;", "Φυσικά. Οργανώνουμε μνημόσυνα σε ναούς σε όλη την Αττική."),
    ],
}

SVC_CONTENT["anthostolismos"] = {
    "body": f"""
<h2>Στολισμός με φροντίδα σε κάθε λεπτομέρεια</h2>
<p>Συνεργαζόμαστε με ανθοπώλες που εμπιστευόμαστε και αναλαμβάνουμε όλο τον ανθοστολισμό της τελετής. Μαζί σας επιλέγουμε λουλούδια, χρώματα και ύφος, από έναν λιτό και ήρεμο στολισμό μέχρι πιο πλούσιες συνθέσεις, πάντα σύμφωνα με τις επιθυμίες σας και τον προϋπολογισμό σας.</p>
{features([
    ("cross", "Στολισμός ναού", "Συνθέσεις σε κηροπήγια και βάσεις, στολισμός του διαδρόμου και του χώρου γύρω από το φέρετρο."),
    ("flower", "Στολισμός φερέτρου", "Ανθοσύνθεση για το καπάκι του φερέτρου, με τα λουλούδια που αγαπούσε ο άνθρωπός σας."),
    ("heart", "Στεφάνια", "Στεφάνια σε διάφορα μεγέθη και χρώματα, με κορδέλα και προσωπική αφιέρωση."),
    ("candle", "Μνημόσυνα", "Ανθοστολισμός για μνημόσυνα, καθώς και λουλούδια για τον τάφο."),
])}
<h2>Από τη δουλειά μας</h2>
<p>Μερικά από τα στεφάνια και τους στολισμούς που έχουμε επιμεληθεί.</p>
{carousel(STEFANIA, "Φωτογραφίες από στεφάνια και ανθοστολισμούς")}
<h2>Στεφάνια για συγγενείς, φίλους και συναδέλφους</h2>
<p>Πολλοί θέλουν να στείλουν στεφάνι αλλά δεν γνωρίζουν σε ποιον να απευθυνθούν. Μπορούν να επικοινωνήσουν απευθείας μαζί μας: κανονίζουμε το στεφάνι με την αφιέρωση που επιθυμούν και φροντίζουμε να βρίσκεται στον ναό εγκαίρως.</p>
{note(f"Για στεφάνι σε κηδεία που οργανώνουμε εμείς, καλέστε μας στο {BIZ['phone']} με το όνομα του εκλιπόντος και την αφιέρωση που θέλετε να γραφτεί στην κορδέλα.")}
""",
    "faq": [
        ("Μπορώ να επιλέξω τα λουλούδια;", "Ναι. Σας προτείνουμε επιλογές, αλλά εσείς αποφασίζετε για τα λουλούδια, τα χρώματα και το μέγεθος του στολισμού."),
        ("Πώς στέλνω στεφάνι σε μια κηδεία;", "Καλέστε μας με το όνομα του εκλιπόντος και την αφιέρωση για την κορδέλα. Αναλαμβάνουμε την παραγγελία και την παράδοση στον ναό."),
        ("Αναλαμβάνετε στολισμό και για μνημόσυνα;", "Ναι. Στολίζουμε τον ναό για μνημόσυνα και μπορούμε να φροντίσουμε και λουλούδια για τον τάφο."),
    ],
}

SVC_CONTENT["metafora-sorou"] = {
    "body": f"""
<h2>Μεταφορά σορού εντός Ελλάδας</h2>
<p>Οργανώνουμε μεταφορά σορού από την Αττική σε οποιαδήποτε πόλη ή χωριό της Ελλάδας, οδικώς ή αεροπορικώς, και συντονίζουμε την τελετή με την τοπική ενορία και το κοιμητήριο, ώστε η οικογένεια να μη χρειαστεί να κανονίσει τίποτα από απόσταση.</p>
{features([
    ("globe", "Συνεργάτες στο εξωτερικό", "Συντονισμός με γραφεία τελετών και αρχές της χώρας όπου συνέβη ο θάνατος."),
    ("doc", "Έγγραφα & προξενεία", "Συγκέντρωση και επικύρωση των εγγράφων που απαιτούνται για τη μεταφορά."),
    ("plane", "Αεροπορική μεταφορά", "Μεταφορά της σορού σε ειδικό φέρετρο, σύμφωνα με τους διεθνείς κανονισμούς."),
    ("car", "Παραλαβή & τελετή", "Παραλαβή από το αεροδρόμιο και οργάνωση της κηδείας όπου επιθυμείτε."),
])}
<h2>Επαναπατρισμός από το εξωτερικό</h2>
<p>Ο επαναπατρισμός σορού απαιτεί συντονισμό με αρχές, προξενεία, αεροπορικές εταιρείες και συνεργάτες στο εξωτερικό. Αναλαμβάνουμε όλη τη διαδικασία, από την πρώτη επικοινωνία μέχρι την παραλαβή στο αεροδρόμιο και την τελετή.</p>
<h2>Από την Ελλάδα προς το εξωτερικό</h2>
<p>Αναλαμβάνουμε επίσης τη μεταφορά σορού από την Ελλάδα σε άλλη χώρα, για οικογένειες που επιθυμούν η ταφή να γίνει στον τόπο καταγωγής του εκλιπόντος. Φροντίζουμε για τα πιστοποιητικά, την προετοιμασία της σορού και την αεροπορική μεταφορά.</p>
{note("Σε περίπτωση θανάτου στο εξωτερικό, καλέστε μας όσο το δυνατόν νωρίτερα. Η έγκαιρη επικοινωνία με τις αρχές της χώρας επιταχύνει σημαντικά τη διαδικασία.")}
""",
    "faq": [
        ("Πόσο χρόνο χρειάζεται ο επαναπατρισμός;", "Εξαρτάται από τη χώρα και τις διαδικασίες των τοπικών αρχών. Συνήθως απαιτούνται μερικές ημέρες. Σας κρατάμε ενήμερους σε κάθε στάδιο."),
        ("Ποια έγγραφα χρειάζονται;", "Συνήθως η πράξη ή το πιστοποιητικό θανάτου, η άδεια μεταφοράς σορού και τα έγγραφα του προξενείου. Τα ακριβή έγγραφα διαφέρουν ανά χώρα και τα συγκεντρώνουμε εμείς."),
        ("Καλύπτεται το κόστος από ασφάλεια;", "Ορισμένα ταξιδιωτικά ή ιδιωτικά ασφαλιστήρια καλύπτουν τον επαναπατρισμό. Ελέγξτε το συμβόλαιό σας και θα συνεργαστούμε με την ασφαλιστική εταιρεία."),
    ],
}

SVC_CONTENT["diadikasies"] = {
    "body": f"""
<h2>Τα έγγραφα της κηδείας</h2>
<p>Μετά από έναν θάνατο απαιτείται μια σειρά από έγγραφα και ενέργειες σε δημόσιες υπηρεσίες. Γνωρίζουμε τις διαδικασίες και τις διεκπεραιώνουμε για λογαριασμό σας, ώστε να μη χρειαστεί να επισκεφθείτε υπηρεσίες σε μια τόσο δύσκολη στιγμή.</p>
{features([
    ("hospital", "Ιατρική βεβαίωση θανάτου", "Σας καθοδηγούμε για την έκδοσή της, είτε ο θάνατος συνέβη στο σπίτι είτε σε νοσοκομείο."),
    ("doc", "Ληξιαρχική πράξη θανάτου", "Δήλωση του θανάτου στο ληξιαρχείο και παραλαβή αντιγράφων."),
    ("map", "Άδεια ταφής", "Έκδοση της άδειας ταφής και συνεννόηση με το κοιμητήριο."),
    ("shield", "Έξοδα κηδείας", "Βοήθεια με τα δικαιολογητικά για το επίδομα εξόδων κηδείας από τον ασφαλιστικό φορέα (e-ΕΦΚΑ)."),
])}
<h2>Τι ακολουθεί μετά την κηδεία</h2>
<p>Μετά την τελετή, η οικογένεια συχνά χρειάζεται να προχωρήσει σε ενέργειες όπως η διακοπή της σύνταξης, η αίτηση για σύνταξη χηρείας, ή η ενημέρωση τραπεζών και υπηρεσιών κοινής ωφέλειας. Σας εξηγούμε απλά ποια έγγραφα χρειάζεστε και σε ποια υπηρεσία να απευθυνθείτε.</p>
{check_list(["Αντίγραφα ληξιαρχικής πράξης θανάτου για τις υπηρεσίες", "Καθοδήγηση για σύνταξη χηρείας και ασφαλιστικά", "Δικαιολογητικά για επίδομα εξόδων κηδείας", "Πληροφορίες για πιστοποιητικό εγγυτέρων συγγενών"])}
{note("Κρατήστε πρόχειρα την αστυνομική ταυτότητα και τον ΑΜΚΑ του εκλιπόντος. Είναι τα πρώτα στοιχεία που θα χρειαστούμε.")}
""",
    "faq": [
        ("Ποια έγγραφα χρειάζεται να φέρω;", "Αρχικά την αστυνομική ταυτότητα του εκλιπόντος, τον ΑΜΚΑ και, αν υπάρχει, το βιβλιάριο ή τα στοιχεία ασφάλισης. Τα υπόλοιπα τα αναλαμβάνουμε εμείς."),
        ("Δικαιούμαι επίδομα εξόδων κηδείας;", "Αν ο εκλιπών ήταν ασφαλισμένος ή συνταξιούχος, οι οικείοι που κατέβαλαν τα έξοδα μπορεί να δικαιούνται επίδομα από τον e-ΕΦΚΑ. Σας ενημερώνουμε και σας βοηθάμε με τα δικαιολογητικά."),
        ("Πού εκδίδεται η ληξιαρχική πράξη θανάτου;", "Στο ληξιαρχείο του δήμου όπου συνέβη ο θάνατος. Τη δήλωση του θανάτου την αναλαμβάνουμε εμείς."),
    ],
}

def side_call(title="Είμαστε εδώ 24/7", text="Καλέστε μας τώρα. Θα σας εξηγήσουμε με ηρεμία τι χρειάζεται να γίνει."):
    return f"""<div class="side-card dark">
        <h3>{title}</h3>
        <p>{text}</p>
        <a class="btn btn-light" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone']}</a>
        <a class="btn btn-outline-light" href="tel:{BIZ['phone2_tel']}">{I['phone']}{BIZ['phone2']}</a>
        <a class="btn btn-outline-light" href="tel:{BIZ['mobile_tel']}">{I['mobile']}{BIZ['mobile']}</a>
      </div>"""

CUR = ' aria-current="page"'
for s in SERVICES:
    path = "/ypiresies/%s/" % s["slug"]
    c = SVC_CONTENT[s["slug"]]
    crumbs = [("Αρχική", "/"), ("Υπηρεσίες", "/ypiresies/"), (s["title"], path)]
    side_links = "".join(
        f'<li><a href="/ypiresies/{o["slug"]}/"{CUR if o is s else ""}>{o["title"]}{I["arrow"]}</a></li>' for o in SERVICES)
    others = [o for o in SERVICES if o is not s][:3]
    body = page_hero(crumbs, s["h1"], s["lead"]) + f"""
<section class="section">
  <div class="wrap content-grid">
    <article class="prose">
      {c['body']}
      <h2>Συχνές ερωτήσεις</h2>
      {faq_html(c['faq'])}
    </article>
    <aside class="sidebar">
      {side_call()}
      <div class="side-card">
        <h3>Υπηρεσίες</h3>
        <ul class="side-links">{side_links}</ul>
      </div>
      <div class="side-card">
        <h3>Το γραφείο μας</h3>
        <p>{BIZ['street']}, {BIZ['city']}<br><a href="{MAPS_LINK}" target="_blank" rel="noopener">Οδηγίες στον χάρτη →</a></p>
      </div>
    </aside>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      {sec_title("Άλλες υπηρεσίες")}
      <a class="btn btn-ghost" href="/ypiresies/">Όλες οι υπηρεσίες {I['arrow']}</a>
    </div>
    {service_cards(others).replace('class="services-grid"', 'class="services-grid three"')}
  </div>
</section>
{cta_band()}
"""
    service_ld = {"@type": "Service", "name": s["title"], "serviceType": s["title"], "description": s["desc"], "url": url(path),
                  "provider": {"@id": url("/#funeralhome")}, "areaServed": {"@type": "AdministrativeArea", "name": "Αττική"}}
    build_page(path, s["seo_title"], s["desc"], crumbs, body, [service_ld, faq_ld(c["faq"])], active=path)
    PAGES.append((path, "0.8"))

# ================================================================= ΤΙ ΚΑΝΩ ΤΩΡΑ
def tl(items):
    return '<ol class="timeline">' + "".join(
        f'<li class="{"call" if call else ""}"><span class="n">{i + 1}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d, call) in enumerate(items)) + "</ol>"

CALL = f'<a href="tel:{BIZ["phone_tel"]}">{BIZ["phone"]}</a> ή στο κινητό <a href="tel:{BIZ["mobile_tel"]}">{BIZ["mobile"]}</a>'
guide_home = tl([
    ("Διατηρήστε την ψυχραιμία σας", "Δεν χρειάζεται να βιαστείτε. Πάρτε λίγο χρόνο με τον άνθρωπό σας και με την οικογένεια.", False),
    ("Καλέστε ιατρό", "Χρειάζεται ιατρός (π.χ. ο θεράπων ιατρός ή εφημερεύων ιατρός) για να διαπιστώσει τον θάνατο και να εκδώσει την ιατρική βεβαίωση θανάτου. Αν δεν γνωρίζετε ποιον να καλέσετε, μας λέτε και σας βοηθάμε.", False),
    ("Καλέστε μας", f"Στο {CALL}, οποιαδήποτε ώρα. Θα έρθουμε για την παραλαβή και θα σας εξηγήσουμε τα επόμενα βήματα.", True),
    ("Ετοιμάστε τα βασικά στοιχεία", "Αστυνομική ταυτότητα και ΑΜΚΑ του εκλιπόντος. Αν υπάρχουν επιθυμίες του για την τελετή (ναός, κοιμητήριο, αποτέφρωση), ενημερώστε μας.", False),
    ("Αφήστε τα υπόλοιπα σε εμάς", "Συζητάμε μαζί σας τις λεπτομέρειες της τελετής και αναλαμβάνουμε ναό, κοιμητήριο, αγγελτήρια και έγγραφα.", False),
])
guide_hosp = tl([
    ("Ενημερωθείτε από το νοσοκομείο", "Το ιατρικό προσωπικό του νοσοκομείου εκδίδει την ιατρική βεβαίωση θανάτου.", False),
    ("Καλέστε μας", f"Στο {CALL}. Επικοινωνούμε εμείς με το νοσοκομείο και αναλαμβάνουμε την παραλαβή της σορού.", True),
    ("Παραλάβετε τα προσωπικά αντικείμενα", "Αν σας ζητηθεί, παραλάβετε τα προσωπικά αντικείμενα του εκλιπόντος από το νοσοκομείο.", False),
    ("Συναντηθείτε μαζί μας", "Στο γραφείο μας στη Φορμίωνος 233 στον Βύρωνα ή όπου σας εξυπηρετεί, για να οργανώσουμε μαζί την τελετή.", False),
])
guide_abroad = tl([
    ("Καλέστε μας το συντομότερο", f"Στο {CALL}. Όσο νωρίτερα ξεκινήσει η διαδικασία, τόσο πιο γρήγορα ολοκληρώνεται ο επαναπατρισμός.", True),
    ("Ενημερώστε το ελληνικό προξενείο", "Η ελληνική πρεσβεία ή το προξενείο της χώρας μπορεί να βοηθήσει με τα έγγραφα. Συντονιζόμαστε κι εμείς μαζί τους.", False),
    ("Ελέγξτε την ασφάλιση", "Αν υπάρχει ταξιδιωτική ή ιδιωτική ασφάλιση, ενημερώστε την ασφαλιστική εταιρεία. Μπορεί να καλύπτει τον επαναπατρισμό.", False),
    ("Αναλαμβάνουμε τη μεταφορά", "Συντονίζουμε τα έγγραφα, την αεροπορική μεταφορά, την παραλαβή στην Ελλάδα και την τελετή.", False),
])
GUIDE_FAQ = [
    ("Χρειάζεται να καλέσω την αστυνομία;", "Όχι σε περίπτωση φυσικού θανάτου με ιατρική βεβαίωση. Αν ο θάνατος είναι αιφνίδιος ή από άγνωστη αιτία, μπορεί να απαιτηθεί ενημέρωση των αρχών και ιατροδικαστική εξέταση. Καλέστε μας και θα σας καθοδηγήσουμε."),
    ("Τι γίνεται αν ο θάνατος συμβεί νύχτα ή αργία;", f"Καλέστε μας στο κινητό {BIZ['mobile']}. Είμαστε διαθέσιμοι 24 ώρες το 24ωρο, κάθε ημέρα του χρόνου."),
    ("Πρέπει να αποφασίσω αμέσως για την κηδεία;", "Όχι. Αφού γίνει η παραλαβή, έχετε τον χρόνο να συζητήσετε με την οικογένεια. Θα σας εξηγήσουμε όλες τις επιλογές με ηρεμία."),
]
guide_body = page_hero([("Αρχική", "/"), ("Τι κάνω τώρα", "/ti-kano-tora/")],
    "Τι κάνω τώρα;",
    "Ένας απλός οδηγός για τα πρώτα βήματα μετά από μια απώλεια. Αν δεν είστε σίγουροι για οτιδήποτε, καλέστε μας: είμαστε εδώ 24 ώρες το 24ωρο.") + f"""
<section class="section">
  <div class="wrap content-grid">
    <div>
      <div class="guide-tabs" role="tablist" aria-label="Πού συνέβη ο θάνατος">
        <button role="tab" aria-selected="true" aria-controls="g-home" id="t-home">Στο σπίτι</button>
        <button role="tab" aria-selected="false" aria-controls="g-hosp" id="t-hosp">Σε νοσοκομείο</button>
        <button role="tab" aria-selected="false" aria-controls="g-abroad" id="t-abroad">Στο εξωτερικό</button>
      </div>
      <div class="guide-panel" id="g-home" role="tabpanel" aria-labelledby="t-home">{guide_home}</div>
      <div class="guide-panel" id="g-hosp" role="tabpanel" aria-labelledby="t-hosp" hidden>{guide_hosp}</div>
      <div class="guide-panel" id="g-abroad" role="tabpanel" aria-labelledby="t-abroad" hidden>{guide_abroad}</div>
      <div class="prose">
        <h2>Συχνές ερωτήσεις</h2>
        {faq_html(GUIDE_FAQ)}
      </div>
    </div>
    <aside class="sidebar">
      {side_call("Καλέστε μας τώρα", "Οποιαδήποτε ώρα, ημέρα ή νύχτα. Θα μιλήσετε απευθείας με τον υπεύθυνο.")}
      <div class="side-card">
        <h3>Έχετε έτοιμα</h3>
        {check_list(["Αστυνομική ταυτότητα του εκλιπόντος", "ΑΜΚΑ", "Ιατρική βεβαίωση θανάτου", "Στοιχεία ασφαλιστικού φορέα"])}
      </div>
    </aside>
  </div>
</section>
{cta_band()}
"""
build_page("/ti-kano-tora/", "Τι Κάνω Όταν Πεθάνει Κάποιος · Οδηγός Πρώτων Βημάτων · Σοφογιάννης",
           "Τι κάνω όταν συμβεί ένας θάνατος στο σπίτι, σε νοσοκομείο ή στο εξωτερικό; Απλός οδηγός από το Γραφείο Τελετών Σοφογιάννης, Βύρωνας. Τηλ. 210 7600 900.",
           [("Αρχική", "/"), ("Τι κάνω τώρα", "/ti-kano-tora/")], guide_body,
           [faq_ld(GUIDE_FAQ), {"@type": "HowTo", "name": "Τι κάνω όταν συμβεί θάνατος στο σπίτι", "step": [
               {"@type": "HowToStep", "position": 1, "name": "Καλέστε ιατρό", "text": "Ιατρός διαπιστώνει τον θάνατο και εκδίδει την ιατρική βεβαίωση θανάτου."},
               {"@type": "HowToStep", "position": 2, "name": "Καλέστε το γραφείο τελετών", "text": "Καλέστε στο 210 7600 900 ή στο 6944 14 58 44 για την παραλαβή και τα επόμενα βήματα."},
               {"@type": "HowToStep", "position": 3, "name": "Ετοιμάστε τα στοιχεία", "text": "Αστυνομική ταυτότητα και ΑΜΚΑ του εκλιπόντος."},
               {"@type": "HowToStep", "position": 4, "name": "Οργάνωση τελετής", "text": "Το γραφείο τελετών αναλαμβάνει ναό, κοιμητήριο, αγγελτήρια και έγγραφα."}]}])
PAGES.append(("/ti-kano-tora/", "0.8"))

# ================================================================= CONTACT
contact_body = page_hero([("Αρχική", "/"), ("Επικοινωνία", "/epikoinonia/")],
    "Επικοινωνία",
    "Για άμεση εξυπηρέτηση προτιμήστε το τηλέφωνο. Στο κινητό μας βρίσκετε 24 ώρες το 24ωρο. Για οτιδήποτε άλλο, στείλτε μας email ή επισκεφθείτε μας στο γραφείο.", actions=False) + f"""
<section class="section">
  <div class="wrap contact-layout">
    <div class="contact-cards">
      <a class="contact-card" href="tel:{BIZ['phone_tel']}"><span class="ic">{I['phone']}</span><span><small>Τηλέφωνο γραφείου</small><strong>{BIZ['phone']}</strong></span></a>
      <a class="contact-card" href="tel:{BIZ['phone2_tel']}"><span class="ic">{I['phone']}</span><span><small>Δεύτερη γραμμή</small><strong>{BIZ['phone2']}</strong></span></a>
      <a class="contact-card accent" href="tel:{BIZ['mobile_tel']}"><span class="ic">{I['mobile']}</span><span><small>Κινητό · 24/7</small><strong>{BIZ['mobile']}</strong></span></a>
      <div class="contact-card"><span class="ic">{I['fax']}</span><span><small>Fax</small><strong>{BIZ['fax']}</strong></span></div>
      <a class="contact-card wide" href="mailto:{BIZ['email']}"><span class="ic">{I['mail']}</span><span><small>Email</small><strong>{BIZ['email']}</strong></span></a>
    </div>
    {contact_card()}
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    {sec_title("Πού θα μας βρείτε")}
    <div class="office">
      <div class="map"><iframe src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Χάρτης: {BIZ['name']}, {BIZ['street']}, {BIZ['city']}"></iframe></div>
      <div class="office-info">
        <span class="ic">{I['pin']}</span>
        <div><small>Το γραφείο μας</small><strong>{BIZ['street']}, {BIZ['city']}</strong><span>Αττική</span></div>
        <a class="btn btn-primary" href="{MAPS_LINK}" target="_blank" rel="noopener">Οδηγίες {I['arrow']}</a>
      </div>
    </div>
  </div>
</section>
"""
build_page("/epikoinonia/", "Επικοινωνία · Γραφείο Τελετών Σοφογιάννης · Βύρωνας",
           "Επικοινωνήστε με το Γραφείο Τελετών Σοφογιάννης: Φορμίωνος 233, Βύρωνας. Τηλ. 210 7600 900, 210 7600 907, κιν. 6944 14 58 44, fax 210 7600 908.",
           [("Αρχική", "/"), ("Επικοινωνία", "/epikoinonia/")], contact_body,
           [{"@type": "ContactPage", "url": url("/epikoinonia/"), "mainEntity": {"@id": url("/#funeralhome")}}])
PAGES.append(("/epikoinonia/", "0.9"))

# ================================================================= 404
nf_body = f"""<section class="notfound"><div class="wrap">
  <img src="/images/logo-emblem.webp?v={LOGO_V}" alt="" width="120" height="120">
  <h1>Η σελίδα δεν βρέθηκε</h1>
  <p class="lead">Η σελίδα που αναζητάτε δεν υπάρχει. Αν χρειάζεστε βοήθεια, καλέστε μας οποιαδήποτε ώρα.</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="/">Αρχική σελίδα</a>
    <a class="btn btn-ghost" href="tel:{BIZ['phone_tel']}">{I['phone']}{BIZ['phone']}</a>
  </div>
</div></section>
"""
nf = head("/404", "Η σελίδα δεν βρέθηκε · " + BIZ["name"], "Η σελίδα δεν βρέθηκε.", graph("/", BIZ["name"], "", None)).replace(
    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex">')
write("/404.html", nf + header("") + nf_body + footer())

# ================================================================= sitemap / robots
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p, pr in PAGES:
    sm.append(f"  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>\n")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {url('/sitemap.xml')}\n")
print("Built %d pages" % (len(PAGES) + 1))
