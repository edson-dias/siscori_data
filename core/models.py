from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return self.email

    objects = UsuarioManager()


class Infos(models.Model):

    nome_prod = models.CharField('nome_prod', max_length=30, help_text='Máximo 30 caracteres')
    marca = models.CharField('marca', max_length=50)
    cod_marca = models.CharField('cod_marca', max_length=50)
    descricao = models.CharField('descricao', max_length=500)
    ncm = models.CharField('ncm', max_length=50)
    porto = models.CharField('porto', max_length=50)
    pa = models.CharField('pa', max_length=50)
    po = models.CharField('po', max_length=50)

    class Meta:
        verbose_name = 'Info'
        verbose_name_plural = 'Infos'

    def __str__(self):
        return self.nome_prod


class ValoresMensais(models.Model):
    mes = models.IntegerField('mes')
    ano = models.IntegerField('ano')
    quant = models.IntegerField('quant')
    valor = models.FloatField('valor', max_length=50)
    infos_prod = models.ForeignKey(Infos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Valor'
        verbose_name_plural = 'Valores'

    def __str__(self):
        return f'{self.mes}, {self.ano}, {self.infos_prod}'


class KeywordSiscori(models.Model):
    keywords = models.CharField('keywords', max_length=200)
    infos_prod = models.ForeignKey(Infos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return f'{self.keywords}, {self.infos_prod}'




