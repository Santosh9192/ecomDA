# E-Commerce Sales Analytics
## Entity Relationship Diagram (ERD)

---

### Version 1.0 | January 2024

---

## Database Schema Overview

The database follows a **normalized star-schema-like** design with 11 tables optimized for analytical queries.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                              E-COMMERCE DATABASE SCHEMA                          │
│                                                                                  │
│     ┌──────────────┐        ┌────────────────┐        ┌──────────────┐          │
│     │   Regions    │        │    States      │        │    Cities    │          │
│     ├──────────────┤        ├────────────────┤        ├──────────────┤          │
│  ┌──│PK region_id  │──1:N──>│PK state_id     │──1:N──>│PK city_id    │──┐       │
│  │  │   region_name│        │FK region_id    │        │FK state_id   │  │       │
│  │  │   created_at │        │   state_name   │        │   city_name  │  │       │
│  │  └──────────────┘        │   created_at   │        │   created_at │  │       │
│  │                          └────────────────┘        └──────────────┘  │       │
│  │                                                                       │       │
│  │  ┌──────────────┐                                                     │       │
│  │  │  Categories  │                                                     │       │
│  │  ├──────────────┤                                                     │       │
│  │  │PK category_id│                                                     │       │
│  └──│   category_nm│──┐                                                  │       │
│     │   description│  │                                                  │       │
│     │   created_at │  │                                                  │       │
│     └──────────────┘  │                                                  │       │
│            │          │                                                  │       │
│            │1:N       │                                                  │       │
│            │          │                                                  │       │
│     ┌──────┴────┐     │                                                  │       │
│     │SubCategor.│     │                                                  │       │
│     ├───────────┤     │                                                  │       │
│     │PK subcat  │     │                                                  │       │
│     │FK cat_id  │──┐  │                                                  │       │
│     │   sub_nm  │  │  │                                                  │       │
│     │   crtd_at │  │  │                                                  │       │
│     └───────────┘  │  │                                                  │       │
│            │       │  │                                                  │       │
│            │1:N    │  │                                                  │       │
│            │       │  │                                                  │       │
│     ┌──────┴────┐  │  │              ┌──────────────┐                    │       │
│     │ Products  │  │  │              │  Customers   │                    │       │
│     ├───────────┤  │  │              ├──────────────┤                    │       │
│     │PK prod_id │  │  │         ┌───>│PK customer_id│<───────────────────│──┐    │
│     │FK subcat  │──┘  │         │    │   cust_name   │    ┌───────────┐  │  │    │
│     │FK cat_id  │─────┘         │    │   segment    │    │ Shipping  │  │  │    │
│     │   prod_nm │              │    │   email      │    ├───────────┤  │  │    │
│     │   unit_pr │    ┌─────────│────│── reg_date   │    │PK ship_id │  │  │    │
│     │   unit_cst│    │         │    │FK city_id    │──┐ │   ship_md │  │  │    │
│     └───────────┘    │         │    │FK state_id   │──┤ │   ship_cst│  │  │    │
│          │           │         │    │FK region_id  │──┤ │   est_days│  │  │    │
│          │1:N        │         │    │   created_at │  │ │   crtd_at │  │  │    │
│          │           │         │    │   updated_at │  │ └───────────┘  │  │    │
│          ▼           │         │    └──────────────┘  │               │  │    │
│     ┌──────────────┐ │         │            │         │               │  │    │
│     │ Order_Items   │ │         │            │         │               │  │    │
│     ├──────────────┤ │         │            │         │               │  │    │
│     │PK oi_id      │ │         │            │         │               │  │    │
│  ┌──│FK order_id   │ │         │            │         │               │  │    │
│  │  │FK product_id │<┘         │            │         │               │  │    │
│  │  │   quantity   │           │            │         │               │  │    │
│  │  │   discount   │           │            │         │               │  │    │
│  │  │   sales      │           │            │         │               │  │    │
│  │  │   profit     │           │            │         │               │  │    │
│  │  │   ship_cost  │           │            │         │               │  │    │
│  │  │   return_st  │           │            │         │               │  │    │
│  │  └──────┬───────┘           │            │         │               │  │    │
│  │         │                   │            │         │               │  │    │
│  │         │1:1?               │            │         │               │  │    │
│  │         ▼                   │            │         │               │  │    │
│  │  ┌──────────────┐           │            │         │               │  │    │
│  │  │   Returns    │           │            │         │               │  │    │
│  │  ├──────────────┤           │            │         │               │  │    │
│  │  │PK return_id  │           │            │         │               │  │    │
│  │  │FK oi_id      │           │            │         │               │  │    │
│  │  │   ret_date   │           │            │         │               │  │    │
│  │  │   ret_reason │           │            │         │               │  │    │
│  │  │   ref_amt    │           │            │         │               │  │    │
│  │  │   ret_st     │           │            │         │               │  │    │
│  │  └──────────────┘           │            │         │               │  │    │
│  │                             │            │         │               │  │    │
│  │  ┌──────────────────────────────────────────────────────────────────┘  │    │
│  │  │                           Orders                                     │    │
│  │  ├──────────────────────────────────────────────────────────────────────┤    │
│  └──│PK order_id              │            │         │                     │    │
│     │   order_date            │            │         │                     │    │
│     │   ship_date             │            │         │                     │    │
│     │FK customer_id───────────┘            │         │                     │    │
│     │FK shipping_id────────────────────────┘         │                     │    │
│     │FK payment_id───────────────────────────────────│──┐                  │    │
│     │FK city_id──────────────────────────────────────│──│──────────────────┘    │
│     │FK state_id─────────────────────────────────────│──│──────────────────┘    │
│     │FK region_id────────────────────────────────────┘  │                      │
│     │   order_status                                    │                      │
│     │   created_at                                      │                      │
│     └───────────────────────────────────────────────────│──────────────────────┘
│                                                         │
│                                                  ┌──────┴──────┐
│                                                  │  Payments   │
│                                                  ├─────────────┤
│                                                  │PK pay_id    │
│                                                  │   pay_mode  │
│                                                  │   pay_st    │
│                                                  │   crtd_at   │
│                                                  └─────────────┘
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Relationships Summary

| **Parent Table** | **Child Table** | **Relationship** | **Foreign Key** |
|---|---|---|---|
| Regions | States | 1:N | States.region_id → Regions.region_id |
| States | Cities | 1:N | Cities.state_id → States.state_id |
| Regions | Customers | 1:N | Customers.region_id → Regions.region_id |
| States | Customers | 1:N | Customers.state_id → States.state_id |
| Cities | Customers | 1:N | Customers.city_id → Cities.city_id |
| Categories | SubCategories | 1:N | SubCategories.category_id → Categories.category_id |
| Categories | Products | 1:N | Products.category_id → Categories.category_id |
| SubCategories | Products | 1:N | Products.subcategory_id → SubCategories.subcategory_id |
| Customers | Orders | 1:N | Orders.customer_id → Customers.customer_id |
| Products | Order_Items | 1:N | Order_Items.product_id → Products.product_id |
| Orders | Order_Items | 1:N | Order_Items.order_id → Orders.order_id |
| Shipping | Orders | 1:N | Orders.shipping_id → Shipping.shipping_id |
| Payments | Orders | 1:N | Orders.payment_id → Payments.payment_id |
| Regions | Orders | 1:N | Orders.region_id → Regions.region_id |
| States | Orders | 1:N | Orders.state_id → States.state_id |
| Cities | Orders | 1:N | Orders.city_id → Cities.city_id |
| Order_Items | Returns | 1:1 | Returns.order_item_id → Order_Items.order_item_id |

---

## Cardinality Notes

| **Relationship** | **Type** | **Explanation** |
|---|---|---|
| Order → Order_Items | One-to-Many | One order can have multiple line items |
| Order_Item → Product | Many-to-One | Multiple orders can contain the same product |
| Customer → Orders | One-to-Many | One customer can place multiple orders |
| Region → State → City | Hierarchical | Geographic hierarchy (parent-child) |
| Category → SubCategory → Product | Hierarchical | Product hierarchy (parent-child) |
| Order_Item → Returns | One-to-One | Each returned item has one return record |

---

## Indexing Strategy

| **Index Type** | **Columns** | **Purpose** |
|---|---|---|
| Primary (PK) | All `_id` columns | Uniqueness and fast lookups |
| Foreign Key | customer_id, product_id, region_id, etc. | Join performance |
| Composite | (order_date, region_id) | Date-range analysis |
| Composite | (sales, profit) | Financial analysis |
| Filtered | (return_status) | Return rate analysis |
| Functional | (EXTRACT(YEAR FROM order_date)) | Year-based aggregation |

---

## Key Design Decisions

1. **Surrogate Keys**: All tables use auto-incrementing SERIAL primary keys
2. **Natural Keys**: Business identifiers (Order ID, Customer ID) stored as VARCHAR
3. **Soft Deletes**: No data is physically deleted; status flags indicate state
4. **Audit Columns**: All tables include `created_at` and `updated_at` timestamps
5. **Check Constraints**: Business rules enforced at database level
6. **Cascading**: FK constraints use CASCADE for parent deletes
7. **Indexes**: Strategically placed for common query patterns

---

## Views Created

| **View Name** | **Purpose** | **Key Columns** |
|---|---|---|
| vw_order_summary | Comprehensive order view | Order details + customer + region + shipping |
| vw_product_performance | Product analytics | Product sales, profit, margin, return rate |
| vw_customer_ltv | Customer lifetime value | Customer orders, sales, profit, AOV |

---

*For interactive ERD, see the Power BI model view in `powerbi/Ecommerce Dashboard.pbix`*
