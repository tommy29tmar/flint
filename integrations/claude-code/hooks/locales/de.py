"""German locale patterns for the Hewn classifier.

Community-refine status: synthesized 1:1 from the Italian locale by
translating equivalent idioms. NOT yet validated against a corpus of
real German prompts. PRs with real-prompt evidence welcome.

Load by setting HEWN_LOCALE=de (or HEWN_LOCALE=en,de to stack).
"""
from __future__ import annotations


IR_RULES: list[tuple[str, int]] = [
    # "erkläre warum", "warum schlägt X fehl", "was soll ich überwachen"
    (r"erkl[aä]re?\s+warum|\bwarum\b.*(?:schl[aä]gt|schlag\w*|fehl\w*|bricht|br[eu]cht|crash\w*|kaputt|bug|fehler|nicht\s+funktion)|was\s+(?:soll\s+ich\s+)?(?:[uü]berwach\w+|monitor\w+)|monitor.*prod|was\s+(?:soll\s+ich\s+)?pr[uü]fen|was\s+(?:ist\s+)?(?:kaputt|nicht\s+in\s+ordnung)", 3),
    # "studiere dieses repo", "analysiere den code / das Auth-Modul" — allow compound prefix
    (r"\b(?:studier[ee]?|analysier[ee]?|untersuche|pr[uü]fe|bewerte|inspizier[ee]?)\s+(?:dieses?\s+|diese\s+|das\s+|die\s+|den\s+)?[\w-]*(?:repo|repository|verzeichnis|code[- ]?base|code|projekt|modul|impl\w*)\b", 3),
    # "was fehlt / ist kaputt / ist fragil / würde ich entfernen"
    (r"\bwas\s+(?:fehlt|ist\s+kaputt|ist\s+fragil|ist\s+solide|ist\s+falsch|w[uü]rde\s+ich\s+(?:entfernen|k[uü]rzen|streichen))", 2),
    # "finde den bug", "debugge diese Funktion" — broad object noun list
    (r"\b(?:finde|behebe|korrigier[ee]?|repariere|debugge|l[oö]se)\s+(?:den\s+|die\s+|das\s+|einen\s+|eine\s+|dieses?\s+|diese\s+|diesen\s+)?(?:bug|race|fehler|problem|issue|schwachstelle|leck|deadlock|funktion|methode|klasse|modul|skript|code|test|api)", 3),
    # "refaktoriere", "überarbeite"
    (r"\brefaktor(?:isier[ee]?|ier\w+)\b|\b[uü]berarbeite\b|\brefactoring\b", 2),
]

PROSE_RULES: list[tuple[str, int]] = [
    # "erkläre mir wie einem Kind / als wäre ich 5"
    (r"\berkl[aä]re?\s+mir\b.*(?:wie\s+einem|als\s+w[aä]re|kind|anf[aä]nger|einsteiger)|\bwie\s+funktioniert\b.*(?:f[uü]r\s+einen|anf[aä]nger)", 3),
    # "denke laut nach", "diskutiere den tradeoff"
    (r"\bdenke\s+laut\s+nach\b|\bdiskutier[ee]?\s+(?:den\s+)?tradeoff|\b[uü]berleg[ee]?\s+laut\b|\bdiskussion\b", 3),
    # "kein IR", "nur prosa", "ohne markdown"
    (r"\bkein(?:e|en)?\s+(?:ir|hewn|flint|code)\b|\bnur\s+prosa\b|\bohne\s+markdown\b", 5),
]

FINDINGS_RULES: list[str] = [
    # "welche/was sind die N wichtigsten/gravierendsten Bugs" — "was sind" also opens findings
    r"\b(?:welche|was)\s+(?:sind\s+)?(?:die\s+)?(?:\d+|wenige|top|wichtigsten|wahrscheinlichsten|h[aä]ufigsten|gravierendsten|schwersten|kritischsten|gef[aä]hrlichsten)\s+(?:\w+\s+)?(?:bugs?|probleme?|fehler|risiken|schwachstellen|blocker|blockierenden?)\b",
    # "welche bugs wird ein user treffen / finden / sehen"
    r"\bwelche\s+(?:bugs?|probleme?|fehler|risiken)\s+(?:wird|werden|k[oö]nnte|k[oö]nnten|trifft|treffen|finden|sehen|erleben)\w*",
    # "ordne / priorisiere / sortiere bugs nach Schwere / Wahrscheinlichkeit / Auswirkung"
    r"\b(?:ordne|priorisier[ee]?|sortier[ee]?|klassifizier[ee]?)\b.*\b(?:bugs?|probleme?|risiken|schwachstellen|blockierenden?)\b.*\b(?:schwere|schweregrad|wahrscheinlichkeit|auswirkung|impact)\b",
    # "finde die N wichtigsten Bugs" — allow adjective between number and noun
    r"\b(?:finde|identifizier[ee]?|liste|aufz[aä]hl\w+)\s+(?:die\s+)?(?:top\s+)?\d+\s+(?:\w+\s+)?(?:bugs?|probleme?|fehler|risiken|schwachstellen|blockierenden?|l[uü]cken)",
]

CODE_ARTIFACT_RULES: list[str] = [
    # "schreib(e) (mir) einen Regression-Test" — short imperative + optional indirect object + compound noun
    r"\bschreib(?:e)?\s+(?:mir\s+)?(?:den\s+|die\s+|das\s+|einen\s+|eine\s+|ein\s+)?[\w-]*(?:test|code|snippet|fix|patch|skript|funktion|methode|klasse|implementierung)",
    # "zeig(e) (mir) den aktualisierten Code" — allow adjective between article and noun
    r"\b(?:zeig[ee]?|gib\s+mir)\s+(?:mir\s+)?(?:den\s+|die\s+|das\s+|einen\s+|eine\s+)?(?:\w+\s+)?(?:code|datei|diff|patch|snippet|config|modul|klasse)",
    # "implementiere den/einen X"
    r"\bimplementier[ee]?\s+(?:den\s+|die\s+|das\s+|einen\s+|eine\s+|ein\s+)",
    # "wende den Fix / die Patch an"
    r"\bwende\s+(?:den\s+|die\s+|das\s+)(?:fix|patch|[aä]nderung|korrektur|update)\s+an",
]

POLISHED_AUDIENCE_RULES: list[str] = [
    # "für die Leitung / Stakeholder / Kunden / nicht technisch"
    r"\bf[uü]r\s+(?:die\s+)?(?:leitung|f[uü]hrung|leadership|stakeholder|kunden|[oö]ffentlichkeit)\b|\bnicht[- ]?technisch\b",
    # "Memo für die Leitung / Kunden", "Brief an Kunden"
    r"\bmemo\s+(?:f[uü]r|an)\s+(?:leitung|f[uü]hrung|leadership|stakeholder|kunden)|\bbrief\s+an\s+kunden\b",
    # "Post-Mortem für Kunden / Öffentlichkeit"
    r"\bpost[- ]?mortem\s+(?:f[uü]r\s+(?:die\s+)?kunden|[oö]ffentlichkeit|extern)\b",
    # "Ton: professionell / beruhigend / blameless"
    r"\bton\s*:?\s*(?:professionell|beruhigend|blameless|reflektiv|narrativ)\b",
    # "X Absätze"
    r"\b(?:2|3|4|5|zwei|drei|vier|f[uü]nf)\s+abs[aä]tze?\b",
]
