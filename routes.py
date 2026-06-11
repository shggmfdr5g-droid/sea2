# Sea route waypoints with transit times for realistic shipping lane visualization
# Format: [lat, lng, "Port/Segment Name", transit_days_from_previous]

ROUTE_WAYPOINTS = {
    # 上海 → 洛杉矶 (North Pacific, ~14-16 days)
    ("上海", "洛杉矶"): [
        [31.23, 121.47, "上海", 0],
        [30.5, 123.0,  "东海", 0.5],
        [29.0, 126.0,  "琉球群岛海域", 1],
        [30.0, 130.0, "太平洋西北", 0.5],
        [35.0, 140.0, "日本以南海域", 1.5],
        [40.0, 150.0, "北太平洋", 2],
        [45.0, 160.0, "北太平洋中部", 2],
        [48.0, 170.0, "阿留申群岛以南海域", 1.5],
        [48.0, -175.0, "北太平洋", 1],
        [45.0, -160.0, "东北太平洋", 1.5],
        [42.0, -145.0, "东北太平洋", 1.5],
        [38.0, -130.0, "加州外海", 1],
        [34.5, -121.0, "加州沿海", 0.5],
        [33.77, -118.22, "洛杉矶", 0.5],
    ],
    # 上海 → 鹿特丹 (via Suez, ~28-32 days)
    ("上海", "鹿特丹"): [
        [31.23, 121.47, "上海", 0],
        [25.0, 120.0, "台湾海峡", 1],
        [22.0, 115.0, "南海", 0.5],
        [10.0, 110.0, "南海中部", 1.5],
        [1.26, 103.84, "新加坡海峡", 2],
        [5.0, 95.0, "马六甲海峡", 1],
        [6.0, 78.0, "印度洋", 1.5],
        [12.0, 55.0, "阿拉伯海", 2],
        [17.0, 41.0, "红海", 2],
        [30.0, 32.5, "苏伊士运河", 2],
        [31.5, 31.5, "塞得港", 0.5],
        [35.5, 28.0, "地中海东部", 1],
        [37.0, 15.0, "地中海中部", 1.5],
        [38.0, 10.0, "地中海西部", 1.5],
        [42.0, 5.0, "巴利阿里海域", 1],
        [46.0, -1.0, "比斯开湾", 2],
        [50.0, 0.0, "英吉利海峡", 1.5],
        [51.5, 3.0, "北海", 1],
        [51.91, 4.48, "鹿特丹", 0.5],
    ],
    # 上海 → 温哥华 (~14 days)
    ("上海", "温哥华"): [
        [31.23, 121.47, "上海", 0],
        [32.0, 125.0, "东海", 0.5],
        [34.0, 130.0, "对马海峡", 1],
        [38.0, 138.0, "日本海", 1],
        [43.0, 145.0, "北海道以南海域", 1.5],
        [46.0, 155.0, "千岛群岛外海", 1.5],
        [50.0, 165.0, "北太平洋", 2],
        [53.0, 175.0, "白令海", 1.5],
        [54.0, -170.0, "阿拉斯加湾", 1.5],
        [52.0, -150.0, "阿拉斯加湾", 1],
        [50.0, -135.0, "加拿大西海岸", 1.5],
        [49.28, -123.12, "温哥华", 1],
    ],
    # 宁波 → 洛杉矶
    ("宁波", "洛杉矶"): [
        [29.87, 121.55, "宁波", 0],
        [29.0, 124.0, "东海", 0.5],
        [30.0, 130.0, "太平洋西北", 1],
        [35.0, 142.0, "日本外海", 1.5],
        [40.0, 152.0, "北太平洋", 2],
        [45.0, 165.0, "北太平洋中部", 2],
        [48.0, 180.0, "国际日期变更线", 1.5],
        [47.0, -165.0, "北太平洋", 1.5],
        [43.0, -150.0, "东北太平洋", 1.5],
        [38.0, -132.0, "加州外海", 1.5],
        [33.77, -118.22, "洛杉矶", 1],
    ],
    # 深圳 → 洛杉矶
    ("深圳", "洛杉矶"): [
        [22.54, 113.88, "深圳", 0],
        [21.0, 115.0, "南海", 0.5],
        [20.0, 118.0, "巴士海峡", 1],
        [22.0, 125.0, "菲律宾海", 1.5],
        [27.0, 135.0, "太平洋西部", 2],
        [33.0, 145.0, "太平洋", 2],
        [40.0, 155.0, "北太平洋", 2],
        [45.0, 168.0, "北太平洋中部", 2],
        [48.0, -178.0, "北太平洋", 1.5],
        [45.0, -158.0, "东北太平洋", 1.5],
        [40.0, -140.0, "东北太平洋", 1.5],
        [35.0, -125.0, "加州外海", 1],
        [33.77, -118.22, "洛杉矶", 1],
    ],
    # 青岛 → 温哥华
    ("青岛", "温哥华"): [
        [36.07, 120.38, "青岛", 0],
        [35.0, 124.0, "黄海", 0.5],
        [34.0, 130.0, "对马海峡", 1],
        [38.0, 138.0, "日本海", 1],
        [44.0, 148.0, "千岛群岛", 1.5],
        [50.0, 162.0, "北太平洋", 2],
        [54.0, 180.0, "白令海", 1.5],
        [55.0, -165.0, "阿拉斯加湾", 1.5],
        [52.0, -145.0, "阿拉斯加湾", 1.5],
        [49.28, -123.12, "温哥华", 1.5],
    ],
    # 上海 → 汉堡 (via Suez)
    ("上海", "汉堡"): [
        [31.23, 121.47, "上海", 0],
        [22.0, 115.0, "南海", 1.5],
        [1.26, 103.84, "新加坡海峡", 3],
        [6.0, 78.0, "印度洋", 2],
        [12.0, 55.0, "阿拉伯海", 2],
        [17.0, 41.0, "红海", 2],
        [30.0, 32.5, "苏伊士运河", 2],
        [35.5, 28.0, "地中海东部", 1],
        [37.0, 10.0, "地中海", 1.5],
        [36.0, -5.0, "直布罗陀海峡", 1.5],
        [45.0, -8.0, "比斯开湾", 2],
        [50.5, 0.5, "英吉利海峡", 1.5],
        [53.5, 5.0, "北海", 1],
        [53.55, 9.97, "汉堡", 1],
    ],
    # 深圳 → 汉堡
    ("深圳", "汉堡"): [
        [22.54, 113.88, "深圳", 0],
        [20.0, 115.0, "南海", 0.5],
        [1.26, 103.84, "新加坡", 3],
        [6.0, 78.0, "印度洋", 2],
        [12.0, 55.0, "阿拉伯海", 2],
        [30.0, 32.5, "苏伊士运河", 3],
        [35.5, 28.0, "地中海", 1],
        [36.0, -5.0, "直布罗陀", 1.5],
        [45.0, -8.0, "比斯开湾", 2],
        [50.5, 0.5, "英吉利海峡", 1.5],
        [53.55, 9.97, "汉堡", 1.5],
    ],
    # 天津 → 汉堡
    ("天津", "汉堡"): [
        [38.98, 117.72, "天津", 0],
        [35.0, 122.0, "黄海", 1],
        [31.0, 123.0, "东海", 1],
        [22.0, 115.0, "南海", 1.5],
        [1.26, 103.84, "新加坡", 3],
        [6.0, 78.0, "印度洋", 2],
        [12.0, 55.0, "阿拉伯海", 2],
        [30.0, 32.5, "苏伊士运河", 3],
        [35.5, 28.0, "地中海", 1],
        [36.0, -5.0, "直布罗陀", 1.5],
        [45.0, -8.0, "比斯开湾", 2],
        [53.55, 9.97, "汉堡", 2],
    ],
}

def get_route_waypoints(origin, destination):
    """Get waypoints for a route, returns list of [lat, lng, name, days]"""
    key = (origin, destination)
    if key in ROUTE_WAYPOINTS:
        return ROUTE_WAYPOINTS[key]
    
    rev_key = (destination, origin)
    if rev_key in ROUTE_WAYPOINTS:
        rev = list(reversed(ROUTE_WAYPOINTS[rev_key]))
        # Recalculate transit days in reverse
        for i in range(len(rev)):
            rev[i] = [rev[i][0], rev[i][1], rev[i][2], 0]
        for i in range(1, len(rev)):
            orig_idx = len(ROUTE_WAYPOINTS[rev_key]) - 1 - i
            rev[i][3] = ROUTE_WAYPOINTS[rev_key][orig_idx + 1][3] if orig_idx + 1 < len(ROUTE_WAYPOINTS[rev_key]) else 0
        return rev
    
    return None

def get_route_waypoints_simple(origin, destination):
    """Get waypoints as simple [lat, lng] pairs for map drawing"""
    wp = get_route_waypoints(origin, destination)
    if wp:
        return [[p[0], p[1]] for p in wp]
    return None

def get_transit_info(origin, destination):
    """Get itinerary with transit days and cumulative days"""
    wp = get_route_waypoints(origin, destination)
    if not wp:
        return None
    
    info = []
    cumulative = 0
    total_days = sum(p[3] for p in wp)
    
    for i, p in enumerate(wp):
        cumulative += p[3]
        info.append({
            "name": p[2],
            "lat": p[0],
            "lng": p[1],
            "transit_days": p[3],
            "cumulative_days": round(cumulative, 1),
            "is_port": (i == 0 or i == len(wp) - 1),
        })
    
    return {"stops": info, "total_days": round(total_days, 1)}

def get_current_position(origin, destination, etd, eta, status="scheduled"):
    """Calculate current vessel position along the route"""
    if status != "in_transit":
        return None
    
    wp = get_route_waypoints(origin, destination)
    if not wp:
        return None
    
    from datetime import datetime, timedelta
    try:
        etd_dt = datetime.strptime(etd, "%Y-%m-%d")
        eta_dt = datetime.strptime(eta, "%Y-%m-%d")
    except:
        return None
    
    now = datetime.now()
    total_days = (eta_dt - etd_dt).days
    elapsed = (now - etd_dt).days
    
    if elapsed <= 0:
        return {"lat": wp[0][0], "lng": wp[0][1], "progress": 0, "next_stop": wp[1][2]}
    if elapsed >= total_days:
        return {"lat": wp[-1][0], "lng": wp[-1][1], "progress": 1, "next_stop": "已到达"}
    
    # Find position along route
    progress = elapsed / total_days if total_days > 0 else 0
    total_cumulative = sum(p[3] for p in wp)
    if total_cumulative <= 0:
        total_cumulative = len(wp) - 1
        segment_progress = progress * total_cumulative
    else:
        segment_progress = progress * total_cumulative
    
    # Find which segment we're in
    cumulative = 0
    for i in range(len(wp) - 1):
        next_cumulative = cumulative + wp[i+1][3]
        if segment_progress <= next_cumulative or i == len(wp) - 2:
            seg_fraction = (segment_progress - cumulative) / wp[i+1][3] if wp[i+1][3] > 0 else 0.5
            seg_fraction = max(0, min(1, seg_fraction))
            lat = wp[i][0] + (wp[i+1][0] - wp[i][0]) * seg_fraction
            lng = wp[i][1] + (wp[i+1][1] - wp[i][1]) * seg_fraction
            return {
                "lat": round(lat, 4),
                "lng": round(lng, 4),
                "progress": round(progress * 100, 1),
                "next_stop": wp[i+1][2],
                "days_to_next": round(wp[i+1][3] * (1 - seg_fraction), 1),
            }
        cumulative = next_cumulative
    
    return {"lat": wp[-1][0], "lng": wp[-1][1], "progress": 100, "next_stop": "已到达"}

if __name__ == "__main__":
    # Test
    info = get_transit_info("上海", "洛杉矶")
    print(f"Shanghai->LA: {info['total_days']} days, {len(info['stops'])} stops")
    for s in info['stops']:
        print(f"  {s['cumulative_days']:5.1f}d  {s['name']} (+{s['transit_days']}d)")
    
    pos = get_current_position("上海", "洛杉矶", "2026-06-15", "2026-06-30", "in_transit")
    if pos:
        print(f"\nCurrent position: {pos['lat']}, {pos['lng']}")
        print(f"Progress: {pos['progress']}%, Next: {pos['next_stop']} in {pos['days_to_next']}d")
