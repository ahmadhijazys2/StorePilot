package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.PrimaryKey;

@Entity(tableName = "purchases",
        foreignKeys = {
            @ForeignKey(entity = Product.class, parentColumns = "id", childColumns = "productId", onDelete = ForeignKey.SET_NULL),
            @ForeignKey(entity = User.class, parentColumns = "id", childColumns = "purchasedBy", onDelete = ForeignKey.SET_NULL)
        })
public class Purchase {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public Integer productId;
    public int quantity;
    public double totalCost;
    public long purchaseDate;
    public Integer purchasedBy;
    public String supplier;
    public String notes;

    public Purchase() {}

    public Purchase(Integer productId, int quantity, double totalCost, long purchaseDate,
                    Integer purchasedBy, String supplier, String notes) {
        this.productId = productId;
        this.quantity = quantity;
        this.totalCost = totalCost;
        this.purchaseDate = purchaseDate;
        this.purchasedBy = purchasedBy;
        this.supplier = supplier;
        this.notes = notes;
    }

    public int getId() { return id; }
    public Integer getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public double getTotalCost() { return totalCost; }
    public long getPurchaseDate() { return purchaseDate; }
    public Integer getPurchasedBy() { return purchasedBy; }
    public String getSupplier() { return supplier; }
    public String getNotes() { return notes; }
}
