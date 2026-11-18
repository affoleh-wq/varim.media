# VARiM content engine

Шаблоны роликов (1080×1920, 21 с, одна музыкальная дорожка) и постеров для соцсетей VARiM.
Нужны: python3, playwright, google-chrome (`/usr/bin/google-chrome`), ffmpeg, шрифт Inter.

## Как собрать контент для матча

1. Данные матча — со страницы `https://varim.net/predictions/<match>/` (WebFetch). Проверить, что 1X2 в сумме ≈ 100%.
2. Записать `data/<slug>.json` (примеры лежат в `data/`). Поле `template` выбирает формат:
   - `tpl_story.html` — **Underdog Story** (явный фаворит). Поля: `hook` [4 слова], `hookSize`, `codes` {home, away} (3 буквы), `colors` {home, away}, `posHome/posAway`, `ptsHome/ptsAway`, `winsHome/winsAway` (побед в последних 5), `formHome/formAway` (W/D/L, свежие первыми), `banner`, `probs` [home, draw, away], `pick`, `score` "h-a", `scorePct`, `others` [[счёт, %]×3], `h2h` {date, a, score, b}, `ctaTitle`, `ctaAsk`. Пример: `data/wales-portugal.json`.
   - `tpl_quiz.html` — **Score Quiz** (равный матч, светлая тема). Поля: `probs`, `over25`, `btts`, `clue`, `h2h` {date, a, score, b}, `score`, `scorePct`, `others` [[счёт, %]×3]. Пример: `data/denmark-norway.json`.
   - `tpl_top3.html` — **3 Stats**. Поля: `stat3`, `formHome/formAway`, `tagHome/tagAway`, `stat2`, `h2h` {date, a, ga, gb, b}, `group`, `table` [[место, команда, очки]×2], `probs`, `pick`, `score`, `scorePct`. Пример: `data/poland-sweden.json`.
   Необязательные поля (с 18.11): Story — `tape` [[подпись, home, away, lowWins?, 'ord'?]…] вместо позиций/очков, `ask` (вопрос на 1-м кадре; по умолчанию «Can <аутсайдер> stop them?»), фаворит может быть и хозяином; Quiz — `fact` {label, text}, если нет `h2h`; 3 Stats — `hot` ('home'|'away'), а вместо `h2h`+`table` можно `cmp` [[подпись, h, a, lowWins?]…], `cmpNote`, `venueLabel`, `venue` [[текст, значение]…]. Примеры: `data/coritiba-santos.json`, `data/remo-chapecoense.json`, `data/flamengo-athletico.json`.
   Первая сцена: хук виден с кадра t=0 (класс `.now`), остальное появляется за ≤0.3 с (`.aq`, `--d` ≤0.05s). `film.py check` снимает и кадр t=0 (`check_s1a.jpg`).
   - `video.html` — исходный формат «data breakdown» (`data/switzerland-scotland.json`).
   Общие поля: `slug`, `home`, `away`, `league`, `when` ("17 NOV 2026 · 19:45 UTC"). Весь текст — на английском.
3. Флаги сборных — в `engine.js` (`FLAGS`). Для новой сборной добавить SVG простого флага; клубных эмблем не рисовать (нейтральный значок).
4. `python3 film.py check data/<slug>.json` → кадры `out/<slug>/check_*.jpg`; посмотреть, что текст не переносится и не обрезается.
5. `./make.sh data/<slug>.json` → `out/<slug>/varim_<slug>_tiktok.mp4` (~2–3 мин).
6. `python3 poster.py data/<slug>.json` → `out/<slug>/varim_<slug>_pinterest.png` (1000×1500) и `_instagram.png` (1080×1350).
7. Для публикации: JPEG (`ffmpeg -i x.png -q:v 2 x.jpg`) + mp4 → в `YYYY-MM-DD/` этого репозитория, push, ссылки вида
   `https://raw.githubusercontent.com/affoleh-wq/varim.media/main/YYYY-MM-DD/<file>`.

## Куда публиковать

- Instagram (varim.media, account 17841442758876562) и Threads (varim.media, account 29426142563685167) — Windsor.ai for Social Media.
- TikTok (varimnet) и Pinterest (varimnet, доска «Prediction VARiM», boardId 1109081914425837488) — Metricool, blogId 8176877. TikTok требует `tiktokData.title`.
- Instagram — не более 5 хештегов. Pinterest — заголовок до 100 знаков, описание до 500, ссылка на страницу матча.
- Без коэффициентов, букмекеров и бонусов; в каждом посте «Model estimate, not a guarantee. 18+».
