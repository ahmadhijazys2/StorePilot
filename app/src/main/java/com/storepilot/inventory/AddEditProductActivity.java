package com.storepilot.inventory;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.PermissionManager;
import com.storepilot.db.entities.Product;
import com.storepilot.viewmodels.ProductViewModel;

public class AddEditProductActivity extends BaseActivity {

    public static final String EXTRA_PRODUCT_ID = "product_id";

    private EditText etName, etCategory, etSize, etColor, etQuantity, etPrice, etCostPrice;
    private Button btnSave;
    private ProductViewModel productViewModel;
    private Product existingProduct = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_edit_product);

        if (!PermissionManager.currentUserHasPermission(PermissionManager.MANAGE_PRODUCTS)) {
            Toast.makeText(this, "Only the Owner can add or edit products.", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        etName = findViewById(R.id.etProductName);
        etCategory = findViewById(R.id.etProductCategory);
        etSize = findViewById(R.id.etProductSize);
        etColor = findViewById(R.id.etProductColor);
        etQuantity = findViewById(R.id.etProductQuantity);
        etPrice = findViewById(R.id.etProductPrice);
        etCostPrice = findViewById(R.id.etProductCostPrice);
        btnSave = findViewById(R.id.btnSaveProduct);

        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);

        int productId = getIntent().getIntExtra(EXTRA_PRODUCT_ID, -1);
        if (productId != -1) {
            productViewModel.getById(productId).observe(this, product -> {
                if (product != null && existingProduct == null) {
                    existingProduct = product;
                    populateFields(product);
                }
            });
        }

        btnSave.setOnClickListener(v -> saveProduct());
    }

    private void populateFields(Product product) {
        etName.setText(product.getName());
        etCategory.setText(product.getCategory());
        etSize.setText(product.getSize());
        etColor.setText(product.getColor());
        etQuantity.setText(String.valueOf(product.getQuantity()));
        etPrice.setText(String.valueOf(product.getPrice()));
        etCostPrice.setText(String.valueOf(product.getCostPrice()));
    }

    private void saveProduct() {
        String name = etName.getText().toString().trim();
        String category = etCategory.getText().toString().trim();
        String size = etSize.getText().toString().trim();
        String color = etColor.getText().toString().trim();
        String qtyStr = etQuantity.getText().toString().trim();
        String priceStr = etPrice.getText().toString().trim();
        String costStr = etCostPrice.getText().toString().trim();

        if (name.isEmpty() || qtyStr.isEmpty() || priceStr.isEmpty()) {
            Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
            return;
        }

        int qty = Integer.parseInt(qtyStr);
        double price = Double.parseDouble(priceStr);
        double cost = costStr.isEmpty() ? 0 : Double.parseDouble(costStr);

        if (existingProduct != null) {
            existingProduct.name = name;
            existingProduct.category = category;
            existingProduct.size = size;
            existingProduct.color = color;
            existingProduct.quantity = qty;
            existingProduct.price = price;
            existingProduct.costPrice = cost;
            productViewModel.update(existingProduct);
        } else {
            Product product = new Product(name, category, size, color, qty, price, cost, "", System.currentTimeMillis());
            productViewModel.insert(product);
        }
        finish();
    }
}
