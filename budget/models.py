from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(user_model)
    account = models.ManyToManyField('Account', through='UserAccount')


class Account(models.Model):
    """
    Accounts as in
    חשבונות
    """
    name = models.CharField(max_length=45)
    is_archived = models.BooleanField(default=False)


class UserAccount(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    permissions = models.IntegerField(choices='')


class TransactionCategory(models.Model):
    """
    SubCategories are removed if Parent Category is deleted for now
    """
    name = models.CharField(max_length=60)
    icon = models.IntegerField(choices='')
    color = models.CharField(max_length=7)
    is_archived = models.BooleanField(default=False)
    subcategory = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True)


class Transaction(models.Model):
    """
    Basic Building block,
    Transaction currently are saved even if the category was deleted and/or the user who created them is deleted.
    If the Account is deleted though - the transactions will be removed as well.
    """

    class Meta:
        ordering = ('-transaction_datetime', )

    amount = models.PositiveIntegerField()
    transaction_type = models.IntegerField(choices='', db_index=True) # income/expense
    transaction_method = models.IntegerField(choices='', db_index=True) # card/cash
    transaction_datetime = models.DateTimeField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='categories', related_query_name='transaction')
    user_account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, related_name='user_accounts', null=True)
    
    # These should be set if UserAccount is deleted
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounts', null=True)
    user_name = models.CharField(max_length=30, null=True)


class Budget(models.Model):
    pass
