"""French locale patterns for the Hewn classifier.

Community-refine status: synthesized 1:1 from the Italian locale by
translating equivalent idioms. NOT yet validated against a corpus of
real French prompts. PRs with real-prompt evidence welcome.

Load by setting HEWN_LOCALE=fr (or HEWN_LOCALE=en,fr to stack).
"""
from __future__ import annotations


IR_RULES: list[tuple[str, int]] = [
    # "explique pourquoi X échoue", "pourquoi X échoue", "que monitorer"
    (r"explique\s+pourquoi|\bpourquoi\b.*(?:[eé]chou\w*|crash\w*|cass[eé]\w*|plante|bug|erreur|ne\s+(?:fonctionne|marche)\s+pas)|que\s+(?:dois[- ]je\s+)?monitor(?:er|e)?|monitor.*prod|que\s+(?:dois[- ]je\s+)?contr[oô]ler|qu'?est[- ]ce\s+qui\s+(?:ne\s+)?(?:va\s+pas|marche\s+pas)", 3),
    # "étudie ce repo", "analyse le code"
    (r"\b(?:[eé]tudie|[eé]tudier|analyse|examine|[eé]value|inspecte)\s+(?:ce\s+|cette\s+|le\s+|la\s+|les\s+)?(?:repo|d[eé]p[oô]t|r[eé]p(?:ertoire)?|dir(?:ectory)?|code|projet|module|impl\w*)\b", 3),
    # "qu'est-ce qui manque / est cassé / est fragile / je couperais"
    (r"qu'?est[- ]ce\s+qui\s+(?:manque|est\s+cass[eé]|est\s+fragile|est\s+solide|ne\s+va\s+pas)|\bje\s+couperais\b", 2),
    # "trouve le bug", "corrige/répare/débogue cette fonction" — broad object noun list
    (r"\b(?:trouve|corrige|r[eé]pare|r[eé]sous|d[eé]bogue|d[eé]buggue)\s+(?:le\s+|la\s+|les\s+|un\s+|une\s+|ce\s+|cette\s+|ces\s+)?(?:bug|race|erreur|probl[eè]me|issue|vuln[eé]rabilit[eé]|fuite|deadlock|fonction|m[eé]thode|classe|module|script|code|test|api)", 3),
    # "refactorise", "refactore", "redessine"
    (r"\brefactor[ei][sr]?\w*\b|\bred[eé]ssin[ei]\b|\brefactoring\b", 2),
]

PROSE_RULES: list[tuple[str, int]] = [
    # "explique-moi comme si j'avais 5 ans"
    (r"\bexplique[- ]moi\b.*(?:comme\s+si|comme\s+à\s+un|enfant|d[eé]butant|junior)|\bcomment\s+ça\s+marche\b.*(?:pour\s+un|à\s+un|d[eé]butant)", 3),
    # "raisonne sur le tradeoff", "réfléchis à voix haute"
    (r"\braisonne\s+sur\s+(?:le\s+)?(?:tradeoff|compromis)|\br[eé]fl[eé]chis\s+à\s+voix\s+haute\b|\bdiscussion\b", 3),
    # "pas d'IR", "seulement de la prose", "sans markdown"
    (r"\bpas\s+d[e']\s*(?:ir|hewn|flint|code)\b|\bseulement\s+de\s+la\s+prose\b|\bsans\s+markdown\b", 5),
]

FINDINGS_RULES: list[str] = [
    # "quels sont les 3 bugs les plus probables qu'un utilisateur rencontrera"
    r"\b(?:quels|quelles)\s+(?:sont\s+)?(?:les\s+)?(?:\d+|quelques|top|principaux|probables|plus\s+probables)\s+(?:bugs?|probl[eè]mes?|erreurs?|risques?|vuln[eé]rabilit[eé]s?|bloqueurs?|bloquants?)\b",
    # "quels bugs rencontrera / trouvera / verra"
    r"\bquels?\s+(?:bugs?|probl[eè]mes?|erreurs?|risques?)\s+(?:rencontrer|trouver|voir|affronter)\w*",
    # "classe / trie / priorise les bugs par gravité / probabilité / impact"
    r"\b(?:classe|trie|priorise)\b.*\b(?:bugs?|probl[eè]mes?|risques?|vuln[eé]rabilit[eé]s?|bloquants?)\b.*\b(?:gravit[eé]|s[eé]v[eé]rit[eé]|probabilit[eé]|impact)\b",
    # "trouve(-moi) les N bugs" — hyphenated enclitic + optional adjective before noun
    r"\b(?:trouve(?:[- ]moi)?|identifie(?:[- ]moi)?|liste(?:[- ]moi)?|[eé]num[eè]re(?:[- ]moi)?|montre[- ]moi)\s+(?:les\s+)?(?:top\s+)?\d+\s+(?:\w+\s+)?(?:bugs?|probl[eè]mes?|erreurs?|risques?|vuln[eé]rabilit[eé]s?|bloquants?|failles?)",
]

CODE_ARTIFACT_RULES: list[str] = [
    # "écris(-moi) le/un test/code" — hyphenated enclitic
    r"\b[eé]cris(?:[- ]moi)?\s+(?:le\s+|la\s+|un\s+|une\s+|les\s+)?(?:code|tests?|snippet|fix|patch|script|fonction|m[eé]thode|classe|impl[eé]mentation)",
    # "montre le code mis à jour / diff / patch"
    r"\b(?:montre|montre[- ]moi|affiche|affiche[- ]moi)\s+(?:le\s+|la\s+|un\s+|une\s+)?(?:code|fichier|diff|patch|snippet|config|module|classe)(?:\s+(?:mis\s+à\s+jour|à\s+jour|actualis[eé]))?",
    # "implémente le/un X"
    r"\bimpl[eé]mente\s+(?:le\s+|la\s+|un\s+|une\s+|les\s+)",
    # "applique le fix / la patch / le changement"
    r"\bapplique\s+(?:le\s+|la\s+)(?:fix|patch|changement|correction|modification|mise[- ]à[- ]jour)",
]

POLISHED_AUDIENCE_RULES: list[str] = [
    # "pour la direction / stakeholders / clients / non technique"
    r"\bpour\s+(?:la\s+|le\s+|les\s+)?(?:direction|leadership|stakeholders?|clients?|public)\b|\bnon\s+technique\b",
    # "memo pour la direction / clients", "lettre aux clients"
    r"\bm[eé]mo\s+(?:pour|au|aux)\s+(?:direction|leadership|stakeholders?|clients?)|\blettre\s+(?:pour|aux)\s+clients?\b",
    # "post-mortem pour les clients / public"
    r"\bpost[- ]?mortem\s+(?:pour\s+(?:les\s+)?clients?|public|externe)\b",
    # "ton professionnel / rassurant / blameless"
    r"\bton\s+(?:professionnel|rassurant|blameless|r[eé]flexif|narratif)\b",
    # "X paragraphes"
    r"\b(?:2|3|4|5|deux|trois|quatre|cinq)\s+paragraphes?\b",
]
