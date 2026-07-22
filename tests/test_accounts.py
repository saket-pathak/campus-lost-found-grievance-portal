import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation_roles():
    student = User.objects.create_user(username='student1', password='pass', role='student')
    staff = User.objects.create_user(username='staff1', password='pass', role='staff')
    admin = User.objects.create_superuser(username='admin1', password='pass', email='a@a.com')
    admin.role = 'admin'
    admin.save()
    
    assert student.is_student is True
    assert staff.is_staff_user is True
    assert admin.is_admin_user is True
    
    assert User.objects.students().count() == 1
    assert User.objects.staff().count() == 1
    assert User.objects.admins().count() == 1

@pytest.mark.django_db
def test_login_view(client):
    user = User.objects.create_user(username='testuser', password='password123', role='student')
    login_url = reverse('accounts:login')
    
    # GET login page
    response = client.get(login_url)
    assert response.status_code == 200
    
    # POST login correct with username
    response = client.post(login_url, {'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 302
    
    # Logout before testing email login
    client.logout()
    response = client.post(login_url, {'username': 'testuser@example.com', 'password': 'password123'})
    assert response.status_code == 200

    user = User.objects.get(username='testuser')
    user.email = 'testuser@example.com'
    user.save()

    response = client.post(login_url, {'username': 'testuser@example.com', 'password': 'password123'})
    assert response.status_code == 302
    
    # Logout before testing incorrect login
    client.logout()
    response = client.post(login_url, {'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert "correct username and password" in response.content.decode()


@pytest.mark.django_db
def test_register_view(client):
    register_url = reverse('accounts:register')
    
    # GET register page
    response = client.get(register_url)
    assert response.status_code == 200
    
    # POST register correct
    data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'newuser@example.com',
        'role': 'student',
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
    }
    response = client.post(register_url, data)
    assert response.status_code == 302
    assert '/accounts/register/success/' in response.url
    
    # Verify user exists in database
    assert User.objects.filter(username='newuser').exists()
