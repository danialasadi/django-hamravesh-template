from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self,phone_number , email , password ,**kwargs):



        if not phone_number :
            raise ValueError('Phone number must be entered')

        if not email :
            raise ValueError('email must be entered')

        if not password :
            raise ValueError('password must be entered')


        user = self.model(phone_number = phone_number , email = self.normalize_email(email) ,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self,phone_number,email,password,**kwargs):



        if not phone_number:
            raise ValueError('Phone number must be entered')

        if not email:
            raise ValueError('email must be entered')

        if not password:
            raise ValueError('password must be entered')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user




















    #
    #
    #
    # from django.contrib.auth.base_user import BaseUserManager
    #
    # class UserManager(BaseUserManager):
    #
    #     def create_user(self, phone_number, email, password, **kwargs):
    #         if not phone_number:
    #             raise ValueError('Phone number must be entered')
    #
    #         if not email:
    #             raise ValueError('Email must be entered')
    #
    #         if not password:
    #             raise ValueError('Password must be entered')
    #
    #         user = self.model(phone_number=phone_number, email=self.normalize_email(email), **kwargs)
    #         user.set_password(password)
    #         user.save(using=self._db)
    #         return user
    #
    #     def create_superuser(self, phone_number, email, password, **kwargs):
    #         kwargs.setdefault('is_staff', True)
    #         kwargs.setdefault('is_superuser', True)
    #
    #         return self.create_user(phone_number, email, password, **kwargs)
    #
    #
    #
    #
    #
    #
    #
    #








