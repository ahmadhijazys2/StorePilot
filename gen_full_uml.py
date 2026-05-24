#!/usr/bin/env python3
"""Full UML — no Purchase, no VideoMetric. Clean arrows."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# ── Palette ───────────────────────────────────────────────────────────────────
C_ENTITY  = '#1B3A5C'
C_DAO     = '#1565C0'
C_REPO    = '#BF360C'
C_VM      = '#1B5E20'
C_CORE    = '#4A148C'
C_ACT     = '#37474F'
C_FRAG    = '#455A64'

C_UI      = '#0288D1'   # Activity/Fragment → ViewModel arrow
C_BODY    = '#E3F2FD'
C_DAO_BG  = '#E8EAF6'
C_REPO_BG = '#FBE9E7'
C_VM_BG   = '#E8F5E9'
C_CORE_BG = '#F3E5F5'
C_ACT_BG  = '#ECEFF1'
C_GOLD    = '#F4A261'
C_WHITE   = '#FFFFFF'
C_DARK    = '#212121'
C_GREY    = '#757575'

FW, FH = 34, 28


# ── Helpers ───────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, title, attrs, hc, bc, fs=6.0, ts=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.03',
                                facecolor=bc, edgecolor=hc, linewidth=0.9, zorder=2))
    hh = max(h * 0.20, 0.30)
    ax.add_patch(FancyBboxPatch((x, y+h-hh), w, hh, boxstyle='round,pad=0.02',
                                facecolor=hc, edgecolor=hc, linewidth=0.9, zorder=3))
    ax.text(x+w/2, y+h-hh/2, title, ha='center', va='center',
            fontsize=ts, fontweight='bold', color='white', zorder=4)
    ax.plot([x, x+w], [y+h-hh, y+h-hh], color=hc, lw=0.6, zorder=4)
    if attrs:
        row = (h - hh - 0.06) / len(attrs)
        for i, a in enumerate(attrs):
            ax.text(x+0.07, y+h-hh-0.06-(i+0.5)*row, a,
                    ha='left', va='center', fontsize=fs,
                    color=C_DARK, fontfamily='monospace', zorder=4)


def arr(ax, x1, y1, x2, y2, color, lw=1.0, label='', rad=0.0,
        style='->', lbl_side='top'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}',
                                mutation_scale=9))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        dy = 0.10 if lbl_side == 'top' else -0.16
        ax.text(mx, my+dy, label, ha='center', va='center',
                fontsize=5.5, color=color, fontstyle='italic',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=0.5))


def dash_arr(ax, x1, y1, x2, y2, color, lw=0.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle='dashed',
                                connectionstyle='arc3,rad=0',
                                mutation_scale=7))


def ui_link(ax, fx, fy, vx, vy, rad=0.0):
    """Dotted arrow: Activity/Fragment (bottom) → ViewModel (top)."""
    ax.annotate('', xy=(vx, vy), xytext=(fx, fy),
                arrowprops=dict(arrowstyle='->', color=C_UI, lw=0.65,
                                linestyle='dotted',
                                connectionstyle=f'arc3,rad={rad}',
                                mutation_scale=6))


def hline(ax, y, color=C_GOLD, lw=1.5, ls='--'):
    ax.plot([0.3, FW-0.3], [y, y], color=color, lw=lw, linestyle=ls, zorder=1)


def sec(ax, x, y, text, color):
    ax.text(x, y, f'▶  {text}', fontsize=9.5, fontweight='bold', color=color)


# ═════════════════════════════════════════════════════════════════════════════
def build():
    fig, ax = plt.subplots(figsize=(FW, FH))
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.axis('off')
    fig.patch.set_facecolor(C_WHITE)

    # Title
    ax.text(FW/2, FH-0.45, 'StorePilot — UML Class Diagram',
            ha='center', fontsize=22, fontweight='bold', color=C_ENTITY)
    ax.text(FW/2, FH-1.0,
            'Entities · DAOs · Repositories · ViewModels · Core/Helpers · Activities & Fragments',
            ha='center', fontsize=10, color=C_GREY)
    hline(ax, FH-1.35, C_GOLD, lw=2.5, ls='-')

    # ══════════════════════════════════════════════════════════════════════
    # 1.  ENTITIES
    # ══════════════════════════════════════════════════════════════════════
    sec(ax, 0.35, FH-1.65, 'ENTITIES  (Room @Entity — 10 tables)', C_ENTITY)

    EW, EH = 3.0, 2.55
    EY = FH - 1.90  # top of box = EY - EH

    # Row-1: User  Product  Order  OrderItem  CartItem
    e_r1 = [
        (0.35, 'User',
         ['id: int (PK)', 'fullName: String', 'username: String *',
          'email: String *', 'phone: String',
          'passwordHash: String', 'salt: String',
          'role: String', 'createdAt: long']),
        (3.55, 'Product',
         ['id: int (PK)', 'name: String', 'category: String',
          'size: String', 'color: String', 'quantity: int',
          'price: double', 'costPrice: double',
          'imageUrl: String', 'createdAt: long']),
        (6.75, 'Order',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'totalPrice: double', 'status: String',
          'createdAt: long', 'paymentMethod: String',
          'shippingAddress: String']),
        (9.95, 'OrderItem',
         ['id: int (PK)', 'orderId: int (FK→Order)',
          'productId: int (FK→Product)',
          'quantity: int', 'unitPrice: double']),
        (13.15, 'CartItem',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'productId: int (FK→Product)', 'quantity: int']),
    ]
    for (ex, name, attrs) in e_r1:
        box(ax, ex, EY-EH, EW, EH, name, attrs, C_ENTITY, C_BODY)

    # Row-2: Sale  Task  Season  SupportMessage  Favorite
    EY2 = EY - EH - 0.55
    EH2 = 2.55
    e_r2 = [
        (0.35, 'Sale',
         ['id: int (PK)', 'productId: int (FK→Product)',
          'quantity: int', 'totalPrice: double',
          'saleDate: long', 'soldBy: int (FK→User)',
          'notes: String']),
        (3.55, 'Task',
         ['id: int (PK)', 'title: String',
          'description: String',
          'assignedTo: int (FK→User)',
          'createdBy: int (FK→User)',
          'status: String', 'priority: String',
          'isPrivate: boolean', 'dueDate: long',
          'createdAt: long']),
        (6.75, 'Season',
         ['id: int (PK)', 'name: String',
          'startDate: long', 'endDate: long',
          'alertDaysBeforeEnd: int',
          'isActive: boolean', 'notes: String']),
        (9.95, 'SupportMessage',
         ['id: int (PK)', 'senderId: int (FK→User)',
          'senderRole: String',
          'messageText: String', 'imageUrl: String',
          'timestamp: long',
          'customerId: int (FK→User)',
          'isRead: boolean']),
        (13.15, 'Favorite',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'productId: int (FK→Product)',
          'addedAt: long']),
    ]
    for (ex, name, attrs) in e_r2:
        box(ax, ex, EY2-EH2, EW, EH2, name, attrs, C_ENTITY, C_BODY)

    # ── Entity arrows ─────────────────────────────────────────────────────
    # centres (mid-x, mid-y of right edge / left edge etc.)
    def ecx(col): return [0.35,3.55,6.75,9.95,13.15][col] + EW/2
    def ecy1(col): return EY - EH/2          # row-1 centre y
    def ecy2(col): return EY2 - EH2/2        # row-2 centre y
    def ebot1(col): return EY - EH            # bottom of row-1
    def ebot2(col): return EY2 - EH2          # bottom of row-2
    def etop2(col): return EY2                # top of row-2
    def eright1(col): return [0.35,3.55,6.75,9.95,13.15][col] + EW
    def eleft1(col): return [0.35,3.55,6.75,9.95,13.15][col]

    # User → Order  (1:N, horizontal)
    arr(ax, eright1(0), ecy1(0), eleft1(2), ecy1(2),
        C_ENTITY, lw=1.5, label='1:N')
    # Order → OrderItem (1:N, horizontal)
    arr(ax, eright1(2), ecy1(2), eleft1(3), ecy1(3),
        '#1565C0', lw=1.5, label='1:N')
    # Product → OrderItem (diagonal down-right)
    arr(ax, ecx(1), ebot1(1), ecx(3), EY-EH+0.4,
        '#E65100', lw=1.0, label='1:N', rad=-0.25)
    # User → CartItem  (horizontal row1, slightly offset)
    arr(ax, eright1(0), EY-EH+0.55, eleft1(4), EY-EH+0.55,
        '#2E7D32', lw=1.2, label='1:N (customerId)', lbl_side='top')
    # Product → CartItem
    arr(ax, eright1(1), EY-EH+0.25, eleft1(4), EY-EH+0.25,
        '#E65100', lw=0.9, label='1:N', lbl_side='top')
    # User → Sale (vertical, left side)
    arr(ax, ecx(0), ebot1(0), ecx(0), etop2(0),
        '#E65100', lw=1.2, label='1:N', lbl_side='top')
    # User → Task
    arr(ax, ecx(0)+0.2, ebot1(0), ecx(1)+0.2, etop2(1),
        '#7B1FA2', lw=1.2, label='1:N', rad=0.2)
    # User → SupportMessage
    arr(ax, eright1(0), ecy1(0)-0.5, eleft1(3), etop2(3)+0.2,
        '#00838F', lw=1.0, label='1:N (senderId)', rad=0.15)
    # User → Favorite
    arr(ax, eright1(0), ecy1(0)-0.9, eleft1(4), etop2(4)+0.2,
        '#7B1FA2', lw=0.9, label='1:N (customerId)', rad=0.1)
    # Product → Sale
    arr(ax, ecx(1)-0.2, ebot1(1), ecx(0)-0.2, etop2(0),
        '#E65100', lw=0.9, label='1:N', rad=-0.25)
    # Product → Favorite
    arr(ax, eright1(1), ecy1(1)-0.5, eleft1(4), EY2-EH2*0.6,
        '#E65100', lw=0.9, label='1:N', rad=0.1)

    hline(ax, EY2-EH2-0.3)

    # ══════════════════════════════════════════════════════════════════════
    # 2.  DAOs
    # ══════════════════════════════════════════════════════════════════════
    DY = EY2 - EH2 - 0.30
    sec(ax, 0.35, DY, 'DAOs  (@Dao interfaces — 9 DAOs)', C_DAO)
    DY -= 0.28
    DW, DH = 3.5, 1.65

    daos = [
        (0.35,  'UserDao',
         ['insert/update/delete(User)',
          'getByUsername(): LiveData<User>',
          'getByEmail(): LiveData<User>',
          'getAll(): LiveData<List<User>>',
          'getById(id): LiveData<User>']),
        (4.05,  'ProductDao',
         ['insert/update/delete(Product)',
          'getAll(): LiveData<List<Product>>',
          'getLowStock(thr): LiveData',
          'searchProducts(q): LiveData',
          'getById(id): LiveData<Product>']),
        (7.75,  'OrderDao',
         ['insert/update(Order)',
          'getAll(): LiveData<List<Order>>',
          'getByCustomer(cId): LiveData',
          'getTodayCount(start): LiveData<Integer>',
          'getTodayRevenue(start): LiveData<Double>']),
        (11.45, 'OrderItemDao',
         ['insert(OrderItem)',
          'getByOrder(orderId): LiveData',
          'getAll(): LiveData<List<OrderItem>>']),
        (15.15, 'CartDao',
         ['insert/update/delete(CartItem)',
          'getByCustomer(cId): LiveData',
          'getCount(cId): LiveData<Integer>',
          'clearCart(cId)']),
        (18.85, 'FavoriteDao',
         ['insert/delete(Favorite)',
          'getByCustomer(cId): LiveData',
          'isFavorite(cId,pId): LiveData<Boolean>']),
        (22.55, 'SaleDao',
         ['insert/update/delete(Sale)',
          'getAll(): LiveData<List<Sale>>',
          'getSalesTotalByWeek(ref): LiveData',
          'getSalesTotalByMonth(ref): LiveData',
          'getTodaySalesTotal(s,e): LiveData']),
        (26.25, 'TaskDao',
         ['insert/update/delete(Task)',
          'getAll(): LiveData', 'getByUser(uid): LiveData',
          'getTeamTasks(): LiveData',
          'getPrivateTasks(uid): LiveData',
          'getPendingTaskCount(uid): LiveData']),
        (29.95, 'SupportMsgDao',
         ['insert/update(SupportMessage)',
          'getMessagesForCustomer(cId): LiveData',
          'getConversationCustomerIds(): LiveData',
          'getLatestMessage(cId): SupportMessage',
          'getUnreadCount(cId): LiveData',
          'markAllAsRead(cId)']),
    ]
    for (dx, name, attrs) in daos:
        box(ax, dx, DY-DH, DW, DH, name, attrs, C_DAO, C_DAO_BG, fs=5.7, ts=7.0)

    hline(ax, DY-DH-0.28)

    # ══════════════════════════════════════════════════════════════════════
    # 3.  REPOSITORIES
    # ══════════════════════════════════════════════════════════════════════
    RY = DY - DH - 0.28
    sec(ax, 0.35, RY, 'Repositories  (9 repos — data layer, runs on dbExecutor)', C_REPO)
    RY -= 0.28
    RW, RH = 3.5, 1.55

    repos = [
        (0.35,  'UserRepository',
         ['login(username,pwd): LiveData<User>',
          'register(User)', 'getAllUsers(): LiveData',
          'deleteUser(User)']),
        (4.05,  'ProductRepository',
         ['insert/update/delete(Product)',
          'getAllProducts(): LiveData',
          'getLowStock(thr): LiveData',
          'search(query): LiveData']),
        (7.75,  'OrderRepository',
         ['placeOrder(cId,method,addr,items)',
          'updateOrderStatus(orderId,status)',
          'getByCustomer(cId): LiveData',
          'getAllOrders(): LiveData',
          'getTodayOrderCount(): LiveData']),
        (11.45, 'CartRepository',
         ['addToCart(CartItem)',
          'updateCartItem(CartItem)',
          'removeCartItem(CartItem)',
          'getCartItems(cId): LiveData',
          'getCartCount(cId): LiveData',
          'clearCart(cId)']),
        (15.15, 'FavoritesRepository',
         ['addFavorite(cId,pId)',
          'removeFavorite(cId,pId)',
          'getFavorites(cId): LiveData',
          'isFavorite(cId,pId): LiveData']),
        (18.85, 'SaleRepository',
         ['insertSale(Sale)',
          'getAllSales(): LiveData',
          'getSalesTotalByRange(): LiveData',
          'getTodaySalesTotal(): LiveData']),
        (22.55, 'TaskRepository',
         ['insert/update/delete(Task)',
          'getAllTasks(): LiveData',
          'getByUser(uid): LiveData',
          'getTeamTasks(): LiveData',
          'getPrivateTasks(uid): LiveData',
          'getPendingCount(uid): LiveData']),
        (26.25, 'SeasonRepository',
         ['insert/update/delete(Season)',
          'getAllSeasons(): LiveData',
          'getActiveSeason(): LiveData',
          'getById(id): LiveData']),
        (29.95, 'SupportRepository',
         ['sendMessage(SupportMessage)',
          'getMessages(cId): LiveData',
          'getConversations(): LiveData',
          'markAllRead(cId)']),
    ]
    for (rx, name, attrs) in repos:
        box(ax, rx, RY-RH, RW, RH, name, attrs, C_REPO, C_REPO_BG, fs=5.7, ts=7.0)

    # Repo → DAO dashed arrows (straight vertical)
    rd_map = [
        (0.35,  0.35),   # UserRepo → UserDao
        (4.05,  4.05),   # ProductRepo → ProductDao
        (7.75,  7.75),   # OrderRepo → OrderDao + OrderItemDao
        (11.45, 15.15),  # CartRepo → CartDao
        (15.15, 18.85),  # FavRepo → FavoriteDao
        (18.85, 22.55),  # SaleRepo → SaleDao
        (22.55, 26.25),  # TaskRepo → TaskDao
        (26.25, 29.95),  # SeasonRepo → SupportMsgDao (no SeasonDao shown – closest)
        (29.95, 29.95),  # SupportRepo → SupportMsgDao
    ]
    for (rx, dx) in rd_map:
        dash_arr(ax, rx+RW/2, RY-RH, dx+DW/2, DY-DH,
                 C_REPO, lw=0.9)

    hline(ax, RY-RH-0.28)

    # ══════════════════════════════════════════════════════════════════════
    # 4.  VIEW MODELS
    # ══════════════════════════════════════════════════════════════════════
    VY = RY - RH - 0.28
    sec(ax, 0.35, VY, 'ViewModels  (9 ViewModels — AndroidViewModel, lifecycle-aware)', C_VM)
    VY -= 0.28
    VW, VH = 3.5, 1.55

    vms = [
        (0.35,  'AuthViewModel',
         ['login(username,pwd)',
          'register(User)',
          'loggedInUser: MutableLiveData<User>',
          'loginError: MutableLiveData<String>']),
        (4.05,  'ProductViewModel',
         ['getAllProducts(): LiveData',
          'getLowStock(): LiveData',
          'insert/update/delete(Product)',
          'search(query): LiveData']),
        (7.75,  'OrderViewModel',
         ['placeOrder(cId,method,addr,items)',
          'updateOrderStatus(id,status)',
          'getByCustomer(cId): LiveData',
          'orderPlaced: MutableLiveData<Boolean>']),
        (11.45, 'CartViewModel',
         ['getCartItems(cId): LiveData',
          'addToCart(pId,qty)',
          'update/remove(CartItem)',
          'clearCart(cId)',
          'cartCount: LiveData<Integer>']),
        (15.15, 'FavoritesViewModel',
         ['getFavorites(cId): LiveData',
          'addFavorite(cId,pId)',
          'removeFavorite(cId,pId)',
          'isFavorite(cId,pId): LiveData']),
        (18.85, 'SaleViewModel',
         ['getAllSales(): LiveData',
          'insertSale(Sale)',
          'getTodayTotal(): LiveData',
          'getTotalByRange(): LiveData']),
        (22.55, 'TaskViewModel',
         ['getAll/ByUser/Team/Private(): LiveData',
          'insert/update/delete(Task)',
          'getPendingCount(uid): LiveData',
          'currentTab: MutableLiveData<Integer>']),
        (26.25, 'SeasonViewModel',
         ['getAllSeasons(): LiveData',
          'getActive(): LiveData',
          'insert/update/delete(Season)',
          'getById(id): LiveData']),
        (29.95, 'SupportViewModel',
         ['getMessages(cId): LiveData',
          'sendMessage(cId,text,role)',
          'getConversations(): LiveData',
          'markRead(cId)']),
    ]
    for (vx, name, attrs) in vms:
        box(ax, vx, VY-VH, VW, VH, name, attrs, C_VM, C_VM_BG, fs=5.7, ts=7.0)

    # VM → Repo arrows (straight vertical)
    for (vx, rx) in [(0.35,0.35),(4.05,4.05),(7.75,7.75),(11.45,11.45),
                     (15.15,15.15),(18.85,18.85),(22.55,22.55),(26.25,26.25),(29.95,29.95)]:
        arr(ax, vx+VW/2, VY-VH, rx+RW/2, RY-RH,
            C_VM, lw=0.85)

    hline(ax, VY-VH-0.28)

    # ══════════════════════════════════════════════════════════════════════
    # 5.  CORE / HELPERS
    # ══════════════════════════════════════════════════════════════════════
    CY = VY - VH - 0.28
    sec(ax, 0.35, CY, 'Core & Helpers  (singletons · utilities · Firebase wrappers)', C_CORE)
    CY -= 0.28
    CW, CH = 3.85, 1.80

    cores = [
        (0.35,  'AppDatabase',
         ['singleton (volatile INSTANCE)',
          'dbExecutor: ExecutorService (4 threads)',
          'getUserDao(): UserDao  …×10 DAOs',
          'getInstance(ctx): AppDatabase',
          'seedDemoData(ctx)',
          'version=2, fallbackToDestructiveMigration']),
        (4.40,  'SessionManager',
         ['singleton', 'loggedInUser: User (in-memory)',
          'getInstance(): SessionManager',
          'setLoggedInUser(User)',
          'getLoggedInUser(): User',
          'clearSession()',  'isLoggedIn(): boolean']),
        (8.45,  'CryptoUtil',
         ['ALGORITHM: PBKDF2WithHmacSHA256',
          'ITERATIONS: 65 536   KEY_LEN: 256 bit',
          'generateSalt(): String  (SecureRandom)',
          'hashPassword(pwd,salt): String',
          'verifyPassword(pwd,hash,salt): boolean']),
        (12.50, 'PermissionManager',
         ['static role→permission map',
          'hasPermission(role,perm): boolean',
          'Permissions: MANAGE_USERS, MANAGE_PRODUCTS,',
          '  VIEW_PRODUCTS, CREATE_SALE,',
          '  VIEW_SALES_HISTORY, MANAGE_TASKS,',
          '  MANAGE_SEASONS, VIEW_ADMIN']),
        (16.55, 'NotificationHelper',
         ['CHANNEL_ID: storepilot_low_stock',
          'NOTIF_ID: 1001',
          'createChannel(ctx)',
          'sendLowStockNotification(ctx,count)',
          'cancelAll(ctx)']),
        (20.60, 'LowStockReceiver',
         ['extends BroadcastReceiver',
          'LOW_STOCK_THRESHOLD: 5',
          'onReceive(ctx, intent)',
          'checkNow(ctx) — Firestore query',
          'scheduleAlarm(ctx) — 1-hour repeat']),
        (24.65, 'FirebaseAuthHelper',
         ['auth: FirebaseAuth',
          'signUp(email,pwd,callback)',
          'signIn(email,pwd,callback)',
          'signOut()',
          'getCurrentUser(): FirebaseUser']),
        (28.70, 'FirebaseConfig',
         ['COLLECTION: "products"',
          'LOW_STOCK_FIELD: "quantity"',
          'getFirestore(): FirebaseFirestore',
          'getAuth(): FirebaseAuth']),
    ]
    for (cx, name, attrs) in cores:
        box(ax, cx, CY-CH, CW, CH, name, attrs, C_CORE, C_CORE_BG, fs=5.6, ts=7.0)

    hline(ax, CY-CH-0.28)

    # ══════════════════════════════════════════════════════════════════════
    # 6.  ACTIVITIES & FRAGMENTS
    # ══════════════════════════════════════════════════════════════════════
    AY = CY - CH - 0.28
    sec(ax, 0.35, AY, 'Activities & Fragments  (UI Layer)', C_ACT)
    AY -= 0.28
    AW, AH = 3.85, 1.55

    # Auth activities
    sec(ax, 0.35, AY - 0.05, '  Auth / Entry', C_ACT)
    auth = [
        (0.35,  'StorePilotApp',
         ['extends Application', 'initFirebase()',
          'createNotificationChannel()',
          'scheduleAlarm() — AlarmManager']),
        (4.40,  'WelcomeActivity',
         ['extends AppCompatActivity',
          'checkSession() → navigateByRole()',
          '→ LoginActivity | RoleSelectionActivity']),
        (8.45,  'RoleSelectionActivity',
         ['extends AppCompatActivity',
          'selectedRole: String (OWNER|CUSTOMER)',
          '→ RegisterActivity(role=…)']),
        (12.50, 'LoginActivity',
         ['extends BaseActivity',
          'AuthViewModel', 'login(username,pwd)',
          '→ CustomerMainActivity | MainActivity']),
        (16.55, 'RegisterActivity',
         ['extends AppCompatActivity',
          'role: String (pre-filled)',
          'AuthViewModel.register(User)',
          '→ LoginActivity']),
        (20.60, 'SetupActivity',
         ['extends AppCompatActivity',
          'First-run owner creation',
          'enableDemoMode(): seedDemoData()',
          '→ MainActivity']),
        (24.65, 'BaseActivity',
         ['extends AppCompatActivity',
          'checkPermission(perm): boolean',
          'requirePermission(perm)',
          'showToast(msg)']),
        (28.70, 'MainActivity',
         ['extends BaseActivity',
          'bottom nav — 5 tabs',
          'PermissionManager gating',
          'SessionManager.getLoggedInUser()']),
    ]
    for (ax2, name, attrs) in auth:
        box(ax, ax2, AY-AH-0.25, AW, AH, name, attrs, C_ACT, C_ACT_BG, fs=5.6, ts=7.0)

    hline(ax, AY-AH-0.55, '#90A4AE', lw=1.0, ls=':')

    # Customer fragments
    FY = AY - AH - 0.55
    sec(ax, 0.35, FY, '  Customer UI', C_FRAG)
    FY -= 0.22
    FW2, FH2 = 3.85, 1.45

    cust = [
        (0.35,  'CustomerMainActivity',
         ['bottom nav — 5 tabs',
          'CustomerHomeFragment | CartFragment',
          'OrderHistoryFragment | FavoritesFragment',
          'SupportChatFragment']),
        (4.40,  'CustomerHomeFragment',
         ['ProductViewModel + CartViewModel',
          'GridLayoutManager (2 cols)',
          'live search — TextWatcher',
          '→ ProductDetailFragment']),
        (8.45,  'ProductDetailFragment',
         ['ProductViewModel',
          'CartViewModel.addToCart()',
          'FavoritesViewModel.addFavorite()',
          '← Back to CustomerHomeFragment']),
        (12.50, 'CartFragment',
         ['CartViewModel',
          'CartItemAdapter (+/−/trash)',
          'total price footer',
          '→ CheckoutFragment']),
        (16.55, 'CheckoutFragment',
         ['CartViewModel + OrderViewModel',
          'ProductViewModel (price lookup)',
          'address + payment radio group',
          '→ OrderConfirmationFragment']),
        (20.60, 'OrderHistoryFragment',
         ['OrderViewModel',
          'CustomerOrderAdapter',
          'colour-coded status badges',
          'LiveData auto-refresh']),
        (24.65, 'FavoritesFragment',
         ['FavoritesViewModel + CartViewModel',
          'heart toggle → removeFavorite()',
          '+ Cart inline button',
          'LiveData auto-refresh']),
        (28.70, 'SupportChatFragment',
         ['SupportViewModel',
          'MessageAdapter (sent / received)',
          'stackFromEnd=true',
          'markAllRead on open']),
    ]
    for (fx, name, attrs) in cust:
        box(ax, fx, FY-FH2-0.05, FW2, FH2, name, attrs, C_FRAG, C_ACT_BG, fs=5.6, ts=7.0)

    hline(ax, FY-FH2-0.35, '#90A4AE', lw=1.0, ls=':')

    # Manager fragments
    MY = FY - FH2 - 0.35
    sec(ax, 0.35, MY, '  Manager / Staff UI', '#546E7A')
    MY -= 0.22
    MH = 1.45

    mgr = [
        (0.35,  'DashboardFragment',
         ['SaleVM + ProductVM + OrderVM',
          'TaskVM + SeasonVM',
          '4 KPI cards + season alert card',
          'LiveData auto-refresh']),
        (4.40,  'ProductListFragment',
         ['ProductViewModel',
          'ProductListAdapter',
          'FAB gated by MANAGE_PRODUCTS',
          '→ ProductDetailsFragment']),
        (8.45,  'ProductDetailsFragment',
         ['ProductViewModel',
          'full detail + edit / delete',
          'permission gating',
          '→ AddEditProductActivity']),
        (12.50, 'AddEditProductActivity',
         ['ProductViewModel',
          'insert / update (Product)',
          'image URL input',
          '→ finish() back to list']),
        (16.55, 'OrderManagementFragment',
         ['OrderViewModel',
          'ManagerOrderAdapter',
          'status Spinner (firstTime guard)',
          'PENDING→PROCESSING→SHIPPED…']),
        (20.60, 'TaskListFragment',
         ['TaskViewModel  (switchMap tabs)',
          '3 tabs: My Tasks / Team / Private',
          'TaskAdapter + priority chips',
          'FAB → AddEditTaskActivity']),
        (24.65, 'SalesHistoryFragment',
         ['SaleViewModel + SaleAdapter',
          'date-range filter',
          'total aggregation row',
          'FAB → AddSaleActivity']),
        (28.70, 'SeasonListFragment',
         ['SeasonViewModel + SeasonAdapter',
          'end-date alert badge',
          'FAB → AddEditSeasonActivity',
          'isActive toggle']),
    ]
    for (mx, name, attrs) in mgr:
        box(ax, mx, MY-MH-0.05, FW2, MH, name, attrs, '#546E7A', C_ACT_BG, fs=5.6, ts=7.0)

    hline(ax, MY-MH-0.35, '#90A4AE', lw=1.0, ls=':')

    # Support + Admin fragments
    SY = MY - MH - 0.35
    sec(ax, 0.35, SY, '  Support & Admin', '#455A64')
    SY -= 0.22
    SH = 1.40
    supp = [
        (0.35,  'SupportConversationsFragment',
         ['SupportViewModel',
          'ConversationListAdapter',
          'manager inbox view',
          '→ SupportInboxFragment(cId)']),
        (4.40,  'SupportInboxFragment',
         ['SupportViewModel',
          'MessageAdapter (dual view)',
          'reply as STAFF role',
          'markAllRead on open']),
        (8.45,  'UserManagementFragment',
         ['UserAdapter (read-only list)',
          'OWNER only — VIEW_ADMIN perm',
          'displays all registered users']),
        (12.50, 'AddEditTaskActivity',
         ['TaskViewModel',
          'insert / update (Task)',
          'priority + status spinners',
          'due-date DatePicker']),
        (16.55, 'AddSaleActivity',
         ['SaleViewModel + ProductViewModel',
          'insert(Sale)',
          'auto-decrement product.quantity']),
        (20.60, 'AddEditSeasonActivity',
         ['SeasonViewModel',
          'insert / update (Season)',
          'date pickers + alertDays field',
          'isActive checkbox']),
    ]
    for (sx, name, attrs) in supp:
        box(ax, sx, SY-SH-0.05, FW2, SH, name, attrs, '#455A64', C_ACT_BG, fs=5.6, ts=7.0)

    # ══════════════════════════════════════════════════════════════════════
    # 7.  Activity / Fragment → ViewModel  (dotted blue arrows)
    # ══════════════════════════════════════════════════════════════════════
    vm_btm = VY - VH          # bottom edge of all ViewModel boxes ≈ 14.00

    # x-centre helpers  (all UI sections share the same column x-positions)
    def vxc(i): return [0.35,4.05,7.75,11.45,15.15,18.85,22.55,26.25,29.95][i] + VW/2
    def uxc(i): return [0.35,4.40,8.45,12.50,16.55,20.60,24.65,28.70][i] + AW/2

    # ── Auth Activities  (top y = AY - 0.25) ─────────────────────────────
    ui_link(ax, uxc(3), AY-0.25, vxc(0), vm_btm, rad= 0.25)  # LoginActivity       → AuthVM
    ui_link(ax, uxc(4), AY-0.25, vxc(0), vm_btm, rad= 0.30)  # RegisterActivity    → AuthVM

    # ── Customer Fragments  (top y = FY - 0.05) ──────────────────────────
    ui_link(ax, uxc(1), FY-0.05, vxc(1), vm_btm, rad=-0.05)  # CustomerHomeFrag    → ProductVM
    ui_link(ax, uxc(1), FY-0.05, vxc(3), vm_btm, rad=-0.15)  # CustomerHomeFrag    → CartVM
    ui_link(ax, uxc(2), FY-0.05, vxc(1), vm_btm, rad=-0.05)  # ProductDetailFrag   → ProductVM
    ui_link(ax, uxc(2), FY-0.05, vxc(3), vm_btm, rad= 0.08)  # ProductDetailFrag   → CartVM
    ui_link(ax, uxc(2), FY-0.05, vxc(4), vm_btm, rad= 0.14)  # ProductDetailFrag   → FavoritesVM
    ui_link(ax, uxc(3), FY-0.05, vxc(3), vm_btm, rad= 0.05)  # CartFragment        → CartVM
    ui_link(ax, uxc(4), FY-0.05, vxc(2), vm_btm, rad= 0.15)  # CheckoutFrag        → OrderVM
    ui_link(ax, uxc(4), FY-0.05, vxc(3), vm_btm, rad= 0.10)  # CheckoutFrag        → CartVM
    ui_link(ax, uxc(5), FY-0.05, vxc(2), vm_btm, rad= 0.20)  # OrderHistoryFrag    → OrderVM
    ui_link(ax, uxc(6), FY-0.05, vxc(4), vm_btm, rad= 0.10)  # FavoritesFrag       → FavoritesVM
    ui_link(ax, uxc(6), FY-0.05, vxc(3), vm_btm, rad= 0.18)  # FavoritesFrag       → CartVM
    ui_link(ax, uxc(7), FY-0.05, vxc(8), vm_btm, rad= 0.05)  # SupportChatFrag     → SupportVM

    # ── Manager Fragments  (top y = MY - 0.05) ───────────────────────────
    ui_link(ax, uxc(0), MY-0.05, vxc(5), vm_btm, rad=-0.30)  # DashboardFrag       → SaleVM
    ui_link(ax, uxc(0), MY-0.05, vxc(1), vm_btm, rad=-0.18)  # DashboardFrag       → ProductVM
    ui_link(ax, uxc(0), MY-0.05, vxc(2), vm_btm, rad=-0.22)  # DashboardFrag       → OrderVM
    ui_link(ax, uxc(0), MY-0.05, vxc(6), vm_btm, rad=-0.35)  # DashboardFrag       → TaskVM
    ui_link(ax, uxc(0), MY-0.05, vxc(7), vm_btm, rad=-0.40)  # DashboardFrag       → SeasonVM
    ui_link(ax, uxc(1), MY-0.05, vxc(1), vm_btm, rad=-0.10)  # ProductListFrag     → ProductVM
    ui_link(ax, uxc(2), MY-0.05, vxc(1), vm_btm, rad=-0.08)  # ProductDetailsFrag  → ProductVM
    ui_link(ax, uxc(3), MY-0.05, vxc(1), vm_btm, rad=-0.05)  # AddEditProductAct   → ProductVM
    ui_link(ax, uxc(4), MY-0.05, vxc(2), vm_btm, rad= 0.25)  # OrderMgmtFrag       → OrderVM
    ui_link(ax, uxc(5), MY-0.05, vxc(6), vm_btm, rad=-0.05)  # TaskListFrag        → TaskVM
    ui_link(ax, uxc(6), MY-0.05, vxc(5), vm_btm, rad= 0.05)  # SalesHistoryFrag    → SaleVM
    ui_link(ax, uxc(7), MY-0.05, vxc(7), vm_btm, rad= 0.05)  # SeasonListFrag      → SeasonVM

    # ── Support / Admin  (top y = SY - 0.05) ─────────────────────────────
    ui_link(ax, uxc(0), SY-0.05, vxc(8), vm_btm, rad=-0.38)  # SupportConvsFrag    → SupportVM
    ui_link(ax, uxc(1), SY-0.05, vxc(8), vm_btm, rad=-0.33)  # SupportInboxFrag    → SupportVM
    ui_link(ax, uxc(3), SY-0.05, vxc(6), vm_btm, rad=-0.10)  # AddEditTaskAct      → TaskVM
    ui_link(ax, uxc(4), SY-0.05, vxc(5), vm_btm, rad=-0.05)  # AddSaleAct          → SaleVM
    ui_link(ax, uxc(4), SY-0.05, vxc(1), vm_btm, rad=-0.12)  # AddSaleAct          → ProductVM
    ui_link(ax, uxc(5), SY-0.05, vxc(7), vm_btm, rad= 0.05)  # AddEditSeasonAct    → SeasonVM

    # ── Legend (top-right) ────────────────────────────────────────────────
    lx, ly = FW - 4.8, FH - 1.55
    ax.text(lx, ly, 'Colour Legend', fontsize=9, fontweight='bold', color=C_DARK)
    legend = [
        (C_ENTITY, C_BODY,    'Entity (@Room @Entity)'),
        (C_DAO,    C_DAO_BG,  'DAO (@Dao interface)'),
        (C_REPO,   C_REPO_BG, 'Repository (data layer)'),
        (C_VM,     C_VM_BG,   'ViewModel (lifecycle-aware)'),
        (C_CORE,   C_CORE_BG, 'Core / Utility / Helper'),
        (C_ACT,    C_ACT_BG,  'Activity / Fragment (UI)'),
    ]
    for i, (hc, bc, lbl) in enumerate(legend):
        ax.add_patch(FancyBboxPatch(
            (lx, ly - 0.44*(i+1)), 0.55, 0.30,
            boxstyle='round,pad=0.03', facecolor=bc,
            edgecolor=hc, linewidth=1.2, zorder=3))
        ax.text(lx + 0.72, ly - 0.44*(i+1) + 0.15, lbl,
                fontsize=7.5, va='center', color=C_DARK)

    ax.text(lx, ly - 0.44*7 - 0.15, 'Arrow Legend', fontsize=9, fontweight='bold', color=C_DARK)
    algs = [
        (C_ENTITY, '-',       '──▶  Entity FK (1:N)'),
        (C_REPO,   'dashed',  '- - ▶  Repo uses DAO'),
        (C_VM,     '-',       '──▶  ViewModel → Repo'),
        (C_UI,     'dotted',  '·····▶  Activity/Fragment uses ViewModel'),
    ]
    for i, (c, ls, lbl) in enumerate(algs):
        ay0 = ly - 0.44*7 - 0.50 - 0.35*i
        ax.plot([lx, lx+0.55], [ay0, ay0], color=c, lw=1.5, linestyle=ls)
        ax.annotate('', xy=(lx+0.57, ay0), xytext=(lx+0.53, ay0),
                    arrowprops=dict(arrowstyle='->', color=c, lw=1.2, mutation_scale=8))
        ax.text(lx + 0.72, ay0, lbl[5:], fontsize=7, va='center', color=c)

    plt.tight_layout(rect=[0, 0, 1, 1])
    out = '/home/user/StorePilot/uml_diagram.png'
    fig.savefig(out, dpi=160, bbox_inches='tight', facecolor=C_WHITE)
    plt.close(fig)
    print(f'Saved: {out}')


if __name__ == '__main__':
    build()
