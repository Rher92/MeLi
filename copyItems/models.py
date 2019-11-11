from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=40, unique=True)
    user_id = models.CharField(max_length=40)
    access_token = models.CharField(max_length=100)
    app_id = models.CharField(max_length=100)
    app_secret_key = models.CharField(max_length=100)
    offset_query = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PublicationData(models.Model):
    account = models.ForeignKey(Account,
        on_delete=models.CASCADE)
    meli_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    category_id = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    currency_id = models.CharField(max_length=10)
    available_quantity = models.CharField(max_length=10)
    buying_mode = models.CharField(max_length=30)
    listing_type_id = models.CharField(max_length=30)
    video_id = models.CharField(max_length=100, null=True, blank=True)
    copy_item= models.CharField(max_length=100,
        null=True, blank=True)
    copy = models.BooleanField(default=True)

    def __str__(self):
        return 'Account:{0} /  Publication:{1} / \
        MeLi ID:{2}'.format(self.account.name, self.title, self.meli_id)


class Attributes(models.Model):
    id_attributes = models.CharField(max_length=30, null=True)
    value_attributes = models.CharField(max_length=30, null=True)
    publication_data = models.ForeignKey(PublicationData,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.value_attributes


class SalesTerm(models.Model):
    id_sale_terms = models.CharField(max_length=30)
    sale_terms = models.CharField(max_length=30)
    value_id_terms = models.CharField(max_length=30, null=True)
    publication_data = models.ForeignKey(PublicationData,
        on_delete=models.CASCADE)    

    def __str__(self):
        return self.sale_terms


class Pictures(models.Model):
    source = models.CharField(max_length=100)
    publication_data = models.ForeignKey(PublicationData,
        on_delete=models.CASCADE)    

    def __str__(self):
        return self.source        


class Description(models.Model):
    description = models.TextField()
    publication_data = models.ForeignKey(PublicationData,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class OrigintoCopy(models.Model):
    account_origin = models.CharField(max_length=100)
    account_copy = models.CharField(max_length=100)         
    pub_id_origin = models.CharField(max_length=100)
    pub_id_Copy = models.CharField(max_length=100)

    def __str__(self):
        return ('Account Origen: {} - Account Copy:{} / Pub Origin:{} - Pub Copy:{}'.format(
            self.account_origin,
            self.account_copy,
            self.pub_id_origin,
            self.pub_id_Copy))    
