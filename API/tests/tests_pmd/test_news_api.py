import os

import allure
import pytest

from API.models.pmd.internal_news_v1 import NewsApi


@pytest.mark.api
@allure.feature('Новости')
class TestNewsApi(NewsApi):

    @allure.title('Создание новости, картинки png/PNG/jpg/JPG/svg/SVG')
    @pytest.mark.parametrize('image_format', ('png', 'PNG', 'jpg', 'JPG', 'svg', 'SVG'))
    def test_create_news_pic(self, news_admin_client, news_public_client, image_format):
        with allure.step(f'Создаем картинку с форматом {image_format}'):
            image = self.create_image(image_format)

        new_id = self.create_new(news_admin_client, self.get_news_data(), image)
        with allure.step('Проверяем, что новость создалась'):
            assert self.get_new_by_id(news_public_client, new_id), f'Новости с айди {new_id} не существует'

        self.delete_new_by_id(news_admin_client, new_id)

        os.remove(f'example.{image_format}')

    @allure.title('Создание новости с пустым/слишком большим названием')
    @pytest.mark.parametrize('invalid_name', (' ',
                                              'status_codeststatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codest'))
    def test_create_new_invalid_name(self, news_admin_client, invalid_name):
        image = self.create_image('PNG')

        self.create_new_400(news_admin_client, self.get_news_data({'name': invalid_name}), image)

        os.remove('example.PNG')

    @allure.title('Корректное редактирование заголовка и текста новости')
    def test_edit_correct_news_tittle_and_text(self, news_admin_client):
        self.patch_new_by_id(news_admin_client, '264ec288-bc20-46f9-a2d1-7f641077e51c', self.get_news_data())

    @allure.title('Корректное обновление картинки новости')
    def test_update_correct_news_image(self, news_admin_client):
        image = self.create_image('PNG')

        self.get_change_image(news_admin_client, '264ec288-bc20-46f9-a2d1-7f641077e51c', image)

        os.remove('example.PNG')

    @allure.title('Корректное редактирование статуса активности новости')
    @pytest.mark.parametrize('status', (True, False))
    def test_edit_correct_news_status_active(self, news_admin_client, news_public_client, status):
        self.patch_new_by_id(news_admin_client, '264ec288-bc20-46f9-a2d1-7f641077e51c',
                             self.get_news_data({'isActive': status}))
        with allure.step('Проверяем, что новость появилась в списке неактивных'):
            assert any(
                item['id'] == '264ec288-bc20-46f9-a2d1-7f641077e51c' for item in
                self.get_all_news(news_public_client, status)['news']), 'В списке неактивных такой новости нет'

    @allure.title('Некорректное редактирование новости пустым/слишком большим названием')
    @pytest.mark.parametrize('invalid_name', (' ',
                                              'status_codeststatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codestatus_codestatus_codestatus_codestatus_codestatqqstatus_codest'))
    def test_edit_new_invalid_name(self, news_admin_client, invalid_name):
        self.patch_new_by_id_400(news_admin_client, '264ec288-bc20-46f9-a2d1-7f641077e51c',
                                 self.get_news_data({"name": invalid_name}))

    @allure.title('Получение всех новостей')
    def test_get_all_news(self, news_public_client):
        self.get_all_news(news_public_client)

    @allure.title('Получение активных/неактивных новостей')
    @pytest.mark.parametrize('status', (True, False))
    def test_get_active_news(self, news_public_client, status):
        self.get_all_news(news_public_client, status)

    @allure.title('Получение картинки по id новости')
    def test_image_by_news_id(self, news_public_client):
        self.get_image_by_id(news_public_client, '264ec288-bc20-46f9-a2d1-7f641077e51c')

    @allure.title('Получение дефолтной картинки')
    def test_api_get_news_default_image(self, news_public_client):
        self.get_default_image(news_public_client)

    @allure.title('Проверка работа свапа новостей')
    @pytest.mark.parametrize(('old_number', 'new_number'), ([1, 2], [2, 1]))
    def test_swap_news(self, news_admin_client, news_public_client, old_number, new_number):
        swap_data = self.get_news_swap_data(news_public_client, old_number, new_number)
        with allure.step(f'Проверяем работу свапа новости с номером {old_number} на новость с номером {new_number}'):
            self.swap_news(news_admin_client, swap_data)
            assert self.get_all_news(news_public_client)['news'][new_number - 1]['id'] == swap_data[
                'id'], 'Новость не переместилась'
