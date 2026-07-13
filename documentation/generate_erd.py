"""
Generate Entity Relationship Diagram (ERD) as a PNG image.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ER_Diagram.png')

fig, ax = plt.subplots(figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_facecolor('#1E1E1E')
fig.patch.set_facecolor('#1E1E1E')

TBL = dict(boxstyle='round,pad=0.3', facecolor='#252526', edgecolor='#2E86AB', linewidth=2)
TBL_SEL = dict(boxstyle='round,pad=0.3', facecolor='#1a3a4a', edgecolor='#44BBA4', linewidth=2)
TXT_STYLE = dict(fontsize=8, color='white', family='monospace')
HDR_STYLE = dict(fontsize=10, color='#2E86AB', weight='bold', family='monospace')
PK_STYLE = dict(fontsize=8, color='#F18F01', family='monospace')

def draw_table(ax, x, y, name, columns, selected=False):
    style = TBL_SEL if selected else TBL
    lines = [f'[ {name} ]'] + columns
    text = '\n'.join(lines)
    ax.text(x, y, text, transform=ax.transData, fontdict=dict(
        fontsize=8, color='white', family='monospace',
        verticalalignment='top'), bbox=style)

def draw_arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#44BBA4', lw=1.5, connectionstyle='arc3,rad=0.2'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my, label, fontdict=dict(fontsize=7, color='#44BBA4', ha='center', family='monospace'))

# Title
ax.text(9, 11.5, 'E-Commerce Database Schema - Entity Relationship Diagram', 
        fontdict=dict(fontsize=16, color='#2E86AB', weight='bold', ha='center', family='sans-serif'), transform=ax.transData)
ax.text(9, 11.0, '11 Tables | Normalized Design | Analytical Ready', 
        fontdict=dict(fontsize=10, color='#666666', ha='center', family='sans-serif'), transform=ax.transData)

# Tables (2 rows, split across the canvas)
# Row 1 (top): Dimensions
draw_table(ax, 0.5, 10.2, 'Regions', 
    [' PK region_id SERIAL', ' region_name VARCHAR', ' created_at TIMESTAMP'])

draw_table(ax, 3.5, 10.2, 'States', 
    [' PK state_id SERIAL', ' FK region_id INT', ' state_name VARCHAR'])

draw_table(ax, 6.5, 10.2, 'Cities', 
    [' PK city_id SERIAL', ' FK state_id INT', ' city_name VARCHAR'])

draw_table(ax, 9.5, 10.2, 'Categories', 
    [' PK category_id SERIAL', ' category_name VARCHAR', ' description TEXT'])

draw_table(ax, 12.5, 10.2, 'SubCategories', 
    [' PK subcategory_id SERIAL', ' FK category_id INT', ' subcategory_name VARCHAR'])

# Row 2 (middle): Core business entities
draw_table(ax, 0.5, 7.2, 'Customers', 
    [' PK customer_id VARCHAR', ' customer_name VARCHAR', ' segment VARCHAR',
     ' email VARCHAR', ' registration_date DATE', ' FK city_id INT',
     ' FK state_id INT', ' FK region_id INT'], selected=True)

draw_table(ax, 4.5, 7.2, 'Products', 
    [' PK product_id SERIAL', ' FK subcategory_id INT', ' FK category_id INT',
     ' product_name VARCHAR', ' unit_price DECIMAL', ' unit_cost DECIMAL'])

draw_table(ax, 8.5, 7.2, 'Shipping', 
    [' PK shipping_id SERIAL', ' shipping_mode VARCHAR', ' shipping_cost DECIMAL',
     ' estimated_days INT'])

draw_table(ax, 11.5, 7.2, 'Payments', 
    [' PK payment_id SERIAL', ' payment_mode VARCHAR', ' payment_status VARCHAR'])

# Row 3 (bottom): Transactions
draw_table(ax, 1.0, 3.5, 'Orders', 
    [' PK order_id VARCHAR', ' order_date DATE', ' ship_date DATE',
     ' FK customer_id VARCHAR', ' FK shipping_id INT', ' FK payment_id INT',
     ' FK city_id INT', ' FK state_id INT', ' FK region_id INT',
     ' order_status VARCHAR'], selected=True)

draw_table(ax, 6.0, 3.5, 'Order_Items', 
    [' PK order_item_id SERIAL', ' FK order_id VARCHAR', ' FK product_id INT',
     ' quantity INT', ' discount DECIMAL', ' sales DECIMAL',
     ' profit DECIMAL', ' shipping_cost DECIMAL', ' return_status VARCHAR'], selected=True)

draw_table(ax, 11.5, 3.5, 'Returns', 
    [' PK return_id SERIAL', ' FK order_item_id INT', ' return_date DATE',
     ' return_reason VARCHAR', ' refund_amount DECIMAL', ' return_status VARCHAR'])

# Relationships
# Region -> State
draw_arrow(ax, 1.5, 10.1, 4.0, 10.1, '1:N')
# State -> City
draw_arrow(ax, 4.5, 10.1, 7.0, 10.1, '1:N')
# Category -> SubCategory
draw_arrow(ax, 10.5, 10.1, 13.0, 10.1, '1:N')
# Region -> Customers
draw_arrow(ax, 1.5, 10.0, 1.5, 8.0, '1:N')
# State -> Customers
draw_arrow(ax, 4.5, 10.0, 3.5, 8.0, '1:N')
# City -> Customers
draw_arrow(ax, 7.5, 10.0, 2.5, 8.0, '1:N')
# Category -> Products
draw_arrow(ax, 10.5, 10.0, 5.5, 8.0, '1:N')
# SubCategory -> Products
draw_arrow(ax, 13.5, 10.0, 6.5, 8.0, '1:N')
# Customers -> Orders
draw_arrow(ax, 1.5, 7.0, 2.0, 4.5, '1:N')
# Shipping -> Orders
draw_arrow(ax, 9.5, 7.0, 4.0, 4.5, '1:N')
# Payments -> Orders
draw_arrow(ax, 12.5, 7.0, 4.0, 4.0, '1:N')
# Products -> Order_Items
draw_arrow(ax, 5.5, 7.0, 7.0, 4.5, '1:N')
# Orders -> Order_Items
draw_arrow(ax, 2.0, 3.3, 7.0, 3.8, '1:N')
# Order_Items -> Returns
draw_arrow(ax, 7.0, 3.3, 12.0, 3.8, '1:1')

# Legend
legend_x, legend_y = 14.0, 10.5
ax.text(legend_x, legend_y, 'LEGEND', fontdict=dict(fontsize=10, color='#2E86AB', weight='bold', family='monospace'), transform=ax.transData)
ax.text(legend_x, legend_y-0.5, 'PK = Primary Key', fontdict=dict(fontsize=8, color='#F18F01', family='monospace'), transform=ax.transData)
ax.text(legend_x, legend_y-1.0, 'FK = Foreign Key', fontdict=dict(fontsize=8, color='white', family='monospace'), transform=ax.transData)
ax.text(legend_x, legend_y-1.5, 'SERIAL = Auto-increment', fontdict=dict(fontsize=8, color='#888', family='monospace'), transform=ax.transData)
ax.text(legend_x, legend_y-2.0, '1:N = One to Many', fontdict=dict(fontsize=8, color='#44BBA4', family='monospace'), transform=ax.transData)
ax.text(legend_x, legend_y-2.5, '1:1 = One to One', fontdict=dict(fontsize=8, color='#44BBA4', family='monospace'), transform=ax.transData)
patch_sel = mpatches.Patch(color='#1a3a4a', label='Core Tables')
ax.legend(handles=[patch_sel], loc='lower right', fontsize=8, facecolor='#252526', edgecolor='#2E86AB')

plt.tight_layout(pad=2)
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches='tight', facecolor='#1E1E1E', edgecolor='none')
plt.close()
print(f"ER Diagram saved: {OUTPUT_FILE}")
