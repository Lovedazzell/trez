from django.contrib.auth.base_user import BaseUserManager


# custom manager

class UserManager(BaseUserManager):

    use_in_migrations: True

    def create_user(self,email,password,**extra_fields):
        if not  email:
            raise ValueError('Email must be required')
        email = self.normalize_email(email)
        user = self.model(email = email ,  **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff status must be True for superuser')
        
        return self.create_user(email,password,**extra_fields)