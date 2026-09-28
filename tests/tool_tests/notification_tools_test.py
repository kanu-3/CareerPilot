from backend.tools.notification_tool import (
    create_notification,
    get_notifications,
    mark_notification_read,
)


USER_ID = 1


print("\n========== CREATE NOTIFICATION ==========")

notification = create_notification(
    user_id=USER_ID,
    notification_type="learning",
    title="New learning task",
    message="You have a high-priority LangChain learning task.",
)

print(notification)


notification_id = notification["notification_id"]


print("\n========== GET NOTIFICATIONS ==========")

notifications = get_notifications(
    user_id=USER_ID,
)

for item in notifications:
    print(item)


print("\n========== GET UNREAD NOTIFICATIONS ==========")

unread = get_notifications(
    user_id=USER_ID,
    unread_only=True,
)

for item in unread:
    print(item)


print("\n========== MARK AS READ ==========")

result = mark_notification_read(
    user_id=USER_ID,
    notification_id=notification_id,
)

print(result)


print("\n========== VERIFY ==========")

notifications = get_notifications(
    user_id=USER_ID,
)

for item in notifications:
    print(item)