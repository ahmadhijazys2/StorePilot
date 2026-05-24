#!/usr/bin/env python3
"""Generate UML class diagram and navigation flow diagram as PNG images."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np

# ── Colours ─────────────────────────────────────────────────────────────────
C_HEADER   = '#1B3A5C'   # dark blue  – class header
C_BODY     = '#EAF4FB'   # light blue – class body
C_BORDER   = '#2E86AB'   # accent blue
C_ARROW    = '#0D1B2A'   # near black
C_GOLD     = '#F4A261'   # gold accent
C_GREEN    = '#2E7D32'
C_ORANGE   = '#E65100'
C_PURPLE   = '#6A1B9A'
C_WHITE    = '#FFFFFF'
C_GREY     = '#F5F5F5'
C_DARKGREY = '#333333'


def draw_class_box(ax, x, y, w, h, name, attrs, header_color=C_HEADER,
                   body_color=C_BODY, border_color=C_BORDER, fontsize=7):
    """Draw a UML-style class box."""
    lw = 1.2
    # body
    body = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02',
                          facecolor=body_color, edgecolor=border_color, linewidth=lw, zorder=2)
    ax.add_patch(body)
    # header bar
    hh = 0.22
    header = FancyBboxPatch((x, y + h - hh), w, hh, boxstyle='round,pad=0.01',
                            facecolor=header_color, edgecolor=border_color, linewidth=lw, zorder=3)
    ax.add_patch(header)
    # class name
    ax.text(x + w/2, y + h - hh/2, name, ha='center', va='center',
            fontsize=fontsize+1, fontweight='bold', color='white', zorder=4)
    # separator line
    ax.plot([x, x+w], [y+h-hh, y+h-hh], color=border_color, lw=1, zorder=4)
    # attributes
    line_h = (h - hh - 0.04) / max(len(attrs), 1)
    for i, attr in enumerate(attrs):
        ty = y + h - hh - 0.04 - (i+0.5)*line_h
        ax.text(x + 0.06, ty, attr, ha='left', va='center',
                fontsize=fontsize-0.5, color=C_DARKGREY, zorder=4,
                fontfamily='monospace')


def arrow(ax, x1, y1, x2, y2, label='', color=C_ARROW, style='->',
          lw=1.2, label_offset=(0, 0.05), fontsize=6.5):
    """Draw an arrow between two points."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle='arc3,rad=0.0'))
    if label:
        mx, my = (x1+x2)/2 + label_offset[0], (y1+y2)/2 + label_offset[1]
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=fontsize,
                color=color, fontstyle='italic',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))


def curved_arrow(ax, x1, y1, x2, y2, label='', color=C_ARROW, rad=0.3,
                 lw=1.2, fontsize=6.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.08, label, ha='center', va='bottom', fontsize=fontsize,
                color=color, fontstyle='italic',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — UML CLASS DIAGRAM
# ════════════════════════════════════════════════════════════════════════════
def build_uml():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor(C_WHITE)

    # ── Title ──────────────────────────────────────────────────────────────
    ax.text(8, 10.65, 'StorePilot — UML Class Diagram', ha='center', va='center',
            fontsize=16, fontweight='bold', color=C_HEADER)
    ax.text(8, 10.35, 'Room @Entity classes · MVVM Architecture layers · Relationships',
            ha='center', va='center', fontsize=9, color='#555555')
    ax.plot([0.3, 15.7], [10.2, 10.2], color=C_GOLD, lw=2)

    # ── Section label: Entities ───────────────────────────────────────────
    ax.text(0.3, 9.95, '▶  ENTITIES  (Room @Entity)',
            fontsize=9, fontweight='bold', color=C_HEADER)

    # Entity boxes  (x, y, w, h, name, attrs)
    entities = [
        # User
        (0.3, 7.5, 2.2, 2.2, 'User',
         ['id: int (PK)', 'fullName: String', 'username: String*',
          'email: String*', 'phone: String', 'passwordHash: String',
          'salt: String', 'role: String', 'createdAt: long']),
        # Product
        (3.0, 7.5, 2.3, 2.2, 'Product',
         ['id: int (PK)', 'name: String', 'category: String',
          'size: String', 'color: String', 'quantity: int',
          'price: double', 'costPrice: double', 'imageUrl: String']),
        # Order
        (5.8, 7.5, 2.4, 2.2, 'Order',
         ['id: int (PK)', 'customerId: int (FK)', 'totalPrice: double',
          'status: String', 'createdAt: long',
          'paymentMethod: String', 'shippingAddress: String']),
        # OrderItem
        (8.7, 7.5, 2.3, 2.2, 'OrderItem',
         ['id: int (PK)', 'orderId: int (FK)', 'productId: int (FK)',
          'quantity: int', 'unitPrice: double']),
        # CartItem
        (11.5, 7.5, 2.2, 2.2, 'CartItem',
         ['id: int (PK)', 'customerId: int (FK)',
          'productId: int (FK)', 'quantity: int']),
        # Sale
        (0.3, 4.8, 2.2, 2.1, 'Sale',
         ['id: int (PK)', 'productId: int (FK)', 'quantity: int',
          'totalPrice: double', 'saleDate: long',
          'soldBy: int (FK)', 'notes: String']),
        # Purchase
        (3.0, 4.8, 2.4, 2.1, 'Purchase',
         ['id: int (PK)', 'productId: int (FK)', 'quantity: int',
          'totalCost: double', 'purchaseDate: long',
          'purchasedBy: int (FK)', 'supplier: String']),
        # Task
        (5.8, 4.8, 2.4, 2.1, 'Task',
         ['id: int (PK)', 'title: String', 'description: String',
          'assignedTo: int (FK)', 'createdBy: int (FK)',
          'status: String', 'priority: String', 'isPrivate: boolean']),
        # Season
        (8.7, 4.8, 2.3, 2.1, 'Season',
         ['id: int (PK)', 'name: String', 'startDate: long',
          'endDate: long', 'alertDaysBeforeEnd: int',
          'isActive: boolean', 'notes: String']),
        # SupportMessage
        (11.5, 4.8, 2.4, 2.1, 'SupportMessage',
         ['id: int (PK)', 'senderId: int (FK)', 'senderRole: String',
          'messageText: String', 'imageUrl: String',
          'timestamp: long', 'customerId: int (FK)']),
        # Favorite
        (0.3, 2.4, 2.2, 1.8, 'Favorite',
         ['id: int (PK)', 'customerId: int (FK)',
          'productId: int (FK)', 'addedAt: long']),
        # VideoMetric
        (3.0, 2.4, 2.4, 1.8, 'VideoMetric',
         ['id: int (PK)', 'title: String', 'platform: String',
          'views: long', 'likes: long', 'shares: long',
          'comments: long', 'videoDate: long']),
    ]
    for (x, y, w, h, name, attrs) in entities:
        draw_class_box(ax, x, y, w, h, name, attrs, fontsize=6.8)

    # ── Relationship arrows ───────────────────────────────────────────────
    # User → Order (1:N)  User.right → Order.left (bottom of headers)
    arrow(ax, 2.5, 8.45, 5.8, 8.45, '1 : N', color=C_BORDER, lw=1.5)
    # Order → OrderItem (1:N)
    arrow(ax, 8.2, 8.45, 8.7, 8.45, '1 : N', color=C_BORDER, lw=1.5)
    # User → CartItem
    arrow(ax, 1.4, 7.5, 1.4, 6.9, '', color=C_GREEN, lw=1.2)
    ax.annotate('', xy=(11.5, 8.25), xytext=(1.4, 6.9),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=1.2,
                                connectionstyle='arc3,rad=0'))
    ax.text(6.8, 7.05, '1:N  (customerId)', ha='center', fontsize=6,
            color=C_GREEN, fontstyle='italic')
    # User → Favorite
    arrow(ax, 0.9, 7.5, 0.9, 4.1, '1:N', color='#7B1FA2', lw=1.2, label_offset=(-0.15, 0))
    # Product → Sale
    arrow(ax, 3.8, 7.5, 1.8, 6.9, '1:N', color=C_ORANGE, lw=1.2)
    # Product → OrderItem
    arrow(ax, 4.15, 7.5, 9.2, 9.7, '1:N', color=C_ORANGE, lw=1.2)
    # Product → Purchase
    curved_arrow(ax, 4.15, 7.5, 3.8, 6.9, '1:N', color=C_ORANGE, rad=-0.2)
    # User → Task (assignedTo)
    arrow(ax, 1.3, 7.5, 6.5, 6.9, 'assignedTo 1:N', color=C_PURPLE, lw=1.1, label_offset=(0, 0.08))
    # User → SupportMessage
    arrow(ax, 1.5, 7.5, 12.2, 6.9, 'senderId / customerId', color='#00838F', lw=1.1, label_offset=(0, 0.08))

    # ── Legend: relationship types ────────────────────────────────────────
    lx, ly = 13.9, 9.9
    ax.text(lx, ly, 'Legend', fontsize=8, fontweight='bold', color=C_HEADER)
    items = [
        (C_BORDER,   '──▶  1:N (Order FK)'),
        (C_GREEN,    '──▶  1:N (CartItem FK)'),
        (C_ORANGE,   '──▶  1:N (Sale/Purchase FK)'),
        (C_PURPLE,   '──▶  1:N (Task FK)'),
        ('#00838F',  '──▶  1:N (Support FK)'),
        ('#7B1FA2',  '──▶  1:N (Favorite FK)'),
    ]
    for i, (c, lbl) in enumerate(items):
        ax.plot([lx, lx+0.4], [ly-0.28*(i+1), ly-0.28*(i+1)], color=c, lw=1.5)
        ax.annotate('', xy=(lx+0.42, ly-0.28*(i+1)),
                    xytext=(lx+0.38, ly-0.28*(i+1)),
                    arrowprops=dict(arrowstyle='->', color=c, lw=1.2))
        ax.text(lx+0.55, ly-0.28*(i+1), lbl[5:], fontsize=6.5, va='center', color=c)

    # ── MVVM section ──────────────────────────────────────────────────────
    ax.plot([0.3, 15.7], [2.25, 2.25], color=C_GOLD, lw=1.5, linestyle='--')
    ax.text(0.3, 2.08, '▶  MVVM ARCHITECTURE LAYERS', fontsize=9,
            fontweight='bold', color=C_HEADER)

    layers = [
        (0.5,  1.3, 2.8,  0.55, 'UI Layer',         'Fragment / Activity\nobserves LiveData',       '#E3F2FD', '#1565C0'),
        (3.7,  1.3, 2.8,  0.55, 'ViewModel',        'Lifecycle-aware\nUI state holder',             '#E8F5E9', '#2E7D32'),
        (6.9,  1.3, 2.8,  0.55, 'Repository',       'Runs on dbExecutor\n4-thread pool',            '#FFF3E0', '#E65100'),
        (10.1, 1.3, 2.8,  0.55, 'DAO',              'Room @Dao interface\nSQL annotations',         '#F3E5F5', '#6A1B9A'),
        (13.3, 1.3, 2.2,  0.55, 'Room DB',          'SQLite file\nstorepilot.db',                  '#FCE4EC', '#880E4F'),
    ]
    for (x, y, w, h, title, sub, bg, fg) in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                             facecolor=bg, edgecolor=fg, linewidth=1.5, zorder=2)
        ax.add_patch(box)
        ax.text(x+w/2, y+h*0.65, title, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=fg, zorder=3)
        ax.text(x+w/2, y+h*0.28, sub, ha='center', va='center',
                fontsize=6.5, color=C_DARKGREY, zorder=3)

    # arrows between layers
    for x1, x2, lbl in [
        (3.3,  3.7,  'observes\nLiveData'),
        (6.5,  6.9,  'calls\nrepo'),
        (9.7,  10.1, 'uses\nDAO'),
        (12.9, 13.3, 'query\nSQLite'),
    ]:
        ax.annotate('', xy=(x2, 1.575), xytext=(x1, 1.575),
                    arrowprops=dict(arrowstyle='<->', color=C_ARROW, lw=1.3))
        ax.text((x1+x2)/2, 1.72, lbl, ha='center', va='bottom',
                fontsize=5.5, color=C_ARROW)

    plt.tight_layout(rect=[0, 0, 1, 1])
    out = '/home/user/StorePilot/uml_diagram.png'
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor=C_WHITE)
    plt.close(fig)
    print(f'Saved: {out}')
    return out


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — NAVIGATION FLOW DIAGRAM
# ════════════════════════════════════════════════════════════════════════════
def draw_box(ax, x, y, w, h, text, bg='#1B3A5C', fg='white',
             fontsize=8, border='#2E86AB', lw=1.5, radius='round,pad=0.08'):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle=radius,
                         facecolor=bg, edgecolor=border, linewidth=lw, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=fg, zorder=4, fontweight='bold',
            multialignment='center')

def nav_arrow(ax, x1, y1, x2, y2, label='', color=C_ARROW,
              rad=0.0, lw=1.2, fontsize=7):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}',
                                mutation_scale=12))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + (0.15 if rad else 0), my, label, ha='center',
                va='bottom', fontsize=fontsize, color=color, fontstyle='italic',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=1))


def build_nav():
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor(C_WHITE)

    # Title
    ax.text(8, 13.65, 'StorePilot — Navigation Flow Diagram', ha='center', va='center',
            fontsize=16, fontweight='bold', color=C_HEADER)
    ax.text(8, 13.3, 'Activity & Fragment navigation · Role-based routing · User flows',
            ha='center', va='center', fontsize=9, color='#555555')
    ax.plot([0.3, 15.7], [13.1, 13.1], color=C_GOLD, lw=2)

    # ── Colour palette per layer ──────────────────────────────────────────
    ACT   = '#1B3A5C'   # Activity – dark blue
    FRAG  = '#2E86AB'   # Fragment  – accent blue
    SYS   = '#4A4A4A'   # System    – dark grey
    CUST  = '#2E7D32'   # Customer  – green
    MGR   = '#6A1B9A'   # Manager   – purple
    WARN  = '#E65100'   # Condition – orange

    # ── Row 1: App launch ─────────────────────────────────────────────────
    draw_box(ax, 8, 12.5, 4.5, 0.55,
             'App Launch  ·  StorePilotApp.onCreate()\nFirebase init  ·  NotificationChannel  ·  AlarmManager',
             bg=SYS, fg='white', fontsize=7.5, border=C_GOLD, lw=2)

    nav_arrow(ax, 8, 12.22, 8, 11.72)

    # ── Row 2: WelcomeActivity ────────────────────────────────────────────
    draw_box(ax, 8, 11.45, 3.2, 0.5, 'WelcomeActivity', bg=ACT, fontsize=9)

    # Condition diamond
    ax.add_patch(mpatches.FancyBboxPatch((6.4, 10.55), 3.2, 0.55,
                 boxstyle='round,pad=0.05', facecolor='#FFF8E1',
                 edgecolor=WARN, linewidth=1.5, zorder=3))
    ax.text(8, 10.825, 'Already logged in?', ha='center', va='center',
            fontsize=8, color=WARN, fontweight='bold', zorder=4)
    nav_arrow(ax, 8, 11.2, 8, 11.1)

    # YES branch → left
    nav_arrow(ax, 6.4, 10.825, 4.0, 10.825, 'YES', color=C_GREEN, lw=1.5)
    draw_box(ax, 2.8, 10.825, 2.0, 0.5, 'role check\n→ auto-route', bg='#E8F5E9',
             fg=C_GREEN, border=C_GREEN, fontsize=7.5)
    nav_arrow(ax, 8, 10.55, 8, 10.0, 'NO', color=WARN, lw=1.5)

    # ── Row 3: Login / Register ───────────────────────────────────────────
    draw_box(ax, 6.0, 9.7, 2.6, 0.55, 'LoginActivity', bg=ACT, fontsize=8.5)
    draw_box(ax, 9.5, 9.7, 2.8, 0.55, 'RoleSelectionActivity', bg=ACT, fontsize=8)
    draw_box(ax, 13.2, 9.7, 2.5, 0.55, 'SetupActivity\n(first run)', bg=ACT, fontsize=8)

    nav_arrow(ax, 7.3, 10.0, 7.0, 9.975, '', color=C_BORDER)
    nav_arrow(ax, 8.7, 10.0, 9.0, 9.975, '', color=C_BORDER)
    nav_arrow(ax, 10.9, 9.7, 11.95, 9.7, 'no users', color=WARN, lw=1.2)

    draw_box(ax, 9.5, 8.85, 2.8, 0.55, 'RegisterActivity', bg=ACT, fontsize=8.5)
    nav_arrow(ax, 9.5, 9.425, 9.5, 9.125)

    # ── Role-check box ───────────────────────────────────────────────────
    draw_box(ax, 8, 8.1, 3.8, 0.5, 'Login success  →  role check', bg='#FFF3E0',
             fg='#BF360C', border=WARN, fontsize=8.5)
    nav_arrow(ax, 6.0, 9.425, 6.5, 8.35, 'success', color=C_GREEN, lw=1.2)
    nav_arrow(ax, 9.5, 8.575, 9.0, 8.35, 'success', color=C_GREEN, lw=1.2)

    # ── Two main destinations ─────────────────────────────────────────────
    nav_arrow(ax, 6.0, 7.85, 4.0, 7.35, 'CUSTOMER', color=CUST, lw=1.8)
    nav_arrow(ax, 10.0, 7.85, 12.0, 7.35, 'STAFF / MANAGER', color=MGR, lw=1.8)

    # ── CustomerMainActivity ──────────────────────────────────────────────
    draw_box(ax, 3.2, 7.0, 3.6, 0.6, 'CustomerMainActivity', bg=CUST, fontsize=9)

    cust_frags = [
        (1.0,  5.9, 'CustomerHome\nFragment',    FRAG),
        (2.5,  5.9, 'CartFragment',              FRAG),
        (4.0,  5.9, 'Order\nHistory',            FRAG),
        (5.5,  5.9, 'Favourites\nFragment',      FRAG),
        (7.0,  5.9, 'SupportChat\nFragment',     FRAG),
    ]
    for (fx, fy, lbl, col) in cust_frags:
        draw_box(ax, fx, fy, 1.35, 0.75, lbl, bg=col, fontsize=6.5, border=CUST)
        nav_arrow(ax, 3.2, 6.7, fx, fy+0.375, '', color=CUST, lw=0.9)

    # Sub-fragments under CustomerHome
    draw_box(ax, 1.0, 4.8, 1.35, 0.6, 'Product\nDetail', bg='#B3E5FC', fg=C_HEADER,
             border=FRAG, fontsize=6.5)
    nav_arrow(ax, 1.0, 5.525, 1.0, 5.1, 'tap card', color=FRAG, lw=0.9)

    draw_box(ax, 2.5, 4.8, 1.35, 0.6, 'Checkout\nFragment', bg='#B3E5FC', fg=C_HEADER,
             border=FRAG, fontsize=6.5)
    nav_arrow(ax, 2.5, 5.525, 2.5, 5.1, 'tap checkout', color=FRAG, lw=0.9)

    draw_box(ax, 1.75, 3.85, 1.35, 0.6, 'Order\nConfirmation', bg='#B3E5FC', fg=C_HEADER,
             border=FRAG, fontsize=6.5)
    nav_arrow(ax, 2.5, 4.5, 2.0, 4.15, 'place order', color=C_GREEN, lw=0.9)

    # ── MainActivity (Staff) ──────────────────────────────────────────────
    draw_box(ax, 12.8, 7.0, 3.6, 0.6, 'MainActivity  (Staff)', bg=MGR, fontsize=9)

    mgr_frags = [
        (9.8,  5.6, 'Dashboard\nFragment',       MGR),
        (11.3, 5.6, 'Product\nListFragment',     MGR),
        (12.8, 5.6, 'Sales\nHistory',            MGR),
        (14.3, 5.6, 'Task\nListFragment',        MGR),
        (15.6, 5.6, 'More\nMenu',               '#37474F'),
    ]
    for (fx, fy, lbl, col) in mgr_frags:
        draw_box(ax, fx, fy, 1.3, 0.75, lbl, bg=col, fontsize=6.5, border=MGR)
        nav_arrow(ax, 12.8, 6.7, fx, fy+0.375, '', color=MGR, lw=0.9)

    # More menu sub-items
    more_items = [
        (9.8,  4.5, 'Purchase\nHistory'),
        (11.1, 4.5, 'Season\nList'),
        (12.4, 4.5, 'Order Mgmt\nFragment'),
        (13.7, 4.5, 'Support\nInbox'),
        (15.0, 4.5, 'User Mgmt\n(OWNER)'),
    ]
    for (fx, fy, lbl) in more_items:
        draw_box(ax, fx, fy, 1.2, 0.65, lbl, bg='#455A64', fg='white',
                 border='#90A4AE', fontsize=6)
        nav_arrow(ax, 15.6, 5.225, fx, fy+0.325, '', color='#455A64', lw=0.8)

    # AddEdit activities
    draw_box(ax, 11.3, 4.5, 1.3, 0.6, 'AddEdit\nProduct', bg='#E8EAF6', fg='#1A237E',
             border='#3949AB', fontsize=6.5)
    nav_arrow(ax, 11.3, 5.225, 11.3, 4.8, 'FAB +', color='#3949AB', lw=0.9)

    draw_box(ax, 12.8, 4.5, 1.3, 0.6, 'AddSale\nActivity', bg='#E8EAF6', fg='#1A237E',
             border='#3949AB', fontsize=6.5)
    nav_arrow(ax, 12.8, 5.225, 12.8, 4.8, 'FAB +', color='#3949AB', lw=0.9)

    draw_box(ax, 14.2, 3.55, 1.3, 0.6, 'AddEdit\nTask', bg='#E8EAF6', fg='#1A237E',
             border='#3949AB', fontsize=6.5)
    nav_arrow(ax, 14.3, 5.225, 14.2, 3.85, 'FAB +', color='#3949AB', lw=0.9)

    # ── Logout / back to Welcome ──────────────────────────────────────────
    draw_box(ax, 8, 2.7, 3.2, 0.5, 'Logout  →  clear session', bg='#FFEBEE',
             fg='#B71C1C', border='#E53935', fontsize=8)
    nav_arrow(ax, 3.2, 6.7, 1.8, 2.95, '', color='#B71C1C', lw=0.9, rad=0.15)
    nav_arrow(ax, 12.8, 6.7, 14.2, 2.95, '', color='#B71C1C', lw=0.9, rad=-0.15)
    nav_arrow(ax, 8, 2.45, 8, 1.85)

    draw_box(ax, 8, 1.6, 3.2, 0.5, 'WelcomeActivity', bg=ACT, fontsize=9)

    # ── Legend ────────────────────────────────────────────────────────────
    legend_items = [
        (ACT,      'Activity'),
        (FRAG,     'Fragment (Customer)'),
        (MGR,      'Fragment (Manager)'),
        (CUST,     'Customer route'),
        (MGR,      'Manager/Staff route'),
        (WARN,     'Condition / branch'),
        ('#B71C1C','Logout / back'),
    ]
    lx0, ly0 = 0.3, 3.5
    ax.text(lx0, ly0+0.3, 'Legend', fontsize=8.5, fontweight='bold', color=C_HEADER)
    for i, (c, lbl) in enumerate(legend_items):
        bx = FancyBboxPatch((lx0, ly0 - 0.38*(i+1)), 0.45, 0.24,
                             boxstyle='round,pad=0.03', facecolor=c,
                             edgecolor='white', linewidth=1, zorder=3)
        ax.add_patch(bx)
        ax.text(lx0 + 0.58, ly0 - 0.38*(i+1) + 0.12, lbl,
                fontsize=7, va='center', color=C_DARKGREY)

    plt.tight_layout(rect=[0, 0, 1, 1])
    out = '/home/user/StorePilot/nav_flow_diagram.png'
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor=C_WHITE)
    plt.close(fig)
    print(f'Saved: {out}')
    return out


if __name__ == '__main__':
    uml = build_uml()
    nav = build_nav()
    print('Done.')
