create database if not exists ecommerce_lakehouse;
use ecommerce_lakehouse;
select count(*) from customer_sales;
select count(*) from category_sales;
select count(*) from country_sales;
select count(*) from product_sales;

describe customer_sales;
describe product_sales;
select sum(total_spent)
from customer_sales;

