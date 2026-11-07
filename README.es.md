# curiosidade-viral

[![Curiosidad viral](guia/assets/banner-es.jpg)](https://inematds.github.io/curiosidade-viral/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

curiosidade-viral es un kit (una "skill" para Claude Code o Codex) que crea reels verticales de curiosidades sin que nadie aparezca: una voz explica y la pantalla muestra de cerca un objeto cotidiano. Sirve para quien quiere crear una cuenta de contenido corto sin grabar ni editar. El kit verifica el gancho antes de gastar, pide tu aprobación para un storyboard, graba la voz en tu computadora y monta el video con código. También incluye dos agentes que leen mensajes y cifras de anuncios y solo proponen. Necesitas Node.js, ffmpeg, Python y Claude Code o Codex.

📖 Guía completa: **https://inematds.github.io/curiosidade-viral/guia/es/**

**Reels de curiosidades sin mostrar el rostro, hechos con IA, y el modelo que convierte las visualizaciones en resultados.**

Una voz explica y la pantalla muestra, en grande y con textura, algo cotidiano (el refrigerador, la cebolla, el celular), con lo invisible dibujado encima. Tú haces la pregunta; la IA investiga los datos con fuentes, escribe 4 ganchos, prepara el storyboard para que lo apruebes y solo entonces graba la voz (local) y renderiza el video (con código, sin IA de video).

Y como viralizar es la parte fácil, el kit incluye el resto del modelo: **dos agentes que solo proponen** (Curio se ocupa de la cuenta, Clic se ocupa de los anuncios con 4 reglas escritas en código) y el **enlace etiquetado por reel**, para saber qué atrajo a cada persona.


## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| `SKILL.md` | la skill (Claude Code / Codex): el proceso completo paso a paso |
| `metodo/` | las reglas: `gancho.md` (5 pruebas, formatos, prohibiciones), `roteiro.md` (bucle de curiosidad, duración, formato del JSON), `imagem.md` (el objeto siempre en pantalla, lo invisible dibujado, movimiento, sonido) |
| `ferramentas/` | `novo.py`, `gancho_check.py` (verificador), `storyboard.py`, `voz.py` (voz local sincronizada con la palabra), `montar.py`, `mezcla.py`, `preparar.py` |
| `motor/` | base del renderizado (HyperFrames + Three.js), fuentes locales |
| `agentes/` | `curio.md` + `curio_triagem.py`, `clic.md` + `clic_regras.py`, `link.py`, ejemplos |
| `exemplos/geladeira/` | el reel de demostración, desde el guion hasta el MP4 |
| `docs/caso-e-metodo.md` | el caso real (una semana, cuenta desde cero) y lo que enseña |
| `testes/` | `python3 -m unittest discover -s testes` |

## El proceso, de principio a fin

🧠 = tú (director) · 🤖 = la IA (Claude Code / Codex, con suscripción) · ⚙️ = script

| # | Paso | Quién | Comando |
|---|---|---|---|
| 1 | La pregunta del reel y quién lo ve | 🧠 | — |
| 2 | Carpeta nueva | ⚙️ | `python3 ferramentas/novo.py <slug> "<pergunta>" --duracao 30` |
| 3 | Datos con fuentes (`fatos.md`) | 🤖 | — |
| 4 | 4 ganchos + guion + escenas + texto de la publicación | 🤖 | `exemplos/<slug>/roteiro.json`, `pie.txt` |
| 5 | Verificador | ⚙️ | `python3 ferramentas/gancho_check.py exemplos/<slug>` |
| 6 | **Storyboard: la única instancia de aprobación** | ⚙️ → 🧠 | `python3 ferramentas/storyboard.py exemplos/<slug> --abrir` |
| 7 | Voz local | ⚙️ | `python3 ferramentas/voz.py --projeto exemplos/<slug> exemplos/<slug>/roteiro.json` |
| 8 | Imágenes del objeto (3–5 vistas de lo mismo) | 🤖 | Codex image_gen (suscripción) o tus fotos |
| 9 | Página del reel | 🤖 | `index.html` + `js/` (copia el ejemplo del refrigerador) |
| 10 | Reloj + música + preparar | ⚙️ | `montar.py` → `mezcla.py` → `preparar.py` |
| 11 | Prueba + fotogramas estáticos | ⚙️ → 🧠 | `npx hyperframes check` · `npx hyperframes snapshot` |
| 12 | Renderizado | ⚙️ | `npx hyperframes render --output renders/<slug>.mp4` |
| 13 | Revisar el MP4 | 🤖 + 🧠 | hoja de fotogramas + `checklists/antes-de-postar.md` |
| 14 | Enlace etiquetado | ⚙️ | `python3 agentes/link.py <url> --conta <conta> --onde reel --reel <slug>` |
| 15 | Publicar manualmente desde el celular | 🧠 | — |
| 16 | Curio: separa mensajes y propone respuestas (4 veces al día) | ⚙️ → 🧠 | `python3 agentes/curio_triagem.py mensagens.json --link <link> --estado estado.json` |
| 17 | Clic: propone reducir o aumentar anuncios según las 4 reglas | ⚙️ → 🧠 | `python3 agentes/clic_regras.py metricas.json` |

## Instalar

```bash
git clone https://github.com/inematds/curiosidade-viral.git
cd curiosidade-viral
bash instalar.sh
```

Necesita Node.js 22+, ffmpeg y Python 3 con numpy (Ubuntu/Debian: `sudo apt install python3-numpy`; Mac: `python3 -m pip install numpy`).

**Voz local (opcional, requiere GPU NVIDIA):** `voz.py` usa Chatterbox (clona tu voz a partir de 10–20 s de audio) y Whisper (mide el tiempo de cada palabra). Indica dónde están: `CHATTERBOX_PYTHON` (python del entorno de Chatterbox), `INEMAVOX_DIR`
(carpeta con el venv de Whisper) y `VC_VOZ=/caminho/tu-voz.wav`. Sin GPU, omite la voz: `montar.py --sem-voz` crea el reel con subtítulos y música.

Nada de esto llama a una API de pago.

## Las 6 lecciones del caso

1. Vende (u ofrece) lo que ya enseñas: la pregunta más común era «¿cómo haces eso?».
2. Mide desde el primer minuto: un día sin medir, 19 personas abrieron la página de pago y nadie compró.
3. Concentra el presupuesto: unos pocos anuncios con presupuesto devolvieron cerca de 2 veces; muchos con poco presupuesto, cerca de la mitad.
4. Etiqueta cada enlace: una venta sin origen no se puede repetir.
5. Automatiza la atención, no las decisiones: los agentes proponen, tú decides.
6. El contenido orgánico también vende: la bio vendió sin ningún anuncio.

Las cifras del caso corresponden a una semana y no son una promesa de resultados.

Licencia MIT · INEMA · https://inema.club