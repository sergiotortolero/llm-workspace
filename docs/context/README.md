# Contexto del orquestador — cómo funciona

Este es el "cerebro" personalizado de tu agente maestro. Aquí vive el contexto que Claude
Code **no** hereda de tu Claude en la web (claude.ai). Para personalizar al orquestador,
trasvasamos ese contexto aquí.

## Las 4 capas de contexto (de más a menos "obligatorio")

1. **`CLAUDE.md`** (raíz + cada proyecto) — *reglas e instrucciones* que Claude SIEMPRE
   sigue. Se carga en cada sesión. Aquí van reglas, no datos largos.
2. **Memoria** (`MEMORY.md` + archivos en la carpeta de memoria de Claude) — *hechos
   durables atómicos* que se recuerdan automáticamente (quién eres, metas, decisiones).
3. **`docs/context/`** (esta carpeta) — *contexto de referencia largo*: tu perfil, tu
   negocio, tus metas, glosario. Demasiado extenso para memoria, pero valioso. Se consulta
   cuando hace falta.
4. **`docs/` de cada proyecto** (prd/adr/audits) — contexto específico de cada producto.

## El flujo (cómo me das contexto)

```
   Tú pegas/copias  ──►   docs/context/inbox/   ──►   yo lo proceso (/context-sync)  ──►
   (chat, NotebookLM,        (volcado crudo,            lo distribuyo a la capa correcta:
    notas, voz, etc.)         sin orden)                 memoria / CLAUDE.md / context / PRD
```

1. **Tú** sueltas lo que tengas en `inbox/` (sin preocuparte por el formato).
2. **Yo** lo leo, te hago preguntas si algo no queda claro, y lo *destilo* a la capa que
   corresponda (un hecho durable → memoria; una regla → CLAUDE.md; perfil → `about-me.md`;
   info de producto → el PRD del proyecto).
3. Lo crudo en `inbox/` se puede archivar una vez procesado.

## Por dónde empezar
- Lee **`ONBOARDING.md`** → te dice exactamente qué compartir, por prioridad.
- Mira **`about-me.md`** → ya lo sembré con lo que sé de ti; corrige y completa los `[GAP]`.
