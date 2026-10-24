import allure
import pytest

from API.models.ppinfo.brief import Brief


@pytest.mark.api
@allure.label('priority', 'Высокий')
@allure.feature('Заявки')
class TestBrief(Brief):

    ######################### Количество заявок

    @allure.title('Получение всех заявок по статусам')
    @pytest.mark.parametrize('brief_status', ['statusPublished', 'statusInWork', 'statusDone', 'statusDeclined'])
    def test_get_briefs(self, ppinfo_client, brief_status):

        self.get_briefs(ppinfo_client, self.get_briefs_params({'status': brief_status}))

    @allure.title('Получение всех заявок от лица пользователя')
    def test_get_user_briefs(self, ppinfo_user_client):
        self.get_briefs_user(ppinfo_user_client)

    @allure.title('Получение количества заявок по всем статусам')
    def test_get_brief_count(self, ppinfo_client):

        self.get_statuses_count(ppinfo_client)

    @allure.title('Сравнение реального числа заявок и чисел в каунтерах')
    @pytest.mark.parametrize('brief_status', ['statusPublished', 'statusInWork', 'statusDone', 'statusDeclined'])
    def test_assert_brief_count(self, ppinfo_client, brief_status):

        params = self.get_briefs_params({'status': brief_status})
        params_2 = self.get_briefs_params({'status': brief_status, 'isOwned': False})

        counter_value = [i['count'] for i in self.get_statuses_count(ppinfo_client)['statuses'] if i['status'] == brief_status]

        if brief_status != 'statusPublished':
            with allure.step('Проверяем, что кол-во заявок соответствует числу в каунтере'):
                assert (len(self.get_briefs(ppinfo_client, params)['briefs']) + len(self.get_briefs(ppinfo_client, params_2)['briefs']) ==
                        counter_value[
                            0]), (
                    f'Реальное число заявок: {len(self.get_briefs(ppinfo_client, params)["briefs"]) + len(self.get_briefs(ppinfo_client, params_2)["briefs"])},'
                    f' число в каунтере: {counter_value[0]}')
        else:
            with allure.step('Проверяем, что кол-во заявок соответствует числу в каунтере'):
                assert len(self.get_briefs(ppinfo_client, params)['briefs']) == counter_value[0], (
                    f'Реальное число заявок: {len(self.get_briefs(ppinfo_client, params)["briefs"]) + len(self.get_briefs(ppinfo_client, params_2)["briefs"])},'
                    f' число в каунтере: {counter_value[0]}')

    ######################### Комментарии

    @allure.title('Комментарий для инициатора на бриф')
    def test_comment_initiator(self, ppinfo_client, ppinfo_user_client):

        brief_id = self.create_brief_and_take_to_work(ppinfo_client, ppinfo_user_client)

        self.put_comment(ppinfo_client, brief_id, self.initiator_data)

        with allure.step('Проверяем, что комментарий появился'):
            assert self.get_brief_by_id(ppinfo_client, brief_id)['comments'][0][
                       'comment'] == 'qwe_initiator', (f'Текущий комментарий в заявке : '
                                                       f'{self.get_brief_by_id(ppinfo_client, brief_id)["comments"][0]["comment"]}')

    @allure.title('Комментарий для администратора на бриф')
    def test_comment_executor(self, ppinfo_client, ppinfo_user_client):

        brief_id = self.create_brief_and_take_to_work(ppinfo_client, ppinfo_user_client)

        self.put_comment(ppinfo_client, brief_id, self.executor_data)

        with allure.step('Проверяем, что комментарий появился'):
            assert self.get_brief_by_id(ppinfo_client, brief_id)['comments'][0]['comment'] == 'qwe_executor', (
                f'Текущий комментарий в заявке : '
                f'{self.get_brief_by_id(ppinfo_client, brief_id)["comments"][0]["comment"]}')

    ######################### Создание продуктов

    @allure.title('Согласование/отклонение заявки на внешний продукт')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_create_external_product(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('create_external_product', 'createProduct')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на внутренний продукт')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_create_internal_product(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('create_internal_product', 'createProduct')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### СТРОКА

    @allure.title('Согласование/отклонение заявки на редактирование продукта / стринга / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_string_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('string_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / стринга / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_string_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('string_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / стринга / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_string_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('string_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Мэни селект

    @allure.title('Согласование/отклонение заявки на редактирование продукта / мэни селект / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_manyselect_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('manyselect_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / мэни селект  / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_manyselect_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('manyselect_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / мэни селект  / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_manyselect_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('manyselect_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Дата

    @allure.title('Согласование/отклонение заявки на редактирование продукта / дата  / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_date_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('date_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / дата  / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_date_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('date_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / дата  / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_date_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('date_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Число

    @allure.title('Согласование заявки на редактирование продукта / число  / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_num_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('num_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / число  / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_num_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('num_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / число  / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_num_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('num_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Юзер

    @allure.title('Согласование/отклонение заявки на редактирование продукта / юзер  / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_user_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('user_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / юзер  / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_user_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('user_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / юзер  / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_user_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('user_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Множество

    @allure.title('Согласование/отклонение заявки на редактирование продукта / множество  / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multi_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multi_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / множество  / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multi_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multi_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / множество  / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multi_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multi_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Мультиюзер

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Мультиюзер  / add')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiuser_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiuser_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Мультиюзер  / replace - 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiuser_replace_minus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiuser_replace_minus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Мультиюзер  / replace + 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiuser_replace_plus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiuser_replace_plus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Мультиюзер  / remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-168',
                  'PPInfo - Множественный выбор в атрибуте с типом "Сотрудник"')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiuser_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiuser_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### ОдинПродукт

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Продукт  / add')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_product_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('product_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Продукт  / replace')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_product_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('product_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Продукт  / remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_product_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('product_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### МультиПродукт

    @allure.title("Согласование/отклонение заявки на редактирование продукта / МультиПродукт  / add")
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiproduct_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiproduct_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиПродукт  / replace - 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiproduct_replace_minus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiproduct_replace_minus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title("Согласование/отклонение заявки на редактирование продукта / МультиПродукт  / replace + 1")
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiproduct_replace_plus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiproduct_replace_plus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиПродукт  / remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-126',
                  'PPInfo - Отображение связанных продуктов на странице продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multiproduct_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multiproduct_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### МультиСсылка

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиСсылка  / add')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multilink_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multilink_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиСсылка  / replace - 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multilink_replace_minus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multilink_replace_minus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиСсылка  / replace + 1')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multilink_replace_plus(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multilink_replace_plus')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / МультиСсылка  / remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-666', 'PPInfo - Добавление ссылок (объединённая)')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multilink_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multilink_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Многострочный текст

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Многострочный текст / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multistring_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multistring_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Многострочный текст / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multistring_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multistring_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Многострочный текст / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_multistring_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('multistring_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    ######################### Ссылка

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Ссылка / add')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_link_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('link_add')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Ссылка / replace')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_link_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('link_replace')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

    @allure.title('Согласование/отклонение заявки на редактирование продукта / Ссылка / remove')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_link_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('link_remove')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)


    ############################ Основной проект


    @allure.title('Изменение атрибута в продукте / Основной проект jira/ add ')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_main_project_jira_add(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('main_project_jira_add', bi_code='BI_260')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)


    @allure.title('Изменение атрибута в продукте / Основной продукт/ replace ')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_main_project_jira_replace(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('main_project_jira_product_replace', bi_code='BI_260')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)


    @allure.title('Изменение атрибута в продукте / Основной продукт/ remove')
    @allure.issue('https://jira.mts.ru/browse/PPI-4125', 'PPInfo - Основной проект Jira продукта')
    @pytest.mark.parametrize('status', ['statusApproval', 'statusDeclined'])
    def test_brief_service_update_product_main_project_jira_remove(self, ppinfo_client, ppinfo_user_client, status):
        body = self.get_briefs_body('main_project_jira_product_remove', bi_code='BI_260')

        self.full_cycle(ppinfo_client, ppinfo_user_client, body, status)

