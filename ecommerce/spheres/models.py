from django.db import models

class Subscriber(models.Model):
    apiToken = models.CharField(max_length=255)
    User_First_Name = models.CharField(max_length=50)
    User_Last_Name = models.CharField(max_length=50)
    User_Name = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Date_Joined = models.DateTimeField(auto_now_add=True)
    Last_Modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.User_First_Name} {self.User_Last_Name}"

class Administrator(models.Model):
    FName = models.CharField(max_length=50)
    SName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.FName} {self.SName}"

class Product(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField()
    Stock_Quantity = models.IntegerField()

    def __str__(self):
        return self.Name

class Order(models.Model):
    Order_Date = models.DateTimeField(auto_now_add=True)
    Total_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=50)
    Subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}"

class OrderDetails(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.IntegerField()
    Administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)

    def __str__(self):
        return f"OrderDetails #{self.id}"

class Payment(models.Model):
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Payment_Date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50)
    Subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment #{self.id}"
