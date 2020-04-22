// Creating references
// You can also define relaionship separately
// > many-to-one; < one-to-many; - one-to-one
// admin_id int [ref: > U.id] // inline relationship (many-to-one)

Table Customer {
    customer_id int [pk, increment]
    first_name  varchar
    last_name  varchar
    address  varchar
    city  varchar
    state  varchar
    postcode  varchar
    country  varchar
    phone  varchar
    email  varchar
    orders_relationship  varchar
}

Table Orders {
    order_id int [pk, increment]
    customer_id  int [ref: < Customer.customer_id]
    shipper_id  int [ref: < Shipper.shipper_id]
    order_number  int
    order_details  varchar
    customer_relationship varchar
    shipper_relationship varchar
    details_relationship varchar
}

Table OrderDetails {
    order_details_id int [pk, increment]
    order_id int [ref: < Orders.order_id]
    product_id int [ref: < Products.product_id]
    quantity int
    price int
    total int
    order_description varchar
}

Table Products {
    product_id int [pk, increment]
    category_id int [ref: < Category.category_id]
    product_name varchar
    product_description varchar
    unit_price  float
}

Table Category {
    category_id int [pk, increment]
    category_name  varchar
    category_description  varchar
    products_relationship  varchar
}

Table Shipper {
    shipper_id int [pk, increment]
    company_name  varchar
    phone  varchar
    orders  varchar
}