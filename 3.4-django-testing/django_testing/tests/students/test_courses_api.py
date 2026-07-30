import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура-фабрика для создания курсов."""

    def factory(**kwargs):
        return baker.make(Course, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    """Фикстура-фабрика для создания студентов."""

    def factory(**kwargs):
        return baker.make(Student, **kwargs)

    return factory


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    url = reverse('courses-list')
    data = {"name": "Новый курс"}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.first().name == "Новый курс"


@pytest.mark.django_db
def test_get_courses_list(course_factory, api_client):
    """Тест получения списка курсов."""
    course_factory(_quantity=3)
    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_get_single_course(course_factory, api_client):
    """Тест получения одного курса."""
    course = course_factory(name="Математика")
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == "Математика"


@pytest.mark.django_db
def test_filter_courses_by_id(course_factory, api_client):
    """Тест фильтрации списка курсов по ID."""
    courses = course_factory(_quantity=3)
    target_id = courses[0].id
    url = reverse('courses-list')
    response = api_client.get(url, {'id': target_id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_id


@pytest.mark.django_db
def test_filter_courses_by_name(course_factory, api_client):
    """Тест фильтрации списка курсов по названию."""
    course_factory(name="Python")
    course_factory(name="Django")
    url = reverse('courses-list')
    response = api_client.get(url, {'name': "Python"})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Python"


@pytest.mark.django_db
def test_update_course_put(course_factory, api_client, student_factory):
    """Тест полного обновления курса (PUT)."""
    course = course_factory(name="Старое имя")
    student = student_factory()
    url = reverse('courses-detail', args=[course.id])
    data = {
        "name": "Новое имя",
        "students": [student.id]
    }
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "Новое имя"


@pytest.mark.django_db
def test_update_course_patch(course_factory, api_client):
    """Тест частичного обновления курса (PATCH)."""
    course = course_factory(name="Старое имя")
    url = reverse('courses-detail', args=[course.id])
    data = {"name": "Обновленное имя"}
    response = api_client.patch(url, data, format='json')

    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "Обновленное имя"


@pytest.mark.django_db
def test_delete_course(course_factory, api_client):
    """Тест удаления курса."""
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == 0