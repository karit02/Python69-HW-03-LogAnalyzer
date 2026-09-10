from collections import Counter, defaultdict

def analyze_user_activity(log_file_path: str) -> dict:
    #your code here
    #pass
    action_counts = Counter()
    user_actions = defaultdict(int)
    user_durations = defaultdict(float)
    
    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                # ข้ามบรรทัดที่ไม่ครบ 4 elements (<timestamp> <user_id> <action> <duration>)
                if len(parts) != 4:
                    continue
                
                _, user_id, action, duration_str = parts
                
                # ตรวจสอบค่า duration ว่าเป็นตัวเลขหรือไม่
                try:
                    duration = float(duration_str)
                except ValueError:
                    continue

                action_counts[action] += 1
                user_actions[user_id] += 1
                
                # เก็บค่า duration เฉพาะตอนที่ผู้ใช้นั้น login
                if action == "login":
                    user_durations[user_id] = duration
                    
    except FileNotFoundError:
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0
        }

    # กรณีไฟล์ว่างเปล่า หรือไม่มีข้อมูลที่ถูกต้องเลย
    if not user_actions:
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0
        }

    total_users = len(user_actions)
    
    # หาผู้ใช้ที่มีจำนวน action มากที่สุด
    most_active_user = max(user_actions, key=user_actions.get)
    
    # คำนวณค่าเฉลี่ยระยะเวลา session จากผู้ใช้ที่มีการ login
    if user_durations:
        average_session_time = sum(user_durations.values()) / len(user_durations)
    else:
        average_session_time = 0.0

    return {
        "total_users": total_users,
        "action_counts": dict(action_counts),
        "most_active_user": most_active_user,
        "average_session_time": round(average_session_time, 2)
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
