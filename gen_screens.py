#!/usr/bin/env python3
"""Generate pixel-accurate mockups of every StorePilot app screen."""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = '/home/user/StorePilot/screens'
os.makedirs(OUT, exist_ok=True)

# ── palette from screenshots ───────────────────────────────────────────────
BG        = (245, 245, 245)
TOOLBAR   = (30,  30,  30)
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
TEAL      = (0,   188, 212)
GREY_TXT  = (120, 120, 120)
DARK_TXT  = (33,  33,  33)
FIELD_BG  = (250, 250, 250)
FIELD_BDR = (180, 180, 180)
FIELD_ACT = (33,  33,  33)   # active field border (Login email)
BTN_FILL  = (30,  30,  30)
BTN_OUT   = (200, 200, 200)
DIVIDER   = (220, 220, 220)

W, H = 393, 720   # phone content area (no status bar shown in most shots)

def new_canvas(with_toolbar=True, toolbar_title='StorePilot', status=False):
    img = Image.new('RGB', (W, H + (40 if status else 0)), BG)
    d = ImageDraw.Draw(img)
    top = 0
    if status:
        d.rectangle([0, 0, W, 40], fill=TOOLBAR)
        top = 40
    if with_toolbar:
        d.rectangle([0, top, W, top+56], fill=TOOLBAR)
        try:
            tf = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
        except:
            tf = ImageFont.load_default()
        d.text((18, top+18), toolbar_title, font=tf, fill=WHITE)
    return img, d, top + (56 if with_toolbar else 0)


def rounded_rect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=2):
    if fill:
        d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=r, outline=outline, width=width)


def label(d, x, y, text, size=16, bold=False, color=DARK_TXT, anchor='la'):
    try:
        path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold \
               else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        f = ImageFont.truetype(path, size)
    except:
        f = ImageFont.load_default()
    d.text((x, y), text, font=f, fill=color, anchor=anchor)


def text_field(d, x, y, w, h, placeholder, active=False, value='', with_eye=False):
    bdr = FIELD_ACT if active else FIELD_BDR
    lw = 2 if active else 1
    rounded_rect(d, x, y, x+w, y+h, 8, fill=FIELD_BG, outline=bdr, width=lw)
    if active and placeholder:
        # floating label style
        try:
            sf = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
        except:
            sf = ImageFont.load_default()
        d.text((x+14, y+6), placeholder, font=sf, fill=FIELD_ACT)
        # cursor line
        d.rectangle([x+14, y+32, x+16, y+46], fill=FIELD_ACT)
    else:
        label(d, x+14, y+h//2, placeholder, size=15, color=GREY_TXT, anchor='lm')
    if with_eye:
        # simple eye icon (circle + dot)
        ex, ey = x+w-30, y+h//2
        d.ellipse([ex-10, ey-6, ex+10, ey+6], outline=GREY_TXT, width=1)
        d.ellipse([ex-3, ey-3, ex+3, ey+3], fill=GREY_TXT)


def filled_button(d, x, y, w, h, text, size=16):
    rounded_rect(d, x, y, x+w, y+h, 8, fill=BTN_FILL)
    label(d, x+w//2, y+h//2, text, size=size, bold=True, color=WHITE, anchor='mm')


def outline_button(d, x, y, w, h, text, size=16):
    rounded_rect(d, x, y, x+w, y+h, 8, outline=BTN_OUT, width=2)
    label(d, x+w//2, y+h//2, text, size=size, bold=True, color=DARK_TXT, anchor='mm')


# ════════════════════════════════════════════════════════════════════════════
# Screen 1 — WelcomeActivity
# ════════════════════════════════════════════════════════════════════════════
def make_welcome():
    img, d, top = new_canvas(with_toolbar=True, status=True)
    cy = top + 210
    r  = 68
    # teal circle
    d.ellipse([W//2-r, cy-r, W//2+r, cy+r], fill=TEAL)
    # StorePilot bold
    label(d, W//2, cy+r+30, 'StorePilot', size=30, bold=True, color=DARK_TXT, anchor='mm')
    label(d, W//2, cy+r+65, 'Your smart store companion', size=15, color=GREY_TXT, anchor='mm')
    # buttons
    bx = 26
    filled_button(d, bx, cy+r+110, W-2*bx, 52, 'SIGN IN', size=15)
    outline_button(d, bx, cy+r+175, W-2*bx, 52, 'SIGN UP', size=15)
    img.save(f'{OUT}/screen_welcome.png', dpi=(180, 180))
    print('Saved: screen_welcome.png')


# ════════════════════════════════════════════════════════════════════════════
# Screen 2 — RoleSelectionActivity
# ════════════════════════════════════════════════════════════════════════════
def make_role_selection():
    img, d, top = new_canvas(with_toolbar=True)
    cy = top + 200
    label(d, W//2, cy, 'I am signing up as...', size=24, bold=True, anchor='mm')
    label(d, W//2, cy+46, 'Choose your account type', size=15, color=GREY_TXT, anchor='mm')
    bx = 26
    filled_button(d, bx, cy+100, W-2*bx, 54, 'OWNER', size=15)
    outline_button(d, bx, cy+170, W-2*bx, 54, 'CUSTOMER', size=15)
    img.save(f'{OUT}/screen_role_selection.png', dpi=(180, 180))
    print('Saved: screen_role_selection.png')


# ════════════════════════════════════════════════════════════════════════════
# Screen 3 — RegisterActivity (Customer)
# ════════════════════════════════════════════════════════════════════════════
def make_register(role='Customer', suffix='customer'):
    img, d, top = new_canvas(with_toolbar=True)
    y = top + 22
    label(d, 26, y, 'Create Account', size=26, bold=True)
    label(d, 26, y+38, 'Fill in your details to get started', size=14, color=GREY_TXT)
    y += 80
    bx, fw = 26, W-52
    fh = 54
    gap = 14
    fields = [
        ('Full Name', False, False),
        ('Username', False, False),
        ('Email Address', False, False),
        ('Phone Number (optional)', False, False),
        ('Password', False, True),
        ('Confirm Password', False, False),
    ]
    for (ph, act, eye) in fields:
        text_field(d, bx, y, fw, fh, ph, active=act, with_eye=eye)
        y += fh + gap

    label(d, 26, y+4, f'Signing up as: {role}', size=13, bold=True, color=DARK_TXT)
    y += 32
    filled_button(d, bx, y, fw, 52, 'CREATE ACCOUNT', size=14)
    img.save(f'{OUT}/screen_register_{suffix}.png', dpi=(180, 180))
    print(f'Saved: screen_register_{suffix}.png')


# ════════════════════════════════════════════════════════════════════════════
# Screen 4 — LoginActivity
# ════════════════════════════════════════════════════════════════════════════
def make_login():
    img, d, top = new_canvas(with_toolbar=True)
    cy = top + 130
    r  = 55
    d.ellipse([W//2-r, cy-r, W//2+r, cy+r], fill=TEAL)
    label(d, W//2, cy+r+28, 'StorePilot', size=26, bold=True, anchor='mm')
    label(d, W//2, cy+r+58, 'Welcome back!', size=15, color=GREY_TXT, anchor='mm')
    bx, fw = 26, W-52
    fy = cy+r+90
    text_field(d, bx, fy, fw, 56, 'Email', active=True)
    text_field(d, bx, fy+70, fw, 54, 'Password', active=False)
    filled_button(d, bx, fy+144, fw, 52, 'LOGIN', size=15)
    img.save(f'{OUT}/screen_login.png', dpi=(180, 180))
    print('Saved: screen_login.png')


# ════════════════════════════════════════════════════════════════════════════
# Remaining screens — generated from layout XML / code knowledge
# ════════════════════════════════════════════════════════════════════════════

def make_customer_home():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='StorePilot')
    y = top + 14
    label(d, 26, y, 'Hello, Customer!', size=18, bold=True)
    label(d, 26, y+28, 'Discover our products', size=13, color=GREY_TXT)
    # search bar
    sy = y+58
    rounded_rect(d, 26, sy, W-26, sy+44, 22, fill=WHITE, outline=FIELD_BDR, width=1)
    label(d, 60, sy+22, 'Search products...', size=14, color=GREY_TXT, anchor='lm')
    # product grid (2 columns, 3 rows)
    py = sy+58
    cols = [(30, py), (W//2+8, py), (30, py+170), (W//2+8, py+170), (30, py+340), (W//2+8, py+340)]
    pnames = ['T-Shirt (M)', 'Jeans (L)', 'Sneakers', 'Cap', 'Jacket', 'Shorts']
    prices = ['$29.99', '$49.99', '$79.99', '$19.99', '$89.99', '$24.99']
    for i, (px, py2) in enumerate(cols):
        pw = W//2 - 38
        rounded_rect(d, px, py2, px+pw, py2+155, 10, fill=WHITE, outline=DIVIDER, width=1)
        # product image placeholder
        d.rectangle([px+8, py2+8, px+pw-8, py2+85], fill=(220,232,240))
        label(d, px+pw//2, py2+47, '📦', size=28, anchor='mm')
        label(d, px+10, py2+92, pnames[i], size=12, bold=True)
        label(d, px+10, py2+110, prices[i], size=13, bold=True, color=(33,100,180))
        # In Stock badge
        rounded_rect(d, px+10, py2+128, px+70, py2+145, 4, fill=(232,245,233))
        label(d, px+40, py2+136, 'In Stock', size=9, color=(46,125,50), anchor='mm')
        # Add to cart
        rounded_rect(d, px+pw-80, py2+125, px+pw-8, py2+147, 6, fill=BTN_FILL)
        label(d, px+pw-44, py2+136, '+ Cart', size=9, bold=True, color=WHITE, anchor='mm')
    img.save(f'{OUT}/screen_customer_home.png', dpi=(180, 180))
    print('Saved: screen_customer_home.png')


def make_cart():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='My Cart')
    y = top + 20
    items = [
        ('T-Shirt (M)', '$29.99', 2, '$59.98'),
        ('Jeans (L)',   '$49.99', 1, '$49.99'),
        ('Sneakers',    '$79.99', 1, '$79.99'),
    ]
    for name, price, qty, sub in items:
        rounded_rect(d, 14, y, W-14, y+80, 8, fill=WHITE, outline=DIVIDER, width=1)
        d.rectangle([22, y+10, 70, y+70], fill=(220,232,240))
        label(d, 46, y+40, '📦', size=18, anchor='mm')
        label(d, 82, y+16, name, size=14, bold=True)
        label(d, 82, y+36, price, size=13, color=(33,100,180))
        # qty controls
        qx = W-130
        rounded_rect(d, qx, y+45, qx+28, y+69, 4, fill=FIELD_BG, outline=FIELD_BDR, width=1)
        label(d, qx+14, y+57, '−', size=14, bold=True, anchor='mm')
        label(d, qx+42, y+57, str(qty), size=14, bold=True, anchor='mm')
        rounded_rect(d, qx+56, y+45, qx+84, y+69, 4, fill=FIELD_BG, outline=FIELD_BDR, width=1)
        label(d, qx+70, y+57, '+', size=14, bold=True, anchor='mm')
        label(d, W-26, y+57, '🗑', size=16, anchor='rm')
        label(d, W-22, y+16, sub, size=12, bold=True, anchor='ra')
        y += 94
    d.line([14, y+10, W-14, y+10], fill=DIVIDER, width=1)
    label(d, 26, y+28, 'Total', size=16, bold=True)
    label(d, W-26, y+28, '$189.96', size=16, bold=True, anchor='ra')
    filled_button(d, 26, y+68, W-52, 52, 'CHECKOUT', size=15)
    img.save(f'{OUT}/screen_cart.png', dpi=(180, 180))
    print('Saved: screen_cart.png')


def make_support_chat():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Support Chat')
    y = top + 16
    msgs = [
        ('Hello! How can I help you?', False, (235,245,255)),
        ('I need help with my order #1042', True,  (30,30,30)),
        ('Sure! Let me check that for you.', False, (235,245,255)),
        ('Your order is being processed now.', False, (235,245,255)),
        ('Great, thank you!', True,  (30,30,30)),
    ]
    for txt, is_sent, bg in msgs:
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
        except:
            f = ImageFont.load_default()
        bbox = d.textbbox((0,0), txt, font=f)
        tw = bbox[2]-bbox[0]+24
        tw = min(tw, W-80)
        if is_sent:
            bx = W-tw-18
            rounded_rect(d, bx, y, bx+tw, y+38, 14, fill=BTN_FILL)
            d.text((bx+12, y+10), txt, font=f, fill=WHITE)
        else:
            rounded_rect(d, 18, y, 18+tw, y+38, 14, fill=bg, outline=DIVIDER, width=1)
            d.text((30, y+10), txt, font=f, fill=DARK_TXT)
        y += 50
    # input bar
    iy = H-62
    d.rectangle([0, iy, W, H], fill=WHITE)
    d.line([0, iy, W, iy], fill=DIVIDER, width=1)
    rounded_rect(d, 14, iy+10, W-64, iy+46, 22, fill=FIELD_BG, outline=FIELD_BDR, width=1)
    label(d, 30, iy+28, 'Type a message...', size=13, color=GREY_TXT, anchor='lm')
    rounded_rect(d, W-54, iy+10, W-14, iy+46, 22, fill=TEAL)
    label(d, W-34, iy+28, '➤', size=16, color=WHITE, anchor='mm')
    img.save(f'{OUT}/screen_support_chat.png', dpi=(180, 180))
    print('Saved: screen_support_chat.png')


def make_task_list():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Tasks')
    # Tab bar
    ty = top
    tab_w = W//3
    tabs = ['My Tasks', 'Team', 'Private']
    for i, tab in enumerate(tabs):
        x0 = i*tab_w
        if i == 0:
            d.rectangle([x0, ty, x0+tab_w, ty+44], fill=WHITE)
            d.line([x0+8, ty+40, x0+tab_w-8, ty+40], fill=BTN_FILL, width=3)
            label(d, x0+tab_w//2, ty+22, tab, size=13, bold=True, anchor='mm')
        else:
            d.rectangle([x0, ty, x0+tab_w, ty+44], fill=FIELD_BG)
            label(d, x0+tab_w//2, ty+22, tab, size=13, color=GREY_TXT, anchor='mm')
    y = ty+60
    tasks = [
        ('Restock shelves',    'IN PROGRESS', 'HIGH',   (255,236,179), (230,81,0)),
        ('Count inventory',    'TODO',         'MEDIUM', (232,245,233), (46,125,50)),
        ('Update price tags',  'TODO',         'LOW',    (227,242,253), (25,118,210)),
        ('Team meeting prep',  'DONE',         'LOW',    (243,229,245), (106,27,154)),
    ]
    for title, status, prio, pbg, pcol in tasks:
        rounded_rect(d, 14, y, W-14, y+72, 8, fill=WHITE, outline=DIVIDER, width=1)
        label(d, 28, y+14, title, size=14, bold=True)
        # status chip
        sw = 90
        rounded_rect(d, 28, y+36, 28+sw, y+56, 12, fill=pbg)
        label(d, 28+sw//2, y+46, status, size=9, color=pcol, anchor='mm')
        # priority chip
        pw2 = 60
        rounded_rect(d, 28+sw+10, y+36, 28+sw+10+pw2, y+56, 12, fill=FIELD_BG)
        label(d, 28+sw+10+pw2//2, y+46, prio, size=9, color=GREY_TXT, anchor='mm')
        y += 82
    # FAB
    fx, fy, fr = W-54, H-66, 28
    d.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=BTN_FILL)
    label(d, fx, fy, '+', size=28, bold=True, color=WHITE, anchor='mm')
    img.save(f'{OUT}/screen_task_list.png', dpi=(180, 180))
    print('Saved: screen_task_list.png')


def make_product_list():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Inventory')
    y = top + 14
    products = [
        ('T-Shirt (Blue, M)',  'Clothing',  'Qty: 45', '$29.99'),
        ('Jeans (Black, L)',   'Clothing',  'Qty: 12', '$49.99'),
        ('Sneakers (42)',      'Footwear',  'Qty: 8',  '$79.99'),
        ('Baseball Cap',       'Accessory', 'Qty: 3',  '$19.99'),
        ('Winter Jacket',      'Clothing',  'Qty: 0',  '$89.99'),
        ('Running Shorts',     'Sportswear','Qty: 22', '$24.99'),
    ]
    for name, cat, qty, price in products:
        rounded_rect(d, 14, y, W-14, y+62, 8, fill=WHITE, outline=DIVIDER, width=1)
        d.rectangle([22, y+10, 56, y+52], fill=(220,232,240))
        label(d, 39, y+31, '📦', size=16, anchor='mm')
        label(d, 66, y+12, name, size=13, bold=True)
        label(d, 66, y+30, cat, size=12, color=GREY_TXT)
        # qty badge
        qcol = (198,40,40) if '0' in qty else (46,125,50)
        qbg  = (255,235,238) if '0' in qty else (232,245,233)
        rounded_rect(d, 66, y+42, 66+70, y+56, 4, fill=qbg)
        label(d, 101, y+49, qty, size=9, color=qcol, anchor='mm')
        label(d, W-22, y+31, price, size=14, bold=True, color=(33,100,180), anchor='rm')
        y += 72
    # FAB
    fx, fy, fr = W-54, H-66, 28
    d.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=BTN_FILL)
    label(d, fx, fy, '+', size=28, bold=True, color=WHITE, anchor='mm')
    img.save(f'{OUT}/screen_product_list.png', dpi=(180, 180))
    print('Saved: screen_product_list.png')


def make_manager_orders():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Orders')
    y = top + 14
    orders = [
        ('#1042', 'Cust #3', '$59.98',  'PENDING',    (255,152,0),   (255,243,224)),
        ('#1041', 'Cust #7', '$189.96', 'PROCESSING', (30,136,229),  (227,242,253)),
        ('#1040', 'Cust #2', '$49.99',  'SHIPPED',    (142,36,170),  (243,229,245)),
        ('#1039', 'Cust #5', '$79.99',  'DELIVERED',  (67,160,71),   (232,245,233)),
        ('#1038', 'Cust #1', '$24.99',  'CANCELLED',  (229,57,53),   (255,235,238)),
    ]
    for oid, cust, total, status, scol, sbg in orders:
        rounded_rect(d, 14, y, W-14, y+78, 8, fill=WHITE, outline=DIVIDER, width=1)
        label(d, 28, y+12, f'Order {oid}', size=14, bold=True)
        label(d, 28, y+32, cust, size=12, color=GREY_TXT)
        label(d, 28, y+50, total, size=13, bold=True, color=(33,100,180))
        # status badge
        sw = 100
        rounded_rect(d, W-sw-22, y+10, W-22, y+32, 8, fill=sbg)
        label(d, W-22-sw//2, y+21, status, size=9, bold=True, color=scol, anchor='mm')
        # spinner
        rounded_rect(d, W-110, y+42, W-22, y+66, 4, fill=FIELD_BG, outline=FIELD_BDR, width=1)
        label(d, W-66, y+54, 'Change ▾', size=10, color=GREY_TXT, anchor='mm')
        y += 88
    img.save(f'{OUT}/screen_manager_orders.png', dpi=(180, 180))
    print('Saved: screen_manager_orders.png')


def make_dashboard():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Dashboard')
    y = top + 16
    # Season alert card
    rounded_rect(d, 14, y, W-14, y+54, 8, fill=(255,243,224), outline=(255,152,0), width=2)
    label(d, 30, y+10, '⚠  Season Alert', size=13, bold=True, color=(230,81,0))
    label(d, 30, y+30, 'Winter Sale ends in 12 days', size=12, color=(97,26,21))
    y += 68
    # KPI cards
    kpis = [
        ("Today's Sales",   '$1,240.50', (33,150,243),  (227,242,253)),
        ('Low Stock Items',  '3 products',(244,67,54),   (255,235,238)),
        ('Pending Tasks',    '7 tasks',   (255,152,0),   (255,243,224)),
        ("Today's Orders",   '14 orders', (76,175,80),   (232,245,233)),
    ]
    cw = (W-42)//2
    for i, (title, val, col, bg) in enumerate(kpis):
        cx = 14 + (i%2)*(cw+14)
        cy2 = y + (i//2)*110
        rounded_rect(d, cx, cy2, cx+cw, cy2+96, 10, fill=bg, outline=DIVIDER, width=1)
        label(d, cx+cw//2, cy2+28, val, size=22, bold=True, color=col, anchor='mm')
        label(d, cx+cw//2, cy2+56, title, size=11, color=GREY_TXT, anchor='mm')
        # mini bar chart decoration
        for j in range(5):
            bh = 8 + j*4
            bx2 = cx+12+j*14
            d.rectangle([bx2, cy2+78-bh, bx2+10, cy2+78], fill=col+(100,) if len(col)==3 else col)
    img.save(f'{OUT}/screen_dashboard.png', dpi=(180, 180))
    print('Saved: screen_dashboard.png')


def make_notifications():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Notifications')
    y = top + 16
    notifs = [
        ('Low Stock Alert', 'Baseball Cap has only 3 units left.', '2 min ago', (244,67,54), (255,235,238)),
        ('Low Stock Alert', 'Winter Jacket is out of stock!',       '1 hr ago',  (244,67,54), (255,235,238)),
        ('New Order',       'Order #1043 placed by Customer #8.',   '3 hrs ago', (33,150,243),(227,242,253)),
        ('Season Ending',   'Winter Sale ends in 12 days.',         'Today',     (255,152,0), (255,243,224)),
    ]
    for title, msg, time_, col, bg in notifs:
        rounded_rect(d, 14, y, W-14, y+72, 8, fill=bg, outline=DIVIDER, width=1)
        d.ellipse([26, y+22, 50, y+46], fill=col)
        label(d, 38, y+34, '!', size=14, bold=True, color=WHITE, anchor='mm')
        label(d, 62, y+14, title, size=13, bold=True, color=col)
        label(d, 62, y+32, msg, size=11, color=DARK_TXT)
        label(d, W-22, y+14, time_, size=10, color=GREY_TXT, anchor='ra')
        y += 82
    img.save(f'{OUT}/screen_notifications.png', dpi=(180, 180))
    print('Saved: screen_notifications.png')


def make_order_history():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='My Orders')
    y = top + 16
    orders = [
        ('#1042', '3 items', '$59.98',  'PENDING',   (255,152,0),  (255,243,224)),
        ('#1039', '1 item',  '$79.99',  'DELIVERED', (67,160,71),  (232,245,233)),
        ('#1035', '2 items', '$109.98', 'DELIVERED', (67,160,71),  (232,245,233)),
    ]
    for oid, items, total, status, scol, sbg in orders:
        rounded_rect(d, 14, y, W-14, y+82, 8, fill=WHITE, outline=DIVIDER, width=1)
        label(d, 28, y+14, f'Order {oid}', size=15, bold=True)
        label(d, 28, y+36, items, size=13, color=GREY_TXT)
        label(d, 28, y+56, total, size=14, bold=True, color=(33,100,180))
        rounded_rect(d, W-120, y+14, W-22, y+36, 8, fill=sbg)
        label(d, W-71, y+25, status, size=10, bold=True, color=scol, anchor='mm')
        y += 96
    img.save(f'{OUT}/screen_order_history.png', dpi=(180, 180))
    print('Saved: screen_order_history.png')


def make_checkout():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Checkout')
    y = top + 22
    label(d, 26, y, 'Shipping Address', size=16, bold=True)
    y += 36
    bx, fw = 26, W-52
    text_field(d, bx, y, fw, 54, 'Enter your full address...', active=False)
    y += 72
    label(d, 26, y, 'Payment Method', size=16, bold=True)
    y += 36
    opts = [('Cash on Delivery', True), ('PayPal', False), ('Credit Card', False)]
    for opt, checked in opts:
        rounded_rect(d, bx, y, bx+fw, y+46, 8, fill=WHITE, outline=DIVIDER, width=1)
        r = 10
        d.ellipse([bx+14, y+13, bx+14+2*r, y+13+2*r], outline=(60,60,60), width=2)
        if checked:
            d.ellipse([bx+19, y+18, bx+19+10, y+18+10], fill=(60,60,60))
        label(d, bx+44, y+23, opt, size=14, anchor='lm')
        y += 56
    y += 10
    # order summary
    rounded_rect(d, bx, y, bx+fw, y+72, 8, fill=FIELD_BG, outline=DIVIDER, width=1)
    label(d, bx+14, y+14, 'Order Summary', size=13, bold=True)
    label(d, bx+14, y+36, '3 items', size=12, color=GREY_TXT)
    label(d, bx+fw-14, y+36, '$189.96', size=13, bold=True, color=(33,100,180), anchor='ra')
    y += 86
    filled_button(d, bx, y, fw, 52, 'PLACE ORDER', size=15)
    img.save(f'{OUT}/screen_checkout.png', dpi=(180, 180))
    print('Saved: screen_checkout.png')


def make_favorites():
    img, d, top = new_canvas(with_toolbar=True, toolbar_title='Favourites')
    y = top + 16
    favs = [
        ('T-Shirt (Blue, M)', '$29.99', 'In Stock'),
        ('Sneakers (42)',     '$79.99', 'In Stock'),
        ('Winter Jacket',     '$89.99', 'Out of Stock'),
    ]
    for name, price, stock in favs:
        rounded_rect(d, 14, y, W-14, y+84, 8, fill=WHITE, outline=DIVIDER, width=1)
        d.rectangle([22, y+10, 76, y+74], fill=(220,232,240))
        label(d, 49, y+42, '📦', size=22, anchor='mm')
        label(d, 88, y+16, name, size=14, bold=True)
        label(d, 88, y+36, price, size=13, bold=True, color=(33,100,180))
        scol = (46,125,50) if 'In' in stock else (198,40,40)
        sbg  = (232,245,233) if 'In' in stock else (255,235,238)
        rounded_rect(d, 88, y+52, 88+90, y+68, 4, fill=sbg)
        label(d, 133, y+60, stock, size=10, color=scol, anchor='mm')
        # heart icon
        label(d, W-32, y+22, '♥', size=22, color=(229,57,53), anchor='mm')
        # add to cart
        rounded_rect(d, W-120, y+50, W-22, y+72, 6, fill=BTN_FILL)
        label(d, W-71, y+61, '+ Cart', size=11, bold=True, color=WHITE, anchor='mm')
        y += 96
    img.save(f'{OUT}/screen_favorites.png', dpi=(180, 180))
    print('Saved: screen_favorites.png')


if __name__ == '__main__':
    make_welcome()
    make_role_selection()
    make_register('Customer', 'customer')
    make_register('Owner', 'owner')
    make_login()
    make_customer_home()
    make_cart()
    make_support_chat()
    make_task_list()
    make_product_list()
    make_manager_orders()
    make_dashboard()
    make_notifications()
    make_order_history()
    make_checkout()
    make_favorites()
    print('\nAll screens done.')
