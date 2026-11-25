"""
Tweakable numbers in ONE place.

Change a value here and it updates everywhere it is used.
(Hospital name, Patient ID prefix and records-per-page are NOT here: the Super Admin
changes those in the app under  System settings.)
"""

# --- Patient registration ---------------------------------------------------
MAX_PHOTO_BYTES = 2 * 1024 * 1024        # largest profile picture allowed (2 MB)
MIN_BIRTH_YEAR = 1900                    # earliest date of birth accepted

# --- Dashboards: how many rows each card shows ------------------------------
DASHBOARD_RECENT_PATIENTS = 6            # "Recent patient registrations"
DASHBOARD_RECENT_ACTIVITIES = 8          # "Recent activities"
DASHBOARD_RECENT_ADMINS = 5              # "Newest Admin accounts" (Super Admin)
DASHBOARD_CURRENT_ADMISSIONS = 5         # "Currently admitted" (Admin)
NOTIFICATION_COUNT = 6                   # items in the top-bar bell menu

# --- Charts -----------------------------------------------------------------
SUPER_ADMIN_CHART_MONTHS = 6             # Super Admin dashboard bar chart
ADMIN_CHART_DAYS = 7                     # Admin dashboard line chart
REPORT_CHART_MONTHS = 12                 # Reports page bar chart
TOP_ACTIVITY_TYPES = 8                   # "Activity by type" list on Reports

# --- Table page sizes (patient & admission lists use System settings) -------
ADMIN_LIST_PER_PAGE = 10
ACTIVITY_LOG_PER_PAGE = 20

# --- Admissions -------------------------------------------------------------
FUTURE_TOLERANCE_MINUTES = 5             # clock-difference allowance for "not in the future"

# --- Reports: age groups as (label, min_age, max_age) -----------------------
AGE_GROUPS = [
    ("0-12", 0, 12),
    ("13-19", 13, 19),
    ("20-39", 20, 39),
    ("40-59", 40, 59),
    ("60+", 60, 200),
]
