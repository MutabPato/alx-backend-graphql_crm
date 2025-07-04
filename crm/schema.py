import graphene
from graphene_django import DjangoObjectType
from email_validator import validate_email, EmailNotValidError
import re
from .models import Customer, Product, Order


# Graphene object types for the models
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

    # Adding a field to calculate total amount for an order
    total_amount = graphene.Decimal()

    def resolve_total_amount(self, info):
        total = sum(product.price for product in self.products.all())
        return total

# Queries
class Query(graphene.ObjectType):
        all_customers = graphene.List(CustomerType)
        customer_by_id = graphene.Field(CustomerType, id=graphene.ID())

        all_products = graphene.List(ProductType)
        product_by_id = graphene.Field(ProductType, id=graphene.ID())
    
        all_orders = graphene.List(ProductType)
        order_by_id = graphene.Field(OrderType, id=graphene.ID())

        def resolve_all_customers(self, info, **kwargs):
            return Customer.objects.all()
        
        def resolve_customer_by_id(self, info, id):
            try:
                return Customer.objects.get(pk=id)
            except Customer.DoesNotExist:
                return None
            
        def resolve_all_products(self, info, **kwargs):
            return Product.objects.all()
        
        def resolve_product_by_id(self, info, id):
            try:
                return Product.objects.get(pk=id)
            except Product.DoesNotExist:
                return None
            
        def resolve_all_orders(self, info, **kwargs):
            return Customer.objects.all()
        
        def resolve_order_by_id(self, info, id):
            try:
                return Order.objects.get(pk=id)
            except Order.DoesNotExist:
                return None

           
# Mutattions
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    # Output of the mutation
    customer = graphene.Field(CustomerType)
           
    def mutate(self, info, name, email, phone=None):
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise Exception(f"Invalid email format: {e}")
        
        """if phone:
            pattern = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
            if not re.match(pattern, phone):
                raise Exception("Invalid phone number format. Expect formats like +1234567890 or 123-456-7890")
"""
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    # Outputs of the mutation
    ok = graphene.Boolean()
    created_count = graphene.Int()

    def mutate(self, info, customers):
            objs = []
            for customer_data in customers:
                try:
                    validate_email(customer_data.email)
                except EmailNotValidError as e:
                    raise Exception("Invalid email for customer '{customer_data.name}'")
                
                if customer_data.phone:
                    pattern = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
                    if not re.match(pattern, customer_data.phone):
                        raise Exception("Invalid phone number for customer '{customer_data.name}'")

                objs.append(Customer(
                    name=customer_data.name,
                    email=customer_data.email,
                    phone=customer_data.phone
                    )
                )
            
            Customer.objects.bulk_create(objs)
            return BulkCreateCustomers(ok=True, created_count=len(objs))


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=None):
        if price < 0:
            raise Exception("Price cannot be negative.")
        if stock < 0:
            raise Exception("Stock cannot be negative")
        
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        # order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except:
            raise Exception(f"Customer with ID {customer_id} does not exist.")
        
        products_to_add = []
        for product_id in product_ids:
            try:
                product=Product.objects.get(pk=product_id)
                products_to_add.append(product)
            except:
                raise Exception(f"Product with IID {product_id} does not exist.")

        if not products_to_add:
            raise Exception("No valid products provided for the order.")

        order = Order(customer=customer)
        order.save()
        
        order.products.set(products_to_add)

        return CreateOrder(order=order)
    

class Mutation(graphene.ObjectType):
       create_customer = CreateCustomer.Field()
       bulk_create_customers = BulkCreateCustomers.Field()
       create_product = CreateProduct.Field()
       create_order = CreateOrder.Field()
            