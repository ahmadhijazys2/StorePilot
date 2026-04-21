package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "products")
public class Product {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public String name;
    public String category;
    public String size;
    public String color;
    public int quantity;
    public double price;
    public double costPrice;
    public String imageUrl;
    public long createdAt;

    public Product() {}

    public Product(String name, String category, String size, String color,
                   int quantity, double price, double costPrice, String imageUrl, long createdAt) {
        this.name = name;
        this.category = category;
        this.size = size;
        this.color = color;
        this.quantity = quantity;
        this.price = price;
        this.costPrice = costPrice;
        this.imageUrl = imageUrl;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public String getCategory() { return category; }
    public String getSize() { return size; }
    public String getColor() { return color; }
    public int getQuantity() { return quantity; }
    public double getPrice() { return price; }
    public double getCostPrice() { return costPrice; }
    public String getImageUrl() { return imageUrl; }
    public long getCreatedAt() { return createdAt; }
}
