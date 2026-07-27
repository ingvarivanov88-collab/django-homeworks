import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name="Иван Петров", birth_date="2000-01-01")


@pytest.fixture
def course(student):
    course = Course.objects.create(name="Математика")
    course.students.add(student)
    return course


@pytest.mark.django_db
def test_create_course(api_client, student):
    url = reverse('courses-list')
    data = {
        "name": "Физика",
        "students": [student.id]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.first().name == "Физика"


@pytest.mark.django_db
def test_get_courses_list(api_client, course):
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Математика"


@pytest.mark.django_db
def test_get_single_course(api_client, course):
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == "Математика"
    assert len(response.data['students']) == 1


@pytest.mark.django_db
def test_update_course(api_client, course, student):
    url = reverse('courses-detail', args=[course.id])
    data = {
        "name": "Физика",
        "students": [student.id]
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "Физика"


@pytest.mark.django_db
def test_delete_course(api_client, course):
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == 0