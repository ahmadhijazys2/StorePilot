package com.storepilot.purchases;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.Purchase;
import com.storepilot.viewmodels.PurchaseViewModel;

public class AddPurchaseActivity extends BaseActivity {

    private EditText etProductId, etQuantity, etTotalCost, etSupplier, etNotes;
    private Button btnSavePurchase;
    private PurchaseViewModel purchaseViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_purchase);

        etProductId = findViewById(R.id.etPurchaseProductId);
        etQuantity = findViewById(R.id.etPurchaseQuantity);
        etTotalCost = findViewById(R.id.etPurchaseTotalCost);
        etSupplier = findViewById(R.id.etPurchaseSupplier);
        etNotes = findViewById(R.id.etPurchaseNotes);
        btnSavePurchase = findViewById(R.id.btnSavePurchase);

        purchaseViewModel = new ViewModelProvider(this).get(PurchaseViewModel.class);

        btnSavePurchase.setOnClickListener(v -> {
            String productIdStr = etProductId.getText().toString().trim();
            String qtyStr = etQuantity.getText().toString().trim();
            String costStr = etTotalCost.getText().toString().trim();
            String supplier = etSupplier.getText().toString().trim();
            String notes = etNotes.getText().toString().trim();

            if (productIdStr.isEmpty() || qtyStr.isEmpty() || costStr.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }

            int productId = Integer.parseInt(productIdStr);
            int quantity = Integer.parseInt(qtyStr);
            double cost = Double.parseDouble(costStr);
            int userId = SessionManager.getInstance().getLoggedInUser() != null
                    ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

            Purchase purchase = new Purchase(productId, quantity, cost,
                    System.currentTimeMillis(), userId, supplier, notes);
            purchaseViewModel.insert(purchase);
            finish();
        });
    }
}
