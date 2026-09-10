from collections import Counter, defaultdict


def analyze_user_activity(log_file_path: str) -> dict:
    #your code here
    #pass
    users = set()
    action_counts = Counter()
    user_durations = defaultdict(int)
    login_durations = []

    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()

                # ข้ามบรรทัดที่รูปแบบไม่ถูกต้อง
                if len(parts) != 4:
                    continue

                timestamp, user_id, action, duration_str = parts

                # ตรวจสอบ duration ว่าเป็นตัวเลขหรือไม่
                try:
                    duration = int(duration_str)
                except ValueError:
                    continue

                # เก็บข้อมูล
                users.add(user_id)
                action_counts[action] += 1
                user_durations[user_id] += duration

                # เก็บ duration เฉพาะ login
                if action == "login":
                    login_durations.append(duration)

    except FileNotFoundError:
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0
        }

    # หา user ที่มี duration รวมมากที่สุด
    if user_durations:
        most_active_user = max(
            user_durations,
            key=user_durations.get
        )
    else:
        most_active_user = None

    # ค่าเฉลี่ย duration ของ login
    if login_durations:
        average_session_time = sum(login_durations) / len(login_durations)
    else:
        average_session_time = 0.0

    return {
        "total_users": len(users),
        "action_counts": dict(action_counts),
        "most_active_user": most_active_user,
        "average_session_time": average_session_time
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")

    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',  # <----ในส่วนนี้ผมได้เข้าไปแก้ไขใน log จึงได้เป็น u002
#  'total_users': 2}