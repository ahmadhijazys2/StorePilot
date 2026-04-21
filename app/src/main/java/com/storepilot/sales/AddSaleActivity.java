package com.storepilot.sales;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.Sale;
import com.storepilot.viewmodels.SaleViewModel;

public class AddSaleActivity extends BaseActivity {

    private EditText etProductId, etQuantity, etTotalPrice, etNotes;
    private Button btnSaveSale;
    private SaleViewModel saleViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_sale);

        etProductId = findViewById(R.id.etSaleProductId);
        etQuantity = findViewById(R.id.etSaleQuantity);
        etTotalPrice = findViewById(R.id.etSaleTotalPrice);
        etNotes = findViewById(R.id.etSaleNotes);
        btnSaveSale = findViewById(R.id.btnSaveSale);

        saleViewModel = new ViewModelProvider(this).get(SaleViewModel.class);

        btnSaveSale.setOnClickListener(v -> {
            String productIdStr = etProductId.getText().toString().trim();
            String qtyStr = etQuantity.getText().toString().trim();
            String totalStr = etTotalPrice.getText().toString().trim();
            String notes = etNotes.getText().toString().trim();

            if (productIdStr.isEmpty() || qtyStr.isEmpty() || totalStr.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }

            int productId = Integer.parseInt(productIdStr);
            int quantity = Integer.parseInt(qtyStr);
            double total = Double.parseDouble(totalStr);
            int userId = SessionManager.getInstance().getLoggedInUser() != null
                    ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

            Sale sale = new Sale(productId, quantity, total, System.currentTimeMillis(), userId, notes);
            saleViewModel.insert(sale);
            finish();
        });
    }
}
