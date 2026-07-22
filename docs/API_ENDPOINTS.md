# URL Endpoints Reference

Below is the list of routed URL paths and associated controllers.

## Accounts Module
- `/accounts/register/` [GET/POST]: Registration page.
- `/accounts/login/` [GET/POST]: Account login.
- `/accounts/logout/` [POST/GET]: Log out session.
- `/accounts/profile/` [GET/POST]: View and edit user details.

## Core Module
- `/` [GET]: Core homepage / landing panel.

## Lost & Found Module
- `/lostfound/lost/` [GET]: Search and list lost item reports.
- `/lostfound/lost/new/` [GET/POST]: Report a new lost item.
- `/lostfound/lost/<int:pk>/` [GET]: Detailed view of a lost item + suggested matches list.
- `/lostfound/lost/<int:pk>/edit/` [GET/POST]: Edit a lost item report.
- `/lostfound/found/` [GET]: Search and list found items.
- `/lostfound/found/new/` [GET/POST]: Report a found item.
- `/lostfound/found/<int:pk>/` [GET]: View found item details + claim submission form or claim list.
- `/lostfound/found/<int:found_item_pk>/claim/` [POST]: Submit a claim request.
- `/lostfound/claim/<int:pk>/action/` [POST]: Finder or staff approval/rejection action for a claim.

## Grievance Module
- `/grievance/` [GET]: List submitted grievances.
- `/grievance/new/` [GET/POST]: Submit a new grievance.
- `/grievance/<int:pk>/` [GET]: Detail view of grievance, audit logs, assignment form, and status transition form.
- `/grievance/<int:pk>/assign/` [POST]: Staff/Admin assignment handler update.
- `/grievance/<int:pk>/transition/` [POST]: Status transition update handler.

## Dashboard Module
- `/dashboard/` [GET]: Consolidated control panel for staff and administrators.

## Notifications Module
- `/notifications/` [GET]: Notification feeds list.
- `/notifications/<int:pk>/read/` [POST]: Mark a specific notification read.
- `/notifications/read-all/` [POST]: Mark all notifications read.
