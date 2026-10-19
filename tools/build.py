# -*- coding: utf-8 -*-
"""Генератор статичних шаблонів сторінок ukrainianfootball.com.ua (нова структура).
Запуск: python3 build.py  ->  папка ../uf-templates/
Дані взяті з сайту станом на 19.10.2026; у робочій версії їх підставляє WordPress / API."""
import os, json, html, shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uf-templates")
D = "https://ukrainianfootball.com.ua"
E = html.escape

# ---------------------------------------------------------------- дані
LEAGUES = {
 "upl": dict(name="УПЛ", full="Українська Прем'єр-ліга", season="2026/27", gen="УПЛ",
   zones=[(1,3,"eu","Єврокубки"),(13,14,"po","Плей-оф за збереження місця"),(15,16,"rel","Пониження в класі")],
   table=[("Шахтар",9,8,0,1,20,5,24),("Полісся",9,7,1,1,20,8,22),("Харків",8,6,0,2,16,6,18),("Динамо",8,5,1,2,11,8,16),
          ("Карпати",9,4,3,2,17,8,15),("ЛНЗ",9,4,2,3,10,9,14),("Зоря",9,4,2,3,12,13,14),("Епіцентр",9,2,3,4,9,12,9),
          ("Верес",9,2,3,4,6,11,9),("Колос",8,2,2,4,10,13,8),("Буковина",9,1,5,3,7,12,8),("Лівий Берег",8,1,4,3,6,8,7),
          ("Оболонь",8,1,4,3,4,12,7),("Чорноморець",8,1,2,5,5,11,5),("Кудрівка",9,1,2,6,10,21,5),("Кривбас",7,1,2,4,7,13,5)],
   rounds_total=30,
   rounds=[
    (8,True,[("перенесено","","Оболонь","Кривбас","1:0"),("12.10","","Лівий Берег","Зоря","1:3"),("11.10","","ЛНЗ","Кудрівка","2:1"),("11.10","","Динамо","Карпати","1:0"),
             ("11.10","","Буковина","Полісся","2:2"),("10.10","","Колос","Епіцентр","3:1"),("10.10","","Чорноморець","Харків","1:2"),("09.10","","Верес","Шахтар","0:3")]),
    (9,True,[("19.10","","Харків","Лівий Берег","2:1"),("18.10","","Полісся","Динамо","3:1"),("18.10","","Кривбас","ЛНЗ","0:3"),("18.10","","Карпати","Епіцентр","2:2"),
             ("17.10","","Зоря","Чорноморець","2:1"),("17.10","","Кудрівка","Буковина","4:1"),("17.10","","Шахтар","Колос","2:1"),("16.10","","Оболонь","Верес","2:0")]),
    (10,False,[("23.10","13:00","Динамо","Кудрівка",""),("23.10","15:30","Полісся","Оболонь",""),("23.10","15:30","Верес","Колос",""),("24.10","13:00","Лівий Берег","ЛНЗ",""),
              ("24.10","15:30","Епіцентр","Харків",""),("24.10","18:00","Шахтар","Зоря",""),("25.10","13:00","Чорноморець","Карпати",""),("25.10","15:30","Буковина","Кривбас","")]),
    (11,False,[("30.10","18:00","Шахтар","Оболонь",""),("31.10","13:00","Лівий Берег","Буковина",""),("31.10","15:30","Верес","Чорноморець",""),("01.11","13:00","Колос","Полісся",""),
              ("01.11","13:00","ЛНЗ","Харків",""),("02.11","13:00","Кривбас","Динамо",""),("02.11","13:00","Зоря","Епіцентр",""),("02.11","18:00","Карпати","Кудрівка","")])],
   news=[("Карпати вирвали нічию на останніх секундах у домашньому матчі проти Епіцентра","karpaty-vyrvaly-nichyyu-na-ostannih-sekundah-u-domashnomu-matchi-proty-epiczentra","18.10.2026 23:01"),
         ("ЛНЗ перервав безвиграшну виїзну серію, здолавши Кривбас у гостях","lnz-perervav-bezvygrashnu-vyyiznu-seriyu-zdolavshy-kryvbas-u-gostyah","18.10.2026 19:03"),
         ("Полісся майже весь матч у меншості вирвало вольову перемогу над Динамо Київ у матчі УПЛ","polissya-majzhe-ves-match-u-menshosti-vyrvalo-volovu-peremogu-nad-dynamo-kyyiv-u-matchi-upl","18.10.2026 19:01"),
         ("9-й тур УПЛ: Харків – Лівий Берег — статистичний анонс і ключові цифри","9-j-tur-upl-harkiv-livyj-bereg-statystychnyj-anons-i-klyuchovi-czyfry","18.10.2026 15:01"),
         ("Шахтар обіграв Колос, але гості продовжили гольову серію на виїзді","shahtar-obigrav-kolos-ale-gosti-prodovzhyly-golovu-seriyu-na-vyyizdi","17.10.2026 23:01"),
         ("Зоря завдяки пізньому голу Богдана Кушніренка вирвала перемогу над Чорноморцем","zorya-zavdyaky-piznomu-golu-bogdana-kushnirenka-vyrvala-peremogu-nad-chornomorczem","17.10.2026 19:04"),
         ("Статистика і факти перед матчем 9 туру УПЛ Полісся — Динамо Київ","statystyka-i-fakty-pered-matchem-9-turu-upl-polissya-dynamo-kyyiv","17.10.2026 19:03"),
         ("Кудрівка розгромила Буковину та обірвала смугу поразок","kudrivka-rozgromyla-bukovynu-ta-obirvala-smugu-porazok","17.10.2026 19:02"),
         ("УПЛ, 9-й тур: Карпати – Епіцентр — статистичне прев'ю та ключові цифри матчу","upl-9-j-tur-karpaty-epiczentr-statystychne-prevyu-ta-klyuchovi-czyfry-matchu","17.10.2026 19:01"),
         ("Кривбас — ЛНЗ у 9-му турі УПЛ: статистичне прев'ю матчу та ключові цифри протистояння","kryvbas-lnz-u-9-mu-turi-upl-statystychne-prevyu-matchu-ta-klyuchovi-czyfry-protystoyannya","17.10.2026 15:01"),
         ("Трагічна звістка: на війні загинув Роман Максимюк","tragichna-zvistka-na-vijni-zagynuv-roman-maksymyuk","17.10.2026 11:02"),
         ("Младен Бартулович оформив 30-ту тренерську перемогу в Українській Прем'єр-лізі","mladen-bartulovych-oformyv-30-tu-trenersku-peremogu-v-ukrayinskij-premyer-lizi","17.10.2026 11:01")],
   pages=124,
   intro="Українська Прем'єр-ліга — вищий дивізіон чемпіонату України. У сезоні 2026/27 грають 16 клубів, кожен проводить 30 матчів: по два з кожним суперником, вдома і на виїзді.",
   faq=[("Скільки команд грає в УПЛ 2026/27?","16 клубів. Сезон складається з 30 турів."),
        ("Хто потрапляє в єврокубки?","Команди з 1-го по 3-тє місце. Розподіл між Лігою чемпіонів, Лігою Європи та Лігою конференцій залежить від рейтингу УЄФА і переможця Кубка України."),
        ("Хто вилітає з УПЛ?","Клуби на 15-му і 16-му місцях вибувають до Першої ліги. Команди на 13-му і 14-му місцях грають плей-оф за збереження місця.")]),
 "persha-liga": dict(name="Перша ліга", full="Перша ліга України", season="2026/27", gen="Першої ліги",
   zones=[(1,2,"up","Підвищення в класі"),(3,4,"pu","Плей-оф за підвищення"),(13,14,"po","Плей-оф за пониження"),(15,16,"rel","Пониження в класі")],
   table=[("Вікторія",12,7,3,2,16,9,24),("Агробізнес",12,7,2,3,19,14,23),("Полтава",12,6,3,3,22,10,21),("Куликів-Білка",12,6,3,3,25,14,21),
          ("Фенікс-Маріуполь",12,6,3,3,18,13,21),("Олександрія",12,5,5,2,17,11,20),("Локомотив Київ",12,4,5,3,15,13,17),("Прикарпаття",12,4,3,5,12,14,15),
          ("Металіст",12,4,3,5,13,14,15),("Нива Тернопіль",12,3,6,3,12,10,15),("Інгулець",11,4,2,5,11,16,14),("Колос-2",12,4,1,7,12,20,13),
          ("ЮКСА",12,2,5,5,15,19,11),("Чернігів",11,2,4,5,12,16,10),("Пробій",12,2,3,7,12,30,9),("Полісся-2",12,1,5,6,17,25,8)],
   rounds_total=30,
   rounds=[
    (11,True,[("12.10","","Полісся-2","Куликів-Білка","2:4"),("11.10","","Нива Тернопіль","Колос-2","3:1"),("11.10","","Олександрія","Локомотив Київ","1:3"),("11.10","","Прикарпаття","Чернігів","0:1"),
              ("11.10","","ЮКСА","Фенікс-Маріуполь","1:2"),("10.10","","Пробій","Полтава","3:2"),("10.10","","Інгулець","Агробізнес","0:1"),("09.10","","Металіст","Вікторія","2:2")]),
    (12,True,[("18.10","","Пробій","Полісся-2","1:1"),("18.10","","Куликів-Білка","Олександрія","1:1"),("18.10","","Локомотив Київ","Нива Тернопіль","0:0"),("17.10","","Полтава","Прикарпаття","4:0"),
              ("17.10","","Фенікс-Маріуполь","Інгулець","4:1"),("17.10","","Колос-2","ЮКСА","0:0"),("17.10","","Агробізнес","Металіст","1:0"),("17.10","","Вікторія","Чернігів","2:1")]),
    (13,False,[("23.10","","Чернігів","Агробізнес",""),("23.10","13:00","Металіст","Фенікс-Маріуполь",""),("24.10","12:00","Олександрія","Пробій",""),("24.10","13:00","Прикарпаття","Вікторія",""),
               ("24.10","14:00","Полісся-2","Полтава",""),("25.10","12:00","ЮКСА","Локомотив Київ",""),("25.10","13:00","Інгулець","Колос-2",""),("25.10","14:30","Нива Тернопіль","Куликів-Білка","")]),
    (14,False,[("31.10","","Чернігів","Фенікс-Маріуполь",""),("31.10","","Полісся-2","Олександрія",""),("31.10","","Пробій","Нива Тернопіль",""),("31.10","","Полтава","Вікторія",""),
               ("31.10","","Агробізнес","Прикарпаття",""),("31.10","","Локомотив Київ","Інгулець",""),("31.10","","Куликів-Білка","ЮКСА",""),("31.10","","Колос-2","Металіст","")])],
   news=[("Лівий Берег зняв банер фанів Ворскли, щоб уникнути негативу на своєму стадіоні","livyj-bereg-znyav-baner-faniv-vorskly-shhob-unyknuty-negatyvu-na-svoyemu-stadioni","05.05.2026 15:07"),
         ("Металург – Вікторія 0:3: відео голів і огляд матчу після відкладеного розгрому","metalurg-viktoriya-03-video-goliv-i-oglyad-matchu-pislya-vidkladenogo-rozgromu","05.05.2026 11:04"),
         ("Ворскла – Лівий Берег 0:1: суперники на різних курсах, відео голу та огляд матчу","vorskla-livyj-bereg-01-supernyky-na-riznyh-kursah-video-golu-ta-oglyad-matchu","04.05.2026 15:15"),
         ("Перша ліга: Вікторія вщент розгромила запорізький Металург — без шансів для запоріжців","persha-liga-viktoriya-vshhent-rozgromyla-zaporizkyj-metalurg-bez-shansiv-dlya-zaporizhcziv","04.05.2026 15:13"),
         ("Інгулець обіграв Пробій 3:1: відео голів та огляд матчу","ingulecz-obigrav-probij-31-video-goliv-ta-oglyad-matchu","04.05.2026 11:03"),
         ("Фоторепортаж: Чорноморець розгромив Прикарпаття 3:0 — ще один крок до еліти","fotoreportazh-chornomorecz-rozgromyv-prykarpattya-30-shhe-odyn-krok-do-elity","04.05.2026 11:02"),
         ("Тренер Григорчук про розгром у минулому турі: не хочу згадувати той матч","trener-grygorchuk-pro-rozgrom-u-mynulomu-turi-ne-hochu-zgaduvaty-toj-match","04.05.2026 07:05"),
         ("Наставник Прикарпаття розібрав ключові помилки в Одесі — вони коштували очок","nastavnyk-prykarpattya-rozibrav-klyuchovi-pomylky-v-odesi-vony-koshtuvaly-ochok","04.05.2026 07:03"),
         ("Через агресію РФ зірвано ще один матч Першої ліги: коли зіграють Металург — Вікторія","cherez-agresiyu-rf-zirvano-shhe-odyn-match-pershoyi-ligy-koly-zigrayut-metalurg-viktoriya","03.05.2026 23:13")],
   pages=122,
   intro="Перша ліга — другий за силою дивізіон українського футболу. У сезоні 2026/27 грають 16 команд, серед них резервні склади клубів УПЛ. Дві найкращі команди підвищуються до Прем'єр-ліги.",
   faq=[("Скільки команд у Першій лізі 2026/27?","16 команд, сезон триває 30 турів."),
        ("Хто виходить до УПЛ?","Команди на 1-му і 2-му місцях підвищуються напряму. 3-тя і 4-та грають плей-оф за підвищення."),
        ("Хто вилітає до Другої ліги?","15-та і 16-та команди. 13-та і 14-та грають плей-оф за пониження.")]),
 "druga-liga": dict(name="Друга ліга", full="Друга ліга України", season="2026/27", gen="Другої ліги",
   zones=[(1,2,"up","Підвищення в класі")],
   groups=[("Група А",[("Брацлав",7,5,2,0,17,5,17),("Нива Вінниця",7,4,2,1,13,5,14),("Дністер Заліщики",8,4,2,2,16,13,14),("Поділля",7,4,1,2,14,12,13),
                      ("Нива-2 Тернопіль",7,3,0,4,7,13,9),("СК Вільхівці",7,2,2,3,9,12,8),("Скала 1911",7,2,1,4,6,11,7),("Діназ",7,0,4,3,10,17,4),("Рух Львів",7,1,0,6,10,14,3)]),
           ("Група Б",[("Карбон",7,3,3,1,11,8,12),("Ребел",7,3,2,2,14,13,11),("Атлет",7,3,2,2,15,11,11),("Тростянець",7,2,4,1,8,5,10),
                      ("Олександрія-2",7,2,4,1,8,6,10),("Авангард Лозова",7,3,1,3,7,8,10),("Полтава-2",7,2,2,3,4,6,8),("Металург Зп",6,1,3,2,7,8,6),("Пенуел",7,1,1,5,5,14,4)])],
   rounds_total=18,
   dates=[
    ("Група А",[("09.10","","Нива-2 Тернопіль","СК Вільхівці","0:0"),("10.10","","Поділля","Брацлав","1:5"),("11.10","","Рух Львів","Нива Вінниця","1:1"),("11.10","","Дністер Заліщики","Діназ","1:0"),
                ("17.10","","Нива Вінниця","Поділля","2:1"),("17.10","","Дністер Заліщики","Нива-2 Тернопіль","1:1"),("17.10","","Діназ","Скала 1911","1:4"),("18.10","","Брацлав","СК Вільхівці","0:0"),
                ("24.10","","Скала 1911","Дністер Заліщики",""),("24.10","","Рух Львів","Діназ",""),("24.10","","СК Вільхівці","Нива Вінниця",""),("24.10","","Нива-2 Тернопіль","Брацлав",""),
                ("31.10","","Скала 1911","Нива-2 Тернопіль",""),("31.10","","Діназ","Поділля",""),("31.10","","Дністер Заліщики","Рух Львів",""),("31.10","","Нива Вінниця","Брацлав","")]),
    ("Група Б",[("09.10","","Металург Зп","Полтава-2","1:0"),("12.10","","Олександрія-2","Тростянець","0:1"),("12.10","","Пенуел","Карбон","1:8"),("16.10","","Карбон","Ребел","перенесено"),
                ("17.10","","Металург Зп","Олександрія-2","2:0"),("17.10","","Авангард Лозова","Тростянець","1:0"),("18.10","","Полтава-2","Пенуел","3:0"),("20.10","","Ребел","Атлет","0:0"),
                ("24.10","","Олександрія-2","Авангард Лозова",""),("24.10","","Пенуел","Металург Зп",""),("24.10","","Ребел","Полтава-2",""),("24.10","","Тростянець","Атлет",""),
                ("31.10","","Атлет","Авангард Лозова",""),("31.10","","Пенуел","Олександрія-2",""),("31.10","","Металург Зп","Ребел",""),("31.10","","Карбон","Тростянець","")])],
   news=[("Російський балістичний обстріл пошкодив київський футбольний стадіон","rosijskyj-balistychnyj-obstril-poshkodyv-kyyivskyj-futbolnyj-stadion","14.10.2026 15:06"),
         ("Кобін розповів, чому погодився на пропозицію Руха","kobin-rozpoviv-chomu-pogodyvsya-na-propozycziyu-ruha","23.09.2026 15:06"),
         ("60-річний президент став рекордсменом довголіття в українському футболі","60-richnyj-prezydent-stav-rekordsmenom-dovgolittya-v-ukrayinskomu-futboli","19.08.2026 15:32"),
         ("Полтавська Ворскла запланувала повернення у 2027 році","poltavska-vorskla-zaplanuvala-povernennya-u-2027-roczi","07.08.2026 15:16"),
         ("Екс-голкіпер Шахтаря та Динамо отримав нове призначення в Другій лізі","eks-golkiper-shahtarya-ta-dynamo-otrymav-nove-pryznachennya-v-drugij-lizi","25.07.2026 15:06"),
         ("Ужгород зникає з футбольної мапи України: місто втрачає професійний футбол","uzhgorod-znykaye-z-futbolnoyi-mapy-ukrayiny-misto-vtrachaye-profesijnyj-futbol","02.07.2026 15:13"),
         ("Валерій Іващенко працевлаштувався у футбольному клубі Другої ліги України","valerij-ivashhenko-praczevlashtuvavsya-u-futbolnomu-klubi-drugoyi-ligy-ukrayiny","29.06.2026 19:03"),
         ("Рух Львів збереже професійний статус і робитиме ставку на молодь","ruh-lviv-zberezhe-profesijnyj-status-i-robytyme-stavku-na-molod","19.06.2026 15:09"),
         ("ПФЛ офіційно затвердила склад клубів Першої та Другої ліг України","pfl-oficzijno-zatverdyla-sklad-klubiv-pershoyi-ta-drugoyi-lig-ukrayiny","19.06.2026 11:12"),
         ("ПФЛ планує виключити 11 клубів: що відомо про масове відсторонення","pfl-planuye-vyklyuchyty-11-klubiv-shho-vidomo-pro-masove-vidstoronennya","18.06.2026 11:07")],
   pages=2,
   intro="Друга ліга — третій професійний дивізіон. У сезоні 2026/27 18 команд розділені на дві групи по дев'ять. Дві найкращі команди кожної групи підвищуються до Першої ліги.",
   faq=[("Як влаштована Друга ліга 2026/27?","18 команд у двох групах, А і Б, по дев'ять у кожній. Кожна команда грає з суперниками своєї групи вдома і на виїзді."),
        ("Хто виходить до Першої ліги?","Команди на 1-му і 2-му місцях у кожній групі."),
        ("Де дивитися матчі?","Більшість ігор транслює YouTube-канал ПФЛ. Посилання на трансляцію є в картці матчу в календарі.")]),
}
ZB = dict(
  results=[("25.09.2026","21:45","Угорщина","Україна","0:1","Ліга націй, група B2"),("28.09.2026","19:00","Грузія","Україна","0:0","Ліга націй, група B2"),
           ("02.10.2026","21:45","Україна","Північна Ірландія","0:3","Ліга націй, група B2"),("05.10.2026","21:45","Україна","Угорщина","1:2","Ліга націй, група B2")],
  upcoming=[("14.11.2026","21:45","Північна Ірландія","Україна","","Ліга націй, група B2"),("17.11.2026","21:45","Україна","Грузія","","Ліга націй, група B2")],
  news=[("Нові подробиці щодо ситуації Анатолія Трубіна в Бенфіці: воротар не потрапляє до заявки","novi-podrobyczi-shhodo-sytuacziyi-anatoliya-trubina-v-benficzi-vorotar-ne-potraplyaye-do-zayavky","18.08.2026 07:01"),
        ("Збірна України проведе свої домашні матчі Ліги націй у Словаччині — джерела","zbirna-ukrayiny-provede-svoyi-domashni-matchi-ligy-naczij-u-slovachchyni-dzherela","18.07.2026 07:08"),
        ("Георгій Судаков, півзахисник Бенфіки, зробив заяву щодо стану свого здоров'я","georgij-sudakov-pivzahysnyk-benfiky-zrobyv-zayavu-shhodo-stanu-svogo-zdorovya","13.07.2026 07:01"),
        ("Вольфсбург повідомив про стан Еріксена після втрати свідомості в матчі Данії з Україною","volfsburg-povidomyv-pro-stan-eriksena-pislya-vtraty-svidomosti-v-matchi-daniyi-z-ukrayinoyu","09.07.2026 19:11"),
        ("Кейн повідомив про стан Еріксена після непритомності — як почувається колишній одноклубник","kejn-povidomyv-pro-stan-eriksena-pislya-neprytomnosti-yak-pochuvayetsya-kolyshnij-odnoklubnyk","10.06.2026 23:07"),
        ("Тренер збірної Данії оцінив стан Еріксена після непритомності та звернувся до вболівальників","trener-zbirnoyi-daniyi-oczinyv-stan-eriksena-pislya-neprytomnosti-ta-zvernuvsya-do-vbolivalnykiv","08.06.2026 23:15"),
        ("Кардіолог оцінив перспективи Еріксена продовжити кар'єру після непритомності у грі Данія — Україна","kardiolog-oczinyv-perspektyvy-eriksena-prodovzhyty-karyeru-pislya-neprytomnosti-u-gri-daniya-ukrayina","08.06.2026 19:10"),
        ("Крістіан Еріксен, який знепритомнів у матчі Данії з Україною, зробив офіційну заяву","kristian-eriksen-yakyj-zneprytomniv-u-matchi-daniyi-z-ukrayinoyu-zrobyv-oficzijnu-zayavu","08.06.2026 19:07")],
  pages=16)
TRANSFERS=[("Скандальний екс-футболіст збірної України розкрив, як опинився в Казахстані","skandalnyj-eks-futbolist-zbirnoyi-ukrayiny-rozkryv-yak-opynyvsya-v-kazahstani","16.09.2026 15:01"),
 ("Ігор Суркіс попрощався з воротарем київського Динамо","igor-surkis-poproshhavsya-z-vorotarem-kyyivskogo-dynamo","14.09.2026 23:02"),
 ("Перші слова форварда Рената Дадашова: щиро вражений і вже тут","pershi-slova-forvarda-renata-dadashova-shhyro-vrazhenyj-i-vzhe-tut","14.09.2026 15:03"),
 ("Київське Динамо отримало попередження: у гравця є проблеми","kyyivske-dynamo-otrymalo-poperedzhennya-u-gravczya-ye-problemy","14.09.2026 15:01"),
 ("Воротар Динамо Київ попрощався з клубом та оформив трансфер до Полісся","vorotar-dynamo-kyyiv-poproshhavsya-z-klubom-ta-oformyv-transfer-do-polissya","12.09.2026 19:01"),
 ("Бенфіка готова заплатити 7 млн євро за Жуана Ананіаса, гравцем цікавиться й Шахтар","benfika-gotova-zaplatyty-7-mln-yevro-za-zhuana-ananiasa-gravczem-czikavytsya-j-shahtar","12.09.2026 03:01"),
 ("Двоє футболістів, від яких позбулося Динамо, перейшли до Шахтаря","dvoye-futbolistiv-vid-yakyh-pozbulosya-dynamo-perejshly-do-shahtarya","11.09.2026 23:01"),
 ("Верес був за крок від трансферу гравця лондонського Арсеналу","veres-buv-za-krok-vid-transferu-gravczya-londonskogo-arsenalu","10.09.2026 19:03"),
 ("У Вересі пояснили трансферну політику: чому беруть легіонерів, а не українців","u-veresi-poyasnyly-transfernu-polityku-chomu-berut-legioneriv-a-ne-ukrayincziv","10.09.2026 19:01"),
 ("Офіційно: Буковина підписала легіонера з досвідом Англії та Німеччини","oficzijno-bukovyna-pidpysala-legionera-z-dosvidom-angliyi-ta-nimechchyny","10.09.2026 11:01")]
# Архів бомбардирів УПЛ 2025/26 — рядки, які зараз є на сторінці сайту
UPL_SC_ARCH=[("Кауан Еліас","Шахтар",2,3,0),("Ігор Краснопір","Полісся",2,2,0),("Владислав Бабогло","Карпати",2,2,0),("Хоакінете","Епіцентр",2,2,2),
             ("Олександр Тимчик","Динамо",1,1,0),("Георгій Робакідзе","Чорноморець",1,1,0),("Лука Мейрелліш","Шахтар",1,1,0)]

# ---------------------------------------------------------------- шаблон
NAV=[("upl","УПЛ"),("persha-liga","Перша ліга"),("druga-liga","Друга ліга"),("transfery-ukrayiny","Трансфери"),("zbirna-ukrayiny","Збірна України")]

def rel(depth, path):  # path без початкового "/" ; повертає відносне посилання
    return "../"*depth + (path if path else "index.html") + ("" if path.endswith(".html") or not path else "")

class Page:
    def __init__(s, path, title, desc, h1, crumbs, section, sub=None):
        s.path=path.strip("/"); s.depth=len([p for p in s.path.split("/") if p]); s.title=title; s.desc=desc; s.h1=h1
        s.crumbs=crumbs; s.section=section; s.sub=sub
    def u(s, p):  # посилання на іншу сторінку шаблонів
        p=p.strip("/"); return "../"*s.depth + (p+"/" if p else "") + "index.html"

def head(pg, extra_ld=None):
    canon=D+"/"+pg.path+("/" if pg.path else "")
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":D+"/"+p.strip("/")+("/" if p.strip("/") else "")} for i,(n,p) in enumerate(pg.crumbs)]}
    ld=[bc]+(extra_ld or [])
    css=pg.u("").replace("index.html","")+"assets/css/main.css"; js=pg.u("").replace("index.html","")+"assets/js/main.js"
    nav="".join(f'<li><a href="{pg.u(k)}"{" aria-current=\"page\"" if pg.section==k else ""}>{E(v)}</a></li>' for k,v in NAV)
    crumbs=" ".join(f'<li><a href="{pg.u(p)}">{E(n)}</a></li>' if i<len(pg.crumbs)-1 else f'<li aria-current="page">{E(n)}</li>' for i,(n,p) in enumerate(pg.crumbs))
    return f'''<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(pg.title)}</title>
<meta name="description" content="{E(pg.desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{E(pg.title)}">
<meta property="og:description" content="{E(pg.desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="uk_UA">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&family=Unbounded:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Перейти до вмісту</a>
<header class="site-head">
  <div class="wrap site-head__in">
    <a class="logo" href="{pg.u("")}" aria-label="Футбол України — на головну"><svg class="logo__mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#ffd23f"/><circle cx="20" cy="20" r="12.5" fill="#13213c"/><path d="M20 13.4l6.2 4.5-2.4 7.3h-7.6l-2.4-7.3z" fill="#ffd23f"/><path d="M20 7.6v5.8M26.2 17.9l5.8-1.9M23.8 25.2l3.5 4.8M16.2 25.2l-3.5 4.8M13.8 17.9L8 16" stroke="#ffd23f" stroke-width="1.7" fill="none"/></svg><span class="logo__words"><span class="logo__w1">Футбол</span><span class="logo__w2">України</span></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Меню</button>
    <nav id="site-nav" class="site-nav" aria-label="Розділи"><ul>{nav}</ul></nav>
  </div>
</header>
<div class="crumbs-bar"><nav class="crumbs wrap" aria-label="Хлібні крихти"><ol>{crumbs}</ol></nav></div>
'''

def foot(pg):
    links="".join(f'<li><a href="{pg.u(k)}">{E(v)}</a></li>' for k,v in NAV)
    js=pg.u("").replace("index.html","")+"assets/js/main.js"
    return f'''<footer class="site-foot">
  <div class="wrap site-foot__in">
    <a class="logo logo--foot" href="{pg.u("")}"><svg class="logo__mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#ffd23f"/><circle cx="20" cy="20" r="12.5" fill="#13213c"/><path d="M20 13.4l6.2 4.5-2.4 7.3h-7.6l-2.4-7.3z" fill="#ffd23f"/><path d="M20 7.6v5.8M26.2 17.9l5.8-1.9M23.8 25.2l3.5 4.8M16.2 25.2l-3.5 4.8M13.8 17.9L8 16" stroke="#ffd23f" stroke-width="1.7" fill="none"/></svg><span class="logo__words"><span class="logo__w1">Футбол</span><span class="logo__w2">України</span></span></a>
    <ul class="site-foot__nav">{links}</ul>
    <p class="site-foot__copy">© 2026 «Футбол України». Дані турнірних таблиць і календарів оновлюються автоматично.</p>
  </div>
</footer>
<script src="{js}" defer></script>
</body>
</html>
'''

def league_band(pg, key, lg, active, h1, lead=None, tabs=None, stats=None):
    tabs = tabs or [("", "Огляд"),("news","Новини"),("table","Таблиця"),("calendar","Календар"),("bombardyry","Бомбардири")]
    t="".join(f'<li><a href="{pg.u(key+("/"+p if p else ""))}"{" aria-current=\"page\"" if p==active else ""}>{E(n)}</a></li>' for p,n in tabs)
    lead_html=f'<p class="band__lead">{E(lead)}</p>' if lead else ""
    if stats:
        lead_html+='<dl class="band__stats">'+"".join(f'<div><dt>{E(a)}</dt><dd>{b}</dd></div>' for a,b in stats)+'</dl>'
    return f'''<div class="band">
  <div class="wrap">
    <div class="band__title">
      <h1>{E(h1)}</h1>
      {"" if (lg and lg["season"] in h1) else f'<span class="band__season">Сезон {E(lg["season"] if lg else "2026/27")}</span>'}
    </div>
    {lead_html}
    <nav class="subnav" aria-label="Розділ"><ul>{t}</ul></nav>
  </div>
</div>
'''

PAL=[("#1c4fd6","#fff"),("#cf3b2f","#fff"),("#1f8a5b","#fff"),("#ffd23f","#13213c"),("#e0a106","#13213c"),("#6b3fa0","#fff"),("#0e7c86","#fff"),("#f26a21","#fff"),("#4a5a73","#fff"),("#13213c","#ffd23f")]
import re as _re, zlib as _z
def crest(name, big=False):
    w=[x for x in _re.split(r"[\s\-]+",name) if x]
    if len(w)>1: ini=(w[0][0]+w[1][0])
    elif name.isupper() and len(name)<=3: ini=name
    else: ini=name[0]
    bg,fg=PAL[_z.crc32(name.encode())%len(PAL)]
    return f'<span class="crest{" crest--big" if big else ""}" style="--c-bg:{bg};--c-fg:{fg}" aria-hidden="true" data-source="api:team.logo">{E(ini.upper())}</span>'
def pts_word(n):
    m=n%10; h=n%100
    w='очко' if m==1 and h!=11 else ('очки' if 2<=m<=4 and not 12<=h<=14 else 'очок')
    return f'{n} {w}'
def gd(f,a): d=f-a; return f"+{d}" if d>0 else str(d)
def zone(lg,pos):
    for a,b,c,_ in lg["zones"]:
        if a<=pos<=b: return c
    return ""

def table_html(lg, rows, compact=False, caption=None):
    head='<tr><th scope="col" class="c-pos">#</th><th scope="col" class="c-team">Команда</th><th scope="col" title="Матчі">І</th>'
    if not compact: head+='<th scope="col" class="c-wdl" title="Виграші">В</th><th scope="col" class="c-wdl" title="Нічиї">Н</th><th scope="col" class="c-wdl" title="Поразки">П</th><th scope="col" class="c-goals" title="Забиті – пропущені">М</th>'
    head+='<th scope="col" title="Різниця м\'ячів">±</th><th scope="col" class="c-pts" title="Очки">О</th></tr>'
    body=""
    for i,(t,g,w,d,l,f,a,p) in enumerate(rows,1):
        z=zone(lg,i)
        body+=f'<tr class="{("z-"+z) if z else ""}"><td class="c-pos">{i}</td><th scope="row" class="c-team"><span class="team">{crest(t)}{E(t)}</span></th><td>{g}</td>'
        if not compact: body+=f'<td class="c-wdl">{w}</td><td class="c-wdl">{d}</td><td class="c-wdl">{l}</td><td class="c-goals">{f}–{a}</td>'
        body+=f'<td>{gd(f,a)}</td><td class="c-pts">{p}</td></tr>'
    cap=f'<caption>{E(caption)}</caption>' if caption else ""
    return f'<div class="tbl-scroll"><table class="standings{" standings--compact" if compact else ""}" data-source="api:standings">{cap}<thead>{head}</thead><tbody>{body}</tbody></table></div>'

def legend(lg):
    return '<ul class="legend">'+"".join(f'<li class="z-{c}"><span class="legend__sw" aria-hidden="true"></span>{a}–{b}: {E(n)}</li>' for a,b,c,n in lg["zones"])+'</ul>'

def match_rows(ms, show_round_date=True):
    out=""
    for d,t,h,a,s in ms:
        played = bool(s) and s!="перенесено"
        mid = f'<span class="m__score">{E(s)}</span>' if played else (f'<span class="m__time">{E(t)}</span>' if t else '<span class="m__time m__time--tbd">—</span>')
        status = "перенесено" if s=="перенесено" or d=="перенесено" else ("" )
        dd = "" if d=="перенесено" else d
        out+=f'''<li class="m{" m--played" if played else ""}">
  <time class="m__date">{E(dd)}{('<span class="m__flag">перенесено</span>') if status else ""}</time>
  <span class="m__home"><span class="m__name">{E(h)}</span>{crest(h)}</span>{mid}<span class="m__away">{crest(a)}<span class="m__name">{E(a)}</span></span>
</li>'''
    return f'<ul class="matches">{out}</ul>'

def news_list(pg, rub, items, n=None, big=False, thumbs=False):
    items = items[:n] if n else items
    li=""
    for i,(t,slug,dt) in enumerate(items):
        href=pg.u(f"{rub}/news/{slug}")
        date,tm=dt.split(" ")
        iso="-".join(reversed(date.split(".")))+"T"+tm
        lead = big and i==0
        img = f'<a class="news__img" href="{href}" tabindex="-1" aria-hidden="true" data-source="wp:thumbnail"></a>' if (lead or thumbs) else ""
        li+=f'<li class="news__item{" news__item--lead" if lead else ""}{" news__item--thumb" if thumbs and not lead else ""}">{img}<div class="news__txt"><a href="{href}">{E(t)}</a><time datetime="{iso}">{date}, {tm}</time></div></li>'
    return f'<ul class="news">{li}</ul>'

def pagination(pg, base, pages, cur=1):
    def link(n, label=None, cls=""):
        href = pg.u(base) if n==1 else pg.u(base).replace("index.html", f"page/{n}/index.html")
        cur_attr=' aria-current="page"' if n==cur else ""
        return f'<li><a class="{cls}" href="{href}"{cur_attr}>{label or n}</a></li>'
    items=[link(n) for n in range(1,min(4,pages)+1)]
    if pages>5: items.append('<li class="pager__gap" aria-hidden="true">…</li>')
    if pages>4: items.append(link(pages))
    if pages>1: items.append(link(2,"Наступна","pager__next"))
    return f'<nav class="pager" aria-label="Сторінки"><ul>{"".join(items)}</ul></nav>'

def scorers_table(rows, demo=False):
    body=""
    for i,(n,c,m,g,pen) in enumerate(rows,1):
        avg=f"{g/m:.2f}".replace(".",",") if m else "—"
        body+=f'<tr><td class="c-pos">{i}</td><th scope="row" class="c-team">{E(n)}</th><td class="c-club">{E(c)}</td><td class="c-pts">{g}</td><td>{pen}</td><td>{m}</td><td class="c-avg">{avg}</td></tr>'
    note='<p class="devnote">Приклад заповнення. У робочій версії рядки приходять з API (endpoint topscorers), сортування: голи, потім менше матчів.</p>' if demo else ""
    return note+f'<div class="tbl-scroll"><table class="standings scorers" data-source="api:topscorers"><thead><tr><th scope="col" class="c-pos">#</th><th scope="col" class="c-team">Гравець</th><th scope="col" class="c-club">Клуб</th><th scope="col" class="c-pts">Голи</th><th scope="col" title="З них з пенальті">Пен.</th><th scope="col" title="Матчі">І</th><th scope="col" class="c-avg" title="Голів за матч">За матч</th></tr></thead><tbody>{body}</tbody></table></div>'

def demo_scorers(lg):
    teams=[r[0] for r in (lg.get("table") or lg["groups"][0][1]+lg["groups"][1][1])]
    rows=[]; g=[8,7,7,6,5,5,5,4,4,4,3,3]
    for i,x in enumerate(g):
        rows.append((f"Прізвище Ім'я", teams[(i*3)%len(teams)], 9 if i%3 else 8, x, 1 if i in (1,4) else 0))
    return rows

def faq_block(items):
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
    h="".join(f'<details class="faq__item"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)
    return h, ld

def write(pg, body):
    p=os.path.join(OUT, pg.path, "index.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p,"w",encoding="utf-8").write(body)
    PAGES.append((pg.path, pg.h1, pg.title))
PAGES=[]

# ---------------------------------------------------------------- сторінки лiг
def league_pages(key):
    lg=LEAGUES[key]; N=lg["name"]; G=lg["gen"]; base=[("Головна",""),(N,key)]
    groups = lg.get("groups")
    # ---- хаб
    pg=Page(key, f"{lg['full']} {lg['season']}: таблиця, календар, новини — Футбол України",
            f"{lg['full']} {lg['season']}: турнірна таблиця, найближчі матчі, результати туру, бомбардири та останні новини.",
            f"{lg['full']} {lg['season']}", base, key)
    if groups:
        nxt=[(g, [m for m in ms if not m[4]][:4]) for g,ms in lg["dates"]]
        last=[(g, [m for m in ms if m[4] and m[4]!="перенесено"][-4:]) for g,ms in lg["dates"]]
        board="".join(f'<div class="board__group"><h3>{E(g)}</h3>{match_rows(ms)}</div>' for g,ms in nxt)
        board_title="Наступні матчі, 24 жовтня"
        results="".join(f'<h3 class="h3">{E(g)}</h3>{match_rows(ms)}' for g,ms in last)
        mini="".join(f'<h3 class="h3">{E(g)}</h3>'+table_html(lg, rows[:4], compact=True) for g,rows in groups)
    else:
        nr=[r for r in lg["rounds"] if not r[1]][0]; lr=[r for r in lg["rounds"] if r[1]][-1]
        board=match_rows(nr[2]); board_title=f"{nr[0]}-й тур"
        results=match_rows(lr[2]); mini=table_html(lg, lg["table"][:6], compact=True)
    faq_h, faq_ld = faq_block(lg["faq"])
    sc = demo_scorers(lg)[:5]
    rows_all = lg.get("table") or groups[0][1]
    played = max(r[1] for r in rows_all); tot = lg["rounds_total"]
    bar=f'<span class="season-bar" role="img" aria-label="Зіграно {played} з {tot} турів"><span style="width:{played*100//tot}%"></span></span>'
    if groups: ld_txt=" і ".join(f'{crest(r[1][0][0])} {E(r[1][0][0])}' for r in groups) ; ld_lbl="Лідери груп"
    else: ld_txt=f'{crest(rows_all[0][0])} {E(rows_all[0][0])}, {pts_word(rows_all[0][7])}'; ld_lbl="Лідер"
    stats=[(ld_lbl, ld_txt),("Сезон", f'{played} з {tot} турів {bar}')]
    body=head(pg,[faq_ld])+league_band(pg,key,lg,"",pg.h1, lg["intro"], stats=stats)+f'''
<main id="main" class="wrap">
  <section class="board" aria-labelledby="board-h">
    <div class="board__head"><h2 id="board-h">{E(board_title)}</h2><a href="{pg.u(key+"/calendar")}">Календар {E(G)}</a></div>
    {board if groups else f'<div class="board__group">{board}</div>'}
  </section>
  <div class="grid">
    <div class="grid__main">
      <section class="panel" aria-labelledby="news-h">
        <div class="panel__head"><h2 id="news-h">Новини</h2><a href="{pg.u(key+"/news")}">Усі новини {E(G)}</a></div>
        {news_list(pg,key,lg["news"],5,big=True)}
      </section>
      <section class="panel" aria-labelledby="res-h">
        <div class="panel__head"><h2 id="res-h">{"Останні результати" if groups else f"Результати {lr[0]}-го туру"}</h2><a href="{pg.u(key+"/calendar")}">Усі тури</a></div>
        {results}
      </section>
    </div>
    <aside class="grid__side">
      <section class="panel" aria-labelledby="tbl-h">
        <div class="panel__head"><h2 id="tbl-h">Таблиця</h2><a href="{pg.u(key+"/table")}">Повна таблиця</a></div>
        {mini}
      </section>
      <section class="panel" aria-labelledby="sc-h">
        <div class="panel__head"><h2 id="sc-h">Бомбардири</h2><a href="{pg.u(key+"/bombardyry")}">Усі бомбардири</a></div>
        <ol class="toplist" data-source="api:topscorers">{"".join(f'<li><span class="toplist__name">{E(n)}<small>{crest(c)}{E(c)}</small></span><span class="toplist__val">{g}</span></li>' for n,c,m,g,p in sc)}</ol>
        <p class="devnote">Приклад заповнення, дані з API.</p>
      </section>
    </aside>
  </div>
  <section class="about" aria-labelledby="about-h">
    <h2 id="about-h">Про турнір</h2>
    <div class="faq">{faq_h}</div>
  </section>
</main>
'''+foot(pg); write(pg,body)

    # ---- новини
    pg=Page(key+"/news", f"Новини {G} {lg['season']} — Футбол України", f"Усі новини {G}: результати, огляди матчів, коментарі тренерів і гравців, трансфери клубів.",
            f"Новини {G}", base+[("Новини",key+"/news")], key)
    body=head(pg)+league_band(pg,key,lg,"news",pg.h1)+f'''
<main id="main" class="wrap narrow">
  {news_list(pg,key,lg["news"],big=True,thumbs=True)}
  {pagination(pg,key+"/news",lg["pages"])}
</main>
'''+foot(pg); write(pg,body)

    # ---- таблиця
    pg=Page(key+"/table", f"Турнірна таблиця {G} {lg['season']} — Футбол України",
            f"Турнірна таблиця {G} {lg['season']}: очки, різниця м'ячів, зони єврокубків, підвищення і пониження. Оновлюється після кожного матчу.",
            f"Турнірна таблиця {G}", base+[("Таблиця",key+"/table")], key)
    if groups: tb="".join(f'<section class="panel"><h2 class="panel__title">{E(g)}</h2>{table_html(lg,rows)}</section>' for g,rows in groups)
    else: tb=f'<section class="panel">{table_html(lg,lg["table"])}</section>'
    body=head(pg)+league_band(pg,key,lg,"table",pg.h1)+f'''
<main id="main" class="wrap narrow">
  <p class="updated">Оновлено <time datetime="2026-10-19T15:17">19 жовтня 2026, 15:17</time></p>
  {tb}
  {legend(lg)}
  <p class="abbr">І — ігри, В — виграші, Н — нічиї, П — поразки, М — забиті і пропущені м'ячі, ± — різниця, О — очки.</p>
</main>
'''+foot(pg); write(pg,body)

    # ---- календар
    pg=Page(key+"/calendar", f"Календар {G} {lg['season']}: розклад матчів і результати — Футбол України",
            f"Розклад матчів {G} {lg['season']} по турах: дати, час початку, результати зіграних матчів.",
            f"Календар {G} {lg['season']}", base+[("Календар",key+"/calendar")], key)
    if groups:
        cal="".join(f'<section class="panel"><h2 class="panel__title">{E(g)}</h2>{match_rows(ms)}</section>' for g,ms in lg["dates"])
        strip=""
    else:
        have={r[0]:r for r in lg["rounds"]}; cur=[r[0] for r in lg["rounds"] if not r[1]][0]
        strip='<nav class="rounds" aria-label="Тури"><ol>'+"".join(
            f'<li><a href="#tur-{n}" class="{"is-current" if n==cur else ""}{" is-played" if n<cur else ""}"{" aria-current=\"true\"" if n==cur else ""}>{n}</a></li>' for n in range(1,lg["rounds_total"]+1))+'</ol></nav>'
        cal="".join(f'<section class="panel round" id="tur-{n}"><h2 class="panel__title">{n}-й тур{"" if p else " <small>заплановано</small>"}</h2>{match_rows(ms)}</section>' for n,p,ms in lg["rounds"])
    body=head(pg)+league_band(pg,key,lg,"calendar",pg.h1)+f'''
<main id="main" class="wrap narrow">
  {strip}
  {cal}
  <p class="devnote">У шаблоні показано 4 тури. На сайті виводяться всі тури сезону з API (fixtures by season), сторінка відкривається на поточному турі.</p>
</main>
'''+foot(pg); write(pg,body)

    # ---- бомбардири
    pg=Page(key+"/bombardyry", f"Бомбардири {G} {lg['season']}: найкращі снайпери — Футбол України",
            f"Список найкращих бомбардирів {G} {lg['season']}: голи, пенальті, кількість матчів і результативність за гру.",
            f"Бомбардири {G} {lg['season']}", base+[("Бомбардири",key+"/bombardyry")], key)
    arch = f'<p class="archive">Попередні сезони: <a href="{pg.u(key+"/bombardyry/2025-2026")}">2025/26</a></p>' if key=="upl" else ""
    body=head(pg)+league_band(pg,key,lg,"bombardyry",pg.h1)+f'''
<main id="main" class="wrap narrow">
  <section class="panel">{scorers_table(demo_scorers(lg),demo=True)}</section>
  {arch}
</main>
'''+foot(pg); write(pg,body)

for k in LEAGUES: league_pages(k)

# ---- архів бомбардирів УПЛ 2025/26
lg=LEAGUES["upl"]
pg=Page("upl/bombardyry/2025-2026","Бомбардири УПЛ 2025/26: підсумки сезону — Футбол України",
        "Найкращі бомбардири УПЛ сезону 2025/26: голи, пенальті та результативність гравців.",
        "Бомбардири УПЛ 2025/26",[("Головна",""),("УПЛ","upl"),("Бомбардири","upl/bombardyry"),("2025/26","upl/bombardyry/2025-2026")],"upl")
body=head(pg)+league_band(pg,"upl",dict(lg,season="2025/26"),"bombardyry",pg.h1)+f'''
<main id="main" class="wrap narrow">
  <p class="archive">Архів сезону. Поточний сезон: <a href="{pg.u("upl/bombardyry")}">бомбардири УПЛ 2026/27</a></p>
  <section class="panel">{scorers_table(UPL_SC_ARCH)}</section>
  <p class="devnote">Рядки перенесені зі старої сторінки /bombardyry-upl-2025-2026/ як є. Перед запуском замінити повною підсумковою таблицею сезону з API (season_id 2025/26).</p>
</main>
'''+foot(pg); write(pg,body)

# ---------------------------------------------------------------- Збірна
def zb_rows(ms):
    out=""
    for d,t,h,a,s,c in ms:
        mid=f'<span class="m__score">{s}</span>' if s else f'<span class="m__time">{t}</span>'
        out+=f'<li class="m{" m--played" if s else ""}"><time class="m__date">{d[:5]}<small>{E(c)}</small></time><span class="m__home"><span class="m__name">{E(h)}</span>{crest(h)}</span>{mid}<span class="m__away">{crest(a)}<span class="m__name">{E(a)}</span></span></li>'
    return f'<ul class="matches matches--wide">{out}</ul>'
zlg=dict(season="2026/27")
ztabs=[("","Огляд"),("news","Новини"),("calendar","Календар")]
zbase=[("Головна",""),("Збірна України","zbirna-ukrayiny")]
zfaq=[("Хто головний тренер збірної України?","Андреа Мальдера. Італієць очолив команду в травні 2026 року після Сергія Реброва."),
      ("У якій групі Ліги націй грає Україна?","У групі 2 Ліги B разом з Угорщиною, Грузією та Північною Ірландією."),
      ("Де збірна проводить домашні матчі?","Через війну домашні ігри проходять за кордоном. Місце кожного матчу вказане в календарі.")]
pg=Page("zbirna-ukrayiny","Збірна України з футболу: матчі, результати, новини — Футбол України",
        "Національна збірна України: найближчі матчі Ліги націй 2026/27, результати, склад і головні новини команди.",
        "Збірна України з футболу",zbase,"zbirna-ukrayiny")
fh,fl=faq_block(zfaq)
n=ZB["upcoming"][0]
body=head(pg,[fl])+league_band(pg,"zbirna-ukrayiny",zlg,"",pg.h1,"Головний тренер — Андреа Мальдера. Восени 2026 року команда грає в групі 2 Ліги B Ліги націй.",ztabs)+f'''
<main id="main" class="wrap">
  <section class="board board--single" aria-labelledby="board-h">
    <div class="board__head"><h2 id="board-h">Наступний матч</h2><a href="{pg.u("zbirna-ukrayiny/calendar")}">Календар збірної</a></div>
    <div class="nextmatch">
      <span class="nextmatch__team">{crest(n[2],True)}{E(n[2])}</span>
      <span class="nextmatch__mid"><span class="nextmatch__time">{n[1]}</span><time>{n[0]}</time><small>{E(n[5])}</small></span>
      <span class="nextmatch__team">{crest(n[3],True)}{E(n[3])}</span>
    </div>
  </section>
  <div class="grid">
    <div class="grid__main">
      <section class="panel"><div class="panel__head"><h2>Новини</h2><a href="{pg.u("zbirna-ukrayiny/news")}">Усі новини збірної</a></div>{news_list(pg,"zbirna-ukrayiny",ZB["news"],5,big=True)}</section>
    </div>
    <aside class="grid__side">
      <section class="panel"><div class="panel__head"><h2>Результати</h2><a href="{pg.u("zbirna-ukrayiny/calendar")}">Усі матчі</a></div>{zb_rows(list(reversed(ZB["results"])))}</section>
    </aside>
  </div>
  <section class="about"><h2>Про збірну</h2><div class="faq">{fh}</div></section>
</main>
'''+foot(pg); write(pg,body)

pg=Page("zbirna-ukrayiny/news","Новини збірної України з футболу — Футбол України","Новини збірної України: склад, матчі Ліги націй, травми та коментарі тренерського штабу.",
        "Новини збірної України",zbase+[("Новини","zbirna-ukrayiny/news")],"zbirna-ukrayiny")
body=head(pg)+league_band(pg,"zbirna-ukrayiny",zlg,"news",pg.h1,None,ztabs)+f'<main id="main" class="wrap narrow">{news_list(pg,"zbirna-ukrayiny",ZB["news"],big=True,thumbs=True)}{pagination(pg,"zbirna-ukrayiny/news",ZB["pages"])}</main>'+foot(pg); write(pg,body)

pg=Page("zbirna-ukrayiny/calendar","Календар збірної України 2026/27: розклад матчів і результати — Футбол України",
        "Розклад матчів збірної України з футболу: Ліга націй 2026/27, товариські ігри, дати, час початку та результати.",
        "Календар збірної України",zbase+[("Календар","zbirna-ukrayiny/calendar")],"zbirna-ukrayiny")
body=head(pg)+league_band(pg,"zbirna-ukrayiny",zlg,"calendar",pg.h1,None,ztabs)+f'''
<main id="main" class="wrap narrow">
  <section class="panel"><h2 class="panel__title">Майбутні матчі</h2>{zb_rows(ZB["upcoming"])}</section>
  <section class="panel"><h2 class="panel__title">Зіграні матчі</h2>{zb_rows(list(reversed(ZB["results"])))}</section>
  <p class="devnote">Час київський. Дані з API (fixtures by team). Нові турніри (відбір, товариські) з'являються автоматично.</p>
</main>
'''+foot(pg); write(pg,body)

# ---------------------------------------------------------------- Трансфери (рубрика-стрічка, без /news/)
pg=Page("transfery-ukrayiny","Трансфери України: новини, чутки, підписання — Футбол України",
        "Трансферні новини українського футболу: підписання, оренди, чутки та офіційні переходи гравців УПЛ і збірної.",
        "Трансфери України",[("Головна",""),("Трансфери","transfery-ukrayiny")],"transfery-ukrayiny")
body=head(pg)+f'''<div class="band"><div class="wrap"><div class="band__title"><h1>Трансфери України</h1></div>
<p class="band__lead">Переходи, оренди та чутки про гравців українських клубів і легіонерів збірної.</p></div></div>
<main id="main" class="wrap narrow">
  {news_list(pg,"transfery-ukrayiny",TRANSFERS,big=True,thumbs=True)}
  {pagination(pg,"transfery-ukrayiny",296)}
  <p class="devnote">Окрему сторінку /transfery-ukrayiny/news/ не створюємо: вона веде 301 сюди, доки не з'явиться трансферна таблиця. Статті живуть за адресою /transfery-ukrayiny/news/{"{slug}"}/.</p>
</main>
'''+foot(pg); write(pg,body)

# ---------------------------------------------------------------- шаблон статті
slug="polissya-majzhe-ves-match-u-menshosti-vyrvalo-volovu-peremogu-nad-dynamo-kyyiv-u-matchi-upl"
t="Полісся майже весь матч у меншості вирвало вольову перемогу над Динамо Київ у матчі УПЛ"
pg=Page(f"upl/news/{slug}", t+" — Футбол України", "Шаблон сторінки статті: заголовок, дата, картка матчу, текст, теги та блоки з таблицею й іншими новинами рубрики.",
        t,[("Головна",""),("УПЛ","upl"),("Новини","upl/news"),(t,f"upl/news/{slug}")],"upl")
art_ld={"@context":"https://schema.org","@type":"NewsArticle","headline":t,"datePublished":"2026-10-18T19:01:00+03:00","inLanguage":"uk","publisher":{"@type":"Organization","name":"Футбол України"}}
body=head(pg,[art_ld])+f'''
<main id="main" class="wrap">
  <div class="grid">
    <article class="grid__main article">
      <p class="article__rubric"><a href="{pg.u("upl/news")}">Новини УПЛ</a></p>
      <h1>{E(t)}</h1>
      <p class="article__meta"><time datetime="2026-10-18T19:01">18 жовтня 2026, 19:01</time> <span>Автор: <a href="#">Ім'я автора</a></span></p>
      <div class="matchcard" data-source="api:fixture">
        <span class="matchcard__team">{crest("Полісся",True)}Полісся</span>
        <span class="matchcard__score">3:1</span>
        <span class="matchcard__team">Динамо{crest("Динамо",True)}</span>
        <span class="matchcard__meta">УПЛ, 9-й тур, 18 жовтня 2026</span>
      </div>
      <div class="article__body">
        <p class="devnote">Тут виводиться текст статті з WordPress (the_content). Картка матчу вище з'являється, якщо до статті прив'язаний матч.</p>
        <h2>Підзаголовок у тексті</h2>
        <p>Абзаци статті мають ширину до 70 знаків у рядку, щоб текст легко читався з телефона і з комп'ютера.</p>
      </div>
      <ul class="tags"><li><a href="#">Полісся</a></li><li><a href="#">Динамо</a></li><li><a href="{pg.u("upl/calendar")}">9-й тур</a></li></ul>
    </article>
    <aside class="grid__side">
      <section class="panel"><div class="panel__head"><h2>Таблиця УПЛ</h2><a href="{pg.u("upl/table")}">Повна таблиця</a></div>{table_html(lg,lg["table"][:6],compact=True)}</section>
      <section class="panel"><div class="panel__head"><h2>Ще новини</h2><a href="{pg.u("upl/news")}">Усі</a></div>{news_list(pg,"upl",[x for x in lg["news"] if x[1]!=slug],4)}</section>
    </aside>
  </div>
</main>
'''+foot(pg); write(pg,body)

# ---------------------------------------------------------------- індекс шаблонів
idx=Page("", "Шаблони сторінок — Футбол України", "Перелік шаблонів нової структури сайту.", "Шаблони сторінок нової структури", [("Головна","")], "")
rows="".join(f'<tr><td><a href="{idx.u(p)}">/{p}/</a></td><td>{E(h)}</td></tr>' for p,h,_ in sorted(PAGES))
body=head(idx)+f'''<div class="band"><div class="wrap"><div class="band__title"><h1>Шаблони сторінок нової структури</h1></div>
<p class="band__lead">Сторінки з вкладки «301 основа». Дані актуальні на 19.10.2026, у робочій версії їх підставляє WordPress і API.</p></div></div>
<main id="main" class="wrap narrow"><section class="panel"><div class="tbl-scroll"><table class="standings index"><thead><tr><th scope="col" class="c-team">Адреса на сайті</th><th scope="col" class="c-team">Сторінка</th></tr></thead><tbody>{rows}</tbody></table></div></section></main>
'''+foot(idx)
open(os.path.join(OUT,"index.html"),"w",encoding="utf-8").write(body)
print(len(PAGES),"pages")
