from fpdf import FPDF
import os

class ProjectBookPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "StorePilot - Project Book  |  Smart Phones Programming Alternative (5 units)", align="L")
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def cover_page(self):
        self.add_page()
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(33, 97, 140)
        self.ln(30)
        self.cell(0, 14, "StorePilot", align="C")
        self.ln(14)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(60, 60, 60)
        self.cell(0, 10, "Store Management System & Online Shopping App", align="C")
        self.ln(30)
        self.set_draw_color(33, 97, 140)
        self.set_line_width(0.5)
        self.line(40, self.get_y(), 170, self.get_y())
        self.ln(10)
        fields = [
            ("Student Name", "___________________"),
            ("Student ID", "___________________"),
            ("School Name", "___________________"),
            ("Supervisor", "___________________"),
            ("Alternative", "Smart Phones Programming (5 units)"),
            ("Submission Date", "___________________"),
        ]
        self.set_font("Helvetica", "", 12)
        for label, value in fields:
            self.set_text_color(80, 80, 80)
            self.cell(60, 10, f"{label}:", align="R")
            self.set_text_color(0, 0, 0)
            self.set_font("Helvetica", "B", 12)
            self.cell(100, 10, value)
            self.ln(9)
            self.set_font("Helvetica", "", 12)
        self.ln(20)
        self.set_draw_color(33, 97, 140)
        self.line(40, self.get_y(), 170, self.get_y())

    def toc_page(self, items):
        self.add_page()
        self.h1("Table of Contents")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0, 0, 0)
        for num, title, page in items:
            self.set_font("Helvetica", "", 12)
            dots = "." * max(1, 70 - len(f"{num}. {title}") - len(str(page)))
            self.cell(0, 9, f"{num}. {title} {dots} {page}")
            self.ln(9)

    def h1(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(33, 97, 140)
        self.set_fill_color(235, 245, 255)
        self.cell(0, 10, text, fill=True)
        self.ln(12)
        self.set_text_color(0, 0, 0)

    def h2(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(21, 67, 96)
        self.cell(0, 8, text)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def h3(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, text)
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def body(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet(self, text, indent=5):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.set_x(10 + indent)
        self.cell(5, 6, "\x95")
        self.multi_cell(0, 6, text)
        self.ln(1)

    def sub_bullet(self, text, indent=12):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.set_x(10 + indent)
        self.cell(5, 6, "-")
        self.multi_cell(0, 6, text)

    def code_block(self, code):
        self.ln(2)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.set_font("Courier", "", 9)
        self.set_text_color(20, 20, 20)
        lines = code.strip().split("\n")
        for line in lines:
            self.set_x(12)
            self.cell(0, 5, line, fill=True)
            self.ln(5)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def table(self, headers, rows, col_widths=None):
        self.ln(2)
        if col_widths is None:
            w = 190 // len(headers)
            col_widths = [w] * len(headers)
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(33, 97, 140)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in rows:
            self.set_fill_color(240, 248, 255) if fill else self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, cell, border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(4)

    def divider(self):
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)


def build():
    pdf = ProjectBookPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(10, 18, 10)

    # ── Cover ──────────────────────────────────────────────────────────────
    pdf.cover_page()

    # ── TOC (page numbers are approximate) ────────────────────────────────
    toc = [
        ("1", "Introduction", 3),
        ("2", "Project Architecture / Structure", 8),
        ("3", "Project Implementation", 13),
        ("4", "User Guide", 21),
        ("5", "Personal Reflection / Summary", 25),
        ("6", "Bibliography", 28),
        ("7", "Appendices", 29),
    ]
    pdf.toc_page(toc)

    # ══════════════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("1. Introduction")

    pdf.h2("1.1 Project Background")
    pdf.h3("Project Name")
    pdf.body("StorePilot")

    pdf.h3("Short Description")
    pdf.body(
        "StorePilot is a dual-role Android application that combines two worlds in one: a complete "
        "store management system for the owner and staff, and an online shopping app for customers. "
        "The system is built around the MVVM (Model-View-ViewModel) architecture, uses Firebase "
        "Authentication for user verification, and Firebase Firestore as the cloud database."
    )

    pdf.h3("Target Audience")
    pdf.bullet("Small and medium business owners who want digital management of inventory, sales, tasks, and seasonal collections.")
    pdf.bullet("Store managers and employees who need a fast, convenient daily work tool.")
    pdf.bullet("Customers who want to purchase products from the store through a secure, easy-to-use app.")

    pdf.h3("Reasons for Choosing This Topic")
    pdf.bullet("Combines diverse fields: business management, security (password encryption, owner identity verification via secret code), modern UX, and cloud computing.")
    pdf.bullet("High relevance: many small stores still manage inventory and sales manually.")
    pdf.bullet("Opportunity to implement a wide range of advanced topics: Firebase, AlarmManager, Notifications, Fragments, Threads, MVVM, and more.")

    pdf.h2("1.2 Research Process")
    pdf.h3("Domain Knowledge Research")
    pdf.body(
        "A review of existing Store Management / POS systems was conducted, including Square, Shopify, "
        "and Lightspeed. It was found that most of these systems are expensive and complex for small "
        "businesses, and none offer a unified staff + customer interface in a single app."
    )

    pdf.h3("Review of Existing Applications")
    pdf.body(
        "E-commerce apps such as Amazon, Shopify Customer App, and Wix Owner were examined. "
        "The conclusion: combining a management interface with a customer shopping interface in one app "
        "is uncommon in the market."
    )

    pdf.h3("Technologies Not in the Curriculum")
    pdf.bullet("Firebase Firestore - Google's NoSQL cloud database. Supports real-time data syncing and automatic UI updates via snapshot listeners.")
    pdf.bullet("Firebase Authentication - Google's user authentication service. Supports email/password sign-in.")
    pdf.bullet("AlarmManager - Android component for executing code at fixed time intervals, even when the app is in the background.")
    pdf.bullet("PBKDF2WithHmacSHA256 - Advanced password hashing algorithm with a random salt, providing strong protection against brute-force attacks.")

    pdf.h2("1.3 Main Challenges")
    pdf.bullet("Complex permission management: four staff roles (Owner, Store Manager, Shift Manager, Employee) plus Customer, each with different permissions.")
    pdf.bullet("Owner identity verification: implementing a secret code mechanism (777) that appears as a dialog when selecting the Owner role during registration.")
    pdf.bullet("Real-time notifications: when stock falls below the threshold, the system sends a notification even when the app is in the background, using AlarmManager and BroadcastReceiver.")
    pdf.bullet("LiveData chaining: views combining multiple data sources (favorites + products, cart + products) required careful observer management.")
    pdf.bullet("Firestore queries without composite indexes: avoided composite index errors by sorting data in Java instead of using Firestore orderBy() on subcollections.")

    pdf.h3("Need the Project Addresses")
    pdf.body(
        "Small stores need a simple, accessible, and affordable management tool that also allows "
        "customers to shop directly. StorePilot provides a unified solution for both sides in a single application."
    )

    pdf.h2("1.4 Innovations and Adaptations")
    pdf.bullet("Owner authentication code: an innovative method using a secret code (777) to verify the store owner before registration.")
    pdf.bullet("Periodic AlarmManager: checks stock every hour and automatically sends a notification when a product drops below 5 units.")
    pdf.bullet("Test Notification mode: a dedicated button in the More menu that instantly triggers the notification system without waiting for the alarm.")
    pdf.bullet("Automatic sale creation: when an order status is changed to DELIVERED, the system automatically creates a sale record and updates revenue figures.")

    pdf.h2("1.5 Knowledge Domain Description")
    pdf.h3("Required Objects")
    pdf.table(
        ["Object", "Description"],
        [
            ["User", "System user (Owner / Store Manager / Shift Manager / Employee / Customer)"],
            ["Product", "Item in the store inventory"],
            ["Sale", "A recorded sale transaction"],
            ["Order", "A customer order"],
            ["OrderItem", "A single item within an order"],
            ["CartItem", "An item in a customer's shopping cart"],
            ["Favorite", "A product saved in a customer's wishlist"],
            ["Task", "A task assigned to an employee"],
            ["Season", "A seasonal collection or promotion period"],
            ["SupportMessage", "A chat message between customer and staff"],
        ],
        [50, 140],
    )

    pdf.h3("Data Types")
    pdf.bullet("String: names, emails, addresses, roles, statuses")
    pdf.bullet("int: IDs, quantities")
    pdf.bullet("double: prices, totals")
    pdf.bullet("long: timestamps in UNIX format")
    pdf.bullet("boolean: statuses (isActive, isFavorite)")

    pdf.h3("Data Representation")
    pdf.bullet("ArrayList: dynamic lists of objects displayed in RecyclerView components.")
    pdf.bullet("LiveData<List<T>>: reactive observation of Firestore data for automatic UI updates.")
    pdf.bullet("Firestore Collections: cloud storage as nested documents (NoSQL).")
    pdf.bullet("Subcollections: carts/{userId}/items, favorites/{userId}/items, orders/{orderId}/items, support/{customerId}/messages.")

    pdf.h3("Operations on Data")
    pdf.bullet("Insert: each ViewModel calls a Repository that executes add() to Firestore.")
    pdf.bullet("Read: snapshot listeners from Firestore wrap LiveData - the UI updates automatically on any change.")
    pdf.bullet("Update: flow is View -> ViewModel -> Repository -> Firestore document.update().")
    pdf.bullet("Delete: user confirmation required; the document is removed from Firestore.")

    # ══════════════════════════════════════════════════════════════════════
    # 2. ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("2. Project Architecture / Structure")

    pdf.h2("2.1 Welcome Screen Description - WelcomeActivity")
    pdf.body(
        "The welcome screen is the app's entry point. On launch it checks whether the user is already "
        "logged in (SessionManager.isLoggedIn). If yes, it routes them directly based on their role "
        "(Customer -> CustomerMainActivity; Owner/Manager/Employee -> MainActivity). "
        "If not, it displays two buttons: Sign In and Sign Up."
    )

    pdf.h2("2.2 Screen Descriptions")

    screens = [
        ("1. WelcomeActivity", "Entry point",
         "App logo and two buttons. btnLogin -> LoginActivity; btnRegister -> RoleSelectionActivity."),
        ("2. RoleSelectionActivity", "Role selection during registration",
         "Two options: Owner or Customer. btnRoleOwner opens a dialog requesting secret code 777. "
         "btnRoleCustomer navigates directly to RegisterActivity with the Customer role."),
        ("3. LoginActivity", "Login screen",
         "Fields: etEmail (email address), etPassword (password). "
         "btnLogin verifies credentials via Firebase Auth, updates SessionManager, and routes by role."),
        ("4. RegisterActivity", "Registration screen",
         "Fields: etFullName, etUsername, etEmail, etPhone, etPassword, etConfirmPassword. "
         "Encrypts password with PBKDF2WithHmacSHA256, registers with Firebase Auth, saves profile to Firestore."),
        ("5. MainActivity", "Main screen for staff (Owner / Manager / Employee)",
         "BottomNavigationView with tabs: Dashboard, Inventory, Sales, Tasks, More. "
         "More menu: Orders, Support Inbox, Seasons, Admin, Test Notification, Logout. "
         "Starts AlarmManager for hourly stock checks."),
        ("6. CustomerMainActivity", "Main screen for customers",
         "BottomNavigationView with tabs: Shop, Cart, Orders, Favorites, Support. "
         "Sign Out lock icon in the top bar."),
        ("7. AddEditProductActivity", "Add / Edit product (Owner only)",
         "Fields: product name, category, size, color, quantity, selling price, cost price. "
         "btnSaveProduct saves to Firestore. Access restricted by PermissionManager."),
        ("8. AddSaleActivity", "Record a manual sale",
         "Fields: product ID, quantity, total price, notes. Accessible to all staff roles."),
        ("9. AddEditSeasonActivity", "Season / Collection management",
         "Fields: season name, start date, end date, alert days in advance."),
        ("10. AddEditTaskActivity", "Task management",
         "Fields: title, description, assigned to, status (TODO/IN_PROGRESS/DONE), priority, due date."),
    ]

    for name, role, desc in screens:
        pdf.h3(name)
        pdf.body(f"Role: {role}")
        pdf.body(f"Description: {desc}")

    pdf.h2("2.3 Screen Flow Diagram")
    pdf.code_block("""
  +---------------------+
  |   WelcomeActivity   |
  +----------+----------+
             |
      +-------+-------+
      v               v
 LoginActivity   RoleSelectionActivity
      |               |
      |        +------+------+
      |        v             v
      |   [Dialog 777]  RegisterActivity
      |        |          (Customer)
      |   RegisterActivity
      |       (Owner)
      |            |
      +------+-----+
             v
        [role check]
       +------+------+
       v             v
  MainActivity  CustomerMainActivity
  +--+--+--+--+  +--+--+--+--+--+
  DB INV SAL TASK  SHOP CRT ORD FAV SUP
    """)

    pdf.h2("2.4 Project Class Descriptions (UML Overview)")

    pdf.h3("View Layer (Activities + Fragments)")
    pdf.body(
        "Contains all Activities and Fragments. Responsible only for displaying the UI and capturing "
        "user events. Never accesses data sources directly."
    )

    pdf.h3("ViewModel Layer (9 ViewModels)")
    pdf.body(
        "AuthViewModel, ProductViewModel, SaleViewModel, OrderViewModel, CartViewModel, "
        "FavoritesViewModel, TaskViewModel, SeasonViewModel, SupportViewModel. "
        "Each ViewModel exposes LiveData observed by the View layer."
    )

    pdf.h3("Repository Layer (9 Repositories)")
    pdf.body(
        "UserRepository, ProductRepository, SaleRepository, OrderRepository, CartRepository, "
        "FavoritesRepository, TaskRepository, SeasonRepository, SupportRepository. "
        "Each Repository communicates directly with Firestore."
    )

    pdf.h3("Infrastructure Classes")
    pdf.body(
        "AppDatabase, SessionManager, PermissionManager, CryptoUtil, FirebaseAuthHelper, "
        "NotificationHelper, LowStockReceiver, StorePilotApp."
    )

    # ══════════════════════════════════════════════════════════════════════
    # 3. IMPLEMENTATION
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("3. Project Implementation")

    pdf.h2("3.1 Separation of Logic and Display")
    pdf.body(
        "The project strictly separates layers: the View layer (Activities & Fragments) handles only "
        "UI display and event capturing. The ViewModel + Repository layer handles all processing, "
        "validation, and computation. Data access occurs exclusively through Repositories."
    )

    pdf.h2("3.2 Main Class Descriptions")

    pdf.h3("1. AppDatabase")
    pdf.body("Role: Provides a shared thread pool for background operations.")
    pdf.bullet("dbExecutor: ExecutorService with 4 threads.")
    pdf.body("Note: The database is Firestore only. AppDatabase is retained solely to provide the dbExecutor to other components.")

    pdf.h3("2. SessionManager")
    pdf.body("Role: Singleton for managing the logged-in user in memory.")
    pdf.bullet("Attributes: instance (static), loggedInUser.")
    pdf.bullet("setLoggedInUser(User): marks a user as logged in.")
    pdf.bullet("getLoggedInUser(): returns the current user.")
    pdf.bullet("getUserRole(): returns the user's role string.")
    pdf.bullet("isLoggedIn(): checks if a user is currently logged in.")
    pdf.bullet("logout(): resets state and signs out from Firebase Authentication.")

    pdf.h3("3. PermissionManager")
    pdf.body("Role: Static permission table defining which role can perform which action.")
    pdf.bullet("permissionMap: Map<String, List<String>> linking permission to allowed roles.")
    pdf.bullet("Constants: MANAGE_USERS, MANAGE_PRODUCTS, VIEW_PRODUCTS, CREATE_SALE, VIEW_SALES_HISTORY, MANAGE_SEASONS, VIEW_ADMIN.")
    pdf.bullet("hasPermission(role, permission): checks if a specific role is authorized.")
    pdf.bullet("currentUserHasPermission(permission): checks for the currently logged-in user.")
    pdf.code_block("// Restrict product management to Owner and Store Manager\npermissionMap.put(MANAGE_PRODUCTS, Arrays.asList(OWNER, STORE_MANAGER));")

    pdf.h3("4. CryptoUtil")
    pdf.body("Role: Password encryption using PBKDF2WithHmacSHA256.")
    pdf.bullet("generateSalt(): creates a random 16-byte salt.")
    pdf.bullet("hashPassword(password, salt): hashes the password with the given salt.")
    pdf.bullet("verify(password, salt, hash): verifies a plaintext password against a stored hash.")

    pdf.h3("5. FirebaseAuthHelper")
    pdf.body("Role: Wrapper for FirebaseAuth operations.")
    pdf.bullet("signUp(email, password, displayName, callback): creates a new Firebase Auth account and sets the display name.")
    pdf.bullet("signIn(email, password, callback): authenticates an existing user.")
    pdf.bullet("signOut(): signs the current user out of Firebase.")
    pdf.bullet("getCurrentUid(): returns the UID of the currently authenticated user.")

    pdf.h3("6. StorePilotApp")
    pdf.body("Role: Application class - the initialization entry point for the app.")
    pdf.body("onCreate() performs three actions:")
    pdf.bullet("FirebaseApp.initializeApp(this): initializes Firebase.")
    pdf.bullet("NotificationHelper.createNotificationChannel(this): creates the notification channel.")
    pdf.bullet("scheduleLowStockAlarm(this): schedules the hourly stock check.")
    pdf.code_block(
        "public static void scheduleLowStockAlarm(Context context) {\n"
        "    AlarmManager alarmManager =\n"
        "        (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);\n"
        "    Intent intent = new Intent(context, LowStockReceiver.class);\n"
        "    PendingIntent pendingIntent = PendingIntent.getBroadcast(\n"
        "        context, 0, intent,\n"
        "        PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);\n"
        "    alarmManager.setInexactRepeating(\n"
        "        AlarmManager.RTC_WAKEUP,\n"
        "        System.currentTimeMillis() + AlarmManager.INTERVAL_HOUR,\n"
        "        AlarmManager.INTERVAL_HOUR,\n"
        "        pendingIntent);\n"
        "}"
    )

    pdf.h3("7. NotificationHelper")
    pdf.body("Role: Creates the notification channel and sends low-stock alerts.")
    pdf.bullet("createNotificationChannel(context): creates the 'Low Stock Alerts' channel (required on Android 8+).")
    pdf.bullet("sendLowStockNotification(context, count): posts a HIGH-priority notification showing the number of low-stock products.")

    pdf.h3("8. LowStockReceiver (BroadcastReceiver)")
    pdf.body("Role: BroadcastReceiver triggered by AlarmManager. Queries Firestore for products with quantity <= 5.")
    pdf.body("Flow diagram of onReceive():")
    pdf.code_block(
        "onReceive()\n"
        "    |\n"
        "    v\n"
        "Query Firestore: products where quantity <= 5\n"
        "    |\n"
        "    +-- count > 0 --> NotificationHelper.sendLowStockNotification(count)\n"
        "    |\n"
        "    +-- count == 0 && testMode --> send demo notification + show Toast\n"
        "    |\n"
        "    +-- count == 0 && !testMode --> no action"
    )
    pdf.bullet("checkNow(context, testMode): static method for instant manual triggering. When testMode=true, sends a notification even if no products are low.")

    pdf.h3("9. ProductRepository")
    pdf.body("Role: Manages all product operations against Firestore.")
    pdf.bullet("getAllProducts(): returns LiveData backed by a real-time snapshot listener on the 'products' collection.")
    pdf.bullet("insert(product): adds a new document to the 'products' collection.")
    pdf.bullet("update(product): updates the document identified by firestoreId.")
    pdf.bullet("delete(firestoreId): removes the document.")
    pdf.bullet("getLowStockProducts(threshold): returns products with quantity below the threshold.")

    pdf.h3("10. OrderRepository")
    pdf.body("Role: Manages customer orders including automatic sale creation on delivery.")
    pdf.body("Key method - updateOrderStatus:")
    pdf.code_block(
        "public void updateOrderStatus(Order order, String newStatus) {\n"
        "    db.collection(\"orders\")\n"
        "      .document(order.firestoreId)\n"
        "      .update(\"status\", newStatus);\n"
        "    if (\"DELIVERED\".equals(newStatus)) {\n"
        "        // Automatically create a sale record\n"
        "        Sale sale = new Sale(null, 1, order.getTotalPrice(),\n"
        "            System.currentTimeMillis(), null,\n"
        "            \"Order #\" + order.getId() + \" delivered\");\n"
        "        db.collection(\"sales\").add(sale.toMap());\n"
        "    }\n"
        "}"
    )
    pdf.bullet("getActiveOrders(): returns only orders with status other than DELIVERED or CANCELLED. Filtering is done in Java to avoid Firestore composite index requirements.")

    pdf.h3("11. SupportRepository")
    pdf.body("Role: Manages support chat conversations between customers and staff.")
    pdf.bullet("Firestore structure: support/{customerId} (parent doc) + support/{customerId}/messages/{msgId}.")
    pdf.bullet("sendMessage(): creates the parent document using SetOptions.merge() before adding the message to the subcollection. This ensures the conversation appears in the inbox.")
    pdf.bullet("getMessagesForCustomer(): retrieves messages and sorts them by timestamp in Java (avoiding orderBy composite index).")

    pdf.h2("3.3 Database")
    pdf.h3("Database Overview")
    pdf.body(
        "The project uses Firebase Firestore - a NoSQL cloud database. "
        "Data is organized into Collections and Subcollections."
    )
    pdf.table(
        ["Collection", "Contents"],
        [
            ["users", "User profiles (uid, username, email, role, localId)"],
            ["products", "Inventory items (name, category, quantity, price, costPrice)"],
            ["orders", "Customer orders (customerId, totalPrice, status, paymentMethod)"],
            ["orders/{id}/items", "Individual items within each order"],
            ["sales", "Sale transaction records"],
            ["tasks", "Employee tasks"],
            ["seasons", "Seasonal collections and promotions"],
            ["carts/{userId}/items", "Shopping cart items per customer"],
            ["favorites/{userId}/items", "Wishlist items per customer"],
            ["support/{customerId}", "Support conversation per customer"],
            ["support/{customerId}/messages", "Messages within the conversation"],
        ],
        [70, 120],
    )

    pdf.h3("Operations on the Database")
    pdf.bullet("Read: snapshot listeners wrap LiveData - the UI updates automatically whenever data changes in Firestore.")
    pdf.bullet("Write: collection.add(map) for new records; document.update(field, value) for updates.")
    pdf.bullet("Delete: document.delete() - only after user confirmation.")

    # ══════════════════════════════════════════════════════════════════════
    # 4. USER GUIDE
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("4. User Guide")

    pdf.h2("4.1 System Requirements")
    pdf.bullet("Android version: API 24 (Android 7.0 Nougat) and above.")
    pdf.bullet("Internet connection: required for all operations (Firestore & Firebase Auth).")
    pdf.bullet("Required permissions: INTERNET, POST_NOTIFICATIONS (Android 13+), RECEIVE_BOOT_COMPLETED.")

    pdf.h2("4.2 Tested Versions")
    pdf.bullet("Android 13 (API 33) - Pixel 7 emulator.")
    pdf.bullet("Android 11 (API 30) - physical Samsung device.")
    pdf.bullet("Android 8.0 (API 26) - emulator for compatibility testing.")

    pdf.h2("4.3 First-Time Setup")
    pdf.body("1. Run the app from Android Studio on a device or emulator.")
    pdf.body("2. The welcome screen displays Sign In and Sign Up.")
    pdf.body("3. To create an owner account: tap Sign Up -> select Owner -> enter code 777 -> fill the form.")
    pdf.body("4. To create a customer account: tap Sign Up -> select Customer -> fill the form.")

    pdf.h2("4.4 Usage Instructions")

    pdf.h3("Adding a Product (Owner only)")
    pdf.body("1. Tap the Inventory tab.")
    pdf.body("2. Tap the + floating button.")
    pdf.body("3. Fill in: name, category, size, color, quantity, selling price, cost price.")
    pdf.body("4. Tap Save.")

    pdf.h3("Placing an Order (Customer)")
    pdf.body("1. In the Shop tab, select a product -> tap Add to Cart.")
    pdf.body("2. Go to the Cart tab -> verify items.")
    pdf.body("3. Tap Checkout -> choose payment method and delivery address.")
    pdf.body("4. Tap Place Order -> receive a confirmation screen.")

    pdf.h3("Managing an Order (Store Manager)")
    pdf.body("1. In the More menu, tap Orders.")
    pdf.body("2. Tap an order -> change its status (PENDING -> PROCESSING -> DELIVERED).")
    pdf.body("3. Changing to DELIVERED removes the order from the active list and automatically creates a sale record.")

    pdf.h3("Testing Notifications (Test Mode)")
    pdf.body("1. Log in as Owner.")
    pdf.body("2. Open More menu -> tap [TEST] Low Stock Notification.")
    pdf.body("3. Pull down the device notification shade to see the alert.")

    pdf.h3("Signing Out")
    pdf.bullet("Customer: tap the lock icon in the top bar -> confirm in the dialog.")
    pdf.bullet("Owner/Manager: More menu -> Logout.")

    pdf.h2("4.5 User Messages")
    pdf.table(
        ["Situation", "Message"],
        [
            ["Missing form fields", "Please fill all required fields"],
            ["Password mismatch", "Passwords do not match"],
            ["Password too short", "Password must be at least 6 characters"],
            ["Wrong login credentials", "Incorrect email or password"],
            ["Unauthorized screen access", "Only the Owner can add or edit products"],
            ["Order placed successfully", "Order placed!"],
            ["Low stock (notification)", "X product(s) are running low. Tap to review."],
            ["Notifications blocked", "Notifications blocked - enable in Settings"],
        ],
        [80, 110],
    )

    pdf.h2("4.6 Constraints")
    pdf.bullet("Password length: minimum 6 characters.")
    pdf.bullet("Username: must be unique in the system.")
    pdf.bullet("Email: must be in a valid format.")
    pdf.bullet("Prices: positive values only.")
    pdf.bullet("Stock quantity: cannot go below 0.")

    # ══════════════════════════════════════════════════════════════════════
    # 5. REFLECTION
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("5. Personal Reflection / Summary")

    pdf.h2("5.1 Work Process Description")
    pdf.body(
        "I worked on StorePilot for approximately one year. The process began with the initial concept "
        "- combining a management system and a shopping app in one place - and evolved into a complex "
        "project containing over 90 Java files and dozens of XML layouts."
    )

    pdf.h2("5.2 Successes")
    pdf.bullet("Clean MVVM architecture: achieved complete separation between the View, ViewModel, and Repository layers, enabling easy maintenance and fast development.")
    pdf.bullet("Successful Firebase integration: Firestore as a cloud database enables real-time UI updates without any polling mechanism.")
    pdf.bullet("Permission system: PermissionManager is flexible and makes it easy to add new roles and permissions.")
    pdf.bullet("Automatic notifications: AlarmManager + BroadcastReceiver work reliably even when the app is in the background.")
    pdf.bullet("Automatic sale creation: when an order is marked as DELIVERED, the system automatically creates a sale record and updates revenue.")

    pdf.h2("5.3 Challenges and Difficulties")
    pdf.bullet(
        "LiveData observer nesting: early on I registered observers inside other observers, "
        "creating multiple registrations per update. Solution: two separate observers, each storing "
        "data in a local field, with a merge function called when either updates."
    )
    pdf.bullet(
        "Firestore composite indexes: queries with orderBy on subcollections silently failed without "
        "a composite index in the Firestore Console. Solution: removed orderBy() from all subcollection "
        "queries and sort in Java instead."
    )
    pdf.bullet(
        "Support chat inbox empty: messages were saved in Firestore but did not appear in the inbox. "
        "Root cause: the parent support/{customerId} document was never created before messages were "
        "added to the subcollection. Fix: use SetOptions.merge() on the parent document before every sendMessage() call."
    )
    pdf.bullet(
        "Material3 style errors: the app theme is MaterialComponents (M2), not Material3 (M3). "
        "Had to ensure all layouts used Widget.MaterialComponents.* style prefixes."
    )

    pdf.h2("5.4 Learning Process")
    pdf.bullet("Learned design patterns in depth: Singleton, Observer, Repository, Adapter.")
    pdf.bullet("Mastered Firebase end-to-end: Authentication, Firestore, differences between NoSQL and SQL.")
    pdf.bullet("Improved understanding of security mechanisms: PBKDF2, salts, hashing.")
    pdf.bullet("Understood the critical importance of background threads (ExecutorService) to keep the UI thread responsive.")
    pdf.bullet("Learned to use CountDownLatch for synchronizing asynchronous Firestore calls on background threads.")

    pdf.h2("5.5 Tools Taken Forward")
    pdf.bullet("MVVM architecture: will be used in every future Android project.")
    pdf.bullet("Firebase: a convenient and fast cloud service for small and medium projects.")
    pdf.bullet("CountDownLatch for thread synchronization: an elegant solution for async operations that need to block and wait for a result.")

    pdf.h2("5.6 Retrospective View")
    pdf.body("If I were to start the project again:")
    pdf.bullet("I would use Hilt for Dependency Injection from the start instead of creating instances manually.")
    pdf.bullet("I would implement Kotlin Coroutines instead of ExecutorService - cleaner and safer syntax.")
    pdf.bullet("I would add Unit Tests systematically from day one.")
    pdf.bullet("I would consider using Jetpack Compose instead of XML Views.")

    pdf.h2("5.7 Future Improvements")
    pdf.bullet("Firebase Cloud Messaging: real push notifications from the server, not just local.")
    pdf.bullet("Firebase Storage: image upload for product photos.")
    pdf.bullet("Multi-store support: manage multiple store branches under one account.")
    pdf.bullet("Full i18n: Hebrew, English, and Arabic language support.")

    # ══════════════════════════════════════════════════════════════════════
    # 6. BIBLIOGRAPHY
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("6. Bibliography")
    refs = [
        "Google Inc. (2024). Android Developers Documentation. https://developer.android.com/docs",
        "Google Inc. (2024). Firebase Documentation. https://firebase.google.com/docs",
        "Google Inc. (2024). Firebase Firestore Guide. https://firebase.google.com/docs/firestore",
        "Google Inc. (2024). Material Components for Android. https://github.com/material-components/material-components-android",
        "Oracle Corporation. (2024). Java Cryptography Architecture (JCA) Reference Guide. https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html",
        "NIST. (2017). Special Publication 800-132 - Recommendation for Password-Based Key Derivation. National Institute of Standards and Technology.",
        "Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley Professional.",
        "Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.",
        "JetBrains s.r.o. (2024). Android Studio User Guide. https://developer.android.com/studio/intro",
        "Stack Overflow Community. (2024). Android development Q&A. https://stackoverflow.com/questions/tagged/android",
    ]
    for i, ref in enumerate(refs, 1):
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(10)
        pdf.multi_cell(0, 6, f"{i}. {ref}")
        pdf.ln(2)

    # ══════════════════════════════════════════════════════════════════════
    # 7. APPENDICES
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.h1("7. Appendices")

    pdf.h2("Appendix A - google-services.json")
    pdf.body(
        "Located at app/google-services.json. Contains the Firebase project connection settings: "
        "API_KEY, APP_ID, PROJECT_ID. This file must NOT be committed to a public repository."
    )

    pdf.h2("Appendix B - Project Folder Structure")
    pdf.code_block(
        "StorePilot/\n"
        "+-app/\n"
        "  +-google-services.json\n"
        "  +-build.gradle\n"
        "  +-src/main/\n"
        "    +-AndroidManifest.xml\n"
        "    +-java/com/storepilot/\n"
        "    | +-StorePilotApp.java\n"
        "    | +-MainActivity.java\n"
        "    | +-auth/      (WelcomeActivity, LoginActivity,\n"
        "    | |              RegisterActivity, RoleSelectionActivity)\n"
        "    | +-core/      (AppDatabase, SessionManager, PermissionManager,\n"
        "    | |              CryptoUtil, FirebaseAuthHelper,\n"
        "    | |              NotificationHelper, LowStockReceiver)\n"
        "    | +-customer/  (CustomerMainActivity + 8 Fragments)\n"
        "    | +-manager/   (OrderManagementFragment,\n"
        "    | |              SupportConversationsFragment, SupportInboxFragment)\n"
        "    | +-admin/     (UserManagementFragment)\n"
        "    | +-dashboard/ (DashboardFragment)\n"
        "    | +-inventory/ (ProductListFragment, AddEditProductActivity)\n"
        "    | +-sales/     (SalesHistoryFragment, AddSaleActivity)\n"
        "    | +-tasks/     (TaskListFragment, AddEditTaskActivity)\n"
        "    | +-seasons/   (SeasonListFragment, AddEditSeasonActivity)\n"
        "    | +-db/entities/   (9 Entity classes)\n"
        "    | +-repositories/  (9 Repository classes)\n"
        "    | +-viewmodels/    (9 ViewModel classes)\n"
        "    +-res/\n"
        "      +-layout/   (40+ XML files)\n"
        "      +-drawable/ (icons and graphics)\n"
        "      +-values/   (strings, colors, themes)\n"
        "      +-menu/     (navigation menus)"
    )

    pdf.h2("Appendix C - Project Statistics")
    pdf.table(
        ["Metric", "Count"],
        [
            ["Java files", "90+"],
            ["Activities", "10"],
            ["Fragments", "18"],
            ["ViewModels", "9"],
            ["Repositories", "9"],
            ["Firestore Collections", "7"],
            ["Lines of code", "~6,000"],
        ],
        [100, 90],
    )

    pdf.h2("Appendix D - Advanced Topics Implemented")
    pdf.table(
        ["Topic", "Location in Project"],
        [
            ["Fragments (18 fragments)", "Throughout the entire app"],
            ["Threads (ExecutorService, 4 threads)", "AppDatabase.dbExecutor"],
            ["AlarmManager + BroadcastReceiver", "StorePilotApp + LowStockReceiver"],
            ["Notification + NotificationChannel", "NotificationHelper"],
            ["Firebase Authentication", "FirebaseAuthHelper"],
            ["Firebase Firestore (Remote DB)", "All 9 Repositories"],
            ["AlertDialog (owner code, logout)", "RoleSelectionActivity, CustomerMainActivity"],
            ["Async/Background work", "dbExecutor in every Repository"],
            ["LiveData + ViewModel (MVVM)", "All ViewModel and Repository layers"],
            ["PBKDF2WithHmacSHA256 hashing", "CryptoUtil"],
        ],
        [95, 95],
    )

    pdf.h2("Appendix E - Source Code")
    pdf.body(
        "The full source code is available on GitHub:\n"
        "https://github.com/ahmadhijazys2/StorePilot\n\n"
        "All critical methods are documented with Javadoc comments. "
        "Single-line comments are used in less complex sections."
    )
    pdf.h3("Example Javadoc - CryptoUtil.hashPassword()")
    pdf.code_block(
        "/**\n"
        " * Hashes a plaintext password using PBKDF2WithHmacSHA256.\n"
        " *\n"
        " * @param password  the plaintext password to hash\n"
        " * @param salt      the random salt to mix with the password\n"
        " * @return Base64-encoded hash string\n"
        " */\n"
        "public static String hashPassword(String password, String salt) { ... }"
    )

    out_path = "/home/user/StorePilot/StorePilot_Project_Book.pdf"
    pdf.output(out_path)
    print(f"PDF written to: {out_path}")


if __name__ == "__main__":
    build()
