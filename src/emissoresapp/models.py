from django.db import models

# Create your models here.



class Emissor(models.Model):
    name = models.CharField(max_length=200 ,  default="emissor")
    cnpj = models.CharField(max_length=14 , primary_key=True)
    o2id = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name




class Email(models.Model):
    email = models.EmailField(max_length = 254)
    emissor = models.ForeignKey(Emissor, on_delete=models.CASCADE)
    TIPOS = [
        ('PMT', 'PMT'),
        ('CUSTO_CETIP', 'Custo Cetip'),
        ('POSICAO', 'Posicao'),
        ('COBRANCA', 'E-mail Faturamento'),
    ]
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='PMT',
    )
    def __str__(self):
        return self.email
