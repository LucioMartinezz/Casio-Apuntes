# Casio Apuntes: contexto del proyecto

Este archivo resume todo lo que se habló y decidió al construir el proyecto (con Claude Code, octubre 2026). Leelo antes de hacer cambios.

## Quién lo usa y para qué

- El usuario es Lucio, estudiante universitario: matemática financiera, costos, modelos para la toma de decisiones (investigación de operaciones, árboles, Bayes, incertidumbre, bajo riesgo). Habla en **español rioplatense**, no es programador: explicale todo simple y sin jerga.
- Tiene una **Casio fx-9750GIII**, sistema **03.70.3200**. En la facultad no la puede usar; la usa en su casa para estudiar con fórmulas y apuntes cargados.
- Objetivo: escribir apuntes y fórmulas en la PC y pasarlos a la calculadora como archivos `.py`.

## Datos de la calculadora (confirmados en el aparato real)

- Pantalla **128×64** píxeles, monocromo.
- Python (MicroPython) con `casioplot`. Lo que `casioplot` ofrece: `clear_screen`, `set_pixel`, `get_pixel`, `draw_string`, `show_screen`. **No hay `getkey`**: un programa no puede leer las flechas mientras muestra un dibujo.
- **AC/ON lanza `KeyboardInterrupt` y se puede atrapar** con try/except (confirmado con `prueba.py`). Así se pasa de pantalla en el modo dibujo.
- **No trae `matplotl`.**
- El **editor de Python** muestra unos **21 caracteres** de ancho (con la flecha → se ve el resto del renglón) y unos 6 renglones. Según el usuario, el editor acepta como máximo **150 filas por archivo**.
- Por USB aparece como unidad extraíble de unos 3 MB (en la PC original era `D:`). El usuario tiene carpetas `Teoria/` y `Practica/` con apuntes propios. **No tocarlas sin permiso.** Los demos están en `Demo/`.
- Los apuntes del usuario son `.py` de texto plano: **ASCII sin tildes y con fin de línea CRLF** (los escribe en el Bloc de notas y los lee en el editor, sin ejecutarlos).
- Archivos de unos 8 KB en modo dibujo funcionaron bien, aunque tengan renglones de código muy largos.

## Archivos

- `index.html`: **toda la app** en un solo archivo, sin dependencias. Se abre con doble clic y funciona sin internet.
- `prueba.py`: diagnóstico (lista funciones de casioplot, prueba matplotl y que AC/ON se pueda atrapar).
- `README.md`: instrucciones para el usuario.

## Cómo funciona la app (index.html)

### Sintaxis del cuaderno (lo que escribe el usuario)
- `# Título`: empieza un tema/página.
- `{a+b}/{c}`: fracción (se puede anidar); `frac{a}{b}` también funciona.
- `x^2`, `x^{n-1}`: exponente. Sin llaves toma un signo opcional y la palabra pegada.
- `x_i`, `V_{real}`: subíndice.
- `sqrt{…}`, `bar{…}`, `Σ_{t=1}^{n}` (límites arriba y abajo).
- `( … )` y `[ … ]` se agrandan solos si adentro hay una fracción.
- `| a | b |` + `|---|---|`: tabla.
- `graf: x=0..100; y=50x; y=2000+30x; y=0..6000; alto=36`: gráfico (solo en modo dibujo).
- `img: nombre`: imagen (se agrega con el botón 🖼).
- `> texto`: centrado. `---`: línea divisoria. `\{`: carácter literal.

### Modo dibujo (RUN)
- Fuente propia de 5×7 (`FONT_SRC`) y layout en píxeles con cajas `{w, a, d, draw}`: `lay`/`laySeq`. Barra de fracción en baseline-4; exponentes subidos, subíndices bajados.
- `buildDoc` → páginas (`ops`) agrupadas por **tema** (`topic`). Si un tema no entra, se parte en "Título (2)". Renglones anchos opcionales: la página se muestra en partes de 120 px.
- `finalizeOps` junta letras en tiras de texto. `rasterize` dibuja la vista previa. **Tiene que coincidir píxel por píxel con el Python generado**: los dos usan el mismo DDA con división entera para las líneas.
- `buildPython` genera el `.py`: `F` (fuente, solo los caracteres usados; los no-ASCII se remapean a `\x80+`), `P` (pantallas: string de ops + cantidad de partes) y `G` (temas: título ASCII ≤17, palabras para buscar, primera pantalla, cantidad). Funciones: `T`/`L`/`B` (texto/línea/imagen), `Z` (flechita ▸ si hay más pantallas), `D`, `S(tema, pantalla)` y el menú `M`.
- Menú en la calculadora: número + EXE abre el tema; EXE solo pasa al siguiente; `0` muestra más títulos; una palabra busca; **`2.3` va directo a la pantalla 3 del tema 2**. Con un tema en pantalla, **AC/ON pasa a la pantalla siguiente** y en la última vuelve al menú.

### Modo texto (editor)
- `buildText` arma un archivo ASCII de 21 columnas con las fórmulas dibujadas con caracteres (`tNodes`/`tNode`: fracción con guiones, paréntesis altos `/ | \`, `Sum` con límites). Agrega un índice ("INDICE (fila):") si hay varios temas y divide en archivos de hasta 150 filas (`nombre1.py`, `nombre2.py`…). Exporta con CRLF.
- Cada fila guarda **de qué renglones del cuaderno sale** (`src`, `end`) y su tipo (`kind`). Las filas automáticas (índice, "Sigue en…") tienen `src = -1`.
- **Edición en vivo en los dos sentidos:** el panel derecho (archivo) es editable. `applyRight` compara con lo anterior, agranda el cambio a bloques completos y lo traduce de vuelta con `reverseText`/`artLinear` (fracción dibujada → `{a}/{b}`, `=== X ===` → `# X`, tablas, etc.). Las filas sin cambios conservan su renglón original (tildes, gráficos). Probado: 22 fórmulas hacen ida y vuelta exacta.
- Una calculadora chiquita simulada (arriba de "Descargar") muestra lo que entra en pantalla y sigue al cursor.

### Otras funciones
- **📥 Importar texto** (`organize`): ordena apuntes desordenados **con reglas, sin IA**. Detecta títulos (mayúsculas, subrayados con ===/---) y los pasa a minúscula salvo las siglas cortas. Une renglones cortados (no une rótulos que terminan en ":"), convierte fórmulas (`/` → fracción, `**` → `^`, `sqrt(`/`raiz(` → `sqrt{}`, `*` → `·`) y tablas de Excel (tabulaciones). La ventana tiene pasos 1–4 y una vista previa real (páginas dibujadas o archivo de texto).
- Números de fila al costado de los editores, barra de estado (fila, carácter, total de caracteres, filas del archivo /150).
- Los cuadernos se guardan en **localStorage** (`casioApuntes.v1`), **no en el repositorio**.

## Preferencias del usuario (importante)

- Usa el **modo texto** para teoría y fórmulas en general, y el **modo dibujo** para gráficos y fórmulas complicadas.
- En modo texto quiere el editor (izquierda) y el archivo (derecha) **a la par**, con el archivo grande y la calculadora simulada **chica**, como detalle.
- **No le gustó** una tabla de comparación "lo que escribís / cómo queda" debajo del editor (se sacó), ni la calculadora grande en modo texto.
- Para ordenar apuntes eligió **A + C**: el botón de importar (sin IA, sin clave de API) y, para textos largos o complicados, **pasárselos a Claude** para que los convierta a la sintaxis del cuaderno y, si la calculadora está conectada, los copie.
- No quiere add-ins ni modificar el sistema de la calculadora (se le explicó que convertirla a fx-9860GIII es riesgoso).

## Cómo se probó (la PC original no tenía Python ni Node)

- Se sirvió la carpeta con un `HttpListener` de PowerShell y se abrió en el navegador integrado.
- El `.py` generado se ejecutó con **Pyodide**, con un `casioplot` falso que registra píxeles, y se comparó con `rasterize`: todo coincidió píxel por píxel, incluidas pantallas anchas, imágenes y la flechita.
- El menú se probó simulando `input()`.
- Si hay Python en la PC nueva, se puede probar igual con un `casioplot` falso.

## Pendiente / ideas ofrecidas

- **Botones "Guardar copia de mis cuadernos" / "Cargar copia"** (exportar/importar el JSON de localStorage) para pasar los cuadernos entre PCs. Se ofreció; todavía no se hizo.
- La última versión del modo dibujo (con `2.2`) se generó, pero quizás no se copió a la calculadora (`Demo/fin_dib.py`, `Demo/cos_dib.py`). Regenerarla desde la página y copiarla.
- GitHub Pages (página online con link) se mencionó como opción; requiere repositorio público en una cuenta gratis.
