package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Order;
import com.storepilot.db.entities.Product;
import com.storepilot.repositories.OrderRepository;

import java.util.List;

// ViewModel for order operations (placing and managing orders)
public class OrderViewModel extends AndroidViewModel {

    private final OrderRepository orderRepository;

    // Signals that an order was placed successfully (used to show confirmation)
    public final MutableLiveData<Boolean> orderPlaced = new MutableLiveData<>();

    public OrderViewModel(@NonNull Application application) {
        super(application);
        orderRepository = new OrderRepository(application);
    }

    // Place a new order using the cart contents
    public void placeOrder(int customerId, String paymentMethod, String shippingAddress,
                           List<CartItem> cartItems, List<Product> products) {
        orderRepository.placeOrder(customerId, paymentMethod, shippingAddress,
                cartItems, products, () -> orderPlaced.postValue(true));
    }

    // Change the status of an order (manager action)
    public void updateOrderStatus(Order order, String newStatus) {
        orderRepository.updateOrderStatus(order, newStatus);
    }

    // Get all orders for a specific customer
    public LiveData<List<Order>> getOrdersByCustomer(int customerId) {
        return orderRepository.getOrdersByCustomer(customerId);
    }

    // Get all orders (manager view)
    public LiveData<List<Order>> getAllOrders() {
        return orderRepository.getAllOrders();
    }

    // Get today's revenue total
    public LiveData<Double> getTodayRevenue(long startOfDay) {
        return orderRepository.getTodayRevenue(startOfDay);
    }

    // Get today's order count
    public LiveData<Integer> getTodayOrderCount(long startOfDay) {
        return orderRepository.getTodayOrderCount(startOfDay);
    }
}
