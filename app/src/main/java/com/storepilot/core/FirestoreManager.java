package com.storepilot.core;

import android.util.Log;

import com.google.firebase.firestore.FirebaseFirestore;
import com.storepilot.db.entities.Order;
import com.storepilot.db.entities.Product;
import com.storepilot.db.entities.Purchase;
import com.storepilot.db.entities.Sale;
import com.storepilot.db.entities.Task;
import com.storepilot.db.entities.User;

import java.util.HashMap;
import java.util.Map;

/**
 * Central class for all Firestore read/write operations.
 * Called alongside Room so data is synced to the cloud automatically.
 */
public class FirestoreManager {

    private static final String TAG = "FirestoreManager";
    private static FirebaseFirestore db;

    private static FirebaseFirestore get() {
        if (db == null) db = FirebaseFirestore.getInstance();
        return db;
    }

    // ─── USERS ───────────────────────────────────────────────────────────────

    public static void saveUser(User user) {
        Map<String, Object> data = new HashMap<>();
        data.put("fullName",  user.fullName);
        data.put("username",  user.username);
        data.put("email",     user.email);
        data.put("phone",     user.phone);
        data.put("role",      user.role);
        data.put("createdAt", user.createdAt);

        get().collection("users").document(user.username)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "saveUser failed: " + e.getMessage()));
    }

    // ─── PRODUCTS ────────────────────────────────────────────────────────────

    public static void saveProduct(Product p) {
        Map<String, Object> data = new HashMap<>();
        data.put("name",      p.name);
        data.put("category",  p.category);
        data.put("size",      p.size);
        data.put("color",     p.color);
        data.put("quantity",  p.quantity);
        data.put("price",     p.price);
        data.put("costPrice", p.costPrice);
        data.put("imageUrl",  p.imageUrl);
        data.put("createdAt", p.createdAt);
        data.put("localId",   p.id);

        get().collection("products").document("product_" + p.id)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "saveProduct failed: " + e.getMessage()));
    }

    public static void deleteProduct(int productId) {
        get().collection("products").document("product_" + productId)
                .delete()
                .addOnFailureListener(e -> Log.e(TAG, "deleteProduct failed: " + e.getMessage()));
    }

    // ─── TASKS ───────────────────────────────────────────────────────────────

    public static void saveTask(Task t) {
        Map<String, Object> data = new HashMap<>();
        data.put("title",       t.title);
        data.put("description", t.description);
        data.put("assignedTo",  t.assignedTo);
        data.put("createdBy",   t.createdBy);
        data.put("status",      t.status);
        data.put("priority",    t.priority);
        data.put("isPrivate",   t.isPrivate);
        data.put("dueDate",     t.dueDate);
        data.put("createdAt",   t.createdAt);
        data.put("localId",     t.id);

        get().collection("tasks").document("task_" + t.id)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "saveTask failed: " + e.getMessage()));
    }

    public static void deleteTask(int taskId) {
        get().collection("tasks").document("task_" + taskId)
                .delete()
                .addOnFailureListener(e -> Log.e(TAG, "deleteTask failed: " + e.getMessage()));
    }

    // ─── SALES ───────────────────────────────────────────────────────────────

    public static void saveSale(Sale s) {
        Map<String, Object> data = new HashMap<>();
        data.put("productId",  s.productId);
        data.put("quantity",   s.quantity);
        data.put("totalPrice", s.totalPrice);
        data.put("saleDate",   s.saleDate);
        data.put("soldBy",     s.soldBy);
        data.put("notes",      s.notes);
        data.put("localId",    s.id);

        get().collection("sales").document("sale_" + s.saleDate + "_" + s.productId)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "saveSale failed: " + e.getMessage()));
    }

    // ─── ORDERS ──────────────────────────────────────────────────────────────

    public static void saveOrder(Order o) {
        Map<String, Object> data = new HashMap<>();
        data.put("customerId",      o.customerId);
        data.put("totalPrice",      o.totalPrice);
        data.put("status",          o.status);
        data.put("createdAt",       o.createdAt);
        data.put("paymentMethod",   o.paymentMethod);
        data.put("shippingAddress", o.shippingAddress);
        data.put("localId",         o.id);

        get().collection("orders").document("order_" + o.id)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "saveOrder failed: " + e.getMessage()));
    }

    public static void updateOrderStatus(int orderId, String status) {
        get().collection("orders").document("order_" + orderId)
                .update("status", status)
                .addOnFailureListener(e -> Log.e(TAG, "updateOrderStatus failed: " + e.getMessage()));
    }

    // ─── PURCHASES ───────────────────────────────────────────────────────────

    public static void savePurchase(Purchase p) {
        Map<String, Object> data = new HashMap<>();
        data.put("productId",    p.productId);
        data.put("quantity",     p.quantity);
        data.put("totalCost",    p.totalCost);
        data.put("purchaseDate", p.purchaseDate);
        data.put("purchasedBy",  p.purchasedBy);
        data.put("supplier",     p.supplier);
        data.put("notes",        p.notes);
        data.put("localId",      p.id);

        get().collection("purchases").document("purchase_" + p.purchaseDate + "_" + p.productId)
                .set(data)
                .addOnFailureListener(e -> Log.e(TAG, "savePurchase failed: " + e.getMessage()));
    }
}
