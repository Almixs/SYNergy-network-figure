# SYNergy-figures: схеми документа HLD/LLD

Python-скрипти, які малюють схеми документа `SYNergy_campus_HLD_LLD` (v1.0). Усі числа, назви й моделі взято з тексту документа; джерело кожного рисунка вказано в шапці його скрипта.

## Склад

| Скрипт | Рисунок у документі | Вихідні файли |
|---|---|---|
| `fig04_wan.py` | Fig. 4 Inter-site WAN | `out/fig04_wan.png`, `.svg` |
| `fig05_dc.py` | Fig. 5 Data centres | `out/fig05_dc.*` |
| `fig06_site1.py` | Fig. 6 Site 1 | `out/fig06_site1.*` |
| `fig07_site2.py` | Fig. 7 Site 2 | `out/fig07_site2.*` |
| `fig08_site3.py` | Fig. 8 Site 3 | `out/fig08_site3.*` |
| `fig09_admin_ftto.py` | Fig. 9 Administrative building, FTTO | `out/fig09_admin_ftto.*` |
| `fig10_academic.py` | Fig. 10 Academic building | `out/fig10_academic.*` |
| `fig11_dormitory.py` | Fig. 11 Dormitory | `out/fig11_dormitory.*` |
| `fig12_lld_academic.py` | Fig. 12 Sheet SYN-LLD-K3-201 (academic floor 2) | `out/fig12_lld_academic.*` |
| `fig13_lld_dormitory.py` | Fig. 13 Sheet SYN-LLD-D1-201 (dormitory floor 2) | `out/fig13_lld_dormitory.*` |
| `fig14_lld_admin_ftto.py` | Fig. 14 Sheet SYN-LLD-A1-101 (admin floor 1, FTTO) | `out/fig14_lld_admin_ftto.*` |
| `fig15_ftto_riser.py` | Fig. 15 Sheet SYN-LLD-A1-002 (FTTO riser, ELV rooms) | `out/fig15_ftto_riser.*` |
| `fig25_segmentation.py` | Fig. 25 Segmentation and DMZ | `out/fig25_segmentation.*` |
| `fig26_gantt.py` | Fig. 26 Deployment plan (Gantt) | `out/fig26_gantt.*` |

Допоміжні модулі:
- `hwdraw.py` — спільний стиль: іконки, зони, типи ліній, підписи, легенда. Колір і товщину лінії задано в одному місці (`LINKS`), тому всі рисунки однакові.
- `templates.py` — шаблони будівель (адмін, навчальна, гуртожиток) для Fig. 6–8: числа на будівлю в одному місці.
- `sitewan.py` — шини ISP A / ISP B для Fig. 7 і 8.
- `lldsheet.py` — креслення LLD на аркуші A4 альбомної орієнтації (266 × 168 мм): шар плану, легенда, примітки, таблиці, ревізії, штамп. Лінії плану розширюються (`plan_layer`), текст 5–7 pt.
- `plans/` — шари планів Fig. 12–14 (план поверху з трасами, AP і розетками попереднього випуску аркуша); скрипт робить лінії ширшими і додає все інше векторно.
- `make_custom_icons.py` — дві іконки, яких немає у файлі Huawei (див. нижче).
- `build_all.py` — збирає все.

## Конфігурації (`config/`)

`config/` — конфігурації 13 ролей пристроїв з Appendix A документа (v1.3), один файл на роль; перелік і пояснення в [`config/README.md`](config/README.md). Конфігурації не перевірялися в симуляторі: їх написано лише з офіційної документації Huawei, посилання на неї в шапці кожного файлу.

## Збірка

```bash
pip install matplotlib pillow numpy opencv-python-headless --break-system-packages   # якщо ще немає
python3 build_all.py          # усі рисунки
python3 fig09_admin_ftto.py   # один рисунок
```

Потрібен шрифт Liberation Sans (метрики Arial). На Ubuntu: `sudo apt install fonts-liberation`.

## Формат

- PNG 300 dpi, ширина 180 мм (2125 px), вставляється в документ у 100 % ширини тексту.
- Аркуші LLD (Fig. 12–15): 266 × 168 мм (3141 px), на сторінці A4 альбомної орієнтації.
- SVG з текстом як текст, щоб виправити підпис в Inkscape без перезбірки.
- Координати в скриптах у міліметрах від верхнього лівого кута, тож положення легко правити.

## Іконки

`icons/` — синій набір Huawei *Enterprise Networking Product Icons (Flat)*, витягнутий з `Enterprise_Networking_Product_Icons_S_en.pptx` (161 іконка, назва файлу = підпис у презентації).

Чого в наборі немає, і що використано натомість:
- **Маршрутизатор** — іконка Huawei «Core Router» (стандартний символ маршрутизатора в наборі) для NE8000 і AR8700.
- **ODF (floor box)** — `custom_odf.png`, намальована в тому ж стилі (колір #0262A9, той самий розмір і радіус кутів).
- **5G-маршрутизатор AR5710** — «Core Router» з позначкою «5G» (`custom_router_5g.png`).

## Умовні позначення

- Подвійна лінія до пунктирної рамки означає по одному лінку до кожного пристрою пари (M-LAG, HRP). Так зроблено, щоб не малювати повну сітку перехресних ліній.
- Іконка з «тінню» позначає кілька однакових пристроїв (кількість у підписі).
- Шини ISP A / ISP B з точками: точка = підключення до цього провайдера, лінія без точки проходить під шиною.

## Як оновити рисунок у Word

Правою кнопкою на старому рисунку → «Change Picture» → `out/figNN_*.png`. Підпис «Fig. N …» лишається з документа.
