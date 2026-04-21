"""Spanish locale patterns for the Hewn classifier.

Community-refine status: synthesized 1:1 from the Italian locale by
translating equivalent idioms. NOT yet validated against a corpus of
real Spanish prompts. PRs with real-prompt evidence welcome.

Load by setting HEWN_LOCALE=es (or HEWN_LOCALE=en,es to stack).
"""
from __future__ import annotations


IR_RULES: list[tuple[str, int]] = [
    # "explica por qué X falla", "qué monitoreo en producción", "por qué X falla"
    (r"explica\s+por\s+qu[eé]|qu[eé]\s+monitor[eo]?|monitor.*prod|qu[eé]\s+controlo|qu[eé]\s+es\s+lo\s+que\s+(?:no\s+)?funciona|\bpor\s+qu[eé]\b.*(?:falla|fall\w*|crashe\w*|roto|cae|se\s+cae|no\s+funciona|error|bug)", 3),
    # "estudia este repo", "analiza el código"
    (r"\b(?:estudia|estudiar|analiza|examina|eval[uú]a|inspecciona)\s+(?:este\s+|esta\s+|el\s+|la\s+)?(?:repo|repositorio|dir(?:ectorio)?|c[oó]digo|proyecto|m[oó]dulo|impl\w*)\b", 3),
    # "qué falta / está roto / está frágil"
    (r"\bqu[eé]\s+(?:falta|est[aá]\s+roto|est[aá]\s+fr[aá]gil|est[aá]\s+mal|no\s+funciona|quitar[ií]a|cortar[ií]a)", 2),
    # "encuentra el bug", "arregla/corrige/depura/soluciona este..." — broad object noun list
    (r"\b(?:encuentra|arregla|corrige|repara|depura|soluciona)\s+(?:el\s+|la\s+|los\s+|las\s+|un\s+|una\s+|este\s+|esta\s+|esto\s+)?(?:bug|race|error|problema|issue|vulnerabilidad|fuga|deadlock|funci[oó]n|m[eé]todo|clase|m[oó]dulo|script|c[oó]digo|test|api)", 3),
    # "refactoriza", "rediseña"
    (r"\brefactoriza\b|\brefactor[ií]zalo?\b|\brediseña\b|\brefactorizaci[oó]n\b", 2),
]

PROSE_RULES: list[tuple[str, int]] = [
    # "explícame como si tuviera 5 años"
    (r"\bexpl[ií]came\b.*(?:como\s+si|como\s+a\s+un|ni[ñn]o|principiante)|\bcomo\s+funciona\b.*(?:para\s+un|a\s+un|principiant)", 3),
    # "razona sobre el tradeoff", "piensa en voz alta"
    (r"\brazona\s+sobre\s+(?:el\s+)?tradeoff|\bpiensa\s+en\s+voz\s+alta\b|\bdiscusi[oó]n\b", 3),
    # "nada de IR", "solo prosa", "sin markdown"
    (r"\bnada\s+de\s+(?:ir|hewn|flint|c[oó]digo)\b|\bsolo\s+prosa\b|\bsin\s+markdown\b", 5),
]

FINDINGS_RULES: list[str] = [
    # "cuáles son los 3 bugs más probables que un usuario encontrará"
    r"\b(?:cu[aá]les|qu[eé])\s+(?:son\s+)?(?:los\s+|las\s+)?(?:\d+|pocos|top|principales|probables|m[aá]s\s+probables)\s+(?:bugs?|problemas?|errores?|riesgos?|vulnerabilidades?|bloqueos?|bloqueantes?)\b",
    # "qué/cuáles bugs encontrará / encontrará / verá"
    r"\b(?:qu[eé]|cu[aá]les)\s+(?:bugs?|problemas?|errores?|riesgos?)\s+(?:encontrar|ver|enfrentar|toparse)\w*",
    # "clasifica / ordena / prioriza los bugs por gravedad / probabilidad / impacto"
    r"\b(?:clasifica|ordena|prioriza)\b.*\b(?:bugs?|problemas?|riesgos?|vulnerabilidades?|bloqueantes?)\b.*\b(?:gravedad|severidad|probabilidad|impacto)\b",
    # "encuéntra(me) los N bugs" — enclitic pronoun + accent + optional adjective before noun
    r"\b(?:encu[eé]ntra(?:me)?|identifica(?:me)?|enumera(?:me)?|lista(?:me)?|mu[eé]strame)\s+(?:los\s+|las\s+)?(?:top\s+)?\d+\s+(?:\w+\s+)?(?:bugs?|problemas?|errores?|riesgos?|vulnerabilidades?|bloqueantes?|fallos?)",
]

CODE_ARTIFACT_RULES: list[str] = [
    # "escríbe(me) el/un test/código" — enclitic pronoun (escríbeme)
    r"\bescr[ií]be(?:me)?\s+(?:el\s+|la\s+|un\s+|una\s+|los\s+|las\s+)?(?:c[oó]digo|tests?|snippet|fix|patch|script|funci[oó]n|m[eé]todo|clase|implementaci[oó]n)",
    # "muestra el código actualizado / diff / patch"
    r"\b(?:muestra|mu[eé]strame|enseña|ens[eé]ñame)\s+(?:el\s+|la\s+|un\s+|una\s+)?(?:c[oó]digo|archivo|fichero|diff|patch|snippet|config|m[oó]dulo|clase)(?:\s+actualizad\w*)?",
    # "implementa el/un X"
    r"\bimplementa\s+(?:el\s+|la\s+|un\s+|una\s+|los\s+|las\s+)",
    # "aplica el fix / la patch / el cambio"
    r"\baplica\s+(?:el\s+|la\s+)(?:fix|patch|cambio|arreglo|actualizaci[oó]n|correcci[oó]n)",
]

POLISHED_AUDIENCE_RULES: list[str] = [
    # "para el liderazgo / stakeholders / clientes / no técnico"
    r"\bpara\s+(?:el\s+|la\s+)?(?:liderazgo|direcci[oó]n|stakeholders?|clientes?|p[uú]blico)\b|\bno\s+t[eé]cnic[oa]\b",
    # "memo para liderazgo / clientes", "carta a clientes"
    r"\bmemo\s+(?:para|a|al)\s+(?:liderazgo|direcci[oó]n|stakeholders?|clientes?)|\bcarta\s+(?:para|a)\s+clientes?\b",
    # "post-mortem para clientes / público"
    r"\bpost[- ]?mortem\s+(?:para\s+(?:los\s+)?clientes?|p[uú]blico|externo)\b",
    # "tono profesional / tranquilizador / blameless"
    r"\btono\s+(?:profesional|tranquilizador|blameless|reflexivo|narrativo)\b",
    # "X párrafos"
    r"\b(?:2|3|4|5|dos|tres|cuatro|cinco)\s+p[aá]rrafos?\b",
]
