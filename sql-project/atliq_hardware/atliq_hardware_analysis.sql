-- adhoc request 1
-- Provide the list of markets in which customer  "Atliq  Exclusive"  operates its 
-- business in the  APAC  region.
select distinct market 
	from dim_customer
	where region = 'APAC';
    
-- adhoc request 2
-- What is the percentage of unique product increase in 2021 vs. 2020? 
with unique_2020 as
(
	select count(distinct(p.product)) as unique_products_2020
	from dim_product as p
    join fact_sales_monthly as s
    on p.product_code = s.product_code
    group by s.fiscal_year
    having s.fiscal_year = 2020
), unique_2021 as
(
	select count(distinct(p.product)) as unique_products_2021
	from dim_product as p
    join fact_sales_monthly as s
    on p.product_code = s.product_code
    group by s.fiscal_year
    having s.fiscal_year = 2021
)
select unique_2020.unique_products_2020, unique_2021.unique_products_2021, 
		round(((unique_2021.unique_products_2021/unique_2020.unique_products_2020) - 1)*100) as percentage_chg
	from unique_2020
    join unique_2021;

-- adhoc request 3
-- Provide a report with all the unique product counts for each  segment  and 
-- sort them in descending order of product counts.
select segment, count(distinct(product)) as product_count
	from dim_product
    group by segment
    order by product_count desc;
    
-- adhoc request 4
-- Follow-up: Which segment had the most increase in unique products in 
-- 2021 vs 2020?
with p2020 as
(
	select p.segment, count(distinct(p.product)) as count_2020
	from dim_product as p
    left join fact_sales_monthly as s
    on p.product_code = s.product_code
    group by p.segment, s.fiscal_year
    having s.fiscal_year = 2020
), p2021 as
(
	select p.segment, count(distinct(p.product)) as count_2021
	from dim_product as p
    left join fact_sales_monthly as s
    on p.product_code = s.product_code
    group by p.segment, s.fiscal_year
    having s.fiscal_year = 2021
)
select p2020.segment, p2020.count_2020, p2021.count_2021, 
		p2021.count_2021 - p2020.count_2020 as difference
	from p2020
    left join p2021
    on p2020.segment = p2021.segment
    order by difference desc limit 1;
    
-- adhoc request 5
-- Get the products that have the highest and lowest manufacturing costs.
select p.product_code, p.product, m.manufacturing_cost
	from dim_product as p
    left join fact_manufacturing_cost as m
    on p.product_code = m.product_code
    where m.manufacturing_cost in
    (
		(select max(manufacturing_cost) from fact_manufacturing_cost),
        (select min(manufacturing_cost) from fact_manufacturing_cost)
    );
    
-- adhoc request 6
-- Generate a report which contains the top 5 customers who received an 
-- average high  pre_invoice_discount_pct  for the  fiscal  year 2021  and in the 
-- Indian  market.
select c.customer_code, c.customer, round(avg(i.pre_invoice_discount_pct)*100) as average_discount_percentage
	from dim_customer as c
    join fact_pre_invoice_deductions as i
    on c.customer_code = i.customer_code
    group by c.customer_code, c.customer, c.market, i.fiscal_year
    having c.market = 'India' and i.fiscal_year = 2021
    order by average_discount_percentage desc limit 5;
    
-- adhoc request 7
-- Get the complete report of the Gross sales amount for the customer  “Atliq 
-- Exclusive”  for each month. 
select date_format(s.date,'%m') as month, date_format(s.date,'%Y')as year,
		sum(s.sold_quantity) as gross_sales_amount
	from dim_customer as c
    join fact_sales_monthly as s
    on c.customer_code = s.customer_code
    group by c.customer, month, year
    having c.customer = 'Atliq Exclusive';
    
-- adhoc request 8
-- In which quarter of 2020, got the maximum total_sold_quantity?
select 
	case 
		when date_format(s.date,'%m') between 9 and 11 then 'Q1'
        when date_format(s.date,'%m') = 12 or date_format(s.date,'%m') between 1 and 2 then 'Q2'
        when date_format(s.date,'%m') between 3 and 5 then 'Q3'
        when date_format(s.date,'%m') between 6 and 8 then 'Q4'
        end as quarter,
	sum(s.sold_quantity) as total_sold_quantity
    from fact_sales_monthly as s
    group by quarter, s.fiscal_year
    having s.fiscal_year = 2020
    order by total_sold_quantity desc;
    
-- adhoc request 9
-- Which channel helped to bring more gross sales in the fiscal year 2021 
-- and the percentage of contribution?
with channel_result as
(
	select c.channel, sum(s.sold_quantity)/1000000 as gross_sales_mln
	from dim_customer as c
    join fact_sales_monthly as s
    on c.customer_code = s.customer_code
    group by c.channel, s.fiscal_year
    having s.fiscal_year = 2021
), total_sales as
(
	select sum(sold_quantity)/1000000 as total from fact_sales_monthly where fiscal_year = 2021
)
select channel_result.channel, channel_result.gross_sales_mln, 
		round((channel_result.gross_sales_mln/total_sales.total)*100, 1) as pct_contribution
	from channel_result, total_sales;
    
-- adhoc request 10
-- Get the Top 3 products in each division that have a 
-- high total_sold_quantity in the fiscal_year 2021.
with division_table as
(
	select p.division, p.product_code, p.product, sum(s.sold_quantity) as total_sold
	from dim_product as p
    join fact_sales_monthly as s
    on p.product_code = s.product_code
    group by p.division, p.product_code, p.product, s.fiscal_year
    having s.fiscal_year = 2021
), rank_table as
(
	select *, rank() over (partition by division order by total_sold) as rank_order from division_table
)
select * from rank_table where rank_order <= 3;