from app.models.user import User

def test_user_model_fields(new_user):
    assert new_user.username == "testuser"
    assert new_user.email == "test@example.com"
    assert new_user.role == "student"

def test_user_to_dict(new_user):
    data = new_user.to_dict()
    assert 'username' in data
    assert data['email'] == "test@example.com"
