package com.storepilot.core;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PermissionManager {

    // Permission constants
    public static final String MANAGE_USERS = "MANAGE_USERS";
    public static final String MANAGE_PRODUCTS = "MANAGE_PRODUCTS";
    public static final String VIEW_PRODUCTS = "VIEW_PRODUCTS";
    public static final String CREATE_SALE = "CREATE_SALE";
    public static final String VIEW_SALES_HISTORY = "VIEW_SALES_HISTORY";
    public static final String MANAGE_PURCHASES = "MANAGE_PURCHASES";
    public static final String VIEW_REPORTS = "VIEW_REPORTS";
    public static final String MANAGE_SEASONS = "MANAGE_SEASONS";
    public static final String VIEW_MARKETING = "VIEW_MARKETING";
    public static final String CREATE_PRIVATE_TASK = "CREATE_PRIVATE_TASK";
    public static final String VIEW_TEAM_TASKS = "VIEW_TEAM_TASKS";
    public static final String MANAGE_TASKS = "MANAGE_TASKS";
    public static final String VIEW_ADMIN = "VIEW_ADMIN";

    // Role constants
    public static final String OWNER = "OWNER";
    public static final String STORE_MANAGER = "STORE_MANAGER";
    public static final String SHIFT_MANAGER = "SHIFT_MANAGER";
    public static final String EMPLOYEE = "EMPLOYEE";

    private static final Map<String, List<String>> permissionMap = new HashMap<>();

    static {
        permissionMap.put(MANAGE_USERS, Arrays.asList(OWNER));
        permissionMap.put(MANAGE_PRODUCTS, Arrays.asList(OWNER));
        permissionMap.put(VIEW_PRODUCTS, Arrays.asList(OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE));
        permissionMap.put(CREATE_SALE, Arrays.asList(OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE));
        permissionMap.put(VIEW_SALES_HISTORY, Arrays.asList(OWNER, STORE_MANAGER, SHIFT_MANAGER));
        permissionMap.put(MANAGE_PURCHASES, Arrays.asList(OWNER, STORE_MANAGER));
        permissionMap.put(VIEW_REPORTS, Arrays.asList(OWNER, STORE_MANAGER));
        permissionMap.put(MANAGE_SEASONS, Arrays.asList(OWNER, STORE_MANAGER));
        permissionMap.put(VIEW_MARKETING, Arrays.asList(OWNER, STORE_MANAGER));
        permissionMap.put(CREATE_PRIVATE_TASK, Arrays.asList(OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE));
        permissionMap.put(VIEW_TEAM_TASKS, Arrays.asList(OWNER, STORE_MANAGER, SHIFT_MANAGER));
        permissionMap.put(MANAGE_TASKS, Arrays.asList(OWNER, STORE_MANAGER));
        permissionMap.put(VIEW_ADMIN, Arrays.asList(OWNER));
    }

    public static boolean hasPermission(String role, String permission) {
        List<String> allowedRoles = permissionMap.get(permission);
        if (allowedRoles == null) return false;
        return allowedRoles.contains(role);
    }

    public static boolean currentUserHasPermission(String permission) {
        SessionManager session = SessionManager.getInstance();
        String role = session.getUserRole();
        if (role == null) return false;
        return hasPermission(role, permission);
    }
}
