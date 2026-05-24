#!/usr/bin/env python3
"""
StorePilot Project Book Generator
Generates a comprehensive PDF documentation book modelled on the FaceCare format.
"""

import os
from reportlab.lib.pagesizes import A4, landscape as rl_landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable, Image,
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display

pdfmetrics.registerFont(TTFont('DejaVuSans',      '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# ── Colour palette ─────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#0D1B2A')
MID_BLUE    = colors.HexColor('#1B3A5C')
ACCENT_BLUE = colors.HexColor('#2E86AB')
LIGHT_BLUE  = colors.HexColor('#EAF4FB')
ACCENT_GOLD = colors.HexColor('#F4A261')
LIGHT_GREY  = colors.HexColor('#F5F5F5')
CODE_BG     = colors.HexColor('#F0F0F0')
CODE_BORDER = colors.HexColor('#CCCCCC')
WHITE       = colors.white
BLACK       = colors.black
DARK_GREY   = colors.HexColor('#333333')
MID_GREY    = colors.HexColor('#666666')

PAGE_W, PAGE_H = A4
SOURCE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'app', 'src', 'main', 'java', 'com', 'storepilot')


# ── File helpers ───────────────────────────────────────────────────────────────
def read_src(relative_path):
    full = os.path.join(SOURCE_ROOT, relative_path)
    if os.path.exists(full):
        with open(full, 'r', encoding='utf-8') as fh:
            return fh.read()
    return f"// File not found: {relative_path}"


def read_file(full_path):
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as fh:
            return fh.read()
    return f"// File not found: {full_path}"


# ── Styles ─────────────────────────────────────────────────────────────────────
def build_styles():
    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    return dict(
        cover_title=ps('CoverTitle', fontName='Helvetica-Bold', fontSize=38,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=8, leading=46),
        cover_sub=ps('CoverSub', fontName='Helvetica', fontSize=18,
            textColor=ACCENT_GOLD, alignment=TA_CENTER, spaceAfter=6, leading=24),
        cover_info=ps('CoverInfo', fontName='Helvetica', fontSize=12,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=4, leading=18),
        section_banner=ps('SectionBanner', fontName='Helvetica-Bold', fontSize=28,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=0, leading=36),
        page_title=ps('PageTitle', fontName='Helvetica-Bold', fontSize=20,
            textColor=MID_BLUE, alignment=TA_LEFT, spaceAfter=10, spaceBefore=4, leading=26),
        page_subtitle=ps('PageSubtitle', fontName='Helvetica-Bold', fontSize=14,
            textColor=ACCENT_BLUE, alignment=TA_LEFT, spaceAfter=6, spaceBefore=8, leading=18),
        body=ps('BodyText', fontName='Helvetica', fontSize=10, textColor=DARK_GREY,
            alignment=TA_LEFT, spaceAfter=5, spaceBefore=2, leading=15),
        body_justify=ps('BodyJustify', fontName='Helvetica', fontSize=10,
            textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=5, spaceBefore=2, leading=15),
        bullet=ps('BulletText', fontName='Helvetica', fontSize=10, textColor=DARK_GREY,
            alignment=TA_LEFT, spaceAfter=3, spaceBefore=1, leading=14,
            leftIndent=15, bulletIndent=5),
        code_style=ps('CodeStyle', fontName='Courier', fontSize=7.5, textColor=BLACK,
            alignment=TA_LEFT, spaceAfter=0, spaceBefore=0, leading=11,
            leftIndent=4, rightIndent=4),
        code_file=ps('CodeFile', fontName='Helvetica-Bold', fontSize=9, textColor=MID_BLUE,
            alignment=TA_LEFT, spaceAfter=3, spaceBefore=10, leading=13),
        toc_entry=ps('TocEntry', fontName='Helvetica', fontSize=11, textColor=DARK_GREY,
            alignment=TA_LEFT, spaceAfter=4, leading=16),
        toc_section=ps('TocSection', fontName='Helvetica-Bold', fontSize=13,
            textColor=MID_BLUE, alignment=TA_LEFT, spaceAfter=5, spaceBefore=10, leading=18),
        toc_page_num=ps('TocPageNum', fontName='Helvetica', fontSize=11, textColor=MID_GREY,
            alignment=TA_RIGHT, spaceAfter=4, leading=16),
        caption=ps('Caption', fontName='Helvetica-Oblique', fontSize=9, textColor=MID_GREY,
            alignment=TA_CENTER, spaceAfter=6, leading=13),
        label=ps('Label', fontName='Helvetica-Bold', fontSize=10, textColor=MID_BLUE,
            alignment=TA_LEFT, spaceAfter=3, leading=14),
    )


# ── Page callbacks ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canvas.setFillColor(ACCENT_BLUE)
        canvas.rect(0, PAGE_H - 12*mm, PAGE_W, 12*mm, fill=1, stroke=0)
        canvas.setFillColor(ACCENT_GOLD)
        canvas.rect(0, 0, PAGE_W, 8*mm, fill=1, stroke=0)
        canvas.restoreState()
        return
    # Header bar
    canvas.setFillColor(MID_BLUE)
    canvas.rect(0, PAGE_H - 14*mm, PAGE_W, 14*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(18*mm, PAGE_H - 9*mm, 'StorePilot')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(PAGE_W - 18*mm, PAGE_H - 9*mm, 'Android Store Management App')
    # Footer bar
    canvas.setFillColor(LIGHT_GREY)
    canvas.rect(0, 0, PAGE_W, 12*mm, fill=1, stroke=0)
    canvas.setStrokeColor(ACCENT_BLUE)
    canvas.setLineWidth(1.5)
    canvas.line(0, 12*mm, PAGE_W, 12*mm)
    canvas.setFillColor(MID_GREY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(18*mm, 4*mm, 'Ahmad Hijazy  ·  2025')
    canvas.drawCentredString(PAGE_W / 2, 4*mm, 'StorePilot Project Book')
    canvas.setFillColor(ACCENT_BLUE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawRightString(PAGE_W - 18*mm, 4*mm, str(doc.page))
    canvas.restoreState()


A4_L = rl_landscape(A4)
PAGE_WL, PAGE_HL = A4_L   # landscape: ~841.9 × 595.3 pt


def on_page_landscape(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MID_BLUE)
    canvas.rect(0, PAGE_HL - 14*mm, PAGE_WL, 14*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(18*mm, PAGE_HL - 9*mm, 'StorePilot')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(PAGE_WL - 18*mm, PAGE_HL - 9*mm, 'UML Class Diagram')
    canvas.setFillColor(LIGHT_GREY)
    canvas.rect(0, 0, PAGE_WL, 12*mm, fill=1, stroke=0)
    canvas.setStrokeColor(ACCENT_BLUE)
    canvas.setLineWidth(1.5)
    canvas.line(0, 12*mm, PAGE_WL, 12*mm)
    canvas.setFillColor(MID_GREY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(18*mm, 4*mm, 'Ahmad Hijazy  ·  2025')
    canvas.drawCentredString(PAGE_WL / 2, 4*mm, 'StorePilot Project Book')
    canvas.setFillColor(ACCENT_BLUE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawRightString(PAGE_WL - 18*mm, 4*mm, str(doc.page))
    canvas.restoreState()


# ── Flowable builders ──────────────────────────────────────────────────────────
def section_divider(title, styles):
    data = [[Paragraph(title, styles['section_banner'])]]
    t = Table(data, colWidths=[PAGE_W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), MID_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 55),
        ('BOTTOMPADDING', (0,0), (-1,-1), 55),
        ('LEFTPADDING',   (0,0), (-1,-1), 20),
        ('RIGHTPADDING',  (0,0), (-1,-1), 20),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('BOX',           (0,0), (-1,-1), 3, ACCENT_GOLD),
    ]))
    return [PageBreak(), t, Spacer(1, 18*mm)]


def page_header(page_num, title, styles, subtitle=None):
    badge_style = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=14,
        textColor=WHITE, alignment=TA_CENTER, leading=18)
    badge_data = [[
        Paragraph(str(page_num), badge_style),
        Paragraph(title, styles['page_title'])
    ]]
    badge_t = Table(badge_data, colWidths=[14*mm, PAGE_W - 4*cm - 14*mm])
    badge_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), ACCENT_BLUE),
        ('BACKGROUND', (1,0), (1,0), LIGHT_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('BOX',           (0,0), (-1,-1), 1, ACCENT_BLUE),
    ]))
    elems = [badge_t]
    if subtitle:
        elems.append(Spacer(1, 3*mm))
        elems.append(Paragraph(subtitle, styles['page_subtitle']))
    elems.append(HRFlowable(width='100%', thickness=1, color=ACCENT_BLUE, spaceAfter=6))
    return elems


def info_table(rows, styles, col_widths=None):
    if col_widths is None:
        col_widths = [5*cm, PAGE_W - 4*cm - 5*cm]
    data = [[Paragraph(k, styles['label']), Paragraph(v, styles['body'])] for k, v in rows]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND',     (1,0), (1,-1), WHITE),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT_BLUE, WHITE]),
        ('TOPPADDING',     (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',  (0,0), (-1,-1), 5),
        ('LEFTPADDING',    (0,0), (-1,-1), 8),
        ('RIGHTPADDING',   (0,0), (-1,-1), 8),
        ('GRID',           (0,0), (-1,-1), 0.5, CODE_BORDER),
        ('VALIGN',         (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def code_block(code_text, filename, styles):
    elems = [Paragraph(f'  {filename}', styles['code_file'])]
    lines = code_text.split('\n')
    # 40 lines per chunk — keeps each table cell well under one page height
    for i in range(0, len(lines), 40):
        chunk = lines[i:i+40]
        safe = '\n'.join(
            l.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            for l in chunk
        )
        data = [[Paragraph(safe.replace('\n', '<br/>'), styles['code_style'])]]
        t = Table(data, colWidths=[PAGE_W - 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('BOX',           (0,0), (-1,-1), 1, CODE_BORDER),
        ]))
        elems.append(t)
        elems.append(Spacer(1, 1*mm))
    return elems


def bullet_list(items, styles):
    return [Paragraph(f'• {item}', styles['bullet']) for item in items]


def body(text, styles, justify=False):
    return Paragraph(text, styles['body_justify' if justify else 'body'])


def sub(title, styles):
    return Paragraph(title, styles['page_subtitle'])


def sp(h=6):
    return Spacer(1, h*mm)


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def _heb(text):
    """Return visually-ordered Hebrew string for ReportLab (bidi reorder)."""
    return get_display(text)


def build_cover(styles):
    # ── title block ──────────────────────────────────────────────────────────
    elems = [
        Spacer(1, 40*mm),
        Paragraph('StorePilot', styles['cover_title']),
        Spacer(1, 4*mm),
        Paragraph('Android Store Management App', styles['cover_sub']),
        Spacer(1, 8*mm),
        HRFlowable(width='60%', thickness=2, color=ACCENT_GOLD, hAlign='CENTER', spaceAfter=8),
        Spacer(1, 6*mm),
        Paragraph('Project Documentation Book', styles['cover_info']),
        Spacer(1, 14*mm),
    ]

    # ── tech badges ──────────────────────────────────────────────────────────
    bs = ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=10,
                        textColor=WHITE, alignment=TA_CENTER, leading=14)
    badges = [['Android'], ['Java'], ['Room DB'], ['Firebase'], ['MVVM']]
    bd = [[Paragraph(b[0], bs) for b in badges]]
    bt = Table(bd, colWidths=[3.2*cm]*5)
    bt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), ACCENT_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID',     (0,0), (-1,-1), 0.5, MID_BLUE),
        ('BOX',           (0,0), (-1,-1), 1, ACCENT_GOLD),
    ]))
    elems.append(bt)
    elems.append(Spacer(1, 18*mm))

    # ── student info table (bilingual) ───────────────────────────────────────
    en_label = ParagraphStyle('EL', fontName='Helvetica-Bold', fontSize=10,
                              textColor=DARK_GREY, alignment=TA_LEFT, leading=14)
    en_val   = ParagraphStyle('EV', fontName='Helvetica',      fontSize=10,
                              textColor=DARK_GREY, alignment=TA_LEFT, leading=14)
    he_label = ParagraphStyle('HL', fontName='DejaVuSans-Bold', fontSize=10,
                              textColor=DARK_GREY, alignment=TA_RIGHT, leading=14)
    he_val   = ParagraphStyle('HV', fontName='DejaVuSans',      fontSize=10,
                              textColor=DARK_GREY, alignment=TA_RIGHT, leading=14)

    rows = [
        ('Student',    'Ahmad Ashraf Hijazy',            _heb('תלמיד'),   _heb('אחמד אשרף חיגאזי')),
        ('ID',         '331453498',                      _heb('ת.ז.'),    '331453498'),
        ('School',     'Al-Bayan School, Tamra',         _heb('בית ספר'), _heb('אל-באיאן, טמרה')),
        ('Supervisor', 'Mr. Iyad Marieh',                _heb('מנחה'),    _heb('מר איאד מריח')),
        ('Track',      'Software Engineering',           _heb('מסלול'),   '126'),
        ('Major',      'Systems Planning & Programming', _heb('התמחויות'), '-'),
        ('Date',       'May 24, 2026',                   _heb('תאריך'),   _heb('24 במאי 2026')),
    ]

    tdata = []
    for el, ev, hl, hv in rows:
        tdata.append([
            Paragraph(el, en_label),
            Paragraph(ev, en_val),
            Paragraph(hl, he_label),
            Paragraph(hv, he_val),
        ])

    available = PAGE_W - 4*cm   # matches doc left+right margins
    col_w = [3.2*cm, 6.0*cm, 3.2*cm, 5.0*cm]
    info_t = Table(tdata, colWidths=col_w, repeatRows=0)
    info_t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), WHITE),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW',     (0, 0), (-1, -1), 0.5, CODE_BORDER),
        ('BOX',           (0, 0), (-1, -1), 1,   CODE_BORDER),
        ('BACKGROUND',    (0, 0), (-1,  0), LIGHT_BLUE),
    ]))
    elems.append(info_t)
    elems.append(PageBreak())
    return elems


def build_toc(styles):
    elems = page_header(2, 'Table of Contents', styles)
    elems.append(sp(4))
    sections = [
        ('Introduction & Architecture', [
            ('5',  'Introduction — What is StorePilot?'),
            ('6',  'Quick Info'),
            ('7',  'Technology Stack'),
            ('8',  'Project Structure'),
            ('9',  'UML Class Diagram'),
            ('10', 'Navigation Flow Diagram'),
            ('11', 'Room Database Schema'),
        ]),
        ('App Screens', [
            ('13', 'Home / Welcome — WelcomeActivity'),
            ('14', 'Login — LoginActivity'),
            ('15', 'Sign-Up — RegisterActivity'),
            ('16', 'Products (Customer) — CustomerHomeFragment'),
            ('17', 'Cart — CartFragment'),
            ('18', 'Support Chat — SupportChatFragment'),
            ('19', 'Tasks — TaskListFragment'),
            ('20', 'Products (Manager) — ProductListFragment'),
            ('21', 'Manager Orders — OrderManagementFragment'),
            ('22', 'Manager Panel — DashboardFragment'),
            ('23', 'Notifications'),
        ]),
        ('User Guide', [
            ('25', 'Installation Requirements'),
            ('26', 'Tested Devices & Android Versions'),
            ('27', 'How to Use — Customer'),
            ('28', 'How to Use — Manager'),
            ('29', 'Known Limitations'),
        ]),
        ('Implementation (Source Code)', [
            ('31',  'Models — User, Product, Order, OrderItem, CartItem, Sale, Task, Season, SupportMessage, Favorite'),
            ('38',  'Core & Authentication — AppDatabase, SessionManager, CryptoUtil, Auth Activities & ViewModels'),
            ('55',  'Products & Cart — DAOs, Repositories, ViewModels, Fragments, Activities'),
            ('80',  'Adapters — All RecyclerView Adapters'),
            ('100', 'Tasks & Support — Task & Support DAOs, Repos, ViewModels, Fragments'),
            ('125', 'Utilities & System — App Entry, Notifications, Permissions, Sales, Seasons, Dashboard'),
        ]),
        ('Conclusion & Appendices', [
            ('148', 'Self-Reflection'),
            ('151', 'References (APA)'),
            ('153', 'Appendix A — Permissions Map'),
            ('154', 'Appendix B — Notification Channels'),
            ('155', 'Appendix C — Room Database Operations'),
            ('156', 'Appendix D — Build & Deploy Note'),
        ]),
    ]
    for section_name, entries in sections:
        elems.append(Paragraph(section_name, styles['toc_section']))
        for pg, title in entries:
            rd = [[Paragraph(title, styles['toc_entry']),
                   Paragraph(pg, styles['toc_page_num'])]]
            rt = Table(rd, colWidths=[PAGE_W - 4*cm - 2*cm, 2*cm])
            rt.setStyle(TableStyle([
                ('TOPPADDING',    (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING',   (0,0), (-1,-1), 12),
                ('RIGHTPADDING',  (0,0), (-1,-1), 4),
                ('LINEBELOW',     (0,0), (-1,-1), 0.3, CODE_BORDER),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ]))
            elems.append(rt)
    elems.append(PageBreak())
    return elems


def build_intro(styles):
    elems = page_header(5, 'Introduction', styles, 'What is StorePilot?')
    elems += [
        body('StorePilot is a fully offline-capable Android store management application '
             'built for small-to-medium retail businesses. It provides two distinct user '
             'experiences within a single APK: a <b>Customer</b> shopping interface and a '
             '<b>Manager/Owner</b> back-office dashboard. All data is persisted locally '
             'using Room (SQLite), with optional Firebase Authentication and Firestore '
             'integration for cloud sync and low-stock push notifications.', styles, True),
        sp(2),
        body('The project demonstrates a production-quality MVVM architecture on Android, '
             'including role-based access control, a full shopping cart & checkout flow, '
             'real-time support chat, task management, inventory control, sales history, '
             'and season-aware dashboard alerts.', styles, True),
        sp(3),
        sub('Core Features', styles),
    ]
    elems += bullet_list([
        'Dual-role app: Customer shopping + Manager back-office in one APK',
        'Room (SQLite) local database — fully offline capable',
        'PBKDF2/SHA-256 password hashing with random salt',
        'Role-Based Access Control: OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE, CUSTOMER',
        'Full shopping cart, checkout flow and order tracking (PENDING → DELIVERED)',
        'Real-time support chat between customers and store staff',
        'Task management with priority levels (LOW / MEDIUM / HIGH) and private tasks',
        'Inventory management: add, edit, delete products with live low-stock alerts',
        'Sales history with date-range SQL queries',
        'Season management with end-date alerts on the dashboard',
        'Firebase Authentication (optional) + Firestore low-stock push notification',
        'LiveData + ViewModel — reactive UI that survives screen rotation',
        'Demo seed data for first-run experience',
    ], styles)
    elems.append(PageBreak())
    return elems


def build_quick_info(styles):
    elems = page_header(6, 'Quick Info', styles)
    elems.append(sp(3))
    elems.append(info_table([
        ('App Name',         'StorePilot'),
        ('Package',          'com.storepilot'),
        ('Version',          '1.0 (versionCode 1)'),
        ('Min SDK',          'API 24 (Android 7.0 Nougat)'),
        ('Target SDK',       'API 34 (Android 14)'),
        ('Language',         'Java 11'),
        ('Architecture',     'MVVM (Model-View-ViewModel)'),
        ('Database',         'Room (SQLite) — storepilot.db — v2'),
        ('Auth',             'Local PBKDF2/SHA-256 + optional Firebase Auth'),
        ('Build System',     'Gradle (AGP 8.x), Gradle wrapper 8.4'),
        ('Repository',       'github.com/ahmadhijazys2/storepilot'),
        ('Author',           'Ahmad Hijazy'),
        ('Year',             '2025'),
        ('Roles Supported',  'CUSTOMER, EMPLOYEE, SHIFT_MANAGER, STORE_MANAGER, OWNER'),
        ('Demo Credentials', 'owner / ahmad123   manager / sss123   customer / demo123'),
    ], styles, col_widths=[5.5*cm, PAGE_W - 4*cm - 5.5*cm]))
    elems.append(PageBreak())
    return elems


def build_tech_stack(styles):
    elems = page_header(7, 'Technology Stack', styles)
    elems.append(sp(3))
    tech = [
        ('Android SDK',       'API 24-34',  'Core mobile platform'),
        ('Java 11',           'OpenJDK 11', 'Primary language'),
        ('Room',              '2.6.1',      'SQLite ORM — entities, DAOs, migrations'),
        ('LiveData',          '2.7.0',      'Observable data holders for reactive UI'),
        ('ViewModel',         '2.7.0',      'Lifecycle-aware UI state holders'),
        ('Navigation',        '2.7.6',      'Fragment navigation component'),
        ('RecyclerView',      '1.3.2',      'Scrollable list views'),
        ('Material UI',       '1.11.0',     'Bottom nav, cards, FAB, tabs, snackbar'),
        ('ConstraintLayout',  '2.1.4',      'Flexible XML layouts'),
        ('CardView',          '1.0.0',      'Elevated card containers'),
        ('Firebase Auth',     '22.3.1',     'Optional cloud authentication'),
        ('Firebase Firestore','24.11.0',    'Optional cloud DB for low-stock alerts'),
        ('PBKDF2/SHA-256',    'Java Crypto','Password hashing — 65536 iterations, 256-bit key'),
        ('AlarmManager',      'Android SDK','Periodic low-stock check — 1 h interval'),
        ('NotificationMgr',   'Android SDK','Low-stock push notifications'),
        ('ViewBinding',       'AGP 8.x',    'Type-safe view binding (enabled in build.gradle)'),
    ]
    hs = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9,
                        textColor=WHITE, alignment=TA_CENTER, leading=13)
    cs = ParagraphStyle('TC', fontName='Helvetica', fontSize=9,
                        textColor=DARK_GREY, alignment=TA_LEFT, leading=13)
    data = [[Paragraph('Library / Technology', hs),
             Paragraph('Version', hs),
             Paragraph('Purpose', hs)]]
    for lib, ver, purpose in tech:
        data.append([Paragraph(lib, cs), Paragraph(ver, cs), Paragraph(purpose, cs)])
    cw = [5*cm, 3*cm, PAGE_W - 4*cm - 8*cm]
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0), MID_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BLUE]),
        ('TOPPADDING',     (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',  (0,0), (-1,-1), 5),
        ('LEFTPADDING',    (0,0), (-1,-1), 7),
        ('RIGHTPADDING',   (0,0), (-1,-1), 7),
        ('GRID',           (0,0), (-1,-1), 0.5, CODE_BORDER),
        ('VALIGN',         (0,0), (-1,-1), 'TOP'),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def build_project_structure(styles):
    elems = page_header(8, 'Project Structure', styles)
    elems.append(sp(2))
    tree = (
        "app/src/main/java/com/storepilot/\n"
        "├── StorePilotApp.java           ← Application class (Firebase init, alarm)\n"
        "├── MainActivity.java            ← Manager/Owner entry point with bottom nav\n"
        "│\n"
        "├── auth/\n"
        "│   ├── WelcomeActivity.java     ← Splash/welcome screen\n"
        "│   ├── RoleSelectionActivity.java  ← Customer vs Owner role selection\n"
        "│   ├── LoginActivity.java       ← Login form\n"
        "│   ├── RegisterActivity.java    ← Registration form\n"
        "│   ├── SetupActivity.java       ← First-run owner account creation\n"
        "│   ├── CryptoUtil.java          ← PBKDF2 password hashing\n"
        "│   ├── FirebaseAuthHelper.java  ← Firebase Auth wrapper\n"
        "│   └── FirebaseConfig.java      ← Firebase configuration\n"
        "│\n"
        "├── core/\n"
        "│   ├── AppDatabase.java         ← Room database singleton + seed data\n"
        "│   ├── BaseActivity.java        ← Permission helper base class\n"
        "│   ├── SessionManager.java      ← In-memory logged-in user session\n"
        "│   ├── PermissionManager.java   ← Role-to-permission mapping\n"
        "│   ├── NotificationHelper.java  ← Notification channel + sender\n"
        "│   └── LowStockReceiver.java    ← BroadcastReceiver for stock alerts\n"
        "│\n"
        "├── db/\n"
        "│   ├── entities/                ← Room @Entity classes (10 tables)\n"
        "│   │   ├── User.java\n"
        "│   │   ├── Product.java\n"
        "│   │   ├── Order.java / OrderItem.java\n"
        "│   │   ├── CartItem.java / Favorite.java\n"
        "│   │   ├── Sale.java\n"
        "│   │   ├── Task.java / Season.java\n"
        "│   │   └── SupportMessage.java\n"
        "│   └── dao/                     ← Room @Dao interfaces (9 DAOs)\n"
        "│\n"
        "├── repositories/                ← Data layer — wraps DAOs, runs on dbExecutor\n"
        "├── viewmodels/                  ← Lifecycle-aware UI state\n"
        "│\n"
        "├── customer/                    ← Customer shopping UI\n"
        "│   ├── CustomerMainActivity.java\n"
        "│   ├── CustomerHomeFragment.java\n"
        "│   ├── CartFragment.java / CheckoutFragment.java\n"
        "│   ├── ProductDetailFragment.java\n"
        "│   ├── OrderHistoryFragment.java / OrderConfirmationFragment.java\n"
        "│   ├── FavoritesFragment.java / SupportChatFragment.java\n"
        "│   └── adapters/\n"
        "│\n"
        "├── inventory/     ← Manager inventory (ProductList, AddEdit, Details)\n"
        "├── manager/       ← Order management, support inbox\n"
        "├── dashboard/     ← KPI dashboard fragment\n"
        "├── admin/         ← User management (OWNER only)\n"
        "├── sales/         ← Sales history + AddSaleActivity\n"
        "├── seasons/       ← Season list + AddEditSeasonActivity\n"
        "└── tasks/         ← Task list + AddEditTaskActivity"
    )
    data = [[Paragraph(tree.replace('\n', '<br/>').replace(' ', '&nbsp;'),
                       styles['code_style'])]]
    t = Table(data, colWidths=[PAGE_W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('BOX',           (0,0), (-1,-1), 1, CODE_BORDER),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def build_uml(styles):
    # Switch to landscape so the wide UML fills the full page
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uml_diagram.png')
    available_w = PAGE_WL - 4*cm           # landscape width minus margins ≈ 25.7 cm
    available_h = PAGE_HL - 4*cm - 14*mm - 12*mm  # minus header+footer bars
    img_aspect = 5424 / 4464               # width / height of the UML PNG
    # Fit to available area keeping aspect ratio
    if available_w / img_aspect <= available_h:
        iw, ih = available_w, available_w / img_aspect
    else:
        ih, iw = available_h, available_h * img_aspect
    elems = [
        NextPageTemplate('landscape'),
        PageBreak(),
        Image(img_path, width=iw, height=ih),
        NextPageTemplate('portrait'),
        PageBreak(),
    ]
    return elems


def build_nav_flow(styles):
    elems = page_header(10, 'Navigation Flow Diagram', styles)
    elems.append(sp(2))
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nav_flow_diagram.png')
    img = Image(img_path, width=PAGE_W - 4*cm, height=(PAGE_W - 4*cm) * 14/16)
    elems.append(img)
    elems.append(PageBreak())
    return elems


def build_db_schema(styles):
    elems = page_header(11, 'Room Database Schema', styles,
                        'storepilot.db — version 2 — 12 tables')
    elems.append(sp(2))
    tables = [
        ('users',            'id, fullName, username*, email*, phone, passwordHash, salt, role, createdAt'),
        ('products',         'id, name, category, size, color, quantity, price, costPrice, imageUrl, createdAt'),
        ('orders',           'id, customerId(FK), totalPrice, status, createdAt, paymentMethod, shippingAddress'),
        ('order_items',      'id, orderId(FK), productId(FK), quantity, unitPrice'),
        ('cart_items',       'id, customerId(FK), productId(FK), quantity'),
        ('favorites',        'id, customerId(FK), productId(FK), addedAt'),
        ('sales',            'id, productId(FK), quantity, totalPrice, saleDate, soldBy(FK), notes'),
        ('tasks',            'id, title, description, assignedTo(FK), createdBy(FK), status, priority, isPrivate, dueDate, createdAt'),
        ('seasons',          'id, name, startDate, endDate, alertDaysBeforeEnd, isActive, notes'),
        ('support_messages', 'id, senderId(FK), senderRole, messageText, imageUrl, timestamp, customerId(FK), isRead'),
    ]
    hs = ParagraphStyle('TH5', fontName='Helvetica-Bold', fontSize=9,
                        textColor=WHITE, alignment=TA_CENTER, leading=13)
    cb = ParagraphStyle('CB', fontName='Helvetica-Bold', fontSize=9,
                        textColor=MID_BLUE, alignment=TA_LEFT, leading=13)
    cn = ParagraphStyle('CN', fontName='Courier', fontSize=8,
                        textColor=DARK_GREY, alignment=TA_LEFT, leading=12)
    data = [[Paragraph('Table', hs), Paragraph('Columns', hs)]]
    for tname, cols in tables:
        data.append([Paragraph(tname, cb), Paragraph(cols, cn)])
    t = Table(data, colWidths=[4.5*cm, PAGE_W - 4*cm - 4.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0), MID_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BLUE]),
        ('TOPPADDING',     (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',  (0,0), (-1,-1), 5),
        ('LEFTPADDING',    (0,0), (-1,-1), 7),
        ('RIGHTPADDING',   (0,0), (-1,-1), 7),
        ('GRID',           (0,0), (-1,-1), 0.5, CODE_BORDER),
        ('VALIGN',         (0,0), (-1,-1), 'TOP'),
    ]))
    elems.append(t)
    elems.append(sp(3))
    elems.append(body('<b>Key:</b> * = unique index   (FK) = foreign key with ON DELETE SET NULL   '
                      'Database version: 2   10 tables   fallbackToDestructiveMigration() enabled for development', styles))
    elems.append(PageBreak())
    return elems


# ── App Screens ────────────────────────────────────────────────────────────────
SCREENS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screens')

def _screen_img(filename, height_cm=9.5):
    path = os.path.join(SCREENS_DIR, filename)
    if not os.path.exists(path):
        return None
    h = height_cm * cm
    # maintain 393:720 aspect
    w = h * 393 / 720
    return Image(path, width=w, height=h)


def build_screen(pg, title, class_name, desc_list, fields, actions, styles,
                 screenshot=None, extra_screenshots=None):
    elems = page_header(pg, title, styles, f'Class: {class_name}')
    elems.append(sp(2))

    img_objs = []
    if screenshot:
        im = _screen_img(screenshot)
        if im:
            img_objs.append(im)
    if extra_screenshots:
        for s in extra_screenshots:
            im = _screen_img(s)
            if im:
                img_objs.append(im)

    # Build text column content
    text_col = []
    for p in desc_list:
        text_col.append(Paragraph(p, styles['body_justify']))
        text_col.append(Spacer(1, 3*mm))
    if fields:
        text_col.append(Spacer(1, 4*mm))
        text_col.append(Paragraph('UI Components', styles['page_subtitle']))
        text_col += [Paragraph(f'• {f}', styles['bullet']) for f in fields]
    if actions:
        text_col.append(Spacer(1, 4*mm))
        text_col.append(Paragraph('User Actions', styles['page_subtitle']))
        text_col += [Paragraph(f'• {a}', styles['bullet']) for a in actions]

    if img_objs:
        # All screenshots stacked vertically in left column; text in right column
        img_w = img_objs[0].drawWidth   # all screenshots same width
        text_w = PAGE_W - 4*cm - img_w - 8*mm

        if len(img_objs) == 1:
            img_cell_rows = [[img_objs[0]]]
        else:
            img_cell_rows = [[im] for im in img_objs]

        img_inner = Table(img_cell_rows, colWidths=[img_w])
        img_inner.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))

        txt_inner = Table([[t] for t in text_col], colWidths=[text_w])
        txt_inner.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))

        layout = Table([[img_inner, Spacer(8*mm, 1), txt_inner]],
                       colWidths=[img_w, 8*mm, text_w])
        layout.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))
        elems.append(layout)
    else:
        elems += text_col

    elems.append(PageBreak())
    return elems


def build_app_screens(styles):
    elems = section_divider('App Screens', styles)

    elems += build_screen(13, 'Home / Welcome Screen', 'WelcomeActivity',
        ['The Welcome screen is the first screen a user sees after launching the app. '
         'If the user is already logged in, the app immediately routes them to the '
         'correct interface based on their role without showing this screen.',
         'New users can either log in with an existing account or choose a role '
         '(Customer or Owner) before registering.'],
        ['StorePilot logo (teal circle) and tagline',
         'SIGN IN button — navigates to LoginActivity',
         'SIGN UP button — navigates to RoleSelectionActivity',
         'Auto-skip if session is active (navigateByRole())'],
        ['Tap SIGN IN → LoginActivity',
         'Tap SIGN UP → RoleSelectionActivity → RegisterActivity',
         'Already logged in → CustomerMainActivity or MainActivity (automatic)'],
        styles, screenshot='screen_welcome.png')

    elems += build_screen(14, 'Role Selection Screen', 'RoleSelectionActivity',
        ['Shown after tapping SIGN UP on the Welcome screen. The user picks whether '
         'they are signing up as an Owner (staff account) or a Customer.',
         'The selected role is passed to RegisterActivity so the "Signing up as:" '
         'label is pre-filled and the role field is locked.'],
        ['"I am signing up as..." title',
         'OWNER button — staff / manager account',
         'CUSTOMER button — shopping account'],
        ['Tap OWNER → RegisterActivity with role=OWNER',
         'Tap CUSTOMER → RegisterActivity with role=CUSTOMER'],
        styles, screenshot='screen_role_selection.png')

    elems += build_screen(15, 'Login Screen', 'LoginActivity',
        ['The login screen accepts a username or email address with a password. '
         'Credentials are validated locally using PBKDF2/SHA-256 hash comparison.',
         'On the very first install with no users, the app redirects to SetupActivity. '
         'After success the user is routed based on role.'],
        ['StorePilot logo (teal circle) + "Welcome back!" label',
         'Email / Username EditText (outlined, floating label)',
         'Password EditText (textPassword input type)',
         'LOGIN Button — triggers AuthViewModel.login()'],
        ['Enter credentials + tap LOGIN',
         'Empty fields → Toast error',
         'Wrong credentials → loginError LiveData → Toast',
         'Success → role-based navigation'],
        styles, screenshot='screen_login.png')

    elems += build_screen(16, 'Sign-Up / Registration Screen', 'RegisterActivity',
        ['Collects full name, username, email, phone, password and role. '
         'The role is pre-set from RoleSelectionActivity ("Signing up as: Customer" or "Owner").',
         'A PBKDF2 salt+hash is computed on a background thread. Firebase Auth sign-up '
         'is attempted optionally (gracefully ignored on failure).'],
        ['Full Name, Username, Email Address, Phone Number (optional)',
         'Password EditText with visibility toggle (eye icon)',
         'Confirm Password EditText',
         '"Signing up as: <role>" label',
         'CREATE ACCOUNT button'],
        ['Fill all required fields + tap CREATE ACCOUNT',
         'Password < 6 chars → error toast',
         'Passwords mismatch → error toast',
         'Duplicate username/email → "already taken" toast',
         'Success → LoginActivity'],
        styles,
        screenshot='screen_register_customer.png',
        extra_screenshots=['screen_register_owner.png'])

    elems += build_screen(17, 'Products (Customer) — Home Screen', 'CustomerHomeFragment',
        ['Shows all products in a 2-column grid with a live search bar that filters '
         'by name or category as the user types.',
         'Each card shows name, category, price, and stock status. The Add to Cart '
         'button is disabled for out-of-stock items.'],
        ['Personalised greeting (Hello, {name})',
         'Search bar with TextWatcher for live filtering',
         'RecyclerView with GridLayoutManager (2 columns)',
         'Product cards: name, category, price, In Stock / Out of Stock badge',
         'Empty state TextView'],
        ['Type in search → live filtering',
         'Tap product card → ProductDetailFragment',
         'Tap "+ Cart" → CartViewModel.addToCart()'],
        styles, screenshot='screen_customer_home.png')

    elems += build_screen(18, 'Cart Screen', 'CartFragment',
        ['Lists all items the customer has added. Each row shows product name, '
         'unit price, subtotal and quantity controls (+/−/remove).',
         'The Checkout button is disabled when the cart is empty.'],
        ['RecyclerView with CartItemAdapter',
         'Each row: product image placeholder, name, unit price, +/−/trash buttons, subtotal',
         'Total price row at the bottom',
         'CHECKOUT Button (disabled when empty)'],
        ['Tap + → increase quantity',
         'Tap − → decrease or remove if last unit',
         'Tap trash → remove item entirely',
         'Tap CHECKOUT → CheckoutFragment'],
        styles, screenshot='screen_cart.png')

    elems += build_screen(19, 'Checkout Screen', 'CheckoutFragment',
        ['Collects a shipping address and payment method before placing the order. '
         'The cart is validated (non-empty, address filled) before the order is created.',
         'On success, the cart is cleared and the user is sent to OrderConfirmationFragment.'],
        ['Shipping address EditText (multiline)',
         'Payment method radio group: Cash on Delivery / PayPal / Credit Card',
         'Order summary card showing item count and total',
         'PLACE ORDER button (disabled after tap to prevent double-submit)'],
        ['Enter address + pick payment + tap PLACE ORDER',
         'Empty address → Toast error',
         'Empty cart → Toast error',
         'Success → OrderConfirmationFragment, cart cleared'],
        styles, screenshot='screen_checkout.png')

    elems += build_screen(20, 'Support Chat Screen', 'SupportChatFragment',
        ['A WhatsApp-style support chat. Sent messages appear on the right (dark); '
         'received messages appear on the left (light blue). Two XML item layouts are used.',
         'All messages are persisted in the support_messages table and marked as '
         'read when the chat is opened.'],
        ['RecyclerView with LinearLayoutManager (stackFromEnd=true)',
         'MessageAdapter — dual view type (sent / received)',
         'Message EditText + Send button (teal)',
         'Timestamp per message bubble'],
        ['Type message + tap Send → SupportViewModel.sendMessage()',
         'Messages load via LiveData and auto-scroll to latest',
         'All messages marked read on open'],
        styles, screenshot='screen_support_chat.png')

    elems += build_screen(21, 'Task Management Screen', 'TaskListFragment',
        ['Shows work items in three tabs: My Tasks / Team / Private. '
         'Uses switchMap to avoid stacking multiple LiveData observers on tab change.',
         'Each task card shows title, status chip (TODO/IN_PROGRESS/DONE) and '
         'priority chip (LOW/MEDIUM/HIGH).'],
        ['TabLayout with three tabs (My Tasks · Team · Private)',
         'RecyclerView with TaskAdapter',
         'Each row: title, colour-coded status chip, priority chip',
         'FloatingActionButton (+) — add new task'],
        ['Tap tab → switches list via switchMap LiveData',
         'Tap FAB → AddEditTaskActivity',
         'Tasks auto-refresh via LiveData'],
        styles, screenshot='screen_task_list.png')

    elems += build_screen(22, 'Products (Manager) — Inventory Screen', 'ProductListFragment',
        ['Shows all products in a vertical list with name, category, stock quantity and price. '
         'Low-stock items show a red quantity badge. The FAB (+) is hidden from roles '
         'without MANAGE_PRODUCTS permission.'],
        ['RecyclerView with ProductListAdapter',
         'Each row: product image placeholder, name, category, colour-coded stock badge, price',
         'FAB (+) — add product (OWNER/STORE_MANAGER only)'],
        ['Tap product row → ProductDetailsFragment (full details + edit/delete)',
         'Tap FAB → AddEditProductActivity'],
        styles, screenshot='screen_product_list.png')

    elems += build_screen(23, 'Manager Orders Screen', 'OrderManagementFragment',
        ['Lists all customer orders. Each card shows order ID, customer ID, total, '
         'a colour-coded status badge and a "Change ▾" spinner to update the status.',
         'Managers can move orders through PENDING → PROCESSING → SHIPPED → DELIVERED '
         'or mark CANCELLED.'],
        ['RecyclerView with ManagerOrderAdapter',
         'Each row: order ID, customer ID, total, colour-coded status badge',
         '"Change ▾" status spinner — 5 options',
         'Empty state TextView'],
        ['Spinner change → OrderViewModel.updateOrderStatus()',
         'PENDING=orange · PROCESSING=blue · SHIPPED=purple · DELIVERED=green · CANCELLED=red'],
        styles, screenshot='screen_manager_orders.png')

    elems += build_screen(24, 'Manager Panel / Dashboard', 'DashboardFragment',
        ['Default landing screen for all staff roles. Shows four live KPI cards '
         'that auto-update via LiveData: Today\'s Sales, Low Stock Items, '
         'Pending Tasks, and Today\'s Orders.',
         'A season alert card (orange border) appears when any active season ends within 30 days.'],
        ['Season Alert Card (conditional — orange border)',
         'Today\'s Sales total (formatted as currency)',
         'Low Stock Items count (threshold = 10)',
         'Pending Tasks count',
         'Today\'s Orders count'],
        ['All cards refresh automatically via multiple LiveData observers',
         'Season alert hidden when no season is ending soon'],
        styles, screenshot='screen_dashboard.png')

    elems += build_screen(25, 'Notifications', 'NotificationHelper + LowStockReceiver',
        ['StorePilot uses NotificationManager to alert staff when stock is low. '
         'The channel storepilot_low_stock is created at startup with IMPORTANCE_HIGH.',
         'An AlarmManager repeating alarm fires every 1 hour, triggering '
         'LowStockReceiver to query Firestore for products with quantity ≤ 5.'],
        ['Channel ID: storepilot_low_stock',
         'Importance: IMPORTANCE_HIGH (vibration enabled)',
         'Threshold: 5 units',
         'Schedule: setInexactRepeating — 1-hour interval'],
        ['Alarm fires → query Firestore → notify if count > 0',
         'Tap More → Test Notification → immediate manual test',
         'Android 13+ → POST_NOTIFICATIONS runtime permission prompt'],
        styles, screenshot='screen_notifications.png')

    elems += build_screen(26, 'Order History (Customer)', 'OrderHistoryFragment',
        ['Shows the logged-in customer\'s past orders in reverse-chronological order. '
         'Each card shows order ID, item count, total and a colour-coded status badge.',
         'Tapping a card could be extended to show full order details (not yet implemented).'],
        ['RecyclerView with CustomerOrderAdapter',
         'Each row: order ID, item count, total, colour-coded status badge',
         'Empty state TextView when no orders exist'],
        ['LiveData observer refreshes list automatically',
         'Status colours: PENDING=orange · DELIVERED=green'],
        styles, screenshot='screen_order_history.png')

    elems += build_screen(27, 'Favourites Screen', 'FavoritesFragment',
        ['Shows products the customer has heart-marked. Each card shows the product '
         'image placeholder, name, price, stock badge and a filled heart icon.',
         'Tapping the heart removes the item from favourites. The Add to Cart button '
         'is also available inline.'],
        ['RecyclerView with FavoritesAdapter (vertical list)',
         'Each row: image, name, price, stock badge, heart icon, "+ Cart" button',
         'Empty state when no favourites'],
        ['Tap heart → FavoritesViewModel.removeFavorite()',
         'Tap "+ Cart" → CartViewModel.addToCart()',
         'List auto-refreshes via LiveData'],
        styles, screenshot='screen_favorites.png')

    return elems


# ── User Guide ─────────────────────────────────────────────────────────────────
def build_user_guide(styles):
    elems = section_divider('User Guide', styles)

    # Page 25
    elems += page_header(25, 'Installation Requirements', styles)
    elems.append(sp(2))
    elems.append(sub('Development Environment', styles))
    elems += bullet_list([
        'Android Studio Hedgehog (2023.1.1) or later',
        'JDK 11 (bundled with Android Studio)',
        'Android SDK — Build Tools 34.0.0, Platform 34',
        'Gradle 8.4 (wrapper included in repo)',
        'Git for cloning the repository',
    ], styles)
    elems += [sp(3), sub('Firebase Setup (optional)', styles),
              body('Firebase is optional — the app works fully offline without it. '
                   'To enable cloud push notifications and authentication:', styles)]
    elems += bullet_list([
        'Create a Firebase project at console.firebase.google.com',
        'Add Android app with package name com.storepilot',
        'Download google-services.json and place it in app/',
        'Enable Authentication (Email/Password) in Firebase Console',
        'Create a Firestore collection "products" mirroring Room product data',
    ], styles)
    elems += [sp(3), sub('Build & Install Steps', styles)]
    for i, step in enumerate([
        'git clone https://github.com/ahmadhijazys2/storepilot.git',
        'Open project in Android Studio',
        '(Optional) Add app/google-services.json',
        'Connect device (USB debug) or start emulator (API 24+)',
        'Run: Build → Make Project  or press the green Run button',
        'On first launch → Create Owner Account to initialise the database',
        'Optionally enable Demo Mode to populate sample data',
    ], 1):
        elems.append(Paragraph(f'<b>{i}.</b>  {step}', styles['body']))
        elems.append(sp(1))
    elems.append(PageBreak())

    # Page 26
    elems += page_header(26, 'Tested Devices & Android Versions', styles)
    elems.append(sp(2))
    devices = [
        ('Samsung Galaxy S21', 'Android 13 (API 33)', 'Physical — primary test device'),
        ('Google Pixel 6',     'Android 14 (API 34)', 'Physical device'),
        ('Xiaomi Redmi Note 9','Android 11 (API 30)', 'Physical device'),
        ('AVD Pixel 4',        'Android 7.0 (API 24)','Emulator — minimum SDK check'),
        ('AVD Pixel 5',        'Android 10 (API 29)', 'Emulator'),
        ('AVD Pixel 7',        'Android 14 (API 34)', 'Emulator'),
    ]
    hs = ParagraphStyle('TH6', fontName='Helvetica-Bold', fontSize=9,
                        textColor=WHITE, alignment=TA_CENTER, leading=13)
    cs = ParagraphStyle('TC6', fontName='Helvetica', fontSize=9,
                        textColor=DARK_GREY, alignment=TA_LEFT, leading=13)
    data = [[Paragraph('Device', hs), Paragraph('Android Version', hs), Paragraph('Notes', hs)]]
    for d, v, n in devices:
        data.append([Paragraph(d, cs), Paragraph(v, cs), Paragraph(n, cs)])
    dt = Table(data, colWidths=[5.5*cm, 4.5*cm, PAGE_W - 4*cm - 10*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0), MID_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BLUE]),
        ('TOPPADDING',     (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',    (0,0), (-1,-1), 7), ('RIGHTPADDING',  (0,0), (-1,-1), 7),
        ('GRID',           (0,0), (-1,-1), 0.5, CODE_BORDER),
        ('VALIGN',         (0,0), (-1,-1), 'TOP'),
    ]))
    elems.append(dt)
    elems += [sp(3), body('<b>Note:</b> Compiled with Java 11 source/target compatibility to avoid '
                          'a known jlink.exe crash on Windows with AGP 8.x.', styles)]
    elems.append(PageBreak())

    # Page 27
    elems += page_header(27, 'How to Use — Customer', styles)
    elems.append(sp(2))
    for title, desc in [
        ('Register', 'Open app → Tap Register → Select Customer → Fill name, username, email, phone, password → Tap Register → Sign in.'),
        ('Browse Products', 'Home tab shows all products in a grid. Use the search bar to filter by name or category.'),
        ('View Details', 'Tap a product card to see full details: name, category, size, colour, price, and stock status.'),
        ('Add to Cart', 'From home grid or detail screen, tap "Add to Cart". The cart badge updates automatically.'),
        ('Manage Cart', 'Tap Cart tab. Use + and − to adjust quantity or the trash icon to remove an item entirely.'),
        ('Checkout', 'In Cart screen, tap Checkout. Enter shipping address and pick a payment method. Tap Place Order.'),
        ('Track Orders', 'Tap Orders tab to see all past orders with their live status (PENDING → DELIVERED).'),
        ('Favourites', 'Tap the heart icon on any product to save it. View saved products in the Favourites tab.'),
        ('Contact Support', 'Tap Support tab to open the live chat. Type your message and tap Send.'),
    ]:
        elems.append(Paragraph(f'<b>{title}</b>', styles['label']))
        elems.append(body(desc, styles))
        elems.append(sp(1.5))
    elems.append(PageBreak())

    # Page 28
    elems += page_header(28, 'How to Use — Manager', styles)
    elems.append(sp(2))
    for title, desc in [
        ('First Launch', 'If empty database, SetupActivity opens. Enter Owner username + password. Enable Demo Mode to load sample data.'),
        ('Login as Staff', 'Log in with username and password. Staff roles land on the Dashboard.'),
        ('Dashboard', 'Shows today\'s sales, low stock count, pending tasks, today\'s orders, and season alerts.'),
        ('Add Product', 'Tap Inventory → FAB (+) → fill name, category, size, colour, quantity, selling price, cost price → Save.'),
        ('Edit Product', 'Tap product row → detail screen → Edit button → modify fields → Save.'),
        ('Record Sale', 'Tap Sales → FAB (+) → select product, enter quantity → Save. Stock auto-decrements.'),
        ('Manage Orders', 'Tap More → Orders. Use the status spinner on each order card to update its status.'),
        ('Support Inbox', 'Tap More → Support. See customer conversations. Tap a name to open their chat and reply.'),
        ('Tasks', 'Tap Tasks → use tabs (My/Team/Private) → FAB (+) to create a task.'),
        ('Test Notification', 'Tap More → Test Notification (OWNER/MANAGER only) to verify the low-stock channel.'),
        ('User Management', 'Tap More → Admin (OWNER only) to view all registered users and roles.'),
        ('Logout', 'Tap More → Logout to clear the session and return to the Welcome screen.'),
    ]:
        elems.append(Paragraph(f'<b>{title}</b>', styles['label']))
        elems.append(body(desc, styles))
        elems.append(sp(1.5))
    elems.append(PageBreak())

    # Page 29
    elems += page_header(29, 'Known Limitations', styles)
    elems.append(sp(2))
    elems.append(body('The following limitations are known and accepted in the current version:', styles))
    elems.append(sp(2))
    for lim in [
        'No real-time sync — all data is local (Room/SQLite). Firebase Firestore is used only for low-stock notification queries, not for full data sync across devices.',
        'No image upload — product imageUrl is stored as a string but no image-loading library (Glide/Coil) is included. A placeholder is shown instead.',
        'Payment is simulated — the app stores a payment method string but does not integrate a real payment gateway.',
        'Push notifications require Firebase — without a valid google-services.json the LowStockReceiver silently ignores Firestore failures.',
        'No email verification — emails are stored but not verified. Forgot Password shows a static toast.',
        'Session is in-memory — SessionManager holds the user in RAM. Killing the process logs the user out (no persistent token).',
        'Demo seed data is not idempotent — calling seedDemoData() more than once inserts duplicate rows.',
        'No pagination — all queries return the full result set. Large datasets may slow the UI.',
        'fallbackToDestructiveMigration drops and rebuilds the database on schema changes — not suitable for production without proper migrations.',
    ]:
        elems.append(Paragraph(f'• {lim}', styles['bullet']))
        elems.append(sp(1))
    elems.append(PageBreak())
    return elems


# ── Source Code Sections ───────────────────────────────────────────────────────
def build_models(styles):
    elems = section_divider('Implementation (Source Code)', styles)
    elems += page_header(31, 'Models — Room @Entity Classes', styles,
                         'db/entities/ — 10 domain model classes')
    elems.append(body(
        'All model classes are plain Java objects annotated with Room\'s @Entity, '
        '@PrimaryKey, and @ForeignKey annotations. Room generates the SQLite CREATE TABLE '
        'statements at compile time. Each class provides a no-arg constructor (required '
        'by Room) and a convenience constructor for programmatic creation.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('db/entities/User.java',           'db/entities/User.java'),
        ('db/entities/Product.java',        'db/entities/Product.java'),
        ('db/entities/Order.java',          'db/entities/Order.java'),
        ('db/entities/OrderItem.java',      'db/entities/OrderItem.java'),
        ('db/entities/CartItem.java',       'db/entities/CartItem.java'),
        ('db/entities/Sale.java',           'db/entities/Sale.java'),
        ('db/entities/Task.java',           'db/entities/Task.java'),
        ('db/entities/Season.java',         'db/entities/Season.java'),
        ('db/entities/SupportMessage.java', 'db/entities/SupportMessage.java'),
        ('db/entities/Favorite.java',       'db/entities/Favorite.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)
    elems.append(PageBreak())
    return elems


def build_core_auth(styles):
    elems = page_header(38, 'Core & Authentication', styles,
                        'core/ + auth/ — database, session, crypto, activities, ViewModels')
    elems.append(body(
        'Core infrastructure: the Room database singleton with 10-table schema and '
        'seed data, in-memory session management, PBKDF2/SHA-256 password hashing, '
        'role-based permission system, and all authentication activities/ViewModels.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('core/AppDatabase.java',           'core/AppDatabase.java'),
        ('core/BaseActivity.java',          'core/BaseActivity.java'),
        ('core/SessionManager.java',        'core/SessionManager.java'),
        ('core/PermissionManager.java',     'core/PermissionManager.java'),
        ('auth/CryptoUtil.java',            'auth/CryptoUtil.java'),
        ('auth/WelcomeActivity.java',       'auth/WelcomeActivity.java'),
        ('auth/RoleSelectionActivity.java', 'auth/RoleSelectionActivity.java'),
        ('auth/LoginActivity.java',         'auth/LoginActivity.java'),
        ('auth/RegisterActivity.java',      'auth/RegisterActivity.java'),
        ('auth/SetupActivity.java',         'auth/SetupActivity.java'),
        ('viewmodels/AuthViewModel.java',   'viewmodels/AuthViewModel.java'),
        ('db/dao/UserDao.java',             'db/dao/UserDao.java'),
        ('repositories/UserRepository.java','repositories/UserRepository.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)
    elems.append(PageBreak())
    return elems


def build_products_cart(styles):
    elems = page_header(55, 'Products & Cart', styles,
                        'inventory/ + customer/ — DAOs, Repos, ViewModels, Fragments, Activities')
    elems.append(body(
        'Complete product management and customer shopping layer: '
        'product DAOs with low-stock queries, the cart/order pipeline, '
        'checkout flow, order history, and customer-facing browsing screens.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('db/dao/ProductDao.java',              'db/dao/ProductDao.java'),
        ('db/dao/CartDao.java',                 'db/dao/CartDao.java'),
        ('db/dao/OrderDao.java',                'db/dao/OrderDao.java'),
        ('db/dao/OrderItemDao.java',            'db/dao/OrderItemDao.java'),
        ('db/dao/FavoriteDao.java',             'db/dao/FavoriteDao.java'),
        ('repositories/ProductRepository.java', 'repositories/ProductRepository.java'),
        ('repositories/CartRepository.java',    'repositories/CartRepository.java'),
        ('repositories/OrderRepository.java',   'repositories/OrderRepository.java'),
        ('repositories/FavoritesRepository.java','repositories/FavoritesRepository.java'),
        ('viewmodels/ProductViewModel.java',    'viewmodels/ProductViewModel.java'),
        ('viewmodels/CartViewModel.java',       'viewmodels/CartViewModel.java'),
        ('viewmodels/OrderViewModel.java',      'viewmodels/OrderViewModel.java'),
        ('viewmodels/FavoritesViewModel.java',  'viewmodels/FavoritesViewModel.java'),
        ('inventory/ProductListFragment.java',  'inventory/ProductListFragment.java'),
        ('inventory/ProductDetailsFragment.java','inventory/ProductDetailsFragment.java'),
        ('inventory/AddEditProductActivity.java','inventory/AddEditProductActivity.java'),
        ('customer/CustomerHomeFragment.java',  'customer/CustomerHomeFragment.java'),
        ('customer/ProductDetailFragment.java', 'customer/ProductDetailFragment.java'),
        ('customer/CartFragment.java',          'customer/CartFragment.java'),
        ('customer/CheckoutFragment.java',      'customer/CheckoutFragment.java'),
        ('customer/OrderHistoryFragment.java',  'customer/OrderHistoryFragment.java'),
        ('customer/OrderConfirmationFragment.java','customer/OrderConfirmationFragment.java'),
        ('customer/FavoritesFragment.java',     'customer/FavoritesFragment.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)
    elems.append(PageBreak())
    return elems


def build_adapters(styles):
    elems = page_header(80, 'Adapters', styles,
                        'All RecyclerView Adapters across the application')
    elems.append(body(
        'RecyclerView adapters bridge the data layer to the UI using the ViewHolder '
        'pattern. Click callbacks are functional interfaces, keeping adapters '
        'fully decoupled from their hosting fragments.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('customer/adapters/CustomerProductAdapter.java', 'customer/adapters/CustomerProductAdapter.java'),
        ('customer/adapters/CartItemAdapter.java',        'customer/adapters/CartItemAdapter.java'),
        ('customer/adapters/MessageAdapter.java',         'customer/adapters/MessageAdapter.java'),
        ('customer/adapters/CustomerOrderAdapter.java',   'customer/adapters/CustomerOrderAdapter.java'),
        ('manager/adapters/ManagerOrderAdapter.java',     'manager/adapters/ManagerOrderAdapter.java'),
        ('inventory/ProductListAdapter.java',             'inventory/ProductListAdapter.java'),
        ('tasks/TaskAdapter.java',                        'tasks/TaskAdapter.java'),
        ('seasons/SeasonAdapter.java',                    'seasons/SeasonAdapter.java'),
        ('sales/SaleAdapter.java',                        'sales/SaleAdapter.java'),
        ('manager/ConversationListAdapter.java',          'manager/ConversationListAdapter.java'),
        ('admin/UserAdapter.java',                        'admin/UserAdapter.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)
    elems.append(PageBreak())
    return elems


def build_tasks_support(styles):
    elems = page_header(100, 'Tasks & Support', styles,
                        'tasks/ + manager/ — DAOs, Repos, ViewModels, Fragments')
    elems.append(body(
        'Task management system and two-way support chat between customers and staff. '
        'Both features use the MVVM pipeline. The support chat uses two XML item layouts '
        'to render sent and received messages differently.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('db/dao/TaskDao.java',                     'db/dao/TaskDao.java'),
        ('db/dao/SupportMessageDao.java',           'db/dao/SupportMessageDao.java'),
        ('repositories/TaskRepository.java',         'repositories/TaskRepository.java'),
        ('repositories/SupportRepository.java',      'repositories/SupportRepository.java'),
        ('viewmodels/TaskViewModel.java',            'viewmodels/TaskViewModel.java'),
        ('viewmodels/SupportViewModel.java',         'viewmodels/SupportViewModel.java'),
        ('tasks/TaskListFragment.java',              'tasks/TaskListFragment.java'),
        ('tasks/AddEditTaskActivity.java',           'tasks/AddEditTaskActivity.java'),
        ('customer/SupportChatFragment.java',        'customer/SupportChatFragment.java'),
        ('manager/SupportConversationsFragment.java','manager/SupportConversationsFragment.java'),
        ('manager/SupportInboxFragment.java',        'manager/SupportInboxFragment.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)
    elems.append(PageBreak())
    return elems


def build_utilities(styles):
    elems = page_header(125, 'Utilities & System', styles,
                        'App entry, notifications, dashboard, sales, seasons')
    elems.append(body(
        'Application entry points, system utilities (AlarmManager, BroadcastReceiver, '
        'NotificationManager), the management dashboard, and the sales and season '
        'history modules. Includes the full Gradle build configuration.', styles))
    elems.append(sp(2))
    for fname, path in [
        ('StorePilotApp.java',                'StorePilotApp.java'),
        ('MainActivity.java',                 'MainActivity.java'),
        ('customer/CustomerMainActivity.java','customer/CustomerMainActivity.java'),
        ('core/NotificationHelper.java',      'core/NotificationHelper.java'),
        ('core/LowStockReceiver.java',        'core/LowStockReceiver.java'),
        ('dashboard/DashboardFragment.java',  'dashboard/DashboardFragment.java'),
        ('admin/UserManagementFragment.java', 'admin/UserManagementFragment.java'),
        ('db/dao/SaleDao.java',               'db/dao/SaleDao.java'),
        ('db/dao/SeasonDao.java',             'db/dao/SeasonDao.java'),
        ('repositories/SaleRepository.java',  'repositories/SaleRepository.java'),
        ('repositories/SeasonRepository.java','repositories/SeasonRepository.java'),
        ('viewmodels/SaleViewModel.java',     'viewmodels/SaleViewModel.java'),
        ('viewmodels/SeasonViewModel.java',   'viewmodels/SeasonViewModel.java'),
        ('sales/SalesHistoryFragment.java',   'sales/SalesHistoryFragment.java'),
        ('sales/AddSaleActivity.java',        'sales/AddSaleActivity.java'),
        ('seasons/SeasonListFragment.java',   'seasons/SeasonListFragment.java'),
        ('seasons/AddEditSeasonActivity.java','seasons/AddEditSeasonActivity.java'),
        ('manager/OrderManagementFragment.java','manager/OrderManagementFragment.java'),
    ]:
        elems += code_block(read_src(path), fname, styles)

    gradle_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'build.gradle')
    elems += code_block(read_file(gradle_path), 'app/build.gradle', styles)
    elems.append(PageBreak())
    return elems


# ── Conclusion & Appendices ────────────────────────────────────────────────────
def build_conclusion(styles):
    elems = section_divider('Conclusion & Appendices', styles)

    # 148 – Self-Reflection
    elems += page_header(148, 'Self-Reflection', styles)
    elems.append(sp(2))
    elems.append(body(
        'Building StorePilot was a comprehensive exercise in designing a production-grade '
        'Android application from scratch using MVVM architecture. The project challenged '
        'careful thinking about separation of concerns, thread safety, and user experience '
        'across two very different user types within a single codebase.', styles, True))
    elems.append(sp(2))
    elems.append(sub('What Went Well', styles))
    elems += bullet_list([
        'The Repository pattern proved extremely valuable — swapping Room for Firestore would only require changing the repository layer.',
        'PBKDF2 password hashing was straightforward to implement with Java\'s javax.crypto and provides genuinely secure local credential storage.',
        'LiveData made the dashboard self-updating without any polling loops.',
        'Dual-role architecture (one APK, two separate UIs) was clean using a role check at login time.',
        'Demo seed data made testing the full order and chat flows much faster.',
        'Using switchMap in TaskListFragment elegantly solved the "stacking observers on tab change" bug.',
    ], styles)
    elems += [sp(3), sub('Challenges Encountered', styles)]
    elems += bullet_list([
        'Room\'s fallbackToDestructiveMigration wiped data during early schema iterations — a reminder that production apps need proper migrations.',
        'The ManagerOrderAdapter\'s spinner fired its listener on initial bind — solved by the firstTime flag guard.',
        'Firebase Firestore\'s async callback model clashed with Room\'s synchronous background-thread pattern.',
        'Supporting Android 13\'s POST_NOTIFICATIONS runtime permission required a VERSION_CODES.TIRAMISU check.',
    ], styles)
    elems += [sp(3), sub('Future Improvements', styles)]
    elems += bullet_list([
        'Replace fallbackToDestructiveMigration with versioned Room migrations.',
        'Integrate a real payment gateway (Stripe Android SDK).',
        'Add Glide or Coil for product image loading.',
        'Implement full Firestore sync for multi-device inventory.',
        'Add DiffUtil to adapters for smooth animated list updates.',
        'Add JUnit + Mockito tests for ViewModels and Room in-memory DAO tests.',
        'Implement Paging 3 for large product and order lists.',
    ], styles)
    elems.append(PageBreak())

    # 151 – References
    elems += page_header(151, 'References (APA)', styles)
    elems.append(sp(2))
    for ref in [
        'Android Developers. (2024). <i>Room persistence library</i>. Google. https://developer.android.com/training/data-storage/room',
        'Android Developers. (2024). <i>LiveData overview</i>. Google. https://developer.android.com/topic/libraries/architecture/livedata',
        'Android Developers. (2024). <i>ViewModel overview</i>. Google. https://developer.android.com/topic/libraries/architecture/viewmodel',
        'Android Developers. (2024). <i>Navigation component</i>. Google. https://developer.android.com/guide/navigation',
        'Android Developers. (2024). <i>Create and manage notification channels</i>. Google. https://developer.android.com/develop/ui/views/notifications/channels',
        'Android Developers. (2024). <i>Request app permissions</i>. Google. https://developer.android.com/training/permissions/requesting',
        'Firebase. (2024). <i>Firebase Authentication documentation</i>. Google. https://firebase.google.com/docs/auth/android/start',
        'Firebase. (2024). <i>Cloud Firestore documentation</i>. Google. https://firebase.google.com/docs/firestore',
        'NIST. (2017). <i>SP 800-63B — Digital Identity Guidelines</i>. https://doi.org/10.6028/NIST.SP.800-63b',
        'OWASP. (2023). <i>Password storage cheat sheet</i>. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html',
        'Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). <i>Design patterns: Elements of reusable object-oriented software</i>. Addison-Wesley.',
        'Google. (2024). <i>Guide to app architecture</i>. https://developer.android.com/topic/architecture',
        'Google. (2024). <i>Material Design 3 — Android components</i>. https://m3.material.io/develop/android/mdc-android',
    ]:
        elems.append(body(ref, styles))
        elems.append(sp(2))
    elems.append(PageBreak())

    # 153 – Appendix A
    elems += page_header(153, 'Appendix A — Permissions Map', styles,
                         'PermissionManager — role to permission mapping')
    elems.append(sp(2))
    elems.append(body(
        'The table below maps each permission constant to the roles that hold it. '
        'PermissionManager is the single source of truth for this mapping.', styles))
    elems.append(sp(2))
    perms = [
        ('MANAGE_USERS',        'v', '',  '',  ''),
        ('MANAGE_PRODUCTS',     'v', 'v', '',  ''),
        ('VIEW_PRODUCTS',       'v', 'v', 'v', 'v'),
        ('CREATE_SALE',         'v', 'v', 'v', 'v'),
        ('VIEW_SALES_HISTORY',  'v', 'v', 'v', ''),
        ('VIEW_REPORTS',        'v', 'v', '',  ''),
        ('MANAGE_SEASONS',      'v', 'v', '',  ''),
        ('CREATE_PRIVATE_TASK', 'v', 'v', 'v', 'v'),
        ('VIEW_TEAM_TASKS',     'v', 'v', 'v', ''),
        ('MANAGE_TASKS',        'v', 'v', '',  ''),
        ('VIEW_ADMIN',          'v', '',  '',  ''),
    ]
    hs2 = ParagraphStyle('TH7', fontName='Helvetica-Bold', fontSize=9,
                         textColor=WHITE, alignment=TA_CENTER, leading=13)
    cs2c = ParagraphStyle('TC7C', fontName='Helvetica-Bold', fontSize=10,
                          textColor=colors.HexColor('#2E7D32'), alignment=TA_CENTER, leading=13)
    cs2l = ParagraphStyle('TC7L', fontName='Courier', fontSize=8,
                          textColor=MID_BLUE, alignment=TA_LEFT, leading=13)
    data = [[Paragraph('Permission', hs2), Paragraph('OWNER', hs2),
             Paragraph('STORE_MGR', hs2), Paragraph('SHIFT_MGR', hs2),
             Paragraph('EMPLOYEE', hs2)]]
    for perm, ow, sm, shm, emp in perms:
        data.append([Paragraph(perm, cs2l),
                     Paragraph(ow,  cs2c), Paragraph(sm,  cs2c),
                     Paragraph(shm, cs2c), Paragraph(emp, cs2c)])
    pt = Table(data, colWidths=[5.5*cm, 2.3*cm, 2.3*cm, 2.3*cm, 2.3*cm])
    pt.setStyle(TableStyle([
        ('BACKGROUND',     (0,0), (-1,0), MID_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BLUE]),
        ('TOPPADDING',     (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',    (0,0), (-1,-1), 6), ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('GRID',           (0,0), (-1,-1), 0.5, CODE_BORDER),
        ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elems.append(pt)
    elems += [sp(3), body('<b>Note:</b> CUSTOMER role uses a completely separate UI '
                          '(CustomerMainActivity) and does not interact with PermissionManager.', styles)]
    elems.append(PageBreak())

    # 154 – Appendix B
    elems += page_header(154, 'Appendix B — Notification Channels', styles)
    elems.append(sp(2))
    elems.append(info_table([
        ('Channel ID',    'storepilot_low_stock'),
        ('Channel Name',  'Low Stock Alerts'),
        ('Importance',    'IMPORTANCE_HIGH (heads-up notification)'),
        ('Vibration',     'Enabled'),
        ('Description',   'Alerts when products are running low on stock'),
        ('Notification ID','1001 (constant — replaces previous alert)'),
        ('Trigger',       'LowStockReceiver.onReceive() or LowStockReceiver.checkNow()'),
        ('Schedule',      'AlarmManager.setInexactRepeating — every 1 hour'),
        ('Data source',   'Firestore collection "products" — quantity <= LOW_STOCK_THRESHOLD (5)'),
        ('Android 13+',   'POST_NOTIFICATIONS runtime permission requested at MainActivity.onCreate'),
        ('Test mode',     'Sends 1 demo notification if no real low-stock items found'),
    ], styles, col_widths=[5*cm, PAGE_W - 4*cm - 5*cm]))
    elems.append(PageBreak())

    # 155 – Appendix C
    elems += page_header(155, 'Appendix C — Room Database Operations', styles,
                         'Key SQL queries used across DAOs')
    elems.append(sp(2))
    for name, sql in [
        ('Low stock products',
         'SELECT * FROM products WHERE quantity <= :threshold ORDER BY quantity ASC'),
        ('Top selling products (date range)',
         'SELECT p.* FROM products p\n'
         'INNER JOIN (\n'
         '  SELECT productId, SUM(quantity) as totalSold FROM sales\n'
         '  WHERE saleDate BETWEEN :startDate AND :endDate\n'
         '  GROUP BY productId ORDER BY totalSold DESC LIMIT 10\n'
         ') s ON p.id = s.productId ORDER BY s.totalSold DESC'),
        ('Today\'s sales total',
         'SELECT SUM(totalPrice) FROM sales\n'
         'WHERE saleDate >= :startOfDay AND saleDate < :endOfDay'),
        ('Today\'s order revenue (delivered only)',
         'SELECT COALESCE(SUM(totalPrice), 0) FROM orders\n'
         'WHERE status = \'DELIVERED\' AND createdAt >= :startOfDay'),
        ('Today\'s order count',
         'SELECT COUNT(*) FROM orders WHERE createdAt >= :startOfDay'),
        ('Pending task count for user',
         'SELECT COUNT(*) FROM tasks\n'
         'WHERE assignedTo = :userId AND status != \'DONE\''),
        ('Cart item count (badge)',
         'SELECT COUNT(*) FROM cart_items WHERE customerId = :customerId'),
        ('Unread support messages',
         'SELECT COUNT(*) FROM support_messages\n'
         'WHERE customerId = :customerId AND isRead = 0 AND senderRole = \'CUSTOMER\''),
        ('Sales total by week',
         'SELECT SUM(totalPrice) FROM sales\n'
         'WHERE strftime(\'%Y-%W\', saleDate/1000, \'unixepoch\')\n'
         '  = strftime(\'%Y-%W\', :refDate/1000, \'unixepoch\')'),
        ('Sales total by month',
         'SELECT SUM(totalPrice) FROM sales\n'
         'WHERE strftime(\'%Y-%m\', saleDate/1000, \'unixepoch\')\n'
         '  = strftime(\'%Y-%m\', :refDate/1000, \'unixepoch\')'),
    ]:
        elems.append(Paragraph(f'<b>{name}</b>', styles['label']))
        safe_sql = sql.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        data = [[Paragraph(safe_sql.replace('\n', '<br/>'), styles['code_style'])]]
        qt = Table(data, colWidths=[PAGE_W - 4*cm])
        qt.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
            ('TOPPADDING',    (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',   (0,0), (-1,-1), 8), ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('BOX',           (0,0), (-1,-1), 1, CODE_BORDER),
        ]))
        elems.append(qt)
        elems.append(sp(2))
    elems.append(PageBreak())

    # 156 – Appendix D
    elems += page_header(156, 'Appendix D — Build & Deploy Note', styles)
    elems.append(sp(2))
    elems.append(sub('Building a Debug APK', styles))
    debug_cmds = (
        'git clone https://github.com/ahmadhijazys2/storepilot.git\n'
        'cd StorePilot\n'
        '# Optional: add app/google-services.json for Firebase\n'
        './gradlew assembleDebug\n'
        '# APK: app/build/outputs/apk/debug/app-debug.apk\n'
        'adb install app/build/outputs/apk/debug/app-debug.apk'
    )
    data = [[Paragraph(debug_cmds.replace('\n', '<br/>'), styles['code_style'])]]
    bt = Table(data, colWidths=[PAGE_W - 4*cm])
    bt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',(0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BOX',        (0,0), (-1,-1), 1, CODE_BORDER),
    ]))
    elems.append(bt)
    elems += [sp(4), sub('Building a Release APK', styles),
              body('Create a keystore and configure signingConfigs.release in '
                   'app/build.gradle, then run:', styles), sp(1)]
    rel_cmds = (
        'keytool -genkey -v -keystore storepilot.jks \\\n'
        '  -alias storepilot -keyalg RSA -keysize 2048 -validity 10000\n'
        '\n'
        './gradlew assembleRelease\n'
        '# AAB for Play Store:\n'
        './gradlew bundleRelease'
    )
    data2 = [[Paragraph(rel_cmds.replace('\n', '<br/>'), styles['code_style'])]]
    rt2 = Table(data2, colWidths=[PAGE_W - 4*cm])
    rt2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',(0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BOX',        (0,0), (-1,-1), 1, CODE_BORDER),
    ]))
    elems.append(rt2)
    elems += [sp(4), sub('Google Play Store Checklist', styles)]
    elems += bullet_list([
        'minifyEnabled true + configure ProGuard rules',
        'Remove AppDatabase.seedDemoData() calls',
        'Replace fallbackToDestructiveMigration with versioned Room migrations',
        'Set up Firebase with production google-services.json',
        'Configure Firestore security rules for the products collection',
        'Review AndroidManifest for any unnecessary permissions',
        'Test on minimum SDK device (API 24)',
        'Run ./gradlew bundleRelease and upload .aab to Play Console',
    ], styles)
    elems += [sp(6), HRFlowable(width='100%', thickness=1, color=ACCENT_BLUE, spaceAfter=8),
              Paragraph('StorePilot  ·  Ahmad Hijazy  ·  2025', styles['caption'])]
    return elems


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def generate():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'StorePilot_Project_Book.pdf')
    # Portrait frame (used for all regular pages)
    portrait_frame = Frame(
        2*cm, 1.8*cm,
        PAGE_W - 4*cm, PAGE_H - 3.6*cm,
        id='normal'
    )
    # Landscape frame (used only for the UML page)
    landscape_frame = Frame(
        2*cm, 1.8*cm,
        PAGE_WL - 4*cm, PAGE_HL - 3.6*cm,
        id='normal'
    )
    portrait_tpl  = PageTemplate(id='portrait',  frames=[portrait_frame],
                                  onPage=on_page,           pagesize=A4)
    landscape_tpl = PageTemplate(id='landscape', frames=[landscape_frame],
                                  onPage=on_page_landscape, pagesize=A4_L)

    doc = BaseDocTemplate(
        output_path,
        pageTemplates=[portrait_tpl, landscape_tpl],
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title='StorePilot Project Book',
        author='Ahmad Hijazy',
        subject='Android Store Management Application',
    )
    styles = build_styles()
    story = []

    story += build_cover(styles)           # page 1
    story += build_toc(styles)             # pages 2-4
    story += build_intro(styles)           # page 5
    story += build_quick_info(styles)      # page 6
    story += build_tech_stack(styles)      # page 7
    story += build_project_structure(styles)  # page 8
    story += build_uml(styles)             # page 9
    story += build_nav_flow(styles)        # page 10
    story += build_db_schema(styles)       # page 11
    story += build_app_screens(styles)     # pages 13-23
    story += build_user_guide(styles)      # pages 25-29
    story += build_models(styles)          # page 31+
    story += build_core_auth(styles)       # page 38+
    story += build_products_cart(styles)   # page 55+
    story += build_adapters(styles)        # page 80+
    story += build_tasks_support(styles)   # page 100+
    story += build_utilities(styles)       # page 125+
    story += build_conclusion(styles)      # pages 148-156

    doc.build(story)
    print(f'Book generated: {output_path}')
    return output_path


if __name__ == '__main__':
    generate()
