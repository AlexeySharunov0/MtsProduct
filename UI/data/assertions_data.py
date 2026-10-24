from UI.utils.EnvProvider import EnvProvider


class ProductsAsserts:
    productName = [
        'МТС Маркетолог',
        "Виртуальная АТС",
        # "1C",
        "8-800",
        # "Beffo",
        "Call-center",
    ]

    rusSearchPattern_to_productName = [
        ('Маркетолог', 'МТС Маркетолог'),
        ('Марк', 'МТС Маркетолог'),
        ('марк', 'МТС Маркетолог'),
        ("АТС", 'Виртуальная АТС'),
        ("Умный", 'МТС Умный дом'),
    ]

    engSearchPattern_to_productName = [
        ('vfhr', 'МТС Маркетолог'),
        ('Vfhr', 'МТС Маркетолог'),
        ('Vfhrtnjkju', 'МТС Маркетолог'),
        ("FNC", 'Виртуальная АТС'),
        # ("Voice", 'Voice платформа'),
        # ("Voice", 'VoiceBot'),
    ]

    oracleID_to_productName = [
        ('MAfi', 'МТС Live (МТС Афиша)/VR'),
        ('MusM', 'МТС Music'),
        ('UDom', 'МТС Умный дом'),
    ]

    FIO_to_productList = [
        ('Бартеньев', ['E-sensor']),
        ('Филимонова', ['МТС Маркетолог']),
        ('Ahjkjdf', ['МТС Маркетолог']),
        ('Фрол', ['МТС Маркетолог']),
        ('Ahjk', ['МТС Маркетолог']),
    ]

    Old_name_to_new = [
        ('test ctujvso', 'Новое название'),
        ('test fqvxtna', 'Новое название1'),
        ('test oalxxlb', 'Новое название2')
    ]

    showcase = [
        ('Марс', 'МТС Поиск'),
        ('Юпитер', 'МТС Music'),
        ('Уран', 'Сайт МТС')
    ]

    atomicProducts = [
        'MTS Social ads',
        # 'Containerum Managed Kubernetes',
        # 'Гео-онлайн триггеры на фемтосотах',
        'Таргетированный обзвон',
        'МТС Маркетолог. Скоринг',
        # 'МТС Маркетолог. Подготовка креатива',
    ]

    BI_to_productList = [
        ('BI_1287', 'E-sensor'),
        ('BI_60', 'МТС Маркетолог'),
        ('BI_1883', 'MTS Social ads'),
        ('BI_1921', '1C'),
    ]

    code_bi_to_productList = [
        ('1287', 'E-sensor'),
        ('60', 'МТС Маркетолог'),
        ('1883', 'MTS Social ads'),
        ('1921', '1C'),
    ]

    filterText = [
        "Рынок",
        "Web, app",
        "Бренд МТС",
        "Инициировано закрытие",
        "Легкий старт",
    ]

    filter_value = ['Выбрать всё\n206',
                    'Алтухов Александр Николаевич\n3',
                    'Анисимов Роман Эдуардович\n1',
                    'Асламов Иван Александрович\n7',
                    'Бартеньев Алексей Игоревич\n1',
                    'Барсуков Иван Михайлович\n2',
                    'Бирюков Андрей Александрович\n2',
                    'Брянцева Ирина Геннадьевна\n2',
                    'Бурмистров Данила Сергеевич\n18',
                    'Веденина Дарья Игоревна\n9',
                    'Виленская Нина Викторовна\n3',
                    'Гладышева Алёна Ивановна\n1',
                    'Гриценко Артем Юрьевич\n3',
                    'Гурьянов Кирилл Игоревич\n4',
                    'Еремин Федор Сергеевич\n2',
                    'Ерохина Яна Викторовна\n1',
                    'Журавлева Алина Алексеевна\n1',
                    'Зубцов Максим Андреевич\n2',
                    'Исаченко Максим Сергеевич\n1',
                    'Кандауров Виктор Викторович\n1',
                    'Комарин Сергей Александрович\n1',
                    'Комарин Сергей Александрович\n1',
                    'Комарин Сергей Александрович\n1',
                    'Копытин Сергей Сергеевич\n1',
                    'Кузнецова Ольга Андреевна\n1',
                    'Курбатова Вероника Викторовна\n2',
                    'Лесникова Наталья Олеговна\n1',
                    'Лоскутов Артем Андреевич\n1',
                    'Луконина Наталья Игоревна\n1',
                    'Лысенко Михаил Геннадьевич\n3',
                    'Мазов Алексей Валентинович\n4',
                    'Мазурин Данила Николаевич\n2',
                    'Максаков Роман Геннадьевич\n1',
                    'Мартынова Екатерина Анатольевна\n2',
                    'Медников Анатолий Владимирович\n2',
                    'Мельничук Николай Николаевич\n5',
                    'Мирошников Максим Анатольевич\n1',
                    'Наумова Татьяна Васильевна\n1',
                    'Нестеров Илья Игоревич\n32',
                    'Пальцев Кирилл Викторович\n6',
                    'Петряков Максим Олегович\n1',
                    'Платонов Андрей Валентинович\n10',
                    'Поляков Михаил Сергеевич\n2',
                    'Ремизова Элина Александровна\n1',
                    'Рыбакова Евгения Владимировна\n1',
                    'Светиков Илья Денисович\n9',
                    'Светов Даниил Дмитриевич\n2',
                    'Селезнева Ирина Сергеевна\n1',
                    'Старцев Дмитрий Олегович\n1',
                    'Струнина Анна Александровна\n1',
                    'Тарасова Юлия Александровна\n2',
                    'Трунов Юрий Владимирович\n1',
                    'Улитин Денис Олегович\n3',
                    'Фарапонов Владимир Николаевич\n5',
                    'Фадеева Мария Ивановна\n4',
                    'Фомина Анна Игоревна\n1',
                    'Черкасова Татьяна Евгеньевна\n2',
                    'Чухин Игорь Владимирович\n2',
                    'Чухин Игорь Владимирович\n4',
                    'Шаталова Елена Владимировна\n2',
                    'Шкурин Данила Андреевич\n9',
                    'Щербинин Сергей Александрович\n1',
                    'Эрлих Михаил Анатольевич\n1',
                    'Якимов Сергей Юрьевич\n6',
                    'Ярцева Елена Николаевна\n1']

    filter_value2 = ['Выбрать всё\n206',
                     'Алтухов Александр Николаевич\n3',
                     'Анисимов Роман Эдуардович\n1',
                     'Асламов Иван Александрович\n7',
                     'Бартеньев Алексей Игоревич\n1',
                     'Барсуков Иван Михайлович\n2',
                     'Бирюков Андрей Александрович\n2',
                     'Брянцева Ирина Геннадьевна\n2',
                     'Бурмистров Данила Сергеевич\n18',
                     'Веденина Дарья Игоревна\n9',
                     'Виленская Нина Викторовна\n3',
                     'Гладышева Алёна Ивановна\n1',
                     'Гриценко Артем Юрьевич\n3',
                     'Гурьянов Кирилл Игоревич\n4',
                     'Еремин Федор Сергеевич\n2',
                     'Ерохина Яна Викторовна\n1',
                     'Журавлева Алина Алексеевна\n1',
                     'Зубцов Максим Андреевич\n2',
                     'Исаченко Максим Сергеевич\n1',
                     'Кандауров Виктор Викторович\n1',
                     'Комарин Сергей Александрович\n1',
                     'Комарин Сергей Александрович\n1',
                     'Комарин Сергей Александрович\n1',
                     'Копытин Сергей Сергеевич\n1',
                     'Кузнецова Ольга Андреевна\n1',
                     'Курбатова Вероника Викторовна\n2',
                     'Лесникова Наталья Олеговна\n1',
                     'Лоскутов Артем Андреевич\n1',
                     'Луконина Наталья Игоревна\n1',
                     'Лысенко Михаил Геннадьевич\n3',
                     'Мазов Алексей Валентинович\n4',
                     'Мазурин Данила Николаевич\n2',
                     'Максаков Роман Геннадьевич\n1',
                     'Мартынова Екатерина Анатольевна\n2',
                     'Медников Анатолий Владимирович\n2',
                     'Мельничук Николай Николаевич\n5',
                     'Мирошников Максим Анатольевич\n1',
                     'Наумова Татьяна Васильевна\n1',
                     'Нестеров Илья Игоревич\n32',
                     'Пальцев Кирилл Викторович\n6',
                     'Петряков Максим Олегович\n1',
                     'Платонов Андрей Валентинович\n10',
                     'Поляков Михаил Сергеевич\n2',
                     'Ремизова Элина Александровна\n1',
                     'Рыбакова Евгения Владимировна\n1',
                     'Светиков Илья Денисович\n9',
                     'Светов Даниил Дмитриевич\n2',
                     'Селезнева Ирина Сергеевна\n1',
                     'Старцев Дмитрий Олегович\n1',
                     'Струнина Анна Александровна\n1',
                     'Тарасова Юлия Александровна\n2',
                     'Трунов Юрий Владимирович\n1',
                     'Улитин Денис Олегович\n3',
                     'Фарапонов Владимир Николаевич\n5',
                     'Фадеева Мария Ивановна\n4',
                     'Фомина Анна Игоревна\n1',
                     'Черкасова Татьяна Евгеньевна\n2',
                     'Чухин Игорь Владимирович\n4',
                     'Чухин Игорь Владимирович\n2',
                     'Шаталова Елена Владимировна\n2',
                     'Шкурин Данила Андреевич\n9',
                     'Щербинин Сергей Александрович\n1',
                     'Эрлих Михаил Анатольевич\n1',
                     'Якимов Сергей Юрьевич\n6',
                     'Ярцева Елена Николаевна\n1']

    ID_to_productName = [
        ('BI_60', 'МТС Маркетолог'),
        # ('BI_63', '8-800'),
        ('BI_234', 'Cloud Gaming'),
        ('BI_22', 'GOODOK'),
        # ('BI_19', 'KION (OTT)'),
        # ('BI_41', 'Мой МТС'),
    ]

    ID_to_category_to_productName = [
        ('BI_60', 'external', 'МТС Маркетолог'),
        # ('BI_63', 'external', '8-800'),
        ('BI_234', 'external', 'Cloud Gaming'),
        ('BI_22', 'external', 'GOODOK'),
        # ('BI_19', 'external', 'KION (OTT)'),
        # ('BI_41', 'external', 'Мой МТС'),
    ]

    linkToProduct = [
        (EnvProvider.getBaseUrl() + '/product/BI_60/docs'),
        (EnvProvider.getBaseUrl() + '/product/BI_105/docs'),
        (EnvProvider.getBaseUrl() + '/product/BI_234/docs'),
        (EnvProvider.getBaseUrl() + '/product/BI_22/docs'),
    ]

    linkToProductsWithAtomic = [
        (EnvProvider.getBaseUrl() + '/product/BI_60/atomic'),
        (EnvProvider.getBaseUrl() + '/product/BI_105/atomic')
    ]

    linkToProductsWithNoAtomic = [
        (EnvProvider.getBaseUrl() + '/product/BI_234/atomic'),
        (EnvProvider.getBaseUrl() + '/product/BI_22/atomic')
    ]

    linkToDifferentAtomic = [
        (EnvProvider.getBaseUrl() + '/product/BI_60/atomic'),
        (EnvProvider.getBaseUrl() + '/product/BI_22/atomic')
    ]

    linkToAtomicProduct = [
        EnvProvider.getBaseUrl() + '/product/BI_1883/main',
        EnvProvider.getBaseUrl() + '/product/BI_1884/main'
    ]

    linkToExternalProduct = [
        (EnvProvider.getBaseUrl() + '/product/BI_60/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_49/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_22/main'),
        # (EnvProvider.getBaseUrl() + '/product/BI_41/main-info'),
    ]

    linkToInternalProduct = [
        (EnvProvider.getBaseUrl() + '/product/BI_1905/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_1863/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_1921/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_267/main'),
    ]

    linkToMainForAtomicProduct = [
        EnvProvider.getBaseUrl() + '/product/BI_60/atomic'
    ]

    linkToInternalAndExternal = [
        (EnvProvider.getBaseUrl() + '/product/BI_60/main'),
        (EnvProvider.getBaseUrl() + '/product/BI_1905/main')
    ]

    linksToDevelopmentType = [
        ['https://stage.prodboard.example.com/product/BI_241/main', 'Вендорская разработка'],
        ['https://stage.prodboard.example.com/product/BI_19/main', 'Собственная разработка']
    ]

    access_types = ['public', 'closed']

    metrics_description = 'В разделе представлены метрики продукта из Единого дашборда метрик ДФК, а также приведены ссылки, при нажатии на которые можно перейти в профильные дашборды сразу на страницу продукта. Единый дашборд метрик отображается для следующих ролей данного продукта: Вице-президент, Business Owner, Chief Product Owner, Product Owner, сотрудник с предоставленным доступом к данному разделу.\nЗАПРОСИТЬ ДОСТУП'

    metrics_error = 'Сбор метрик ДФК по продукту в процессе разработки. По вопросам добавления продукта на дашборд обращайтесь на ProductDashboard@example.com'

    docs_description = 'В разделе представлены документы, связанные с продуктом: приказы на запуск в Пилот, запуск в Коммерческую эксплуатацию, паспорта критичности и многое другое.'

    docs_error = 'Документы не добавлены'

    atomic_description = 'В разделе представлен список продуктов, входящих в основной продукт.'

    atomic_error = 'Атомарные продукты не указаны'

    project_description = 'В разделе представлен список проектов и заявок из различных систем, направленных на доработку и выделение финансирования по продукту.\nТакже можно перейти в профильные системы и получить дополнительную информацию о заявке, проекте.'

    project_oebs_description = 'Раздел находится в стадии разработки. Выгрузка в Excel будет добавлена позднее. По всем вопросам обращайтесь на ppinfo@example.com'

    eco_description = 'Экосистемный продуктовый модуль (ЭПМ) - продукт, унифицирующий взаимодействие клиента с экосистемой или реализацию продуктовой задачи. В разделе представлена информация о статусах интеграции продукта с ЭПМ. Информация консолидируется из Jira, где команда продукта указывает зависимости по реализации задач командам экосистемных продуктовых модулей.'

    epm_description = 'В разделе представлена информация о наличии/отсутствии интеграции экосистемного продуктового модуля с продуктами. Информация консолидируется из Jira, где команда продукта указывает зависимости на реализации задач командам экосистемных продуктовых модулей.'

    eco_error = 'Интеграция с Экосистемными продуктовыми модулями отсутствует'

    software_description = 'В разделе представлен список приложений, которые входят в состав продукта (источник SAM), а также информационных систем, привязанных к указанным приложениям (источник IMS).\nДля корректировки информации по приложениям необходимо перейти в Архитектурный репозиторий.\nРаздел выстроен на основе принятой в компании метамодели.'

    software_error = 'У продукта нет действующих приложений'

    product_guide_description = 'В разделе представлена инструкция по жизненному циклу данного продукта в компании, от момента разработки концепции до закрытия продукта (при необходимости) с учетом шагов по разработке и масштабированию. Раздел предназначен для владельца продукта и команды разработки.\nИнструкция уникальна для каждого продукта и зависит от типа продукта (внутренний/внешний), типа разработки и других атрибутов.'

    product_guide_error = 'Шаги пока не добавлены'

    ordered_statuses = ['  Запущен в КЭ', '  Разработка', '  Ожидание решения', '  Запуск пилота',
                        '  Формирование идеи',
                        '  Выведен из КЭ', '  Запуск отменен']

    faq_link = 'https://confluence.example.com/pages/viewpage.action?pageId=1037189507#:~:text=5.%20%D0%9A%D0%B0%D0%BA%20%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%20%D0%B2%20PPInfo%3F%20%D0%9A%D0%B5%D0%BC%20%D0%BF%D1%80%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%B5%D1%82%D1%81%D1%8F%20%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%20%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B8%20%D0%B2%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0%3F%20%D0%9A%D0%B0%D0%BA%20%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%20%D0%B1%D0%B0%D0%BD%D0%BA%D0%B0%3F'


class CatalogueAssertions:
    important_attributes_list = ["Бренд МТС", "Chief product owner", "Senior Product Owner", "QBR Memo",
                                 "Вице-президент",
                                 "Инициировано закрытие", "Легкий старт", "Название продукта", "Рынок", "Уровень QBR"]


class NewsAssertions:
    invalid_names = [" ", "test_test_test_test_test_test_test_test_test_test_test_test_test"]
    invalid_descriptions = [" ",
                            "test_test_test_test_test_test_test_ttest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testest_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_ttest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testest_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_ttest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testest_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_testtest_test_test_test_test_test_test_test_test_test_test_test_test"]
