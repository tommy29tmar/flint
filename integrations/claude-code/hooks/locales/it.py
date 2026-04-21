"""Italian locale patterns for the Hewn classifier.

Curated from real prompts by the original author. Validated against
the test corpus in tests/test_hewn_locales.py::ItalianTests.

Load by setting HEWN_LOCALE=it (or HEWN_LOCALE=en,it to stack).
"""
from __future__ import annotations


IR_RULES: list[tuple[str, int]] = [
    # "spiega perché X fallisce", "cosa monitoro", "cosa controllo in prod",
    # "come mai X fallisce/si rompe/crash"
    (r"spieg[ao].*perch[eé]|cosa\s+monit|monit.*prod|cosa\s+controll|cos'?[eè]\s+che\s+non\s+va|\bcome\s+mai\b.*(?:fall\w*|rott\w*|crash|bug|errore|non\s+funzion|non\s+va)", 3),
    # "studia questo repo/progetto", "analizza il codice"
    (r"\b(?:studia|studiare|analizza|esamina|valuta|ispeziona)\s+(?:questo\s+|questa\s+|il\s+|la\s+|lo\s+)?(?:repo|repository|dir(?:ectory)?|codice|progetto|modulo|impl\w*)\b", 3),
    # "cosa manca / è fragile / toglierei" — repo-assessment Italian shape
    (r"\bcosa\s+(?:manca|è\s+fragile|toglierei|togliere|tagliare|è\s+solido|è\s+rotto|non\s+va)", 2),
    # "trova il bug", "correggi", "risolvi la race condition"
    (r"\b(?:trova|correggi|risolvi|sistema|aggiusta)\s+(?:il\s+|la\s+|i\s+|le\s+|un\s+|una\s+)?(?:bug|race|errore|problema|issue|vulnerabilit[aà]|leak|deadlock)", 3),
    # "refactora", "ridisegna" (Italian loan verbs)
    (r"\brefactor[ai]\b|\bridisegn[ai]\b|\brefactoring\b", 2),
]

PROSE_RULES: list[tuple[str, int]] = [
    # tutorial/explanation Italian: "spiegami come se avessi 5 anni"
    (r"\bspiegami\b.*(?:come\s+se|come\s+ad\s+un|come\s+a\s+un|junior|principiante|bambino)|\btutorial\b.*ital|come\s+funziona\b.*(?:per\s+un|a\s+un|principiant)", 3),
    # "ragiona sul tradeoff", "pensa ad alta voce"
    (r"\bragion[ia]\s+sul\s+tradeoff|\bpensa\s+ad\s+alta\s+voce|\bragionamento\b.*tradeoff", 3),
    # "niente IR", "niente Hewn", "solo prosa"
    (r"\bniente\s+(?:ir|hewn|flint|codice)\b|\bsolo\s+prosa\b|\bsenza\s+markdown\b", 5),
]

FINDINGS_RULES: list[str] = [
    # "quali sono i 3 bug più probabili che un utente incontrerà"
    r"\b(?:quali|che|cosa)\s+(?:sono\s+)?(?:i\s+|le\s+)?(?:\d+|pochi|top|principali|probabili|pi[uù]\s+probabili)\s+(?:bug|problemi|errori|rischi|vulnerabilit[aà]|blocchi|bloccanti)\b",
    # "cosa/che bug incontrerà / troverà / vedrà / avrà"
    r"\b(?:cosa|che)\s+(?:bug|problemi|errori|rischi)\s+(?:incontr|trov|vedr|avr)\w*",
    # "classifica / ordina / prioritizza i bug per gravità / probabilità / impatto"
    r"\b(?:classifica|ordina|prioritizza)\b.*\b(?:bug|problemi|rischi|vulnerabilit[aà]|bloccanti)\b.*\b(?:gravit[aà]|probabilit[aà]|impatto)\b",
    # "trova(mi) i top N rischi / bug / problemi" — enclitic pronoun allowed
    r"\b(?:trova(?:mi)?|identifica(?:mi)?|elenca(?:mi)?|lista(?:mi)?|mostrami)\s+(?:i\s+|le\s+)?(?:top\s+)?\d+\s+(?:\w+\s+)?(?:bug|problemi|errori|rischi|vulnerabilit[aà]|bloccanti|falle)",
]

CODE_ARTIFACT_RULES: list[str] = [
    # "scrivi(mi) il/un test/fix/codice" — enclitic pronoun
    r"\bscrivi(?:mi)?\s+(?:il\s+|la\s+|un\s+|una\s+|lo\s+)?(?:codice|test|snippet|fix|patch|script|funzione|metodo|classe|implementazione)",
    # "mostra il codice aggiornato / il diff / la patch"
    r"\b(?:mostra|mostrami)\s+(?:il\s+|la\s+|un\s+|una\s+)?(?:codice|file|diff|patch|snippet|config|modulo|classe)(?:\s+aggiornat\w*)?",
    # "implementa il/un X"
    r"\bimplementa\s+(?:il\s+|la\s+|un\s+|una\s+|lo\s+)",
    # "applica il fix / la patch"
    r"\bapplica\s+(?:il\s+|la\s+)(?:fix|patch|modifica|cambio|update)",
]

POLISHED_AUDIENCE_RULES: list[str] = [
    # "per la leadership / stakeholder / clienti / non tecnico"
    r"\bper\s+(?:la\s+)?(?:leadership|dirigenza|stakeholder|clienti?|pubblico)\b|\bnon\s+tecnic[oa]\b",
    # "memo per la leadership / clienti", "lettera ai clienti"
    r"\bmemo\s+(?:per|ai|al)\s+(?:leadership|dirigenza|stakeholder|clienti?)|\blettera\s+(?:per|ai)\s+clienti?\b",
    # "post-mortem per i clienti / pubblico"
    r"\bpost[- ]?mortem\s+(?:per\s+(?:i\s+)?clienti?|pubblico|esterno)\b",
    # "tono professionale / rassicurante / blameless"
    r"\btono\s+(?:professionale|rassicurante|blameless|riflessivo|narrativo)\b",
    # "X paragrafi"
    r"\b(?:2|3|4|5|due|tre|quattro|cinque)\s+paragraf[io]\b",
]
