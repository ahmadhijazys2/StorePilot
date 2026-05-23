#!/usr/bin/env python3
"""
StorePilot Project Book Generator
Produces a Ministry-of-Education-style project book PDF.
Cover page: bilingual (Hebrew + English). All other pages: English.
"""

from fpdf import FPDF, XPos, YPos
from bidi.algorithm import get_display
import os

# ── Font paths ─────────────────────────────────────────────────────────────────
FONT_REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B= "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

OUT_PATH   = "/home/user/StorePilot/StorePilot_Project_Book.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
C_TITLE   = (0,   70, 127)
C_CHAPTER = (0,   70, 127)
C_SECTION = (30, 100, 180)
C_CODE_BG = (245, 245, 245)
C_CODE_FG = (40,  40,  40)
C_RULE    = (200, 200, 200)
C_BLACK   = (0,    0,   0)
C_WHITE   = (255, 255, 255)
C_GRAY    = (100, 100, 100)

MARGIN = 20
LINE_H = 6
CODE_H = 5


class BookPDF(FPDF):

    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=25)
        self.set_left_margin(MARGIN)
        self.set_right_margin(MARGIN)
        self.add_font('DV',  '',  FONT_REG)
        self.add_font('DV',  'B', FONT_BOLD)
        self.add_font('DVM', '',  FONT_MONO)
        self.add_font('DVM', 'B', FONT_MONO_B)
        self._chapter_num = 0

    def hb(self, text):
        return get_display(text)

    def set_rgb(self, c):
        self.set_text_color(*c)

    def rule(self, color=C_RULE):
        self.set_draw_color(*color)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('DV', 'B', 8)
        self.set_text_color(*C_GRAY)
        self.cell(0, 8, 'StorePilot - Store Management System | Project Book',
                  align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*C_RULE)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())
        self.ln(2)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('DV', '', 8)
        self.set_text_color(*C_GRAY)
        self.cell(0, 8, f'Page {self.page_no() - 1}', align='C')

    def chapter_title(self, title):
        self._chapter_num += 1
        self.add_page()
        self.set_font('DV', 'B', 18)
        self.set_text_color(*C_CHAPTER)
        self.cell(0, 12, f'Chapter {self._chapter_num}: {title}',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*C_CHAPTER)
        self.set_line_width(0.7)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())
        self.set_line_width(0.2)
        self.ln(4)

    def section(self, title):
        self.ln(4)
        self.set_font('DV', 'B', 13)
        self.set_text_color(*C_SECTION)
        self.cell(0, 9, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.rule(C_RULE)
        self.ln(2)
        self.set_rgb(C_BLACK)

    def subsection(self, title):
        self.ln(2)
        self.set_font('DV', 'B', 11)
        self.set_text_color(*C_TITLE)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_rgb(C_BLACK)

    def body(self, text, size=10):
        self.set_font('DV', '', size)
        self.set_rgb(C_BLACK)
        self.multi_cell(0, LINE_H, text)
        self.ln(1)

    def bullet(self, text, size=10):
        self.set_font('DV', '', size)
        self.set_rgb(C_BLACK)
        self.set_x(MARGIN + 4)
        self.multi_cell(0, LINE_H, f'  - {text}')

    def code_block(self, code_text, small=False):
        fs = 7.5 if small else 8.5
        ch = CODE_H if small else CODE_H + 0.5
        lines = code_text.split('\n')
        w = 210 - 2 * MARGIN
        total_h = ch * len(lines) + 4
        self.set_fill_color(*C_CODE_BG)
        self.set_draw_color(*C_RULE)
        self.rect(MARGIN, self.get_y(), w, total_h, 'FD')
        self.set_y(self.get_y() + 2)
        for line in lines:
            self.set_x(MARGIN + 2)
            self.set_font('DVM', '', fs)
            self.set_text_color(*C_CODE_FG)
            self.cell(w - 4, ch, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_BLACK)
        self.ln(2)

    def kv(self, key, value, key_w=55):
        self.set_font('DV', 'B', 10)
        self.set_rgb(C_BLACK)
        self.cell(key_w, LINE_H, key + ':', new_x=XPos.RIGHT)
        self.set_font('DV', '', 10)
        val_w = self.epw - key_w
        self.multi_cell(val_w, LINE_H, value,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def attr_table_header(self):
        self.set_font('DV', 'B', 9)
        self.set_fill_color(*C_TITLE)
        self.set_text_color(*C_WHITE)
        c0, c1, c2 = 42, 36, 22
        c3 = self.epw - c0 - c1 - c2
        self.cell(c0, 7, 'Field Name', border=1, fill=True)
        self.cell(c1, 7, 'Type',       border=1, fill=True)
        self.cell(c2, 7, 'Scope',      border=1, fill=True)
        self.cell(c3, 7, 'Purpose',    border=1, fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*C_BLACK)

    def attr_table_row(self, name, typ, scope, purpose):
        self.set_font('DVM', '', 8)
        c0, c1, c2 = 42, 36, 22
        c3 = self.epw - c0 - c1 - c2
        self.cell(c0, 6, name,  border=1)
        self.cell(c1, 6, typ,   border=1)
        self.cell(c2, 6, scope, border=1)
        self.multi_cell(c3, 6, purpose, border=1,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def make_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*C_TITLE)
    pdf.rect(0, 0, 210, 60, 'F')

    pdf.set_font('DV', 'B', 22)
    pdf.set_text_color(*C_WHITE)
    pdf.set_y(10)
    pdf.cell(0, 12, pdf.hb('ספר פרויקט - מערכת ניהול חנות'),
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('DV', '', 14)
    pdf.cell(0, 9, pdf.hb('תוכנה לניהול מלאי, מכירות והזמנות לקוחות'),
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_y(70)
    pdf.set_font('DV', 'B', 32)
    pdf.set_text_color(*C_TITLE)
    pdf.cell(0, 16, 'StorePilot', align='C',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('DV', 'B', 16)
    pdf.set_text_color(*C_SECTION)
    pdf.cell(0, 10, 'Store Management & E-Commerce Android Application',
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.set_draw_color(*C_RULE)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(10)

    pdf.set_font('DV', '', 14)
    pdf.set_text_color(*C_BLACK)
    pdf.cell(0, 9, 'Project Book', align='C',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 9, 'Final Year Computer Science Project',
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)

    pdf.set_fill_color(240, 245, 255)
    pdf.set_draw_color(*C_SECTION)
    pdf.rect(45, pdf.get_y(), 120, 60, 'FD')
    pdf.set_y(pdf.get_y() + 6)

    for k, v in [
        ('Student',  'Ahmad Hijazy'),
        ('Email',    'ahmadhijazy480@gmail.com'),
        ('School',   'High School - Computer Science Track'),
        ('Year',     '2025 / 2026'),
        ('Language', 'Java (Android)'),
        ('Backend',  'Firebase Firestore + Firebase Auth'),
    ]:
        pdf.set_font('DV', 'B', 10)
        pdf.set_x(50)
        pdf.cell(35, 8, k + ':', new_x=XPos.RIGHT)
        pdf.set_font('DV', '', 10)
        pdf.cell(0, 8, v, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(16)
    pdf.set_font('DV', '', 10)
    pdf.set_text_color(*C_GRAY)
    pdf.cell(0, 7,
             'Submitted in partial fulfillment of final project requirements',
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.set_font('DV', '', 11)
    pdf.set_text_color(*C_SECTION)
    pdf.cell(0, 8, pdf.hb('פרויקט גמר - תכנות Android'),
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, pdf.hb('מוגש לצורך סיום תכנית הלימודים במדעי המחשב'),
             align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def make_toc(pdf):
    pdf.add_page()
    pdf.set_font('DV', 'B', 18)
    pdf.set_text_color(*C_TITLE)
    pdf.cell(0, 14, 'Table of Contents', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.rule(C_TITLE)
    pdf.ln(4)

    toc = [
        ('1', 'Introduction'),
        ('',  '1.1  Background and Motivation'),
        ('',  '1.2  Project Objectives'),
        ('',  '1.3  Target Users'),
        ('',  '1.4  Technology Stack'),
        ('2', 'System Requirements'),
        ('',  '2.1  Functional Requirements'),
        ('',  '2.2  Non-Functional Requirements'),
        ('3', 'System Architecture'),
        ('',  '3.1  MVVM Design Pattern'),
        ('',  '3.2  Firebase Integration'),
        ('',  '3.3  Firestore Data Collections'),
        ('',  '3.4  Role-Based Access Control'),
        ('4', 'Data Model'),
        ('',  '4.1 - 4.8  Entity Classes (User, Product, Order, Sale, Task, Season, CartItem, SupportMessage)'),
        ('5', 'Implementation - Core Modules'),
        ('',  '5.1  StorePilotApp  |  5.2  SessionManager  |  5.3  PermissionManager'),
        ('',  '5.4  FirestoreManager  |  5.5  LowStockReceiver  |  5.6  NotificationHelper'),
        ('',  '5.7  CryptoUtil  |  5.8  BaseActivity & FirebaseAuthHelper'),
        ('6', 'Implementation - Repositories'),
        ('',  '6.1  ProductRepository  |  6.2  UserRepository  |  6.3  OrderRepository'),
        ('',  '6.4  SaleRepository  |  6.5  TaskRepository  |  6.6  SeasonRepository'),
        ('',  '6.7  SupportRepository'),
        ('7', 'Implementation - ViewModels & UI'),
        ('',  '7.1  AuthViewModel & LoginActivity'),
        ('',  '7.2  ProductViewModel & ProductListFragment'),
        ('',  '7.3  OrderViewModel & CheckoutFragment'),
        ('',  '7.4  DashboardFragment'),
        ('8', 'Screen Flow & Navigation'),
        ('9', 'Testing'),
        ('A', 'Appendix: Full Source Code (13 classes)'),
    ]

    for ch, title in toc:
        if ch.strip():
            pdf.set_font('DV', 'B', 11)
            pdf.set_text_color(*C_TITLE)
            indent = 0
        else:
            pdf.set_font('DV', '', 10)
            pdf.set_text_color(*C_BLACK)
            indent = 8
        pdf.set_x(MARGIN + indent)
        pdf.cell(0, 7, f'{ch}  {title}' if ch.strip() else f'    {title}',
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*C_BLACK)


def ch1_introduction(pdf):
    pdf.chapter_title('Introduction')

    pdf.section('1.1  Background and Motivation')
    pdf.body(
        'Small and medium-sized retail stores often struggle to manage their operations '
        'efficiently. Tasks such as tracking inventory, recording sales, managing customer '
        'orders, and scheduling staff are frequently handled through paper records or '
        'disconnected spreadsheets. This results in errors, wasted time, and poor '
        'visibility into the store\'s real-time state.\n\n'
        'StorePilot was developed to solve this problem by providing a single, unified '
        'Android application that digitizes all core store management functions. The '
        'application targets clothing and general retail stores and was designed with '
        'simplicity in mind, so that staff at all technical levels can adopt it quickly.'
    )

    pdf.section('1.2  Project Objectives')
    for o in [
        'Provide a real-time inventory management system with automatic low-stock notifications.',
        'Enable staff to record walk-in sales and track revenue by day, week, and month.',
        'Allow customers to browse products and place online orders from their smartphones.',
        'Implement a task management module for assigning and tracking staff responsibilities.',
        'Manage seasonal product collections with configurable end-of-season dashboard alerts.',
        'Provide a live support chat between customers and store managers.',
        'Enforce role-based access control so each staff role sees only what they need.',
        'Synchronize all data in real time via Firebase Firestore across multiple devices.',
    ]:
        pdf.bullet(o)

    pdf.section('1.3  Target Users')
    for role, desc in [
        ('Owner',         'Full administrative control. Manages users, products, views all data.'),
        ('Store Manager', 'Manages inventory, records sales, manages tasks and customer orders.'),
        ('Shift Manager', 'Records sales, views products, manages team-level tasks.'),
        ('Employee',      'Records sales, views products, creates private personal tasks.'),
        ('Customer',      'Browses products, adds to cart, places orders, tracks delivery, chats.'),
    ]:
        pdf.set_font('DV', 'B', 10)
        pdf.set_rgb(C_SECTION)
        pdf.cell(0, 7, role, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.body(desc)

    pdf.section('1.4  Technology Stack')
    for k, v in [
        ('Platform',        'Android (API 24+), Java'),
        ('Architecture',    'MVVM with LiveData (Google recommended pattern)'),
        ('UI Toolkit',      'Material Design, RecyclerView, CardView, BottomNavigationView'),
        ('Authentication',  'Firebase Authentication (email/password)'),
        ('Database',        'Firebase Cloud Firestore (real-time NoSQL cloud database)'),
        ('Notifications',   'AlarmManager + BroadcastReceiver + NotificationManager'),
        ('IDE',             'Android Studio'),
        ('Build Tool',      'Gradle (Groovy DSL)'),
        ('Min SDK',         'API 24 (Android 7.0 Nougat)'),
        ('Target SDK',      'API 34 (Android 14)'),
    ]:
        pdf.kv(k, v)
        pdf.ln(1)


def ch2_requirements(pdf):
    pdf.chapter_title('System Requirements')

    pdf.section('2.1  Functional Requirements')
    for code, title, desc in [
        ('FR-01', 'User Registration & Login',
         'Staff and customers register with email/password and log in via Firebase Auth. '
         'The system routes them to different UIs based on their role field.'),
        ('FR-02', 'Role-Based Access',
         'Every screen and action is gated by PermissionManager. Unauthorised users '
         'cannot see or trigger features outside their role.'),
        ('FR-03', 'Product Inventory',
         'Authorised staff create, view, edit, and delete products. Each product has '
         'name, category, size, colour, quantity, selling price, cost price, and image URL.'),
        ('FR-04', 'Low-Stock Alerts',
         'AlarmManager triggers LowStockReceiver hourly. When quantity <= 5, '
         'a system notification is posted automatically.'),
        ('FR-05', 'Sales Recording',
         'Employees record manual walk-in sales (product, quantity, price, date, staff).'),
        ('FR-06', 'Customer E-Commerce',
         'Customers browse products, add to Firestore cart, mark favourites, '
         'place orders with address and payment method.'),
        ('FR-07', 'Order Management',
         'Managers view active orders and progress status: '
         'PENDING -> PROCESSING -> SHIPPED -> DELIVERED. '
         'DELIVERED auto-creates a Sale record.'),
        ('FR-08', 'Task Management',
         'Staff create tasks with title, description, assignee, priority, due date. '
         'Tasks can be private or team-wide.'),
        ('FR-09', 'Season Management',
         'Managers define seasonal collections. Dashboard banner appears when '
         'a season ends within 30 days.'),
        ('FR-10', 'Support Chat',
         'Customers open a live chat with managers. Messages stored in '
         'support/{customerId}/messages Firestore sub-collection.'),
        ('FR-11', 'User Management',
         'Owners view all registered users and their roles via the Admin screen.'),
    ]:
        pdf.set_font('DV', 'B', 10)
        pdf.set_rgb(C_SECTION)
        pdf.cell(0, 7, f'{code} - {title}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('DV', '', 10)
        pdf.set_rgb(C_BLACK)
        pdf.multi_cell(0, LINE_H, desc)
        pdf.ln(2)

    pdf.section('2.2  Non-Functional Requirements')
    for k, v in [
        ('Performance',   'Firestore queries return results within 3 seconds on 4G.'),
        ('Usability',     'Material Design guidelines. Bottom navigation for staff; '
                          'separate Activity for customers.'),
        ('Security',      'Firebase Auth manages credentials. No raw passwords stored. '
                          'CryptoUtil provides PBKDF2WithHmacSHA256 hashing.'),
        ('Scalability',   'Firestore scales automatically. Real-time listeners keep all '
                          'connected clients in sync within seconds.'),
        ('Offline Mode',  'Firestore SDK caches recent reads. Writes are queued and '
                          'synced when connectivity resumes.'),
        ('Compatibility', 'Android 7.0+ (API 24+), covering more than 95% of active devices.'),
        ('Notifications', 'NotificationChannel required on API 26+. POST_NOTIFICATIONS '
                          'permission requested on Android 13+.'),
    ]:
        pdf.kv(k, v)
        pdf.ln(2)


def ch3_architecture(pdf):
    pdf.chapter_title('System Architecture')

    pdf.section('3.1  MVVM Design Pattern')
    pdf.body(
        'StorePilot follows the Model-View-ViewModel (MVVM) architecture '
        'recommended by Google for Android. This pattern separates the '
        'application into three layers:'
    )
    for name, desc in [
        ('Model',
         'Data entities (User, Product, Order, etc.) and Repositories. '
         'Repositories wrap all Firestore calls and expose LiveData so the '
         'rest of the app is decoupled from the data source.'),
        ('ViewModel',
         'AndroidViewModel subclasses that hold and transform data for the UI. '
         'They survive configuration changes (e.g. rotation) because they are '
         'scoped to the Activity/Fragment lifecycle, not the View.'),
        ('View',
         'Activities and Fragments observe LiveData from ViewModels. '
         'The UI updates automatically when data changes, with no manual refresh.'),
    ]:
        pdf.subsection(name)
        pdf.body(desc)

    pdf.body('Typical user-action flow:\n'
             '  User taps "Add Sale" -> ViewModel.insert(sale) -> '
             'Repository.insert(sale) -> Firestore.collection("sales").add(...) -> '
             'Snapshot listener fires -> LiveData updated -> UI refreshes automatically.')

    pdf.section('3.2  Firebase Integration')
    pdf.subsection('Firebase Authentication')
    pdf.body(
        'Handles sign-up and sign-in with email/password. After sign-in, '
        'the Firebase UID fetches the user profile from Firestore "users". '
        'FirebaseAuthHelper wraps createUserWithEmailAndPassword() and '
        'signInWithEmailAndPassword() behind a simple AuthCallback interface.'
    )
    pdf.subsection('Firebase Cloud Firestore')
    pdf.body(
        'All application data lives in Firestore. Every repository sets up '
        'addSnapshotListener() in its constructor so changes propagate to '
        'the UI in real time. Batch writes (WriteBatch) are used during order '
        'placement to atomically update 4 collections in a single transaction.'
    )

    pdf.section('3.3  Firestore Data Collections')
    for name, desc in [
        ('users',    'Keyed by Firebase UID. Profile + role.'),
        ('products', 'All store products with quantity, price, cost.'),
        ('sales',    'Manual sales recorded by staff.'),
        ('orders',   'Customer orders. Sub-collection "items" holds line items.'),
        ('tasks',    'Staff tasks with assignee, priority, status.'),
        ('seasons',  'Seasonal collections with start/end dates.'),
        ('carts',    'carts/{customerId}/items/{productId} - persistent cart.'),
        ('favorites','favorites/{customerId}/items/{productId} - wish list.'),
        ('support',  'support/{customerId}/messages - chat history.'),
    ]:
        pdf.set_font('DVM', 'B', 9)
        pdf.set_rgb(C_TITLE)
        pdf.cell(34, 6, name, new_x=XPos.RIGHT)
        pdf.set_font('DV', '', 9)
        pdf.set_rgb(C_BLACK)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(1)

    pdf.section('3.4  Role-Based Access Control')
    pdf.body(
        'PermissionManager holds a static Map<String, List<String>> mapping '
        'each permission constant to the roles that hold it. Every UI element '
        'that requires elevated access calls '
        'PermissionManager.currentUserHasPermission() before rendering. '
        'BaseActivity.hideViewIfUnauthorized() wraps this for Activities.'
    )
    col_w = [60, 20, 20, 20, 20, 20]
    pdf.set_font('DV', 'B', 8)
    pdf.set_fill_color(*C_TITLE)
    pdf.set_text_color(*C_WHITE)
    for i, h in enumerate(['Permission', 'OWNER', 'MGR', 'SHIFT', 'EMP', 'CUST']):
        pdf.cell(col_w[i], 7, h, border=1, fill=True)
    pdf.ln()
    pdf.set_text_color(*C_BLACK)
    for row in [
        ('MANAGE_USERS',     'Y','-','-','-','-'),
        ('MANAGE_PRODUCTS',  'Y','-','-','-','-'),
        ('VIEW_PRODUCTS',    'Y','Y','Y','Y','-'),
        ('CREATE_SALE',      'Y','Y','Y','Y','-'),
        ('VIEW_SALES_HISTORY','Y','Y','Y','-','-'),
        ('MANAGE_SEASONS',   'Y','Y','-','-','-'),
        ('CREATE_PRIVATE_TASK','Y','Y','Y','Y','-'),
        ('VIEW_TEAM_TASKS',  'Y','Y','Y','-','-'),
        ('MANAGE_TASKS',     'Y','Y','-','-','-'),
        ('VIEW_ADMIN',       'Y','-','-','-','-'),
    ]:
        pdf.set_font('DVM', '', 8)
        for i, cell in enumerate(row):
            pdf.set_fill_color(*(220,240,220) if cell=='Y' else C_WHITE)
            pdf.cell(col_w[i], 6, cell, border=1, fill=True)
        pdf.ln()
    pdf.ln(2)


def ch4_data_model(pdf):
    pdf.chapter_title('Data Model')
    pdf.body(
        'Each entity is a plain Java object (POJO) with no ORM annotations - '
        'all persistence is handled directly via Firestore. Every entity provides:\n'
        '  - Default no-arg constructor (required by Firestore deserialization).\n'
        '  - toMap() method converting the object to Map<String,Object>.\n'
        '  - Static fromDoc(DocumentSnapshot) factory for reading from Firestore.\n'
        '  - JavaBeans-style getter methods.'
    )

    def ent(num, name, pkg, desc, fields):
        pdf.section(f'4.{num}  {name}')
        pdf.body(f'Package: com.storepilot.{pkg}\n\n{desc}')
        pdf.attr_table_header()
        for row in fields:
            pdf.attr_table_row(*row)
        pdf.ln(3)

    ent(1, 'User', 'db.entities',
        'Represents both staff and customers. The role field determines permissions.',
        [
            ('id',        'int',    'public', 'Local numeric ID (derived from createdAt)'),
            ('uid',       'String', 'public', 'Firebase Auth UID (Firestore document key)'),
            ('fullName',  'String', 'public', 'Display name'),
            ('username',  'String', 'public', 'Unique username'),
            ('email',     'String', 'public', 'Email used for Firebase Auth'),
            ('phone',     'String', 'public', 'Contact phone'),
            ('role',      'String', 'public', 'OWNER | STORE_MANAGER | SHIFT_MANAGER | EMPLOYEE | CUSTOMER'),
            ('createdAt', 'long',   'public', 'Unix timestamp (ms) of account creation'),
        ])

    ent(2, 'Product', 'db.entities',
        'Represents a store product. quantity triggers the low-stock alert when <= 5.',
        [
            ('id',          'int',    'public', 'Local numeric ID'),
            ('firestoreId', 'String', 'public', 'Firestore auto-generated document ID'),
            ('name',        'String', 'public', 'Product name'),
            ('category',    'String', 'public', 'Category (e.g. Shirts, Pants)'),
            ('size',        'String', 'public', 'Size code (S, M, L, XL)'),
            ('color',       'String', 'public', 'Colour description'),
            ('quantity',    'int',    'public', 'Stock level - alert fires when <= 5'),
            ('price',       'double', 'public', 'Selling price per unit (USD)'),
            ('costPrice',   'double', 'public', 'Purchase cost per unit'),
            ('imageUrl',    'String', 'public', 'Optional product image URL'),
            ('createdAt',   'long',   'public', 'Unix timestamp (ms)'),
        ])

    ent(3, 'Order', 'db.entities',
        'Customer order. Status: PENDING -> PROCESSING -> SHIPPED -> DELIVERED.',
        [
            ('id',             'int',    'public', 'Local numeric ID'),
            ('firestoreId',    'String', 'public', 'Firestore document ID'),
            ('customerId',     'int',    'public', 'References User.id of the customer'),
            ('totalPrice',     'double', 'public', 'Total order value'),
            ('status',         'String', 'public', 'PENDING | PROCESSING | SHIPPED | DELIVERED | CANCELLED'),
            ('createdAt',      'long',   'public', 'Unix timestamp (ms)'),
            ('paymentMethod',  'String', 'public', 'CASH_ON_DELIVERY | PAYPAL | CREDIT_CARD'),
            ('shippingAddress','String', 'public', 'Delivery address'),
        ])

    ent(4, 'Sale', 'db.entities',
        'Records a sale transaction. Created by staff or auto-generated on order delivery.',
        [
            ('id',          'int',     'public', 'Local numeric ID'),
            ('firestoreId', 'String',  'public', 'Firestore document ID'),
            ('productId',   'Integer', 'public', 'References Product.id (nullable)'),
            ('quantity',    'int',     'public', 'Units sold'),
            ('totalPrice',  'double',  'public', 'Revenue for this sale'),
            ('saleDate',    'long',    'public', 'Unix timestamp (ms)'),
            ('soldBy',      'Integer', 'public', 'References User.id of staff (nullable)'),
            ('notes',       'String',  'public', 'Optional notes'),
        ])

    ent(5, 'Task', 'db.entities',
        'Work task with Kanban-style status and privacy flag.',
        [
            ('id',          'int',     'public', 'Local numeric ID'),
            ('firestoreId', 'String',  'public', 'Firestore document ID'),
            ('title',       'String',  'public', 'Short task title'),
            ('description', 'String',  'public', 'Detailed description'),
            ('assignedTo',  'Integer', 'public', 'References User.id of assignee'),
            ('createdBy',   'Integer', 'public', 'References User.id of creator'),
            ('status',      'String',  'public', 'TODO | IN_PROGRESS | DONE'),
            ('priority',    'String',  'public', 'LOW | MEDIUM | HIGH'),
            ('isPrivate',   'boolean', 'public', 'Visible only to creator when true'),
            ('dueDate',     'long',    'public', 'Unix timestamp (ms)'),
            ('createdAt',   'long',    'public', 'Unix timestamp (ms)'),
        ])

    ent(6, 'Season', 'db.entities',
        'Seasonal collection period. Dashboard alerts when endDate is within 30 days.',
        [
            ('id',                'int',     'public', 'Local numeric ID'),
            ('firestoreId',       'String',  'public', 'Firestore document ID'),
            ('name',              'String',  'public', 'Season name (e.g. Summer 2025)'),
            ('startDate',         'long',    'public', 'Season start timestamp (ms)'),
            ('endDate',           'long',    'public', 'Season end timestamp (ms)'),
            ('alertDaysBeforeEnd','int',     'public', 'Days before end when alert triggers (default 30)'),
            ('isActive',          'boolean', 'public', 'Whether season is currently active'),
            ('notes',             'String',  'public', 'Optional notes'),
        ])

    ent(7, 'CartItem', 'db.entities',
        'One line in a customer cart. Persisted in Firestore for cross-device persistence.',
        [
            ('id',          'int',    'public', 'Local numeric ID'),
            ('firestoreId', 'String', 'public', 'Firestore document ID'),
            ('customerId',  'int',    'public', 'References User.id of cart owner'),
            ('productId',   'int',    'public', 'References Product.id'),
            ('quantity',    'int',    'public', 'Units in cart'),
        ])

    ent(8, 'SupportMessage', 'db.entities',
        'One chat message. Stored in support/{customerId}/messages sub-collection.',
        [
            ('id',          'int',    'public', 'Local numeric ID'),
            ('firestoreId', 'String', 'public', 'Firestore document ID'),
            ('senderId',    'int',    'public', 'References User.id'),
            ('senderRole',  'String', 'public', 'Role string for chat bubble styling'),
            ('messageText', 'String', 'public', 'Message content'),
            ('imageUrl',    'String', 'public', 'Optional image attachment URL'),
            ('timestamp',   'long',   'public', 'Unix timestamp (ms)'),
            ('customerId',  'int',    'public', 'Conversation owner'),
            ('isRead',      'boolean','public', 'Read status'),
        ])


def ch5_core_modules(pdf):
    pdf.chapter_title('Implementation - Core Modules')

    pdf.section('5.1  StorePilotApp')
    pdf.body('Package: com.storepilot | Extends: android.app.Application\n\n'
             'Application subclass that runs before any Activity. Performs three startup '
             'tasks in onCreate(): initialises Firebase SDK, creates the notification channel, '
             'and schedules the hourly AlarmManager alarm.')
    pdf.subsection('scheduleLowStockAlarm(context) - key logic')
    pdf.code_block(
        'AlarmManager am = (AlarmManager) context.getSystemService(ALARM_SERVICE);\n'
        'Intent intent   = new Intent(context, LowStockReceiver.class);\n'
        'PendingIntent pi = PendingIntent.getBroadcast(\n'
        '    context, 0, intent,\n'
        '    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);\n'
        'am.setInexactRepeating(\n'
        '    AlarmManager.RTC_WAKEUP,\n'
        '    System.currentTimeMillis() + AlarmManager.INTERVAL_HOUR,\n'
        '    AlarmManager.INTERVAL_HOUR, pi);'
    )

    pdf.section('5.2  SessionManager')
    pdf.body('Package: com.storepilot.core | Pattern: Thread-safe Singleton\n\n'
             'Holds the in-memory User object for the duration of the app session. '
             'All permission checks and role-dependent UI logic query this class.')
    pdf.attr_table_header()
    pdf.attr_table_row('instance',      'SessionManager', 'private static', 'Singleton instance (lazy, synchronized)')
    pdf.attr_table_row('loggedInUser',  'User',           'private',        'Currently authenticated user object')
    pdf.ln(3)
    for m, d in [
        ('getInstance()',      'Returns singleton. Synchronized for thread safety.'),
        ('setLoggedInUser(u)', 'Stores user after successful login.'),
        ('getUserRole()',      'Returns role string or null.'),
        ('logout()',           'Clears user; calls FirebaseAuth.signOut().'),
    ]:
        pdf.kv(m, d, key_w=55)
        pdf.ln(1)

    pdf.section('5.3  PermissionManager')
    pdf.body('Package: com.storepilot.core | Pattern: Pure static utility\n\n'
             'Maps permission constants to allowed role lists via a static Map. '
             'Cannot be modified at runtime.')
    for m, d in [
        ('hasPermission(role, perm)',       'Looks up perm in permissionMap; returns true if role is in the list.'),
        ('currentUserHasPermission(perm)',  'Reads role from SessionManager and delegates to hasPermission().'),
    ]:
        pdf.kv(m, d, key_w=65)
        pdf.ln(1)

    pdf.section('5.4  FirestoreManager')
    pdf.body('Package: com.storepilot.core | Pattern: Static helper\n\n'
             'Provides imperative save/delete methods for User, Product, Task, Sale, Order. '
             'Each method builds a Map<String,Object> and calls Firestore set()/delete(). '
             'Used alongside Repositories for compatibility.')

    pdf.section('5.5  LowStockReceiver')
    pdf.body('Package: com.storepilot.core | Extends: BroadcastReceiver\n\n'
             'Triggered by AlarmManager hourly. Queries Firestore for products with '
             'quantity <= 5. If found, fires a notification. The static checkNow(context, testMode) '
             'can be called from the UI for manual testing.')
    pdf.code_block(
        'public static void checkNow(Context context, boolean testMode) {\n'
        '    FirebaseFirestore.getInstance()\n'
        '        .collection("products")\n'
        '        .whereLessThanOrEqualTo("quantity", LOW_STOCK_THRESHOLD)\n'
        '        .get()\n'
        '        .addOnSuccessListener(snapshots -> {\n'
        '            int count = snapshots != null ? snapshots.size() : 0;\n'
        '            if (count > 0)\n'
        '                NotificationHelper.sendLowStockNotification(context, count);\n'
        '            else if (testMode)\n'
        '                NotificationHelper.sendLowStockNotification(context, 1);\n'
        '        });\n'
        '}'
    )

    pdf.section('5.6  NotificationHelper')
    pdf.body('Package: com.storepilot.core\n\n'
             'Creates the HIGH-importance notification channel (API 26+) and posts '
             'the low-stock notification. CHANNEL_ID = "storepilot_low_stock", '
             'NOTIFICATION_ID = 1001 (fixed so repeated alerts update the same notification).')

    pdf.section('5.7  CryptoUtil')
    pdf.body('Package: com.storepilot.auth\n\n'
             'PBKDF2WithHmacSHA256 password hashing. '
             'ITERATIONS=65536, KEY_LENGTH=256 bits, SALT_BYTES=16. '
             'generateSalt() uses SecureRandom. hashPassword() returns Base64-encoded hash. '
             'verifyPassword() performs constant-time comparison.')

    pdf.section('5.8  BaseActivity & FirebaseAuthHelper')
    pdf.body(
        'BaseActivity (com.storepilot.core): extends AppCompatActivity. Adds '
        'checkPermission(perm) and hideViewIfUnauthorized(view, perm). '
        'All staff Activities extend BaseActivity.\n\n'
        'FirebaseAuthHelper (com.storepilot.auth): wraps FirebaseAuth behind '
        'AuthCallback (onSuccess(uid) / onFailure(error)). Provides signUp(), '
        'signIn(), signOut(), and getCurrentUid().'
    )


def ch6_repositories(pdf):
    pdf.chapter_title('Implementation - Repositories')
    pdf.body(
        'Each Repository is constructed with an Application parameter. The constructor '
        'registers a real-time Firestore snapshot listener that feeds a MutableLiveData, '
        'ensuring the ViewModel always has the latest data without polling.'
    )

    def repo(num, name, coll, desc, methods):
        pdf.section(f'6.{num}  {name}')
        pdf.body(f'Firestore collection: {coll}\n\n{desc}')
        for m, d in methods:
            pdf.kv(m, d, key_w=72)
            pdf.ln(1)

    repo(1, 'ProductRepository', '"products"',
         'Snapshot listener ordered by createdAt. getLowStockCountSync() blocks '
         'with CountDownLatch for background-thread use (called from StorePilotApp).',
         [
             ('getAllProducts()',            'LiveData via snapshot listener.'),
             ('getLowStockProducts(thresh)', 'One-shot query: quantity <= threshold.'),
             ('getLowStockCountSync(t)',     'Synchronous version using CountDownLatch.'),
             ('insert / update / delete',   'CRUD via Firestore; update/delete fall back to localId query if firestoreId missing.'),
         ])

    repo(2, 'UserRepository', '"users"',
         'Document ID = Firebase UID for direct reads. Synchronous lookup methods '
         'use CountDownLatch (called on background thread via AppDatabase.dbExecutor).',
         [
             ('getAllUsers()',        'LiveData via snapshot listener.'),
             ('insert / update',     'Writes document by user.uid.'),
             ('findByUid(uid)',       'Synchronous direct document fetch.'),
             ('findByEmail(email)',   'Synchronous whereEqualTo("email").'),
             ('findByUsername(n)',    'Synchronous whereEqualTo("username").'),
             ('getUserCountSync()',   'Synchronous total user count.'),
         ])

    repo(3, 'OrderRepository', '"orders"',
         'placeOrder() uses WriteBatch to atomically create order + items, '
         'decrement product quantities, and clear cart items. '
         'updateOrderStatus() auto-creates a Sale when status = DELIVERED.',
         [
             ('placeOrder(...)',        'Atomic WriteBatch across 4 collections.'),
             ('updateOrderStatus()',    'Updates status; auto-creates Sale on DELIVERED.'),
             ('getActiveOrders()',      'Snapshot listener excluding DELIVERED/CANCELLED.'),
             ('getOrdersByCustomer()', 'Snapshot filtered by customerId.'),
             ('getTodayRevenue()',      'One-shot sum of DELIVERED order totals since startOfDay.'),
             ('getTodayOrderCount()',   'One-shot count of orders since startOfDay.'),
         ])

    repo(4, 'SaleRepository', '"sales"',
         'Snapshot listener ordered by saleDate. All revenue aggregation methods '
         'delegate to the private sumSalesInRange(start, end) helper.',
         [
             ('getAllSales()',            'LiveData via snapshot listener.'),
             ('getTodaySalesTotal(s,e)', 'Sum totalPrice between two timestamps.'),
             ('getSalesTotalByWeek(ref)','Sum of last 7 days.'),
             ('getSalesTotalByMonth()',  'Sum of last 30 days.'),
             ('insert / update / delete','Standard CRUD.'),
         ])

    repo(5, 'TaskRepository', '"tasks"',
         'Snapshot listener ordered by createdAt. getPendingTaskCount() is used '
         'by DashboardFragment to show the user\'s pending task count.',
         [
             ('getTasksByUser(uid)',    'Snapshot listener filtered by assignedTo.'),
             ('getTeamTasks()',         'One-shot: isPrivate == false.'),
             ('getPrivateTasks(uid)',   'One-shot: isPrivate == true AND createdBy == userId.'),
             ('getPendingTaskCount(u)', 'One-shot: status == TODO AND assignedTo == userId.'),
             ('insert / update / delete','Standard CRUD.'),
         ])

    repo(6, 'SeasonRepository', '"seasons"',
         'Snapshot listener ordered by startDate. getSeasonsEndingSoon() queries '
         'endDate between now and now+30 days.',
         [
             ('getAllSeasons()',           'LiveData via snapshot listener.'),
             ('getSeasonsEndingSoon(now)', 'One-shot query for near-end seasons.'),
             ('insert / update / delete', 'Standard CRUD.'),
         ])

    repo(7, 'SupportRepository', '"support"',
         'Messages stored in support/{customerId}/messages sub-collection. '
         'The parent document is created/merged on every sendMessage() '
         'so getConversationCustomerIds() can list active conversations.',
         [
             ('sendMessage()',                 'Creates parent doc (merge) + adds message.'),
             ('getMessagesForCustomer(cid)',   'Snapshot listener on messages sub-collection; sorted by timestamp in Java.'),
             ('getConversationCustomerIds()',  'Snapshot listener on top-level "support" collection.'),
             ('markAllAsRead(cid)',            'Batch-updates isRead=true on unread messages.'),
             ('getUnreadCount(cid)',           'Snapshot listener counting isRead=false messages.'),
         ])


def ch7_viewmodels_ui(pdf):
    pdf.chapter_title('Implementation - ViewModels & UI')

    pdf.section('7.1  AuthViewModel & LoginActivity')
    pdf.body(
        'AuthViewModel (com.storepilot.viewmodels) extends AndroidViewModel. '
        'Exposes loginSuccess (MutableLiveData<Boolean>) and loginError (MutableLiveData<String>). '
        'login() calls Firebase Auth on the main thread, then fetches the user profile '
        'on a background thread via AppDatabase.dbExecutor, posting results via postValue().'
    )
    pdf.code_block(
        'public void login(String email, String password) {\n'
        '    FirebaseAuth.getInstance()\n'
        '        .signInWithEmailAndPassword(email, password)\n'
        '        .addOnSuccessListener(result -> {\n'
        '            String uid = result.getUser().getUid();\n'
        '            AppDatabase.dbExecutor.execute(() -> {\n'
        '                User user = userRepository.findByUid(uid);\n'
        '                if (user == null) {\n'
        '                    loginError.postValue("Account not found.");\n'
        '                    return;\n'
        '                }\n'
        '                SessionManager.getInstance().setLoggedInUser(user);\n'
        '                loginSuccess.postValue(true);\n'
        '            });\n'
        '        })\n'
        '        .addOnFailureListener(e ->\n'
        '            loginError.postValue("Incorrect email or password."));\n'
        '}'
    )
    pdf.body(
        'LoginActivity observes loginSuccess to route to MainActivity (staff) or '
        'CustomerMainActivity (customer). Observes loginError to show a Toast.'
    )

    pdf.section('7.2  ProductViewModel & ProductListFragment')
    pdf.body(
        'ProductViewModel wraps all ProductRepository operations. '
        'ProductListFragment observes getAllProducts() and passes the list to '
        'ProductListAdapter (RecyclerView). The FAB (+) is hidden when the user '
        'lacks MANAGE_PRODUCTS permission. Item taps push ProductDetailsFragment '
        'onto the back stack via FragmentTransaction.'
    )

    pdf.section('7.3  OrderViewModel & CheckoutFragment')
    pdf.body(
        'OrderViewModel exposes orderPlaced (MutableLiveData<Boolean>). '
        'CheckoutFragment caches the cart items and product list from LiveData. '
        'On "Place Order" tap: validates address and cart, maps radio button to '
        'payment method string, calls orderViewModel.placeOrder(). '
        'Observes orderPlaced to navigate to OrderConfirmationFragment.'
    )
    pdf.subsection('Checkout atomic sequence')
    pdf.code_block(
        'User: fills address, selects payment, taps "Place Order"\n'
        '  -> orderViewModel.placeOrder(custId, method, address, cart, products)\n'
        '     -> OrderRepository.placeOrder(..., onSuccess)\n'
        '        -> Firestore.collection("orders").add(order)\n'
        '           -> WriteBatch:\n'
        '               set  orderRef.collection("items")/doc  = OrderItem\n'
        '               update products/{firestoreId}.quantity  -= qty\n'
        '               delete carts/{custId}/items/product_{id}\n'
        '           -> batch.commit()\n'
        '              -> onSuccess.run()\n'
        '                 -> orderPlaced.postValue(true)\n'
        '  -> Fragment: navigate to OrderConfirmationFragment'
    )

    pdf.section('7.4  DashboardFragment')
    pdf.body(
        'The staff home screen. Uses five ViewModels simultaneously in onViewCreated():\n\n'
        '  SeasonViewModel -> getSeasonsEndingSoon(now)  -> season alert banner\n'
        '  SaleViewModel   -> getTodaySalesTotal(s, e)   -> today revenue card\n'
        '  ProductViewModel-> getLowStockProducts(10)    -> low-stock count card\n'
        '  TaskViewModel   -> getPendingTaskCount(userId)-> pending tasks card\n'
        '  OrderViewModel  -> getTodayOrderCount(startOfDay) -> orders today card\n\n'
        'All five observations use getViewLifecycleOwner() for automatic cleanup.'
    )


def ch8_screen_flow(pdf):
    pdf.chapter_title('Screen Flow & Navigation')

    pdf.section('8.1  Staff Navigation')
    pdf.code_block(
        'App Launch -> WelcomeActivity\n'
        '  +-- [Login]    -> LoginActivity\n'
        '  |                 +-- [staff role] -> MainActivity\n'
        '  |                       Bottom Nav: Dashboard | Products | Sales | Tasks | Seasons\n'
        '  |                       Overflow:   Orders | Support | Admin* | [TEST] Notification | Logout\n'
        '  |                       * OWNER only\n'
        '  +-- [Register] -> RoleSelectionActivity -> RegisterActivity\n'
        '                        (first owner only)    -> SetupActivity'
    )

    pdf.section('8.2  Customer Navigation')
    pdf.code_block(
        'LoginActivity -> [CUSTOMER] -> CustomerMainActivity\n'
        '  Bottom Nav: Home | Cart | Favorites | Orders | Chat\n'
        '    Home      -> CustomerHomeFragment -> ProductDetailFragment\n'
        '    Cart      -> CartFragment -> CheckoutFragment -> OrderConfirmationFragment\n'
        '    Favorites -> FavoritesFragment -> ProductDetailFragment\n'
        '    Orders    -> OrderHistoryFragment\n'
        '    Chat      -> SupportChatFragment'
    )

    pdf.section('8.3  Registration & Authentication Flow')
    pdf.code_block(
        'RegisterActivity.attemptRegister():\n'
        '  1. Validate form (fullName, username, email, phone, password, confirm)\n'
        '  2. Map role name to constant (Customer->CUSTOMER, Manager->STORE_MANAGER, etc.)\n'
        '  3. FirebaseAuthHelper.signUp(email, password, username)\n'
        '     -> Firebase Auth: createUserWithEmailAndPassword()\n'
        '        -> updateProfile(displayName=username)\n'
        '           -> callback.onSuccess(uid)\n'
        '  4. Create User POJO with uid from Firebase\n'
        '  5. UserRepository.insert(user) -> Firestore "users/{uid}"\n'
        '  6. Navigate to LoginActivity'
    )


def ch9_testing(pdf):
    pdf.chapter_title('Testing')

    pdf.section('9.1  Manual Testing Approach')
    pdf.body(
        'Tested on Android emulator (Pixel 6, API 34) and a physical Android 11 device. '
        'Each user role tested independently to verify role-based access.'
    )

    pdf.section('9.2  Test Cases')
    for code, name, steps, result in [
        ('TC-01', 'Registration',
         'Register with each role. Verify Firestore document created with correct role.',
         'PASS - All roles created correctly in Firestore "users" collection.'),
        ('TC-02', 'Login routing',
         'Login as staff -> MainActivity. Login as Customer -> CustomerMainActivity.',
         'PASS - Role-based routing works correctly.'),
        ('TC-03', 'Permission - Add Product',
         'Login as Employee. Navigate Products tab. Verify FAB is hidden.',
         'PASS - FAB hidden for roles without MANAGE_PRODUCTS.'),
        ('TC-04', 'Permission - Admin screen',
         'Login as Store Manager. Open overflow menu. Verify "Admin" is not visible.',
         'PASS - Admin hidden for non-OWNER roles.'),
        ('TC-05', 'Low-stock notification',
         'Reduce product quantity to 3 in Firestore. Tap [TEST] Notification from menu.',
         'PASS - Notification appears in status bar within 2 seconds.'),
        ('TC-06', 'Place Order',
         'Login as Customer. Add 2 items to cart. Complete checkout.',
         'PASS - Order in Firestore "orders". Cart cleared. Manager sees order.'),
        ('TC-07', 'Order status update',
         'Login as Manager. Update order PENDING -> DELIVERED.',
         'PASS - Status updates in real time. Sale record auto-created in "sales".'),
        ('TC-08', 'Season alert',
         'Create season with endDate = today + 10 days.',
         'PASS - Yellow banner appears on Dashboard.'),
        ('TC-09', 'Support chat',
         'Customer sends message. Manager logs in and replies.',
         'PASS - Messages appear in real time on both sides.'),
        ('TC-10', 'Real-time sync',
         'Open app on 2 devices. Add product on device 1.',
         'PASS - Product appears on device 2 within 1 second.'),
    ]:
        pdf.set_font('DV', 'B', 10)
        pdf.set_rgb(C_TITLE)
        pdf.cell(0, 7, f'{code}: {name}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('DV', '', 9)
        pdf.set_rgb(C_BLACK)
        pdf.kv('Steps',  steps)
        pdf.kv('Result', result)
        pdf.ln(3)

    pdf.section('9.3  Known Limitations')
    for lim in [
        'Image upload is URL-based; no Firebase Storage integration.',
        'Payment methods are labels only; no real payment gateway is integrated.',
        'Reports and Marketing modules were removed during development.',
        'Push notifications are Android-only; no email notification support.',
    ]:
        pdf.bullet(lim)


def appendix_source_code(pdf):
    pdf.chapter_title('Appendix: Full Source Code Listings')
    pdf.body(
        'Complete source code for 13 key classes with Javadoc documentation headers. '
        'Code is printed verbatim from the final version of the project.'
    )

    classes = [
        ('A.1  StorePilotApp.java',
"""/**
 * StorePilotApp.java - Package: com.storepilot
 * Application subclass. Runs before any Activity.
 * 1. Initialize Firebase SDK.
 * 2. Create low-stock notification channel (required on API 26+).
 * 3. Schedule hourly AlarmManager alarm for LowStockReceiver.
 */
package com.storepilot;
import android.app.AlarmManager; import android.app.Application;
import android.app.PendingIntent; import android.content.Context;
import android.content.Intent;
import com.google.firebase.FirebaseApp;
import com.storepilot.core.LowStockReceiver;
import com.storepilot.core.NotificationHelper;

public class StorePilotApp extends Application {
    @Override public void onCreate() {
        super.onCreate();
        FirebaseApp.initializeApp(this);
        NotificationHelper.createNotificationChannel(this);
        scheduleLowStockAlarm(this);
    }
    /** Schedules inexact repeating alarm every 1 hour. FLAG_UPDATE_CURRENT is idempotent. */
    public static void scheduleLowStockAlarm(Context context) {
        AlarmManager am = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        Intent intent = new Intent(context, LowStockReceiver.class);
        PendingIntent pi = PendingIntent.getBroadcast(context, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        am.setInexactRepeating(AlarmManager.RTC_WAKEUP,
            System.currentTimeMillis() + AlarmManager.INTERVAL_HOUR,
            AlarmManager.INTERVAL_HOUR, pi);
    }
}"""),

        ('A.2  SessionManager.java',
"""/**
 * SessionManager.java - Package: com.storepilot.core
 * Thread-safe singleton holding the in-memory session.
 * Cleared on logout via logout().
 */
package com.storepilot.core;
import com.google.firebase.auth.FirebaseAuth;
import com.storepilot.db.entities.User;

public class SessionManager {
    private static SessionManager instance;
    private User loggedInUser;
    private SessionManager() {}
    /** Returns the singleton. Synchronized for thread safety. */
    public static synchronized SessionManager getInstance() {
        if (instance == null) instance = new SessionManager();
        return instance;
    }
    public void setLoggedInUser(User user) { this.loggedInUser = user; }
    public User   getLoggedInUser()        { return loggedInUser; }
    public boolean isLoggedIn()            { return loggedInUser != null; }
    public String getUserRole() {
        return loggedInUser != null ? loggedInUser.getRole() : null;
    }
    /** Clears local session and signs out of Firebase Authentication. */
    public void logout() {
        loggedInUser = null;
        FirebaseAuth.getInstance().signOut();
    }
}"""),

        ('A.3  PermissionManager.java',
"""/**
 * PermissionManager.java - Package: com.storepilot.core
 * Pure-static class mapping permission constants to allowed roles.
 * Static initializer populates an immutable map at class load time.
 */
package com.storepilot.core;
import java.util.*; import java.util.Map;

public class PermissionManager {
    public static final String MANAGE_USERS     = "MANAGE_USERS";
    public static final String MANAGE_PRODUCTS  = "MANAGE_PRODUCTS";
    public static final String VIEW_PRODUCTS    = "VIEW_PRODUCTS";
    public static final String CREATE_SALE      = "CREATE_SALE";
    public static final String VIEW_SALES_HISTORY="VIEW_SALES_HISTORY";
    public static final String MANAGE_SEASONS   = "MANAGE_SEASONS";
    public static final String CREATE_PRIVATE_TASK="CREATE_PRIVATE_TASK";
    public static final String VIEW_TEAM_TASKS  = "VIEW_TEAM_TASKS";
    public static final String MANAGE_TASKS     = "MANAGE_TASKS";
    public static final String VIEW_ADMIN       = "VIEW_ADMIN";
    public static final String OWNER="OWNER", STORE_MANAGER="STORE_MANAGER";
    public static final String SHIFT_MANAGER="SHIFT_MANAGER", EMPLOYEE="EMPLOYEE";

    private static final Map<String,List<String>> permissionMap=new HashMap<>();
    static {
        permissionMap.put(MANAGE_USERS,  Arrays.asList(OWNER));
        permissionMap.put(MANAGE_PRODUCTS,Arrays.asList(OWNER));
        permissionMap.put(VIEW_PRODUCTS,
            Arrays.asList(OWNER,STORE_MANAGER,SHIFT_MANAGER,EMPLOYEE));
        permissionMap.put(CREATE_SALE,
            Arrays.asList(OWNER,STORE_MANAGER,SHIFT_MANAGER,EMPLOYEE));
        permissionMap.put(VIEW_SALES_HISTORY,
            Arrays.asList(OWNER,STORE_MANAGER,SHIFT_MANAGER));
        permissionMap.put(MANAGE_SEASONS,Arrays.asList(OWNER,STORE_MANAGER));
        permissionMap.put(CREATE_PRIVATE_TASK,
            Arrays.asList(OWNER,STORE_MANAGER,SHIFT_MANAGER,EMPLOYEE));
        permissionMap.put(VIEW_TEAM_TASKS,
            Arrays.asList(OWNER,STORE_MANAGER,SHIFT_MANAGER));
        permissionMap.put(MANAGE_TASKS, Arrays.asList(OWNER,STORE_MANAGER));
        permissionMap.put(VIEW_ADMIN,   Arrays.asList(OWNER));
    }
    public static boolean hasPermission(String role, String permission) {
        List<String> allowed = permissionMap.get(permission);
        return allowed != null && allowed.contains(role);
    }
    public static boolean currentUserHasPermission(String permission) {
        String role = SessionManager.getInstance().getUserRole();
        return role != null && hasPermission(role, permission);
    }
}"""),

        ('A.4  LowStockReceiver.java',
"""/**
 * LowStockReceiver.java - Package: com.storepilot.core
 * BroadcastReceiver triggered by AlarmManager every hour.
 * Queries Firestore for products with quantity <= LOW_STOCK_THRESHOLD.
 * checkNow(context, testMode) allows manual testing from the UI.
 */
package com.storepilot.core;
import android.content.BroadcastReceiver; import android.content.Context;
import android.content.Intent; import android.widget.Toast;
import com.google.firebase.firestore.FirebaseFirestore;

public class LowStockReceiver extends BroadcastReceiver {
    /** Products at or below this quantity trigger a notification. */
    public static final int LOW_STOCK_THRESHOLD = 5;

    @Override public void onReceive(Context context, Intent intent) {
        checkNow(context, false);
    }

    /**
     * Queries Firestore and fires a low-stock notification.
     * @param testMode If true, sends a demo notification even when no
     *                 real low-stock products exist, and shows a Toast.
     */
    public static void checkNow(Context context, boolean testMode) {
        FirebaseFirestore.getInstance()
            .collection("products")
            .whereLessThanOrEqualTo("quantity", LOW_STOCK_THRESHOLD)
            .get()
            .addOnSuccessListener(snapshots -> {
                int count = snapshots != null ? snapshots.size() : 0;
                if (count > 0) {
                    NotificationHelper.sendLowStockNotification(context, count);
                } else if (testMode) {
                    NotificationHelper.sendLowStockNotification(context, 1);
                    Toast.makeText(context,
                        "No real low-stock items - demo notification sent",
                        Toast.LENGTH_LONG).show();
                }
            })
            .addOnFailureListener(e -> {
                if (testMode) Toast.makeText(context,
                    "Firestore error: " + e.getMessage(),
                    Toast.LENGTH_LONG).show();
            });
    }
}"""),

        ('A.5  NotificationHelper.java',
"""/**
 * NotificationHelper.java - Package: com.storepilot.core
 * Creates the notification channel and posts low-stock notifications.
 * Channel is created once in StorePilotApp.onCreate().
 */
package com.storepilot.core;
import android.app.NotificationChannel; import android.app.NotificationManager;
import android.content.Context; import android.os.Build;
import androidx.core.app.NotificationCompat; import com.storepilot.R;

public class NotificationHelper {
    public static final String CHANNEL_ID = "storepilot_low_stock";
    private static final int NOTIFICATION_ID = 1001;

    /**
     * Creates a HIGH-importance notification channel.
     * Idempotent - safe to call multiple times. No-op below API 26.
     */
    public static void createNotificationChannel(Context context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID, "Low Stock Alerts",
                NotificationManager.IMPORTANCE_HIGH);
            channel.setDescription("Alerts when products are running low");
            channel.enableVibration(true);
            NotificationManager mgr =
                context.getSystemService(NotificationManager.class);
            if (mgr != null) mgr.createNotificationChannel(channel);
        }
    }

    /**
     * Posts a low-stock notification.
     * @param count Number of products at or below the threshold.
     */
    public static void sendLowStockNotification(Context context, int count) {
        String text = count + " product(s) are running low. Tap to review.";
        NotificationCompat.Builder builder =
            new NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle("Low Stock Alert")
                .setContentText(text)
                .setStyle(new NotificationCompat.BigTextStyle().bigText(text))
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true);
        NotificationManager mgr = (NotificationManager)
            context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (mgr != null) mgr.notify(NOTIFICATION_ID, builder.build());
    }
}"""),

        ('A.6  CryptoUtil.java',
"""/**
 * CryptoUtil.java - Package: com.storepilot.auth
 * PBKDF2WithHmacSHA256 password hashing utility.
 * NIST-recommended parameters: 65536 iterations, 256-bit key, 16-byte salt.
 */
package com.storepilot.auth;
import android.util.Base64;
import java.security.*; import java.security.spec.InvalidKeySpecException;
import javax.crypto.SecretKeyFactory; import javax.crypto.spec.PBEKeySpec;

public class CryptoUtil {
    private static final int ITERATIONS = 65536;
    private static final int KEY_LENGTH = 256;
    private static final String ALGORITHM = "PBKDF2WithHmacSHA256";
    private static final int SALT_BYTES = 16;

    /** Generates a cryptographically secure 16-byte random salt (Base64). */
    public static String generateSalt() {
        byte[] salt = new byte[SALT_BYTES];
        new SecureRandom().nextBytes(salt);
        return Base64.encodeToString(salt, Base64.NO_WRAP);
    }

    /** Returns Base64-encoded PBKDF2 hash of password+salt. */
    public static String hashPassword(String password, String salt) {
        try {
            byte[] saltBytes = Base64.decode(salt, Base64.NO_WRAP);
            PBEKeySpec spec = new PBEKeySpec(
                password.toCharArray(), saltBytes, ITERATIONS, KEY_LENGTH);
            SecretKeyFactory factory = SecretKeyFactory.getInstance(ALGORITHM);
            byte[] hash = factory.generateSecret(spec).getEncoded();
            spec.clearPassword();
            return Base64.encodeToString(hash, Base64.NO_WRAP);
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new RuntimeException("Error hashing password", e);
        }
    }

    /** Verifies password by hashing and comparing with the expected hash. */
    public static boolean verifyPassword(
            String password, String salt, String expectedHash) {
        return hashPassword(password, salt).equals(expectedHash);
    }
}"""),

        ('A.7  User.java',
"""/**
 * User.java - Package: com.storepilot.db.entities
 * Data model for all users (staff + customers).
 * Stored in Firestore collection "users", keyed by Firebase UID.
 */
package com.storepilot.db.entities;
import com.google.firebase.firestore.DocumentSnapshot;
import java.util.HashMap; import java.util.Map;

public class User {
    public int id; public String uid, fullName, username, email, phone, role;
    public long createdAt;
    public User() {}
    public User(String fullName, String username, String email, String phone,
                String role, long createdAt) {
        this.fullName=fullName; this.username=username; this.email=email;
        this.phone=phone; this.role=role; this.createdAt=createdAt;
        this.id=(int)(createdAt & 0x7FFFFFFF);
    }
    public Map<String,Object> toMap() {
        Map<String,Object> m=new HashMap<>();
        m.put("localId",id); m.put("uid",uid!=null?uid:"");
        m.put("fullName",fullName!=null?fullName:"");
        m.put("username",username!=null?username:"");
        m.put("email",email!=null?email:"");
        m.put("phone",phone!=null?phone:"");
        m.put("role",role!=null?role:"CUSTOMER");
        m.put("createdAt",createdAt); return m;
    }
    /** Deserializes a Firestore DocumentSnapshot into a User. */
    public static User fromDoc(DocumentSnapshot doc) {
        if (doc==null||!doc.exists()) return null;
        User u=new User(); u.uid=doc.getId();
        u.id=doc.getLong("localId")!=null
            ?doc.getLong("localId").intValue()
            :Math.abs(doc.getId().hashCode());
        u.fullName=doc.getString("fullName");
        u.username=doc.getString("username");
        u.email=doc.getString("email"); u.phone=doc.getString("phone");
        u.role=doc.getString("role");
        u.createdAt=doc.getLong("createdAt")!=null?doc.getLong("createdAt"):0;
        return u;
    }
    public int getId(){return id;} public String getUid(){return uid;}
    public String getFullName(){return fullName!=null?fullName:username;}
    public String getUsername(){return username;}
    public String getEmail(){return email;} public String getPhone(){return phone;}
    public String getRole(){return role;} public long getCreatedAt(){return createdAt;}
}"""),

        ('A.8  Product.java',
"""/**
 * Product.java - Package: com.storepilot.db.entities
 * Store product. "quantity" triggers low-stock alert when <= 5.
 * "firestoreId" enables efficient direct Firestore updates.
 */
package com.storepilot.db.entities;
import com.google.firebase.firestore.DocumentSnapshot;
import java.util.HashMap; import java.util.Map;

public class Product {
    public int id; public String firestoreId, name, category, size, color, imageUrl;
    public int quantity; public double price, costPrice; public long createdAt;
    public Product() {}
    public Product(String name,String category,String size,String color,
                   int quantity,double price,double costPrice,
                   String imageUrl,long createdAt) {
        this.name=name; this.category=category; this.size=size;
        this.color=color; this.quantity=quantity; this.price=price;
        this.costPrice=costPrice; this.imageUrl=imageUrl;
        this.createdAt=createdAt; this.id=(int)(createdAt&0x7FFFFFFF);
    }
    public Map<String,Object> toMap() {
        Map<String,Object> m=new HashMap<>();
        m.put("localId",id); m.put("name",name!=null?name:"");
        m.put("category",category!=null?category:"");
        m.put("size",size!=null?size:""); m.put("color",color!=null?color:"");
        m.put("quantity",quantity); m.put("price",price);
        m.put("costPrice",costPrice); m.put("imageUrl",imageUrl!=null?imageUrl:"");
        m.put("createdAt",createdAt); return m;
    }
    public static Product fromDoc(DocumentSnapshot doc) {
        if (doc==null||!doc.exists()) return null;
        Product p=new Product(); p.firestoreId=doc.getId();
        p.id=doc.getLong("localId")!=null?doc.getLong("localId").intValue()
            :Math.abs(doc.getId().hashCode());
        p.name=doc.getString("name"); p.category=doc.getString("category");
        p.size=doc.getString("size"); p.color=doc.getString("color");
        p.quantity=doc.getLong("quantity")!=null?doc.getLong("quantity").intValue():0;
        p.price=doc.getDouble("price")!=null?doc.getDouble("price"):0;
        p.costPrice=doc.getDouble("costPrice")!=null?doc.getDouble("costPrice"):0;
        p.imageUrl=doc.getString("imageUrl");
        p.createdAt=doc.getLong("createdAt")!=null?doc.getLong("createdAt"):0;
        return p;
    }
    public int getId(){return id;} public String getName(){return name;}
    public String getCategory(){return category;} public String getSize(){return size;}
    public String getColor(){return color;} public int getQuantity(){return quantity;}
    public double getPrice(){return price;} public double getCostPrice(){return costPrice;}
    public String getImageUrl(){return imageUrl;} public long getCreatedAt(){return createdAt;}
}"""),

        ('A.9  ProductRepository.java',
"""/**
 * ProductRepository.java - Package: com.storepilot.repositories
 * Single source of truth for product data.
 * Constructor registers a real-time snapshot listener.
 * Synchronous methods block with CountDownLatch for background-thread use.
 */
package com.storepilot.repositories;
import android.app.Application;
import androidx.lifecycle.LiveData; import androidx.lifecycle.MutableLiveData;
import com.google.firebase.firestore.*;
import com.storepilot.db.entities.Product;
import java.util.*; import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicReference;

public class ProductRepository {
    private final FirebaseFirestore db = FirebaseFirestore.getInstance();
    private final MutableLiveData<List<Product>> productsLiveData =
        new MutableLiveData<>();

    public ProductRepository(Application application) {
        db.collection("products").orderBy("createdAt")
            .addSnapshotListener((snaps, e) -> {
                if (snaps == null) return;
                List<Product> list = new ArrayList<>();
                for (DocumentSnapshot doc : snaps.getDocuments()) {
                    Product p = Product.fromDoc(doc);
                    if (p != null) list.add(p);
                }
                productsLiveData.postValue(list);
            });
    }

    public LiveData<List<Product>> getAllProducts() { return productsLiveData; }

    /** One-shot query for products at or below threshold. */
    public LiveData<List<Product>> getLowStockProducts(int threshold) {
        MutableLiveData<List<Product>> result = new MutableLiveData<>();
        db.collection("products")
            .whereLessThanOrEqualTo("quantity", threshold).get()
            .addOnSuccessListener(snaps -> {
                List<Product> list = new ArrayList<>();
                for (DocumentSnapshot doc : snaps.getDocuments()) {
                    Product p = Product.fromDoc(doc);
                    if (p != null) list.add(p);
                }
                result.postValue(list);
            });
        return result;
    }

    /** Synchronous low-stock count. Blocks current thread - use on background thread only. */
    public int getLowStockCountSync(int threshold) {
        CountDownLatch latch = new CountDownLatch(1);
        AtomicReference<Integer> count = new AtomicReference<>(0);
        db.collection("products")
            .whereLessThanOrEqualTo("quantity", threshold).get()
            .addOnCompleteListener(task -> {
                if (task.isSuccessful()) count.set(task.getResult().size());
                latch.countDown();
            });
        try { latch.await(10, TimeUnit.SECONDS); }
        catch (InterruptedException ignored) {}
        return count.get();
    }

    public void insert(Product product) {
        db.collection("products").add(product.toMap())
            .addOnSuccessListener(ref -> product.firestoreId = ref.getId());
    }
    public void update(Product product) {
        if (product.firestoreId != null && !product.firestoreId.isEmpty())
            db.collection("products").document(product.firestoreId).set(product.toMap());
    }
    public void delete(Product product) {
        if (product.firestoreId != null && !product.firestoreId.isEmpty())
            db.collection("products").document(product.firestoreId).delete();
    }
}"""),

        ('A.10  OrderRepository.java',
"""/**
 * OrderRepository.java - Package: com.storepilot.repositories
 * Handles order placement and lifecycle.
 * placeOrder() uses WriteBatch for atomic multi-collection write.
 * updateOrderStatus() auto-creates Sale on DELIVERED.
 */
package com.storepilot.repositories;
import android.app.Application;
import androidx.lifecycle.LiveData; import androidx.lifecycle.MutableLiveData;
import com.google.firebase.firestore.*;
import com.storepilot.db.entities.*;
import java.util.*;

public class OrderRepository {
    private final FirebaseFirestore db = FirebaseFirestore.getInstance();
    public OrderRepository(Application application) {}

    /** Atomically places an order, creates items, decrements stock, clears cart. */
    public void placeOrder(int customerId, String paymentMethod,
                           String shippingAddress, List<CartItem> cartItems,
                           List<Product> products, Runnable onSuccess) {
        double total = 0;
        for (CartItem ci : cartItems)
            for (Product p : products)
                if (p.getId() == ci.getProductId()) {
                    total += p.getPrice() * ci.getQuantity(); break; }

        Order order = new Order(customerId, total, "PENDING",
            System.currentTimeMillis(), paymentMethod, shippingAddress);

        db.collection("orders").add(order.toMap())
            .addOnSuccessListener(orderRef -> {
                WriteBatch batch = db.batch();
                for (CartItem ci : cartItems)
                    for (Product p : products)
                        if (p.getId() == ci.getProductId()) {
                            OrderItem item = new OrderItem(
                                Math.abs(orderRef.getId().hashCode()),
                                p.getId(), ci.getQuantity(), p.getPrice());
                            batch.set(orderRef.collection("items").document(),
                                item.toMap());
                            int newQty=Math.max(0,p.getQuantity()-ci.getQuantity());
                            if (p.firestoreId != null)
                                batch.update(db.collection("products")
                                    .document(p.firestoreId),"quantity",newQty);
                            batch.delete(db.collection(
                                "carts/"+customerId+"/items")
                                .document("product_"+p.getId()));
                            break;
                        }
                batch.commit().addOnSuccessListener(v -> {
                    if (onSuccess != null) onSuccess.run();
                });
            });
    }

    /** Updates status. Auto-creates Sale record when status becomes DELIVERED. */
    public void updateOrderStatus(Order order, String newStatus) {
        if (order.firestoreId == null) return;
        db.collection("orders").document(order.firestoreId)
            .update("status", newStatus);
        if ("DELIVERED".equals(newStatus)) {
            Sale sale = new Sale(null, 1, order.getTotalPrice(),
                System.currentTimeMillis(), null,
                "Order #" + order.getId() + " delivered");
            db.collection("sales").add(sale.toMap());
        }
    }

    /** Returns active orders (excludes DELIVERED and CANCELLED). */
    public LiveData<List<Order>> getActiveOrders() {
        MutableLiveData<List<Order>> liveData = new MutableLiveData<>();
        db.collection("orders").addSnapshotListener((snaps, e) -> {
            List<Order> list = new ArrayList<>();
            if (snaps != null)
                for (DocumentSnapshot doc : snaps.getDocuments()) {
                    Order o = Order.fromDoc(doc);
                    if (o != null && !"DELIVERED".equals(o.status)
                        && !"CANCELLED".equals(o.status)) list.add(o);
                }
            liveData.postValue(list);
        });
        return liveData;
    }
}"""),

        ('A.11  AuthViewModel.java',
"""/**
 * AuthViewModel.java - Package: com.storepilot.viewmodels
 * Handles login logic. Uses Firebase Auth then fetches Firestore profile
 * on a background thread via AppDatabase.dbExecutor.
 */
package com.storepilot.viewmodels;
import android.app.Application;
import androidx.annotation.NonNull; import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.MutableLiveData;
import com.google.firebase.auth.FirebaseAuth;
import com.storepilot.core.AppDatabase; import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.User; import com.storepilot.repositories.UserRepository;

public class AuthViewModel extends AndroidViewModel {
    private final UserRepository userRepository;
    public final MutableLiveData<String>  loginError  = new MutableLiveData<>();
    public final MutableLiveData<Boolean> loginSuccess = new MutableLiveData<>();

    public AuthViewModel(@NonNull Application application) {
        super(application);
        userRepository = new UserRepository(application);
    }

    public void login(String email, String password) {
        FirebaseAuth.getInstance().signInWithEmailAndPassword(email.trim(), password)
            .addOnSuccessListener(result -> {
                String uid = result.getUser().getUid();
                AppDatabase.dbExecutor.execute(() -> {
                    User user = userRepository.findByUid(uid);
                    if (user == null) {
                        loginError.postValue("Account not found. Please register.");
                        return;
                    }
                    SessionManager.getInstance().setLoggedInUser(user);
                    loginSuccess.postValue(true);
                });
            })
            .addOnFailureListener(e ->
                loginError.postValue("Incorrect email or password."));
    }
}"""),

        ('A.12  LoginActivity.java',
"""/**
 * LoginActivity.java - Package: com.storepilot.auth
 * Handles user login. Observes AuthViewModel for success/failure.
 * Routes to MainActivity (staff) or CustomerMainActivity (customer).
 */
package com.storepilot.auth;
import android.content.Intent; import android.os.Bundle;
import android.widget.Button; import android.widget.Toast;
import androidx.lifecycle.ViewModelProvider;
import com.google.android.material.textfield.TextInputEditText;
import com.storepilot.MainActivity; import com.storepilot.R;
import com.storepilot.core.BaseActivity; import com.storepilot.core.SessionManager;
import com.storepilot.customer.CustomerMainActivity;
import com.storepilot.viewmodels.AuthViewModel;

public class LoginActivity extends BaseActivity {
    private TextInputEditText etEmail, etPassword;
    private Button btnLogin;
    private AuthViewModel authViewModel;

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        etEmail    = findViewById(R.id.etUsername);
        etPassword = findViewById(R.id.etPassword);
        btnLogin   = findViewById(R.id.btnLogin);
        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        authViewModel.loginSuccess.observe(this, success -> {
            if (Boolean.TRUE.equals(success)) {
                String role = SessionManager.getInstance().getUserRole();
                Intent intent = "CUSTOMER".equals(role)
                    ? new Intent(this, CustomerMainActivity.class)
                    : new Intent(this, MainActivity.class);
                startActivity(intent); finish();
            }
        });
        authViewModel.loginError.observe(this, error -> {
            if (error != null)
                Toast.makeText(this, error, Toast.LENGTH_SHORT).show();
        });
        btnLogin.setOnClickListener(v -> {
            String email    = etEmail.getText() != null
                ? etEmail.getText().toString().trim() : "";
            String password = etPassword.getText() != null
                ? etPassword.getText().toString() : "";
            if (email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this,
                    getString(R.string.error_fill_all_fields),
                    Toast.LENGTH_SHORT).show();
                return;
            }
            authViewModel.login(email, password);
        });
    }
}"""),

        ('A.13  DashboardFragment.java',
"""/**
 * DashboardFragment.java - Package: com.storepilot.dashboard
 * Staff home screen showing 5 real-time KPI cards via 5 ViewModels.
 * All LiveData observations use getViewLifecycleOwner() for auto-cleanup.
 */
package com.storepilot.dashboard;
import android.os.Bundle; import android.view.*;
import android.widget.TextView;
import androidx.annotation.*; import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import com.storepilot.R; import com.storepilot.core.SessionManager;
import com.storepilot.viewmodels.*;
import java.text.NumberFormat; import java.util.*;

public class DashboardFragment extends Fragment {
    private TextView tvSeasonAlert, tvTodaySales,
                     tvLowStockCount, tvPendingTasks, tvTodayOrders;
    private View cardSeasonAlert;

    @Nullable @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view,
                              @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        cardSeasonAlert = view.findViewById(R.id.cardSeasonAlert);
        tvSeasonAlert   = view.findViewById(R.id.tvSeasonAlert);
        tvTodaySales    = view.findViewById(R.id.tvTodaySales);
        tvLowStockCount = view.findViewById(R.id.tvLowStockCount);
        tvPendingTasks  = view.findViewById(R.id.tvPendingTasks);
        tvTodayOrders   = view.findViewById(R.id.tvTodayOrders);

        long now = System.currentTimeMillis();
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY,0); cal.set(Calendar.MINUTE,0);
        cal.set(Calendar.SECOND,0); cal.set(Calendar.MILLISECOND,0);
        long startOfDay = cal.getTimeInMillis();
        long endOfDay   = startOfDay + 86400000L;
        int userId = SessionManager.getInstance().getLoggedInUser() != null
            ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

        new ViewModelProvider(this).get(SeasonViewModel.class)
            .getSeasonsEndingSoon(now)
            .observe(getViewLifecycleOwner(), seasons -> {
                if (seasons != null && !seasons.isEmpty()) {
                    cardSeasonAlert.setVisibility(View.VISIBLE);
                    tvSeasonAlert.setText(getString(
                        R.string.season_ending_soon, seasons.get(0).getName()));
                } else cardSeasonAlert.setVisibility(View.GONE);
            });

        new ViewModelProvider(this).get(SaleViewModel.class)
            .getTodaySalesTotal(startOfDay, endOfDay)
            .observe(getViewLifecycleOwner(), total ->
                tvTodaySales.setText(NumberFormat.getCurrencyInstance(
                    Locale.US).format(total != null ? total : 0.0)));

        new ViewModelProvider(this).get(ProductViewModel.class)
            .getLowStockProducts(10)
            .observe(getViewLifecycleOwner(), products ->
                tvLowStockCount.setText(String.valueOf(
                    products != null ? products.size() : 0)));

        new ViewModelProvider(this).get(TaskViewModel.class)
            .getPendingTaskCount(userId)
            .observe(getViewLifecycleOwner(), count ->
                tvPendingTasks.setText(String.valueOf(count != null ? count : 0)));

        new ViewModelProvider(this).get(OrderViewModel.class)
            .getTodayOrderCount(startOfDay)
            .observe(getViewLifecycleOwner(), count -> {
                if (tvTodayOrders != null)
                    tvTodayOrders.setText(
                        String.valueOf(count != null ? count : 0));
            });
    }
}"""),
    ]

    for title, code in classes:
        pdf.section(title)
        pdf.code_block(code, small=True)


def main():
    pdf = BookPDF()
    make_cover(pdf)
    make_toc(pdf)
    ch1_introduction(pdf)
    ch2_requirements(pdf)
    ch3_architecture(pdf)
    ch4_data_model(pdf)
    ch5_core_modules(pdf)
    ch6_repositories(pdf)
    ch7_viewmodels_ui(pdf)
    ch8_screen_flow(pdf)
    ch9_testing(pdf)
    appendix_source_code(pdf)
    pdf.output(OUT_PATH)
    print(f"PDF written to: {OUT_PATH}")
    size_kb = os.path.getsize(OUT_PATH) // 1024
    print(f"File size: {size_kb} KB  |  Pages: {pdf.page}")


if __name__ == '__main__':
    main()
