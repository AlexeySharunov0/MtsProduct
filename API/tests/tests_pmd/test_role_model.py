import allure
import pytest

from API.models.pmd.admin_role_model import RoleModelApi


@pytest.mark.api
@allure.feature('Роли')
class TestRoleModelApi(RoleModelApi):

    @allure.title('Получение всех ролей')
    def test_get_roles(self, pmd_admin_rest_client):

        self.get_roles(pmd_admin_rest_client)

    @allure.title('Создание и удаление роли')
    @pytest.mark.parametrize("is_active", (True, False))
    def test_add_and_delete_role(self, pmd_admin_gw_client, pmd_admin_rest_client, is_active):

        role_id = self.create_role(pmd_admin_gw_client, self.get_new_role_data(is_active=is_active))

        with allure.step('Проверяем, что роль создалась'):
            self.get_role_by_id(pmd_admin_rest_client, role_id)

        self.delete_role(pmd_admin_gw_client, role_id)

        with allure.step('Проверяем, что роль удалилась'):
            self.get_role_by_id_404(pmd_admin_rest_client, role_id)

    @allure.title('Создание роли с некорректным флагом')
    def test_add_invalid_flag(self, pmd_admin_gw_client):

        self.create_role_400(pmd_admin_gw_client, self.get_new_role_data(is_active='билеберда'))

    @allure.title('Создание роли с граничными значениями в названии')
    @pytest.mark.parametrize('name_role', ['',
                                           'wdasdasdasdasdwdasdasd asdasdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'])
    def test_add_invalid_name_role(self, pmd_admin_gw_client, name_role):

        self.create_role_400(pmd_admin_gw_client, self.get_new_role_data(name=name_role))

    @allure.title('Удаление несуществующей роли')
    def test_delete_invalid_role(self, pmd_admin_gw_client):

        self.delete_role_400(pmd_admin_gw_client, '4d2a20e7-4609-414a-9604-ae18b0a15c04')

    @allure.title('Изменение статуса активности у роли')
    @pytest.mark.parametrize('is_active', (True, False))
    def test_replace_active_status(self, pmd_admin_gw_client, pmd_admin_rest_client, is_active):

        params = self.get_new_role_data(name='Еще одна группа для тестов (не трогать)', is_active=is_active)

        self.patch_role_status(pmd_admin_gw_client, self.role_id, params)

        with allure.step(f'Проверяем, что статус активности изменился на {is_active}'):
            assert self.get_role_by_id(pmd_admin_rest_client, self.role_id)[
                       'isActive'] is is_active, f'Текущий статус - {not is_active}'

    @allure.title('Невалидное изменение статуса активности у роли')
    def test_replace_active_invalid_status(self, pmd_admin_gw_client):

        params = self.get_new_role_data(name='Еще одна группа для тестов (не трогать)', is_active='труляля')

        self.patch_role_status_400(pmd_admin_gw_client, self.role_id, params)

    @allure.title('Изменение названия у роли')
    def test_replace_role_name(self, pmd_admin_gw_client, pmd_admin_rest_client):

        role_id = self.create_role(pmd_admin_gw_client, self.get_new_role_data())

        params = self.get_new_role_data(name='тест12345')

        self.patch_role_status(pmd_admin_gw_client, role_id, params)

        with allure.step(f'Проверяем, что имя изменилось'):
            assert self.get_role_by_id(pmd_admin_rest_client, role_id)[
                       'name'] == 'тест12345', f"Текущее имя - {self.get_role_by_id(role_id)['name']}"

        self.delete_role(pmd_admin_gw_client, role_id)

    @allure.title('Невалидное изменение названия у роли')
    @pytest.mark.parametrize('name_role', ['',
                                           'wdasdasdasdasdwdasdasd asdasdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdwdasdasdasdasdqq'])
    def test_replace_role_invalid_name(self, pmd_admin_gw_client, name_role):

        params = self.get_new_role_data(name=name_role)

        self.patch_role_status_400(pmd_admin_gw_client, self.role_id, params)

    @allure.title('Получение роли по логину')
    @pytest.mark.parametrize('login', ['aikostrov1', 'ddsvetov1', 'dpsazonov3'])
    def test_get_roles_by_login(self, pmd_admin_gw_client, login):
        with allure.step('Проверяем, что найденный список непустой'):
            assert self.get_role_by_login(pmd_admin_gw_client, login), 'Ролей по указанному логину не нашлось'

    @allure.title('Получение роли по несуществующему логину')
    @pytest.mark.parametrize('login', ['йцуйцуйцу', '123123', 'qweqweqweqweqwe'])
    def test_get_roles_by_invalid_login(self, pmd_admin_gw_client, login):

        with allure.step('Проверяем, что вернулся пустой список'):
            assert not self.get_role_by_login(pmd_admin_gw_client, login)[
                'roles'], f'Найдены {self.get_role_by_login(pmd_admin_gw_client, login)["roles"]}'

    @allure.title('Изменение атрибутов в роли')
    @pytest.mark.parametrize('attr_id',
                             ('0f4375d8-2a2c-42b9-8aa9-e0e2e6c5bcdb', '794c8bc5-90ad-4642-9575-5c124b6c47fa'))
    @pytest.mark.parametrize("is_editable, is_view, is_owned_view", [(True, True, False), (False, False, True)])
    def test_add_attr_in_role(self, pmd_admin_gw_client, pmd_admin_rest_client, attr_id, is_editable, is_view, is_owned_view):

        data = self.get_data_for_manage(
            {'attributeId': attr_id, 'isEditable': is_editable, 'isView': is_view, 'isOwnedView': is_owned_view})

        self.manage_attr(pmd_admin_gw_client, self.role_id, data)

        cur_attr = \
        [i for i in self.get_role_by_id(pmd_admin_rest_client, self.role_id)['attributes'] if i['id'] == attr_id][0]

        flags = []
        for key in data['updateAttributes'][0].keys():
            if key != 'attributeId':
                if data['updateAttributes'][0][key] != cur_attr[key]:
                    flags.append(key)

        with allure.step('Проверяем, что все поля нужного атрибута обновились'):
            assert not flags, f'Следующие поля не обновились: {flags}'

    @allure.title('Добавление атрибутов в несуществуюющую роль')
    def test_add_attr_in_invalid_role(self, pmd_admin_gw_client):

        data = self.get_data_for_manage()

        self.manage_attr_400(pmd_admin_gw_client, '4d2a20e7-4609-414a-a604-ae18b0a5c04', data)

    @allure.title('Добавление несуществующего атрибута в роль')
    def test_add_invalid_attr_in_role(self, pmd_admin_gw_client):

        data = self.get_data_for_manage({'attributeId': '0555575d8-2a2c-42b9-8aa9-e0e2e6c5bca'})

        self.manage_attr_400(pmd_admin_gw_client, self.role_id, data)

    @allure.title('Добавление юзера в роль и удаление его от туда')
    def test_add_user_in_role(self, pmd_admin_gw_client ,pmd_admin_rest_client):

        self.add_user_role(pmd_admin_gw_client, self.role_id, 'ddsvetov1')

        with allure.step('Проверяем, что юзер добавился в роль'):
            assert any(
                i['login'] == 'ddsvetov1' for i in self.get_role_by_id(pmd_admin_rest_client, self.role_id)['users'])

        self.delete_user_from_role(pmd_admin_gw_client, 'ddsvetov1', {'roleId': self.role_id})

    @allure.title('Добавление юзера в несуществующую роль')
    def test_add_user_in_invalid_role(self, pmd_admin_gw_client):

        self.add_user_role_400(pmd_admin_gw_client, '12a35eea-7777-4d12-89d2-019640284cfd', 'ddsvetov1')

    @allure.title('Добавление несуществующего пользователя в роль')
    def test_add_invalid_user_in_role(self, pmd_admin_gw_client):

        self.add_user_role_404(pmd_admin_gw_client, self.role_id, 'йцуйцуйцуйцу')

    @allure.title('Добавление юзера в роль в которой он уже присутствует')
    def test_duplicate_add_user_in_role(self, pmd_admin_gw_client, pmd_admin_rest_client):
        try:
            self.add_user_role(pmd_admin_gw_client, self.role_id, 'ddsvetov1')

            with allure.step('Проверяем, что юзер добавился в роль'):
                assert any(
                    i['login'] == 'ddsvetov1' for i in self.get_role_by_id(pmd_admin_rest_client, self.role_id)['users'])

            self.add_user_role_400(pmd_admin_gw_client, '12a35eea-7777-4d12-89d2-019640284cfd', 'ddsvetov1')

        finally:
            self.delete_user_from_role(pmd_admin_gw_client, 'ddsvetov1', {'roleId': self.role_id})

    @allure.title('Получение всех пользователей')
    def test_add_invalid_user_in_role(self, pmd_admin_gw_client, ppinfo_user_client):

        self.get_users(pmd_admin_gw_client)

    @allure.title('Роль "Контролёр направления бизнеса"')
    @allure.issue('https://jira.mts.ru/browse/PPI-4315',
                  'PPInfo - Роль "Контролёр направления бизнеса" (админка)')
    def test_role_for_business_direction(self, pmd_admin_rest_client, pmd_admin_gw_client, ppinfo_user_client):



        self.manage_role_and_user_business_direction_attributes(pmd_admin_gw_client, True)

        for attr_name in self.get_attributes_ids().keys():
            for attr in self.get_info_by_product_code_by_user(ppinfo_user_client, 'BI_224')['hidingAttributes']:
                if attr['name'] == attr_name:
                    assert attr['editable'], f'Атрибут {attr_name} не доступе для редактирования в роли "Контролёр направления бизнеса"'


        self.manage_role_and_user_business_direction_attributes(pmd_admin_gw_client, False)



        for attr_name in self.get_attributes_ids().keys():
            for attr in self.get_info_by_product_code_by_user(ppinfo_user_client, 'BI_224')['hidingAttributes']:
                if attr['name'] == attr_name:
                    assert not attr[
                        'editable'], f'Атрибут {attr_name} доступен для редактирования в роли "Контролёр направления бизнеса"'




