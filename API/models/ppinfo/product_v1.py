from typing import Any, Dict

import allure
from faker.providers.person.ru_RU import translit

from API.data.ppinfo import AttributesForFilters, Davinci, InformationSystems
from API.models.pmd.internal_product_v1 import InternalV1ProductUrls
from API.models.ppinfo.product_v2 import ProductV2
from API.utils.generate import Gen

HOST = 'https://stage.prodboard.example.com'


class ProductV1Urls:
    # Не работает
    '''
    https://stage.prodboard.example.com/ppinfo/swagger/v1/product/index.html 
    '''
    # Добавление продукта
    ADD_PRODUCT = 'v1/product'

    # Изменение атрибута внутри продукта
    REPLACE_PRODUCT = 'v1/product'

    # Запрос нужен для создания продукта и смены типа продукта. Он отправляется первым сразу после нажатия на кнопку Создать, после чего фронт берет нужные ему атрибуты и создает продукт.
    SPECIFICATION = 'v1/product/specification'

    # VALIDATE = urljoin(HOST, '/ppinfo/gw/api/v1/product/validate') # Паша сказал, пока не удалять, но не используется

    # Удаление логотипа
    DELETE_LOGO = 'v1/product/{}/logo'

    # Получение проектов davinci
    DAVINCI = 'v1/product/{}/davinci'

    # Получение информационных систем и приложений для раздела тех состав
    INFORMATION_SYSTEMS = 'v1/system/information_systems/{}'


class ProductV1(ProductV1Urls, InternalV1ProductUrls, ProductV2):

    @property
    def text(self):
        return Gen.generate_text(7) + 'test'

    # @property
    def attr_storage(self, bi_code: str = 'BI_2769'):
        return {
            #### Строки
            'string_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_showcase',
                        'values': [{'code': 'test', 'value': 'test'}],
                    }
                ],
            },
            'string_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_showcase',
                        'values': [{'code': 'test2', 'value': 'test2'}],
                    }
                ],
            },
            'string_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPInfo_showcase', 'values': []}],
            },
            #### Мэниселект
            'manyselect_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_StructuralProductType1',
                        'values': [
                            {
                                'code': '(PPInfo_spravochnic_Structural)Main',
                                'value': 'Основной',
                            }
                        ],
                    }
                ],
            },
            'manyselect_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_StructuralProductType1',
                        'values': [
                            {
                                'code': '(PPInfo_spravochnic_Structural)Atomic',
                                'value': 'Атомарный',
                            }
                        ],
                    }
                ],
            },
            'manyselect_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPinfo_StructuralProductType1', 'values': []}],
            },
            #### Дата
            'date_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_start_close_date',
                        'values': [
                            {
                                'code': '2024-01-23T03:00:00Z',
                                'value': '2024-01-23T03:00:00Z',
                            }
                        ],
                    }
                ],
            },
            'date_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_start_close_date',
                        'values': [
                            {
                                'code': '2024-01-24T03:00:00Z',
                                'value': '2024-01-24T03:00:00Z',
                            }
                        ],
                    }
                ],
            },
            'date_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPinfo_start_close_date', 'values': []}],
            },
            #### Число
            'num_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Identifikator_SOL',
                        'values': [{'code': '666', 'value': '666'}],
                    }
                ],
            },
            'num_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Identifikator_SOL',
                        'values': [{'code': '777', 'value': '777'}],
                    }
                ],
            },
            'num_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Identifikator_SOL', 'values': []}],
            },
            #### Юзер
            "user_add": {"id": bi_code, "attributes": [{"id": "employee_business_owner", "values": [
                {"code": "admin_user", "value": "Светов Даниил Дмитриевич"}]}]},
            "user_replace": {"id": bi_code, "attributes": [{"id": "employee_business_owner", "values": [
                {"code": "aigladyshev", "value": "Гладышева Алёна Ивановна"}]}]},
            "user_remove": {"id": bi_code, "attributes": [{"id": "employee_business_owner", "values": []}]},

            #### Множество
            'multi_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Mnozhestvo',
                        'values': [
                            {'code': 'Vtoroi', 'value': 'Второй'},
                            {'code': 'Pervyi', 'value': 'Первый'},
                            {'code': 'Tretii', 'value': 'Третий'},
                        ],
                    }
                ],
            },
            'multi_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Mnozhestvo',
                        'values': [{'code': 'Vtoroi', 'value': 'Второй'}],
                    }
                ],
            },
            'multi_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Mnozhestvo', 'values': []}],
            },
            #### Мультиюзер
            'multiuser_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Rukovoditel_etogo_balagana',
                        'values': [
                            {'code': 'pymaslenkov', 'value': 'Масленков Павел Юрьевич'},
                            {'code': 'admin_user', 'value': 'Светов Даниил Дмитриевич'},
                            {'code': 'regular_user', 'value': 'Костров Алексей Игоревич'},
                        ],
                    }
                ],
            },
            'multiuser_replace_minus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Rukovoditel_etogo_balagana',
                        'values': [
                            {'code': 'pymaslenkov', 'value': 'Масленков Павел Юрьевич'},
                            {'code': 'admin_user', 'value': 'Светов Даниил Дмитриевич'},
                        ],
                    }
                ],
            },
            'multiuser_replace_plus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Rukovoditel_etogo_balagana',
                        'values': [
                            {'code': 'pymaslenkov', 'value': 'Масленков Павел Юрьевич'},
                            {'code': 'admin_user', 'value': 'Светов Даниил Дмитриевич'},
                            {'code': 'regular_user', 'value': 'Костров Алексей Игоревич'},
                        ],
                    }
                ],
            },
            'multiuser_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Rukovoditel_etogo_balagana', 'values': []}],
            },
            #### ОдинПродукт
            'product_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Odin_produkt',
                        'values': [{'code': 'BI_60', 'value': 'МТС Маркетолог'}],
                    }
                ],
            },
            'product_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Odin_produkt',
                        'values': [
                            {'code': 'BI_25', 'value': 'Kaspersky Security для МТС'}
                        ],
                    }
                ],
            },
            'product_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Odin_produkt', 'values': []}],
            },
            #### МультиПродукт
            'multiproduct_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Mnogo_produktov',
                        'values': [
                            {'code': 'BI_270', 'value': 'GPS-Трекер с МТС Поиск'},
                            {'code': 'BI_25', 'value': 'Kaspersky Security для МТС'},
                            {'code': 'BI_1901', 'value': 'Весь МТС'},
                            {'code': 'BI_1972', 'value': 'Весь МТС Полный дом'},
                        ],
                    }
                ],
            },
            'multiproduct_replace_minus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Mnogo_produktov',
                        'values': [
                            {'code': 'BI_1972', 'value': 'Весь МТС Полный дом'},
                            {'code': 'BI_270', 'value': 'GPS-Трекер с МТС Поиск'},
                            {'code': 'BI_25', 'value': 'Kaspersky Security для МТС'},
                        ],
                    }
                ],
            },
            'multiproduct_replace_plus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Mnogo_produktov',
                        'values': [
                            {'code': 'BI_25', 'value': 'Kaspersky Security для МТС'},
                            {'code': 'BI_1972', 'value': 'Весь МТС Полный дом'},
                            {'code': 'BI_270', 'value': 'GPS-Трекер с МТС Поиск'},
                            {'code': 'BI_1984', 'value': 'МТС Маркетолог. Скоринг'},
                        ],
                    }
                ],
            },
            'multiproduct_remove': {
                'id': 'BI_2769',
                'attributes': [{'id': 'Mnogo_produktov', 'values': []}],
            },
            #### МультиСсылка
            'multilink_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Test_mnozh_ssylki',
                        'values': [
                            {'code': 'Линк1', 'value': 'Название ссылки1'},
                            {'value': 'Название ссылки2', 'code': 'Линк2'},
                        ],
                    }
                ],
            },
            'multilink_replace_minus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Test_mnozh_ssylki',
                        'values': [{'code': 'Линк1', 'value': 'Название ссылки1'}],
                    }
                ],
            },
            'multilink_replace_plus': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Test_mnozh_ssylki',
                        'values': [
                            {'code': 'Линк1', 'value': 'Название ссылки1'},
                            {'value': 'Название ссылки2', 'code': 'Линк2'},
                        ],
                    }
                ],
            },
            'multilink_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Test_mnozh_ssylki', 'values': []}],
            },
            #### Многострочный текст
            'multistring_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_resolution',
                        'values': [{'code': 'test', 'value': 'test'}],
                    }
                ],
            },
            'multistring_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPinfo_resolution',
                        'values': [{'code': 'test2', 'value': 'test2'}],
                    }
                ],
            },
            'multistring_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPinfo_resolution', 'values': []}],
            },
            #### Ссылка
            'link_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_site_landing',
                        'values': [{'code': 'https://cashback.example.com', 'value': ''}],
                    }
                ],
            },
            'link_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_site_landing',
                        'values': [
                            {
                                'code': 'https://stage.prodboard.example.com/product/BI_42/main',
                                'value': '',
                            }
                        ],
                    }
                ],
            },
            'link_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPInfo_site_landing', 'values': []}],
            },
            #### Основной продукт
            'main_product_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_main_product',
                        'values': [
                            {
                                'code': 'BI_2683',
                                'value': '1_Не трогать, для АТ, делегирование del',
                            }
                        ],
                    }
                ],
            },
            'main_product_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'PPInfo_main_product',
                        'values': [
                            {
                                'code': 'BI_3266',
                                'value': 'Не трогать (продукт для автотестов)',
                            }
                        ],
                    }
                ],
            },
            'main_product_remove': {
                'id': bi_code,
                'attributes': [{'id': 'PPInfo_main_product', 'values': []}],
            },
            #### Основной проект
            'main_project_jira_add': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Osnovnoi_proekt_Jira',
                        'values': [
                            {
                                'code': 'https://jira.example.com/browse/HRT',
                                'value': 'HR Tribe (HRT)',
                            }
                        ],
                    }
                ],
            },
            'main_project_jira_product_replace': {
                'id': bi_code,
                'attributes': [
                    {
                        'id': 'Osnovnoi_proekt_Jira',
                        'values': [
                            {
                                'code': 'https://jira.example.com/browse/ABPHRGATE',
                                'value': 'HRGATE (ABPHRGATE)',
                            }
                        ],
                    }
                ],
            },
            'main_project_jira_product_remove': {
                'id': bi_code,
                'attributes': [{'id': 'Osnovnoi_proekt_Jira', 'values': []}],
            },
        }

    @allure.step('Получение data для изменения атрибута')
    def get_attribute_update_body(
            self,
            type_of_data: str | list,
            notification: bool = False,
            bi_code: str | None = None,
    ) -> dict[str, Any]:

        data = (
            self.attr_storage(bi_code)[type_of_data]
            if bi_code
            else self.attr_storage()[type_of_data]
        )
        data.update({'notification': notification, 'type': ''})

        return data

    @allure.step('Проверка изменений')
    def check_updates(self, client_ppinfo, data: dict[str, Any]) -> None:
        with allure.step('Проверяем, что изменения действительно применились'):
            required_attr = [
                attr['values']
                for attr in self.get_info_by_product_code(client_ppinfo, 'BI_2769')[
                    'hidingAttributes'
                ]
                if attr['id'] == data['attributes'][0]['id']
            ]
        if required_attr:
            assert all(
                i in data['attributes'][0]['values'] for i in required_attr[0]
            ), f"{required_attr[0]} != {data['attributes'][0]['values']}"
        else:
            assert (
                    required_attr == data['attributes'][0]['values']
            ), f"{required_attr} != {data['attributes'][0]['values']}"

    @allure.step('Проверка структурного типа продукта')
    def check_structural_product_type(self, client_ppinfo, bi_code: str) -> str:
        '''
        Проверка структурного типа продукта
        Args:
            bi_code: Код продукта у которого будем смотреть Структурный тип продуктов
        Returns:
            Значение Структурного типа продукта
        '''
        with allure.step('Проверяем, что изменения действительно применились'):
            main_product = None

            for attr in self.get_info_by_product_code(client_ppinfo, bi_code)[
                'hidingAttributes'
            ]:
                if attr['id'] == 'PPinfo_StructuralProductType':
                    main_product = attr['values'][0]['value']

            return main_product

    @allure.step('Получение данных для создания продукта')
    def get_data_for_product_creation(self, product_type: str, name: str = None, descr: str = None,
                                      notification: bool = False, status: str = 'Arkhiv') -> dict[str, Any]:
        text = self.text
        data = {
            'name': name if name is not None else text,
            'description': descr if descr is not None else text,
            'attributes': [
                {
                    'id': 'EXTRA_ProductName',
                    'values': [{'value': name if name is not None else text}],
                },
                {
                    'id': 'EXTRA_ProductDescription',
                    'values': [{'value': descr if descr is not None else text}],
                },
                {'id': 'PPinfo_status', 'values': [{'value': status}]},
                {'id': 'R&D', 'values': [{'value': 'Maintenance_R&D'}]},
                {'id': 'Tip_obieekta_ucheta', 'values': [{'value': 'Platforma'}]},
                {'id': 'Napravlenie_gruppy', 'values': [{'value': 'Telekom'}]},
            ],
            'type': product_type,
            'notification': notification,
        }

        return data

    @allure.step('Добавление продукта')
    def create_product(self, client, data: dict[str, Any]) -> str:
        with allure.step(f"Создаем продукт с типом {data['type']}"):
            response = client.post(self.ADD_PRODUCT, json=data)

        return response['id']

    @allure.step('Добавление хаба')
    def get_data_for_hub_creation(self, name: str, product_type: str = 'Vneshnii', status: str = '(PPinfo_status)Idea_formation') -> dict[str, Any]:
        data = {
            'name': name,
            'description': 'test_description',
            'notification': False,
            'type': product_type,
            'attributes': [
                {'id': 'EXTRA_ProductName', 'values': [{'value': name}]},
                {'id': 'PPinfo_status', 'values': [{'value': status}]},
                {'id': 'R&D', 'values': [{'value': 'Growth_R&D'}]},
                {'id': 'Tip_obieekta_ucheta', 'values': [{'value': 'Khab'}]},
                {'id': 'Napravlenie_gruppy', 'values': [{'value': 'Fintekh'}]},
                {"id": "Kategoriia_khaba", "values": [{"value": "Ideia"}]},
                {"id": "Tip_obieekta_ucheta", "values": [{"value": "Khab"}]},
            ],
        }

        return data

    @allure.step('Создание хаба')
    def create_hub(self, client, data: Dict[str, Any]) -> str:
        data['isHub'] = True

        response = client.post(self.ADD_PRODUCT, json=data)

        if isinstance(response, dict) and 'id' in response:
            return response['id']
        else:
            raise RuntimeError(f"Не удалось создать хаб, ответ сервера: {response}")

    @allure.step('Невалидное добавление продукта')
    def error_create_product(self, client, data: dict[str, Any]) -> None:
        client.post(self.ADD_PRODUCT, json=data, expected_status_code=400)

    @allure.step('Удаление продукта')
    def delete_product(self, client, bi: str = 'BI_7099') -> dict[str, Any]:
        params = {'codeReason': 'Oshibochnoe_zavedenie', 'description': 'qwe'}

        response = client.delete(self.DELETE_PRODUCT.format(bi), params=params)

        return response

    @allure.step('Изменение атрибута внутри продукта')
    def change_product(self, client, data: dict[str, Any]) -> None:

        client.put(self.REPLACE_PRODUCT, json=data)

    @allure.step('Невалидное изменение атрибута внутри продукта')
    def error_change_product(
            self, client, data: dict[str, Any], status_code: int = 404
    ) -> None:
        with allure.step(f"Меняем атрибут{data['attributes'][0]['id']}"):
            client.put(
                self.REPLACE_PRODUCT, json=data, expected_status_code=status_code
            )

    @allure.step('Меняем статус продукта')
    def change_status(
            self, client, status_code: str, status_name: str, product_id: str = 'BI_2687'
    ):
        data = {
            'id': product_id,
            'attributes': [
                {
                    'id': 'PPinfo_status',
                    'values': [{'code': status_code, 'value': status_name}],
                }
            ],
            'notification': False,
            'type': '',
        }
        client.put(self.REPLACE_PRODUCT, json=data)

    @allure.step('Меняем статус инициировано закрытие')
    def change_start_closed(
            self, client, remove: bool = False, product_id: str = 'BI_2687'
    ):
        data = {
            'id': product_id,
            'attributes': [
                {
                    'id': 'PPinfo_start_close_date',
                    'values': [
                        {
                            'code': '2024-01-16T21:00:00.000Z',
                            'value': '2024-01-16T21:00:00.000Z',
                        }
                    ],
                },
                {
                    'id': 'PPinfo_start_close',
                    'values': (
                        [{'code': '(PPinfo_spravochnik_start_close)Yes', 'value': 'Да'}]
                        if not remove
                        else []
                    ),
                },
            ],
            'notification': False,
            'type': '',
        }
        client.put(self.REPLACE_PRODUCT, json=data)

    # применимые статусы дат: PPinfo_close_date, PPinfo_start_date_MVP,
    # PPinfo_finish_date_MVP, PPInfo_date_In_progress, PPInfo_date_Idea_formation, PPinfo_execution_date
    @allure.step('Смена даты статуса')
    def change_status_date(
            self,
            client,
            status_code: str,
            include_date: bool = True,
            product_id: str = 'BI_2687',
            date_days: str = '16',
    ):
        data = {
            'id': product_id,
            'attributes': [
                {
                    'id': status_code,
                    'values': (
                        [
                            {
                                'code': '2024-01-' + date_days + 'T21:00:00.000Z',
                                'value': '2024-01-' + date_days + 'T21:00:00.000Z',
                            }
                        ]
                        if include_date
                        else []
                    ),
                }
            ],
            'notification': False,
            'type': '',
        }
        client.put(self.REPLACE_PRODUCT, json=data)

    @allure.step('Меняем метки альфа тестирования')
    def change_alpha_testing(
            self,
            client,
            attribute_id: str,
            yes: bool = False,
            product_id: str = 'BI_3266',
            start: bool = False,
            end: bool = False,
    ):
        '''
        Смена метки альфа тестирования и даты его проведения
        Args:
            client: Client
            attribute_id: Имя атрибута, тут может быть Pilot и In_progress
            yes: Тут нужно указать True чтоб значение было да или False чтоб значение было нет
            product_id: BI код продукта
            start: Тут нужно указать True, чтоб указать дату старта альфа тестирования или False чтоб удалить дату
            end: Тут нужно указать True, чтоб указать дату старта альфа тестирования или False чтоб удалить дату
        '''
        data = {
            'id': product_id,
            'attributes': [
                {
                    'id': f"Alpha_{attribute_id}",
                    'values': [
                        {
                            'code': 'Da' if yes else 'Net',
                            'value': 'Да' if yes else 'Нет',
                        }
                    ],
                },
                {
                    'id': f"Data_start_alpha_{attribute_id}",
                    'values': (
                        [
                            {
                                'code': '2025-01-30T21:00:00.000Z',
                                'value': '2025-01-30T21:00:00.000Z',
                            }
                        ]
                        if start
                        else []
                    ),
                },
                {
                    'id': f"Data_finish_alpha_{attribute_id}",
                    'values': (
                        [
                            {
                                'code': '2025-02-27T21:00:00.000Z',
                                'value': '2025-02-27T21:00:00.000Z',
                            }
                        ]
                        if end
                        else []
                    ),
                },
            ],
            'notification': False,
            'type': '',
        }
        client.put(self.REPLACE_PRODUCT, json=data)

    @allure.step('Смена этапа PLM')
    def change_plm_stages(self, client, plm_stage: str, product_id: str = 'BI_2687'):

        data = {
            'id': product_id,
            'attributes': [
                {
                    'id': 'Etap_PLM',
                    'values': (
                        [
                            {
                                'code': (
                                    translit(plm_stage).replace(' ', '_')
                                    if 'MVP' not in plm_stage
                                    else 'Razrabotka_i_zapusk_MVP'
                                ),
                                # Потому что МВП написано по-английски и переводчик не справляется с этим
                                'value': plm_stage,
                            }
                        ]
                        if plm_stage
                        else []
                    ),
                }
            ],
            'notification': False,
            'type': '',
        }
        print(data)
        client.put(self.REPLACE_PRODUCT, json=data)

    @allure.step('Получение приложение и ИС')
    def get_ims_sam(self, client, code: str) -> dict[str, Any]:
        with allure.step(f"Получем ИС и приложение по code {code}"):
            response = client.get(self.INFORMATION_SYSTEMS.format(code))

        InformationSystems(**response)

        return response

    @allure.step('Невалидное получение приложений и ИС')
    def get_ims_sam_error(self, client, code: str):
        client.get(self.INFORMATION_SYSTEMS.format(code), expected_status_code=400)

    @allure.step('Получаем атрибуты по спецификации внешних')
    def get_attr_by_spec(self, client, product_type: str) -> dict[str, Any]:
        params = {'typeProduct': product_type}
        response = client.get(self.SPECIFICATION, params=params)

        AttributesForFilters(**response)

        return response

    @allure.step('Удаление логотипа')
    def delete_logo(self, client) -> None:
        client.delete(self.DELETE_LOGO.format('BI_2687'))

    @allure.step('Получение проектов давинчи')
    def get_davinci(self, client, bi_code) -> dict[str, Any]:
        with allure.step(f"Получем проекты давинчи по коду bi {bi_code}"):
            response = client.get(self.DAVINCI.format(bi_code))

        Davinci(**response)

        return response
