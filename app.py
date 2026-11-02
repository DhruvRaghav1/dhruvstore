      <span class="size">{{p.size_value|pretty_size}} {{p.size_unit}}</span>
      <div class="price-row"><span class="price">₹{{"%.2f"|format(p.price)}}</span>{% if p.old_price > p.price %}<span class="old">₹{{"%.2f"|format(p.old_price)}}</span>{% endif %}</div>
      <p class="stock">{% if p.stock > 0 %}{{p.stock}} packs available{% else %}Out of stock{% endif %}</p>
      {% if p.stock > 0 %}
      <form class="add-form" method="post" action="/add/{{p.id}}">
        <input class="qty-input" type="number" name="qty" value="1" min="1" max="{{p.stock}}" aria-label="Quantity">
        <button class="primary" type="submit">Add to cart</button>
      </form>
      {% endif %}
    </article>
  {% endfor %}
  </div>
  <p id="noResults" class="empty" style="display:none">No products found. Try another search.</p>

  <section class="panel" id="cart">
    <h2>🛒 Your Cart</h2>
    {% if cart %}
      {% for item in cart %}
      <div class="cart-line">
        <div><strong>{{item.name}}</strong> <span class="size">{{item.size_value|pretty_size}} {{item.size_unit}}</span><br><small>₹{{"%.2f"|format(item.price)}} each · Subtotal ₹{{"%.2f"|format(item.price * item.qty)}}</small></div>
        <div class="cart-controls">
          <form method="post" action="/cart/update/{{item.id}}"><input type="hidden" name="action" value="minus"><button class="mini" aria-label="Decrease quantity">−</button></form>
          <strong>{{item.qty}}</strong>
          <form method="post" action="/cart/update/{{item.id}}"><input type="hidden" name="action" value="plus"><button class="mini" aria-label="Increase quantity">+</button></form>
          <form method="post" action="/cart/update/{{item.id}}"><input type="hidden" name="action" value="remove"><button class="remove">Remove</button></form>
        </div>
      </div>
      {% endfor %}
      <div class="total">Total: ₹{{"%.2f"|format(total)}}</div>
      <h2>Delivery Details</h2>
      <p class="empty">Cash on Delivery · Please enter your delivery address.</p>
      <form class="checkout" method="post" action="/order">
        <input name="customer_name" placeholder="Full name" required maxlength="100">
        <input name="phone" placeholder="10-digit mobile number" required pattern="[0-9]{10}" inputmode="numeric">
        <input name="house" placeholder="House / Flat number" required maxlength="120">
        <input name="area" placeholder="Street / Area" required maxlength="150">
        <input name="landmark" placeholder="Nearby landmark (optional)" maxlength="150">
        <input name="city" placeholder="City" required maxlength="100">
        <input name="pincode" placeholder="6-digit PIN code" required pattern="[0-9]{6}" inputmode="numeric">
        <button class="primary wide" type="submit">Place Cash on Delivery Order</button>
      </form>
    {% else %}<p class="empty">Your cart is empty. Add something tasty from our products above!</p>{% endif %}
  </section>
</main>
<footer>© {{year}} Dhruv Store · Thank you for shopping with us ❤️</footer>
<script>
const search = document.getElementById('search');
const cards = [...document.querySelectorAll('.card')];
const filters = [...document.querySelectorAll('.filter')];
const noResults = document.getElementById('noResults');
let category = 'All';
function applyFilters(){
  const term = search.value.trim().toLowerCase();
  let visible = 0;
  cards.forEach(card => {
    const matchesText = card.dataset.name.includes(term);
    const matchesCategory = category === 'All' || card.dataset.category === category;
    const show = matchesText && matchesCategory;
    card.style.display = show ? '' : 'none';
    if(show) visible++;
  });
  noResults.style.display = visible ? 'none' : 'block';
}
search.addEventListener('input', applyFilters);
filters.forEach(btn => btn.addEventListener('click', () => {
  category = btn.dataset.filter;
  filters.forEach(b => b.classList.toggle('active', b === btn));
  applyFilters();
}));
</script>
</body></html>
"""

ADMIN = r"""
<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dhruv Store Admin</title><style>
*{box-sizing:border-box}body{font-family:Arial;background:#f3f6fb;padding:18px;color:#172033}
main{max-width:1000px;margin:auto}.box{background:white;padding:20px;margin:16px 0;border-radius:14px;box-shadow:0 4px 18px #0f172a0c}
input,select{padding:11px;margin:5px 4px 10px 0;max-width:100%;border:1px solid #d7dfeb;border-radius:8px;font:inherit}
button{padding:10px 14px;background:#2563eb;color:white;border:0;border-radius:8px;cursor:pointer;font-weight:bold}
a{color:#1d4ed8}table{width:100%;border-collapse:collapse}td,th{padding:10px;border-bottom:1px solid #e5eaf2;text-align:left}
@media(max-width:600px){.table-wrap{overflow-x:auto}table{min-width:550px}}
</style></head><body><main>
<h1>🛍️ Dhruv Store — Admin</h1><p><a href="/">View Store</a> | <a href="/admin/logout">Logout</a></p>
<div class="box"><h2>Add Product</h2>
<form method="post" action="/admin/add" enctype="multipart/form-data">
<input name="name" placeholder="Product name" required>
<select name="category"><option>Cold Drinks</option><option>Chips</option></select><br>
<label>Selling price ₹ <input name="price" type="number" min="0" step="0.01" placeholder="Selling price" required></label>
<label>Original price ₹ <input name="old_price" type="number" min="0" step="0.01" placeholder="Original price"></label><br>
<label>Pack size <input name="size_value" type="number" min="0.01" step="0.01" value="1" required style="width:110px"></label>
<select name="size_unit"><option value="g">Grams (g)</option><option value="kg">Kilograms (kg)</option><option value="ml">Millilitres (ml)</option><option value="L">Litres (L)</option><option value="piece" selected>Pieces</option></select>
<label>Stock (number of packs) <input name="stock" type="number" min="0" placeholder="Stock quantity" required></label><br>
<label>Product image <input name="image" type="file" accept=".jpg,.jpeg,.png,.webp"></label>
<button type="submit">Add Product</button></form>
<p><small>Example: Cola · 500 ml · Stock 20 means 20 bottles of 500 ml each.</small></p></div>
<div class="box"><h2>Your Products</h2><div class="table-wrap"><table><tr><th>Name</th><th>Category</th><th>Pack size</th><th>Price</th><th>Stock</th><th>Delete</th></tr>
{% for p in products %}<tr><td>{{p.name}}</td><td>{{p.category}}</td><td>{{p.size_value|pretty_size}} {{p.size_unit}}</td><td>₹{{p.price}}</td><td>{{p.stock}}</td>
<td><form method="post" action="/admin/delete/{{p.id}}" onsubmit="return confirm('Delete this product?')"><button>Delete</button></form></td></tr>{% endfor %}
</table></div></div></main></body></html>
"""

# Run database setup when the service starts. No demo products are recreated.
setup()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
