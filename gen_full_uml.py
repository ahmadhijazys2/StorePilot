#!/usr/bin/env python3
"""Full comprehensive UML class diagram for StorePilot."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# ── Colours ───────────────────────────────────────────────────────────────────
C_ENTITY   = '#1B3A5C'   # dark blue  – entity header
C_DAO      = '#1565C0'   # blue       – DAO header
C_REPO     = '#E65100'   # orange     – repository header
C_VM       = '#2E7D32'   # green      – viewmodel header
C_CORE     = '#4A148C'   # deep purple – core/util header
C_ACT      = '#37474F'   # dark grey  – activity/fragment header
C_BODY     = '#EAF4FB'   # light blue – entity body
C_DAO_BG   = '#E3F2FD'
C_REPO_BG  = '#FFF3E0'
C_VM_BG    = '#E8F5E9'
C_CORE_BG  = '#F3E5F5'
C_ACT_BG   = '#ECEFF1'
C_GOLD     = '#F4A261'
C_WHITE    = '#FFFFFF'
C_BLACK    = '#000000'
C_DARK     = '#212121'
C_GREY     = '#757575'
C_BORDER   = '#B0BEC5'

# Arrow colours per relationship type
AR_ENTITY  = '#1B3A5C'
AR_DAO     = '#1565C0'
AR_REPO    = '#E65100'
AR_VM      = '#2E7D32'
AR_USE     = '#9E9E9E'

FIG_W, FIG_H = 36, 26   # inches – very large canvas for full detail

def draw_box(ax, x, y, w, h, title, attrs, hdr_color, body_color,
             fontsize=6.5, title_size=7.5):
    lw = 1.0
    # body
    bp = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02',
                        facecolor=body_color, edgecolor=hdr_color, linewidth=lw, zorder=2)
    ax.add_patch(bp)
    # header
    hh = h * 0.22
    hp = FancyBboxPatch((x, y+h-hh), w, hh, boxstyle='round,pad=0.01',
                        facecolor=hdr_color, edgecolor=hdr_color, linewidth=lw, zorder=3)
    ax.add_patch(hp)
    ax.text(x+w/2, y+h-hh/2, title, ha='center', va='center',
            fontsize=title_size, fontweight='bold', color='white', zorder=4,
            fontfamily='sans-serif')
    ax.plot([x, x+w], [y+h-hh, y+h-hh], color=hdr_color, lw=0.8, zorder=4)
    # attributes
    n = len(attrs)
    if n == 0:
        return
    row_h = (h - hh - 0.04) / n
    for i, attr in enumerate(attrs):
        ty = y + h - hh - 0.04 - (i + 0.5) * row_h
        ax.text(x + 0.06, ty, attr, ha='left', va='center',
                fontsize=fontsize, color=C_DARK, zorder=4,
                fontfamily='monospace')


def arr(ax, x1, y1, x2, y2, color=AR_ENTITY, lw=1.0, label='',
        rad=0.0, style='->', lbl_offset=(0, 0.05)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}',
                                mutation_scale=8))
    if label:
        mx = (x1+x2)/2 + lbl_offset[0]
        my = (y1+y2)/2 + lbl_offset[1]
        ax.text(mx, my, label, ha='center', va='bottom',
                fontsize=5.5, color=color, fontstyle='italic',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.5))


def section_label(ax, x, y, text, color):
    ax.text(x, y, f'▶  {text}', fontsize=9, fontweight='bold', color=color)


def build():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis('off')
    fig.patch.set_facecolor(C_WHITE)

    # ── Main title ────────────────────────────────────────────────────────────
    ax.text(FIG_W/2, FIG_H - 0.5, 'StorePilot — Complete UML Class Diagram',
            ha='center', va='center', fontsize=22, fontweight='bold', color=C_ENTITY)
    ax.text(FIG_W/2, FIG_H - 1.05,
            'Entities · DAOs · Repositories · ViewModels · Activities/Fragments · Core & Helpers',
            ha='center', va='center', fontsize=10, color=C_GREY)
    ax.plot([0.4, FIG_W-0.4], [FIG_H-1.4, FIG_H-1.4], color=C_GOLD, lw=2.5)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — ENTITIES
    # ══════════════════════════════════════════════════════════════════════════
    section_label(ax, 0.4, FIG_H-1.75, 'ENTITIES  (Room @Entity — 12 tables)', C_ENTITY)

    # Row 1 of entities  y = top of box
    E_TOP = FIG_H - 2.1   # top y for first entity row
    E_H   = 2.4            # entity box height
    E_GAP = 0.3            # gap between entity columns

    entities_r1 = [
        # (x, name, attrs)
        (0.4,  'User',
         ['id: int (PK)', 'fullName: String', 'username: String *',
          'email: String *', 'phone: String', 'passwordHash: String',
          'salt: String', 'role: String', 'createdAt: long']),
        (3.5,  'Product',
         ['id: int (PK)', 'name: String', 'category: String',
          'size: String', 'color: String', 'quantity: int',
          'price: double', 'costPrice: double', 'imageUrl: String',
          'createdAt: long']),
        (6.7,  'Order',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'totalPrice: double', 'status: String',
          'createdAt: long', 'paymentMethod: String',
          'shippingAddress: String']),
        (9.8,  'OrderItem',
         ['id: int (PK)', 'orderId: int (FK→Order)',
          'productId: int (FK→Product)',
          'quantity: int', 'unitPrice: double']),
        (12.9, 'CartItem',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'productId: int (FK→Product)', 'quantity: int']),
        (16.0, 'Favorite',
         ['id: int (PK)', 'customerId: int (FK→User)',
          'productId: int (FK→Product)', 'addedAt: long']),
    ]

    E_W = 2.9
    for (ex, name, attrs) in entities_r1:
        draw_box(ax, ex, E_TOP - E_H, E_W, E_H, name, attrs, C_ENTITY, C_BODY)

    # Row 2 of entities
    E_TOP2 = E_TOP - E_H - 0.5
    entities_r2 = [
        (0.4,  'Sale',
         ['id: int (PK)', 'productId: int (FK→Product)',
          'quantity: int', 'totalPrice: double',
          'saleDate: long', 'soldBy: int (FK→User)', 'notes: String']),
        (3.5,  'Purchase',
         ['id: int (PK)', 'productId: int (FK→Product)',
          'quantity: int', 'totalCost: double',
          'purchaseDate: long', 'purchasedBy: int (FK→User)',
          'supplier: String', 'notes: String']),
        (6.7,  'Task',
         ['id: int (PK)', 'title: String', 'description: String',
          'assignedTo: int (FK→User)', 'createdBy: int (FK→User)',
          'status: String  [TODO|IN_PROGRESS|DONE]',
          'priority: String  [LOW|MED|HIGH]',
          'isPrivate: boolean', 'dueDate: long', 'createdAt: long']),
        (9.8,  'Season',
         ['id: int (PK)', 'name: String',
          'startDate: long', 'endDate: long',
          'alertDaysBeforeEnd: int',
          'isActive: boolean', 'notes: String']),
        (12.9, 'SupportMessage',
         ['id: int (PK)', 'senderId: int (FK→User)',
          'senderRole: String  [CUSTOMER|STAFF]',
          'messageText: String', 'imageUrl: String',
          'timestamp: long', 'customerId: int (FK→User)',
          'isRead: boolean']),
        (16.0, 'VideoMetric',
         ['id: int (PK)', 'title: String', 'platform: String',
          'views: long', 'likes: long', 'shares: long',
          'comments: long', 'videoDate: long',
          'recordedBy: int (FK→User)']),
    ]
    E_H2 = 2.6
    for (ex, name, attrs) in entities_r2:
        draw_box(ax, ex, E_TOP2 - E_H2, E_W, E_H2, name, attrs, C_ENTITY, C_BODY)

    # Entity relationship arrows
    # User→Order (1:N)
    arr(ax, 0.4+E_W, E_TOP-E_H+1.2, 6.7, E_TOP-E_H+1.2, color=AR_ENTITY, lw=1.4, label='1:N')
    # Order→OrderItem (1:N)
    arr(ax, 6.7+E_W, E_TOP-E_H+1.0, 9.8, E_TOP-E_H+1.0, color='#1565C0', lw=1.4, label='1:N')
    # Product→OrderItem
    arr(ax, 3.5+E_W, E_TOP-E_H+0.5, 9.8+E_W/2, E_TOP-E_H+0.5, color='#E65100', lw=1.0, label='1:N', rad=-0.2)
    # User→CartItem
    arr(ax, 0.4+E_W/2, E_TOP-E_H, 12.9+E_W/2, E_TOP-E_H, color='#2E7D32', lw=1.0, label='1:N (customerId)', rad=0.15)
    # Product→CartItem
    arr(ax, 3.5+E_W, E_TOP-E_H+0.3, 12.9, E_TOP-E_H+0.3, color='#E65100', lw=0.9, label='1:N', rad=-0.1)
    # User→Favorite
    arr(ax, 0.4+E_W, E_TOP-E_H+0.8, 16.0, E_TOP-E_H+0.8, color='#7B1FA2', lw=1.0, label='1:N', rad=0.1)
    # User→Sale
    arr(ax, 0.4+E_W/2, E_TOP-E_H, 0.4+E_W/2, E_TOP2-E_H2, color='#E65100', lw=1.2, label='1:N', lbl_offset=(0.2, 0))
    # User→Purchase
    arr(ax, 0.4+E_W, E_TOP-E_H+0.6, 3.5, E_TOP2-E_H2+1.2, color='#E65100', lw=0.9, label='1:N')
    # User→Task
    arr(ax, 0.4+E_W, E_TOP-E_H+1.6, 6.7, E_TOP2-E_H2+1.8, color='#7B1FA2', lw=1.2, label='1:N (assignedTo)', lbl_offset=(0.2, 0.1))
    # User→SupportMessage
    arr(ax, 0.4+E_W, E_TOP-E_H+0.2, 12.9, E_TOP2-E_H2+1.5, color='#00838F', lw=1.0, label='1:N (senderId)', lbl_offset=(0, 0.12))
    # Product→Sale
    arr(ax, 3.5+E_W/2, E_TOP-E_H, 0.4+E_W, E_TOP2-E_H2+0.8, color='#E65100', lw=0.9, label='1:N')
    # Product→Purchase
    arr(ax, 3.5+E_W/2, E_TOP-E_H, 3.5+E_W/2, E_TOP2-E_H2, color='#E65100', lw=0.9, label='1:N', lbl_offset=(0.2, 0))

    sep_y = E_TOP2 - E_H2 - 0.35
    ax.plot([0.4, FIG_W-0.4], [sep_y, sep_y], color=C_GOLD, lw=1.5, linestyle='--')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — DAOs
    # ══════════════════════════════════════════════════════════════════════════
    D_TOP = sep_y - 0.15
    section_label(ax, 0.4, D_TOP, 'DAOs  (@Dao interfaces — 12 DAOs)', C_DAO)
    D_TOP -= 0.3
    D_H = 1.6
    D_W = 2.7
    daos = [
        (0.4,   'UserDao',          ['insert(User)', 'update(User)', 'delete(User)', 'getByUsername()', 'getByEmail()', 'getAll()', 'getById()']),
        (3.3,   'ProductDao',       ['insert(Product)', 'update(Product)', 'delete(Product)', 'getAll()', 'getLowStock(:threshold)', 'search(:q)', 'getById()']),
        (6.2,   'OrderDao',         ['insert(Order)', 'update(Order)', 'getByCustomer(:id)', 'getAll()', 'getTodayCount()', 'getTodayRevenue()']),
        (9.1,   'OrderItemDao',     ['insert(OrderItem)', 'getByOrder(:orderId)', 'getAll()']),
        (12.0,  'CartDao',          ['insert(CartItem)', 'update(CartItem)', 'delete(CartItem)', 'getByCustomer(:id)', 'getCount(:id)', 'clear(:id)']),
        (14.9,  'FavoriteDao',      ['insert(Favorite)', 'delete(Favorite)', 'getByCustomer(:id)', 'isFavorite(:cId,:pId)']),
        (17.8,  'SaleDao',          ['insert(Sale)', 'update(Sale)', 'getAll()', 'getByRange()', 'getTotalByWeek()', 'getTotalByMonth()', 'getToday()']),
        (20.7,  'PurchaseDao',      ['insert(Purchase)', 'update(Purchase)', 'getAll()', 'getByRange()', 'getTotalCost()']),
        (23.6,  'TaskDao',          ['insert(Task)', 'update(Task)', 'delete(Task)', 'getAll()', 'getByUser()', 'getByStatus()', 'getTeam()', 'getPrivate()', 'getPendingCount()']),
        (26.5,  'SeasonDao',        ['insert(Season)', 'update(Season)', 'delete(Season)', 'getAll()', 'getActive()', 'getById()']),
        (29.4,  'SupportMsgDao',    ['insert(Msg)', 'update(Msg)', 'getByCustomer()', 'getConversations()', 'getLatest()', 'getUnreadCount()', 'markAllRead()']),
        (32.3,  'VideoMetricDao',   ['insert(VideoMetric)', 'update(VideoMetric)', 'getAll()', 'getByRange()', 'getById()']),
    ]
    for (dx, name, attrs) in daos:
        draw_box(ax, dx, D_TOP - D_H, D_W, D_H, name, attrs, C_DAO, C_DAO_BG, fontsize=5.8, title_size=7.0)

    # DAO→Entity "implements" arrows (dashed)
    dao_entity_map = [
        (0.4+D_W/2,   E_TOP-E_H, C_DAO),       # UserDao → User (top entity row bottom)
        (3.3+D_W/2,   E_TOP2-E_H2, C_DAO),     # ProductDao → Product
        (6.2+D_W/2,   E_TOP2-E_H2, C_DAO),     # OrderDao
        (9.1+D_W/2,   E_TOP-E_H, C_DAO),       # OrderItemDao
        (12.0+D_W/2,  E_TOP-E_H, C_DAO),       # CartDao
        (14.9+D_W/2,  E_TOP-E_H, C_DAO),       # FavoriteDao
        (17.8+D_W/2,  E_TOP2-E_H2, C_DAO),     # SaleDao
        (20.7+D_W/2,  E_TOP2-E_H2, C_DAO),     # PurchaseDao
        (23.6+D_W/2,  E_TOP2-E_H2, C_DAO),     # TaskDao
        (26.5+D_W/2,  E_TOP2-E_H2, C_DAO),     # SeasonDao
        (29.4+D_W/2,  E_TOP2-E_H2, C_DAO),     # SupportMsgDao
        (32.3+D_W/2,  E_TOP2-E_H2, C_DAO),     # VideoMetricDao
    ]

    sep_y2 = D_TOP - D_H - 0.35
    ax.plot([0.4, FIG_W-0.4], [sep_y2, sep_y2], color=C_GOLD, lw=1.5, linestyle='--')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 — Repositories
    # ══════════════════════════════════════════════════════════════════════════
    R_TOP = sep_y2 - 0.15
    section_label(ax, 0.4, R_TOP, 'Repositories  (10 repositories — wraps DAOs, runs on dbExecutor)', C_REPO)
    R_TOP -= 0.3
    R_H = 1.5
    R_W = 3.1
    repos = [
        (0.4,   'UserRepository',      ['login(username,pwd):LiveData', 'register(User)', 'getAllUsers()', 'deleteUser(User)']),
        (3.7,   'ProductRepository',   ['insert/update/delete(Product)', 'getAllProducts()', 'getLowStock(thr)', 'search(query)']),
        (6.95,  'CartRepository',      ['addToCart(CartItem)', 'update/remove(CartItem)', 'getCartItems(cId)', 'getCartCount(cId)', 'clearCart(cId)']),
        (10.2,  'OrderRepository',     ['placeOrder(cId,items)', 'updateStatus(orderId,s)', 'getByCustomer(cId)', 'getAll()', 'getTodayCount()']),
        (13.45, 'FavoritesRepository', ['addFavorite(cId,pId)', 'removeFavorite(cId,pId)', 'getFavorites(cId)', 'isFavorite()']),
        (16.7,  'SaleRepository',      ['insertSale(Sale)', 'getAllSales()', 'getTotalByRange()', 'getTodayTotal()']),
        (19.95, 'PurchaseRepository',  ['insertPurchase(Purchase)', 'getAllPurchases()', 'getTotalCost()', 'getByRange()']),
        (23.2,  'TaskRepository',      ['insert/update/delete(Task)', 'getAll()', 'getByUser(uid)', 'getTeamTasks()', 'getPrivate(uid)', 'getPendingCount(uid)']),
        (26.45, 'SeasonRepository',    ['insert/update/delete(Season)', 'getAll()', 'getActive()', 'getById(id)']),
        (29.7,  'SupportRepository',   ['sendMessage(Msg)', 'getMessages(cId)', 'getConversations()', 'markAllRead(cId)']),
    ]
    for (rx, name, attrs) in repos:
        draw_box(ax, rx, R_TOP - R_H, R_W, R_H, name, attrs, C_REPO, C_REPO_BG, fontsize=5.8, title_size=7.0)

    sep_y3 = R_TOP - R_H - 0.35
    ax.plot([0.4, FIG_W-0.4], [sep_y3, sep_y3], color=C_GOLD, lw=1.5, linestyle='--')

    # Repo→DAO arrows (dashed, uses)
    repo_dao_pairs = [
        (0.4+R_W/2,  D_TOP-D_H,   0.4+D_W/2),    # UserRepo → UserDao
        (3.7+R_W/2,  D_TOP-D_H,   3.3+D_W/2),    # ProductRepo → ProductDao
        (6.95+R_W/2, D_TOP-D_H,   12.0+D_W/2),   # CartRepo → CartDao
        (10.2+R_W/2, D_TOP-D_H,   6.2+D_W/2),    # OrderRepo → OrderDao + OrderItemDao
        (13.45+R_W/2,D_TOP-D_H,   14.9+D_W/2),   # FavRepo → FavoriteDao
        (16.7+R_W/2, D_TOP-D_H,   17.8+D_W/2),   # SaleRepo → SaleDao
        (19.95+R_W/2,D_TOP-D_H,   20.7+D_W/2),   # PurchaseRepo → PurchaseDao
        (23.2+R_W/2, D_TOP-D_H,   23.6+D_W/2),   # TaskRepo → TaskDao
        (26.45+R_W/2,D_TOP-D_H,   26.5+D_W/2),   # SeasonRepo → SeasonDao
        (29.7+R_W/2, D_TOP-D_H,   29.4+D_W/2),   # SupportRepo → SupportMsgDao
    ]
    for (rx, ry, dx) in repo_dao_pairs:
        ax.annotate('', xy=(dx, ry), xytext=(rx, R_TOP-R_H),
                    arrowprops=dict(arrowstyle='->', color=C_REPO, lw=0.8,
                                    linestyle='dashed', connectionstyle='arc3,rad=0',
                                    mutation_scale=7))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 — ViewModels
    # ══════════════════════════════════════════════════════════════════════════
    V_TOP = sep_y3 - 0.15
    section_label(ax, 0.4, V_TOP, 'ViewModels  (10 ViewModels — AndroidViewModel / ViewModel)', C_VM)
    V_TOP -= 0.3
    V_H = 1.5
    V_W = 3.1
    vms = [
        (0.4,   'AuthViewModel',      ['login(username,pwd)', 'register(User)', 'loggedInUser: LiveData<User>', 'loginError: LiveData<String>']),
        (3.7,   'ProductViewModel',   ['getAllProducts(): LiveData', 'getLowStock(): LiveData', 'insert/update/delete()', 'search(query)']),
        (6.95,  'CartViewModel',      ['getCartItems(cId): LiveData', 'addToCart(pId,qty)', 'update/remove()', 'clearCart()', 'cartCount: LiveData']),
        (10.2,  'OrderViewModel',     ['placeOrder(cId,method,addr,items)', 'updateOrderStatus()', 'getByCustomer(): LiveData', 'orderPlaced: MutableLiveData']),
        (13.45, 'FavoritesViewModel', ['getFavorites(cId): LiveData', 'addFavorite()', 'removeFavorite()', 'isFavorite(): LiveData']),
        (16.7,  'SaleViewModel',      ['getAllSales(): LiveData', 'insertSale()', 'getTodayTotal(): LiveData', 'getTotalByRange()']),
        (19.95, 'PurchaseViewModel',  ['getAllPurchases(): LiveData', 'insertPurchase()', 'getTotalCost(): LiveData', 'getByRange()']),
        (23.2,  'TaskViewModel',      ['getAll/ByUser/Team/Private(): LiveData', 'insert/update/delete(Task)', 'getPendingCount(): LiveData', 'currentTab: MutableLiveData']),
        (26.45, 'SeasonViewModel',    ['getAllSeasons(): LiveData', 'getActive(): LiveData', 'insert/update/delete(Season)', 'getById(id)']),
        (29.7,  'SupportViewModel',   ['getMessages(cId): LiveData', 'sendMessage(cId,text)', 'getConversations(): LiveData', 'markRead(cId)']),
    ]
    for (vx, name, attrs) in vms:
        draw_box(ax, vx, V_TOP - V_H, V_W, V_H, name, attrs, C_VM, C_VM_BG, fontsize=5.8, title_size=7.0)

    # VM → Repo arrows
    vm_repo_pairs = [
        (0.4+V_W/2,  0.4+R_W/2),   # AuthVM → UserRepo
        (3.7+V_W/2,  3.7+R_W/2),   # ProductVM → ProductRepo
        (6.95+V_W/2, 6.95+R_W/2),  # CartVM → CartRepo
        (10.2+V_W/2, 10.2+R_W/2),  # OrderVM → OrderRepo
        (13.45+V_W/2,13.45+R_W/2), # FavVM → FavRepo
        (16.7+V_W/2, 16.7+R_W/2),  # SaleVM → SaleRepo
        (19.95+V_W/2,19.95+R_W/2), # PurchaseVM → PurchaseRepo
        (23.2+V_W/2, 23.2+R_W/2),  # TaskVM → TaskRepo
        (26.45+V_W/2,26.45+R_W/2), # SeasonVM → SeasonRepo
        (29.7+V_W/2, 29.7+R_W/2),  # SupportVM → SupportRepo
    ]
    for (vx, rx) in vm_repo_pairs:
        ax.annotate('', xy=(rx, R_TOP-R_H), xytext=(vx, V_TOP-V_H),
                    arrowprops=dict(arrowstyle='->', color=C_VM, lw=0.9,
                                    connectionstyle='arc3,rad=0', mutation_scale=7))

    sep_y4 = V_TOP - V_H - 0.35
    ax.plot([0.4, FIG_W-0.4], [sep_y4, sep_y4], color=C_GOLD, lw=1.5, linestyle='--')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5 — Core / Utilities / Helpers
    # ══════════════════════════════════════════════════════════════════════════
    CR_TOP = sep_y4 - 0.15
    section_label(ax, 0.4, CR_TOP, 'Core & Helpers  (Singletons · Utilities · Firebase wrappers)', C_CORE)
    CR_TOP -= 0.3
    CR_H = 1.7
    CR_W = 3.4
    cores = [
        (0.4,  'AppDatabase',
         ['INSTANCE: AppDatabase (singleton)', 'dbExecutor: ExecutorService (4 threads)',
          '12 @Dao getters', 'getInstance(ctx): AppDatabase',
          'seedDemoData(ctx)', 'version: 2',
          'fallbackToDestructiveMigration()']),
        (4.0,  'SessionManager',
         ['INSTANCE: SessionManager (singleton)', 'loggedInUser: User',
          'getInstance(): SessionManager',
          'setLoggedInUser(User)', 'getLoggedInUser(): User',
          'clearSession()', 'isLoggedIn(): boolean']),
        (7.6,  'CryptoUtil',
         ['ALGORITHM: PBKDF2WithHmacSHA256', 'ITERATIONS: 65536', 'KEY_LENGTH: 256',
          'generateSalt(): String', 'hashPassword(pwd,salt): String',
          'verifyPassword(pwd,hash,salt): boolean']),
        (11.2, 'PermissionManager',
         ['ROLE→PERMISSION mapping (static)', 'hasPermission(role,perm): boolean',
          'MANAGE_USERS · MANAGE_PRODUCTS', 'VIEW_PRODUCTS · CREATE_SALE',
          'VIEW_SALES_HISTORY · MANAGE_PURCHASES',
          'MANAGE_SEASONS · MANAGE_TASKS · VIEW_ADMIN']),
        (14.8, 'NotificationHelper',
         ['CHANNEL_ID: storepilot_low_stock', 'NOTIF_ID: 1001',
          'createChannel(ctx)', 'sendLowStockNotification(ctx,count)',
          'cancelAll(ctx)']),
        (18.4, 'LowStockReceiver',
         ['extends BroadcastReceiver', 'LOW_STOCK_THRESHOLD: 5',
          'onReceive(ctx,intent)', 'checkNow(ctx) — Firestore query',
          'scheduleAlarm(ctx) — 1-hour repeat']),
        (22.0, 'FirebaseAuthHelper',
         ['auth: FirebaseAuth', 'signUp(email,pwd,callback)',
          'signIn(email,pwd,callback)', 'signOut()',
          'getCurrentUser(): FirebaseUser']),
        (25.6, 'FirebaseConfig',
         ['FIRESTORE_COLLECTION: "products"', 'LOW_STOCK_FIELD: "quantity"',
          'getFirestore(): FirebaseFirestore',
          'getAuth(): FirebaseAuth']),
        (29.2, 'StorePilotApp',
         ['extends Application', 'onCreate()',
          'initFirebase()', 'createNotificationChannel()',
          'scheduleAlarm() — AlarmManager']),
        (32.8, 'BaseActivity',
         ['extends AppCompatActivity', 'checkPermission(perm): boolean',
          'requirePermission(perm)', 'navigateByRole()',
          'showToast(msg)']),
    ]
    for (cx, name, attrs) in cores:
        draw_box(ax, cx, CR_TOP - CR_H, CR_W, CR_H, name, attrs, C_CORE, C_CORE_BG, fontsize=5.6, title_size=7.0)

    sep_y5 = CR_TOP - CR_H - 0.35
    ax.plot([0.4, FIG_W-0.4], [sep_y5, sep_y5], color=C_GOLD, lw=1.5, linestyle='--')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6 — Activities & Fragments
    # ══════════════════════════════════════════════════════════════════════════
    AC_TOP = sep_y5 - 0.15
    section_label(ax, 0.4, AC_TOP, 'Activities & Fragments  (UI Layer)', C_ACT)
    AC_TOP -= 0.3
    AC_H = 1.6
    AC_W = 3.2

    # Auth Activities
    section_label(ax, 0.4, AC_TOP - 0.05, '  Auth', '#37474F')
    auth_acts = [
        (0.4,  'WelcomeActivity',        ['extends AppCompatActivity', 'checkSession()', 'navigateByRole()', '→ LoginActivity | RegisterActivity']),
        (3.8,  'RoleSelectionActivity',  ['extends AppCompatActivity', 'selectedRole: String', '→ RegisterActivity(role)']),
        (7.2,  'LoginActivity',          ['extends BaseActivity', 'AuthViewModel', 'login(username,pwd)', '→ CustomerMain | MainActivity']),
        (10.6, 'RegisterActivity',       ['extends AppCompatActivity', 'role: String (pre-set)', 'AuthViewModel', 'register(User)', '→ LoginActivity']),
        (14.0, 'SetupActivity',          ['extends AppCompatActivity', 'First-run owner creation', 'AuthViewModel', 'enableDemoMode()', '→ MainActivity']),
    ]
    AC_H1 = 1.5
    for (ax2, name, attrs) in auth_acts:
        draw_box(ax, ax2, AC_TOP - AC_H1 - 0.25, AC_W, AC_H1, name, attrs, C_ACT, C_ACT_BG, fontsize=5.8, title_size=7.0)

    # Manager Activities / Main
    section_label(ax, 17.8, AC_TOP - 0.05, '  Manager / Inventory', '#37474F')
    mgr_acts = [
        (17.8, 'MainActivity',            ['extends BaseActivity', 'bottom nav (5 tabs)', 'PermissionManager checks', 'SessionManager']),
        (21.2, 'AddEditProductActivity',  ['extends AppCompatActivity', 'ProductViewModel', 'insert/update(Product)', 'image URL field']),
        (24.6, 'AddEditTaskActivity',     ['extends AppCompatActivity', 'TaskViewModel', 'insert/update(Task)', 'priority/status spinners']),
        (28.0, 'AddSaleActivity',         ['extends AppCompatActivity', 'SaleViewModel', 'ProductViewModel', 'insert(Sale) → stock decrement']),
        (31.4, 'AddPurchaseActivity',     ['extends AppCompatActivity', 'PurchaseViewModel', 'ProductViewModel', 'insert(Purchase)']),
    ]
    for (ax2, name, attrs) in mgr_acts:
        draw_box(ax, ax2, AC_TOP - AC_H1 - 0.25, AC_W, AC_H1, name, attrs, C_ACT, C_ACT_BG, fontsize=5.8, title_size=7.0)

    # Customer + Manager Fragments
    sep_y6 = AC_TOP - AC_H1 - 0.6
    ax.plot([0.4, FIG_W-0.4], [sep_y6, sep_y6], color='#CFD8DC', lw=1.0, linestyle=':')

    cust_frags = [
        (0.4,  'CustomerMainActivity',    ['bottom nav (5 tabs)', 'CustomerHomeFragment', 'CartFragment', 'OrderHistoryFragment', 'FavoritesFragment', 'SupportChatFragment']),
        (3.8,  'CustomerHomeFragment',    ['ProductViewModel', 'CartViewModel', 'GridLayoutManager (2-col)', 'live search TextWatcher']),
        (7.2,  'ProductDetailFragment',   ['ProductViewModel', 'CartViewModel', 'FavoritesViewModel', 'Add to Cart / Favourite']),
        (10.6, 'CartFragment',            ['CartViewModel', 'CartItemAdapter', '+/− qty controls', '→ CheckoutFragment']),
        (14.0, 'CheckoutFragment',        ['CartViewModel', 'OrderViewModel', 'ProductViewModel', 'address + payment method', '→ OrderConfirmationFragment']),
        (17.8, 'OrderHistoryFragment',    ['OrderViewModel', 'CustomerOrderAdapter', 'colour-coded status badges']),
        (21.2, 'FavoritesFragment',       ['FavoritesViewModel', 'ProductViewModel', 'CartViewModel', 'heart toggle + Add-to-Cart']),
        (24.6, 'SupportChatFragment',     ['SupportViewModel', 'MessageAdapter (dual view)', 'stackFromEnd=true', 'markAllRead on open']),
        (28.0, 'DashboardFragment',       ['SaleViewModel', 'ProductViewModel', 'OrderViewModel', 'TaskViewModel', 'SeasonViewModel', '4 KPI cards + season alert']),
        (31.4, 'ProductListFragment',     ['ProductViewModel', 'ProductListAdapter', 'FAB gated by MANAGE_PRODUCTS perm']),
    ]
    AC_H2 = 1.5
    frag_y = sep_y6 - AC_H2 - 0.1
    for (fx, name, attrs) in cust_frags:
        draw_box(ax, fx, frag_y, AC_W, AC_H2, name, attrs, '#455A64', C_ACT_BG, fontsize=5.6, title_size=6.8)

    sep_y7 = frag_y - 0.45
    ax.plot([0.4, FIG_W-0.4], [sep_y7, sep_y7], color='#CFD8DC', lw=1.0, linestyle=':')

    mgr_frags = [
        (0.4,  'ProductDetailsFragment',      ['ProductViewModel', 'full detail view', 'edit/delete gated by permission']),
        (3.8,  'OrderManagementFragment',     ['OrderViewModel', 'ManagerOrderAdapter', 'status spinner (firstTime guard)']),
        (7.2,  'TaskListFragment',            ['TaskViewModel', 'switchMap for tab changes', '3 tabs: My/Team/Private']),
        (10.6, 'SalesHistoryFragment',        ['SaleViewModel', 'SaleAdapter', 'date-range filter', 'total aggregation']),
        (14.0, 'PurchaseHistoryFragment',     ['PurchaseViewModel', 'PurchaseAdapter', 'date-range filter']),
        (17.8, 'SeasonListFragment',          ['SeasonViewModel', 'SeasonAdapter', 'end-date alert badge']),
        (21.2, 'SupportConversationsFragment',['SupportViewModel', 'ConversationListAdapter', 'manager inbox']),
        (24.6, 'SupportInboxFragment',        ['SupportViewModel', 'MessageAdapter', 'markAllRead on open']),
        (28.0, 'UserManagementFragment',      ['UserAdapter', 'OWNER only (VIEW_ADMIN perm)', 'list of all registered users']),
        (31.4, 'AddEditSeasonActivity',       ['SeasonViewModel', 'insert/update(Season)', 'date pickers', 'alertDays field']),
    ]
    frag_y2 = sep_y7 - AC_H2 - 0.05
    for (fx, name, attrs) in mgr_frags:
        draw_box(ax, fx, frag_y2, AC_W, AC_H2, name, attrs, '#546E7A', C_ACT_BG, fontsize=5.6, title_size=6.8)

    # ── Legend ────────────────────────────────────────────────────────────────
    lx, ly = FIG_W - 5.5, FIG_H - 1.6
    ax.text(lx, ly, 'Colour Legend', fontsize=9, fontweight='bold', color=C_DARK)
    legend = [
        (C_ENTITY, C_BODY,   'Entity (@Room @Entity)'),
        (C_DAO,    C_DAO_BG, 'DAO (@Dao interface)'),
        (C_REPO,   C_REPO_BG,'Repository (data layer)'),
        (C_VM,     C_VM_BG,  'ViewModel (lifecycle-aware)'),
        (C_CORE,   C_CORE_BG,'Core / Utility / Helper'),
        (C_ACT,    C_ACT_BG, 'Activity / Fragment (UI)'),
    ]
    for i, (hc, bc, lbl) in enumerate(legend):
        bx = FancyBboxPatch((lx, ly - 0.42*(i+1)), 0.55, 0.28,
                            boxstyle='round,pad=0.03', facecolor=bc,
                            edgecolor=hc, linewidth=1.2, zorder=3)
        ax.add_patch(bx)
        ax.text(lx + 0.7, ly - 0.42*(i+1) + 0.14, lbl,
                fontsize=7.5, va='center', color=C_DARK)

    # Arrow legend
    aly = ly - 0.42*7 - 0.2
    ax.text(lx, aly, 'Arrow Legend', fontsize=9, fontweight='bold', color=C_DARK)
    arrows = [
        (AR_ENTITY, '──▶  Entity FK (1:N)'),
        (C_REPO,    '- - ▶  Repo uses DAO'),
        (C_VM,      '──▶  ViewModel uses Repo'),
    ]
    for i, (c, lbl) in enumerate(arrows):
        ax.plot([lx, lx+0.5], [aly-0.32*(i+1), aly-0.32*(i+1)], color=c, lw=1.5)
        ax.annotate('', xy=(lx+0.52, aly-0.32*(i+1)),
                    xytext=(lx+0.48, aly-0.32*(i+1)),
                    arrowprops=dict(arrowstyle='->', color=c, lw=1.2, mutation_scale=8))
        ax.text(lx + 0.65, aly-0.32*(i+1), lbl[5:],
                fontsize=7, va='center', color=c)

    plt.tight_layout(rect=[0, 0, 1, 1])
    out = '/home/user/StorePilot/uml_diagram.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C_WHITE)
    plt.close(fig)
    print(f'Saved: {out}')
    return out


if __name__ == '__main__':
    build()
