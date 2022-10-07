import pytest
from rest_framework.reverse import reverse
from students.models import Course


@pytest.mark.django_db
def test_get_course(api_client, course_factory, student_factory):
    students = student_factory(_quantity=5)
    course = course_factory(students=students)
    url = reverse(f'courses-detail', kwargs={'pk': course.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name
    for j, s in enumerate(data['students']):
        assert s == course.students.all()[j].id


@pytest.mark.django_db
def test_get_courses(api_client, course_factory, student_factory):
    courses = course_factory(_quantity=4, students=student_factory(_quantity=10))
    url = reverse(f'courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name
        for j, s in enumerate(c['students']):
            assert s == courses[i].students.all()[j].id


@pytest.mark.django_db
def test_filter_courses_id(api_client, course_factory, student_factory):
    courses = course_factory(_quantity=4, students=student_factory(_quantity=10))
    url = reverse(f'courses-list') + f'?id={courses[1].id}'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == courses[1].name


@pytest.mark.django_db
def test_filter_courses_name(api_client, course_factory, student_factory):
    courses = course_factory(_quantity=4, students=student_factory(_quantity=10))
    url = reverse(f'courses-list') + f'?name={courses[2].name}'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_create_course(api_client, course_factory, student_factory):
    url = '/api/v1/courses/'
    count = Course.objects.count()
    response = api_client.post(url, data={'name': 'Django course #1'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert response.json()['name'] == 'Django course #1'


@pytest.mark.django_db
def test_update_course(api_client, course_factory, student_factory):
    students = student_factory(_quantity=5)
    course = course_factory(students=students)
    url = '/api/v1/courses/' + f'{course.id}/'
    new_name = 'Django course #1'
    response = api_client.patch(url, data={'name': new_name})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_name


@pytest.mark.django_db
def test_delete_course(api_client, course_factory, student_factory):
    students = student_factory(_quantity=5)
    course = course_factory(students=students)
    url = '/api/v1/courses/' + f'{course.id}/'
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Course.objects.filter(id=course.id).count() == 0
