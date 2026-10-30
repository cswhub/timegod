# TimeGod

一个简洁的 Python 时间处理工具。

## 安装

```bash
pip install timegod

```

## 用法测试
``` py
if __name__ == "__main__":
    print("=" * 60)
    print("TimeGod 测试用例")
    print("=" * 60)

    # ========== 1. None (当前时间) ==========
    print("\n【1. None - 当前时间】")
    tg_now = TimeGod(None)
    print(f"  TimeGod(None).dt = {tg_now.dt}")
    print(f"  TimeGod(None).ts = {tg_now.ts}")
    print(f"  TimeGod(None).iso = {tg_now.iso}")

    # ========== 2. datetime.datetime 对象 ==========
    print("\n【2. datetime.datetime 对象】")
    dt_obj = datetime.datetime(2025, 11, 19, 9, 30, 0)
    tg_dt = TimeGod(dt_obj)
    print("  输入: datetime(2025-11-19 09:30:00)")
    print(f"  TimeGod(dt).dt = {tg_dt.dt}")
    print(f"  TimeGod(dt).ts = {tg_dt.ts}")

    # ========== 3. datetime.date 对象 ==========
    print("\n【3. datetime.date 对象】")
    d_obj = datetime.date(2025, 11, 19)
    tg_d = TimeGod(d_obj)
    print("  输入: date(2025-11-19)")
    print(f"  TimeGod(date).dt = {tg_d.dt} (自动补充 00:00:00)")

    # ========== 4. 时间戳 (秒/毫秒/微秒自动识别) ==========
    print("\n【4. 时间戳自动识别】")

    # 秒级时间戳 (1440086400 = 2015-08-20 16:00:00 UTC)
    ts_sec = 1440086400
    tg_sec = TimeGod(ts_sec)
    print(f"  秒级 ({ts_sec}): {tg_sec.dt}")

    # 毫秒级时间戳
    ts_ms = 1440086400000
    tg_ms = TimeGod(ts_ms)
    print(f"  毫秒级 ({ts_ms}): {tg_ms.dt}")

    # 微秒级时间戳
    ts_us = 1440086400000000
    tg_us = TimeGod(ts_us)
    print(f"  微秒级 ({ts_us}): {tg_us.dt}")

    # ========== 5. MongoDB 格式 ==========
    print("\n【5. MongoDB 格式 ($date)】")
    mongo_dict = {"$date": "2025-11-19T09:30:00.123456Z"}
    tg_mongo = TimeGod(mongo_dict)
    print(f"  输入: {mongo_dict}")
    print(f"  TimeGod(mongo).dt = {tg_mongo.dt}")

    # ========== 6. 字符串格式大全 ==========
    print("\n【6. 字符串格式解析】")

    test_cases = [
        ("20251119", "%Y%m%d"),
        ("2025-11-19", "%Y-%m-%d"),
        ("2025/11/19", "%Y/%m/%d"),
        ("2025-11-19 09:30:00", "%Y-%m-%d %H:%M:%S"),
        ("2025/11/19 09:30:00", "%Y/%m/%d %H:%M:%S"),
        ("2025-11-19T09:30:00", "%Y-%m-%dT%H:%M:%S"),
        ("2025-11-19 09:30:00.123456", "%Y-%m-%d %H:%M:%S.%f"),
        ("2025/11/19 09:30:00.123456", "%Y/%m/%d %H:%M:%S.%f"),
        ("2025-11-19T09:30:00.123456", "%Y-%m-%dT%H:%M:%S.%f"),
        ("2025年11月19日 09:30:00", "%Y年%m月%d日%H:%M:%S"),
    ]

    for s, fmt in test_cases:
        tg = TimeGod(s)
        print(f"  [{fmt:25s}] {s:25s} -> {tg.dt}")

    # ========== 7. ISO 8601 格式 (带时区) ==========
    print("\n【7. ISO 8601 格式 (带时区)】")

    iso_cases = [
        "2025-11-19T09:30:00Z",
        "2025-11-19T09:30:00+00:00",
        "2025-11-19T09:30:00+08:00",
        "2025-11-19T09:30:00.123+08:00",
        "2025-11-19 09:30:00.123456+08:00",
    ]

    for iso in iso_cases:
        tg_local = TimeGod(iso)  # 转为本地时间
        tg_utc = TimeGod(iso)  # 转为 UTC
        print(f"  输入: {iso}")
        print(f"    -> 本地: {tg_local.dt} | UTC: {tg_utc.dt}")

    # ========== 8. 超长微秒截断测试 ==========
    print("\n【8. 超长微秒截断】")
    long_us = "2025-11-19 09:30:00.123456789"  # 9位微秒，超过6位
    tg_long = TimeGod(long_us)
    print(f"  输入: {long_us}")
    print(f"  截断后: {tg_long.dt}")

    # ========== 9. 属性与方法测试 ==========
    print("\n【9. 属性与方法】")
    tg = TimeGod("2025-11-19 09:30:45")
    print(f"  dt = {tg.dt}")
    print(f"  ts = {tg.ts}")
    print(f"  iso = {tg.iso}")
    print(f"  date_str = {tg.date_str}")
    print(f"  year_month = {tg.year_month}")
    print(f"  format() = {tg.format()}")
    print(f"  format('%Y年%m月%d日') = {tg.format('%Y年%m月%d日')}")
    print(f"  __str__ = {tg!s}")
    # print(f"  __str__ = {str(tg)}")

    # ========== 10. 错误处理测试 ==========
    print("\n【10. 错误处理】")

    # 错误的 MongoDB 格式
    try:
        TimeGod({"invalid": "key"})
    except ValueError as e:
        print(f"  错误 MongoDB 格式: {e}")

    # 无法解析的字符串
    try:
        TimeGod("不是时间字符串")
    except ValueError as e:
        print(f"  无效字符串: {e}")

    # 测试星期功能
    print("=" * 60)
    print("星期功能测试")
    print("=" * 60)

    # 测试不同日期
    test_dates = [
        "2025-11-17",  # 周一
        "2025-11-18",  # 周二
        "2025-11-19",  # 周三
        "2025-11-22",  # 周六
        "2025-11-23",  # 周日
    ]

    for date_str in test_dates:
        tg = TimeGod(date_str)
        print(
            f"{tg.date_str} | weekday={tg.weekday} | isoweekday={tg.isoweekday} | {tg.weekday_cn}"
        )

    # 当前时间
    print(f"\n现在: {TimeGod(None).weekday_cn}")

    # 也可以用在 format 中
    tg = TimeGod("2025-11-19")
    print(f"\n自定义格式: {tg.format('%Y-%m-%d')}")

    # ========== 11. 时区转换测试 ==========
    print("\n【11. 时区转换】")
    input_datetime = "2026-06-05 10:00:00"
    tg = TimeGod(input_datetime)
    print(f"传入时间：{input_datetime}")
    tg_utc = tg.change_tz(output_tz=datetime.UTC)
    # tg_utc = tg.change_tz(output_tz=ZoneInfo("UTC"))
    print(f"转换后时间：{tg_utc}")

    print("\n【12. 时区名称查询】")
    print(TimeGod.timezones())

    print("\n【13. 格式化时间差】")

    a = TimeGod("20260226 10:30:30").dt
    b = TimeGod().dt
    print(format_delta(b - a))
    print(format_delta(b - a, "short"))
    print(format_delta(b - a, "iso"))
    print(format_delta(b - a, "total_hours"))
    print(format_delta(b - a, "total_seconds"))

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)



```


