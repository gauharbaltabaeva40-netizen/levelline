# LEVEL LINE — сайт

Tilda-дағы сайттың (levelline.tilda.ws/main) статикалық көшірмесі. GitHub Pages арқылы тегін хостингте тұр.

- `index.html` — негізгі сайт (телефонға арналған)
- `desktop.html` — компьютерде сайтты ортадағы "телефон терезесінде" көрсетеді
- `images/`, `css/`, `js/` — сайттың суреттері мен стильдері

## Tilda-да өзгеріс жасасаңыз — қайта көшіру

```bash
python3 tools/localize.py https://levelline.tilda.ws/main /tmp/levelline-new
python3 tools/optimize.py /tmp/levelline-new /tmp/levelline-originals
```

Сосын `/tmp/levelline-new` ішіндегі файлдарды осы папкаға көшіріп, `index.html` басына компьютерге бағыттайтын `<script>` блогын қайта қосу керек (ескі `index.html`-ден алыңыз).
