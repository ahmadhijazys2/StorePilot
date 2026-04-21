package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.PrimaryKey;

@Entity(tableName = "sales",
        foreignKeys = {
            @ForeignKey(entity = Product.class, parentColumns = "id", childColumns = "productId", onDelete = ForeignKey.SET_NULL),
            @ForeignKey(entity = User.class, parentColumns = "id", childColumns = "soldBy", onDelete = ForeignKey.SET_NULL)
        })
public class Sale {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public Integer productId;
    public int quantity;
    public double totalPrice;
    public long saleDate;
    public Integer soldBy;
    public String notes;

    public Sale() {}

    public Sale(Integer productId, int quantity, double totalPrice, long saleDate, Integer soldBy, String notes) {
        this.productId = productId;
        this.quantity = quantity;
        this.totalPrice = totalPrice;
        this.saleDate = saleDate;
        this.soldBy = soldBy;
        this.notes = notes;
    }

    public int getId() { return id; }
    public Integer getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public double getTotalPrice() { return totalPrice; }
    public long getSaleDate() { return saleDate; }
    public Integer getSoldBy() { return soldBy; }
    public String getNotes() { return notes; }
}
