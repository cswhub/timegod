"""TimeGod - 一个简洁的时间处理工具。"""

import datetime
from datetime import tzinfo
import re
from zoneinfo import ZoneInfo, available_timezones
from typing import Literal

TimeInTypes = None | int | float | str | datetime.date | datetime.datetime | dict
TzTypes = tzinfo | Literal["auto"] | None | str


class TimeGod:
    __slots__ = (
        "_output_tz",
        "_ts",
    )

    def __init__(self, value: TimeInTypes = None, output_tz: TzTypes = None) -> None:
        """当output_tz为None时会返回不带时区信息的时间
        当output_tz为auto时会返回带当前时区信息的时间
        当指定output_tz时区时ZoneInfo("Asia/Shanghai")/datetime.UTC会返回指定时区的时间
        output_tz影响的只有输出
        """
        self._ts: float = self._parse(value)
        self._output_tz: TzTypes = output_tz

    def _parse(self, value: TimeInTypes) -> float:
        if value is None:
            return datetime.datetime.now(datetime.UTC).timestamp()
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        if isinstance(value, datetime.date):
            return datetime.datetime.combine(value, datetime.time.min).timestamp()
        if isinstance(value, (int, float)):
            # 秒/毫秒/微秒 自动识别
            if value > 1e15:
                return value / 1e6
            if value > 1e12:
                return value / 1e3
            return float(value)
        if isinstance(value, dict):  # MongoDB
            date_str = value.get("$date")
            if not date_str:
                raise ValueError(f"无法解析的时间字符串: {value}")
            return (
                datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.UTC).timestamp()
            )
        if isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value).timestamp()
            except ValueError:
                pass

            value = re.sub(r"(\.\d{6})\d+", r"\1", value.strip())
            fmts = (
                "%Y/%m/%d",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S.%f",
                "%Y年%m月%d日",
                "%Y年%-m月%-d日",
                "%Y年%m月%d日 %H:%M:%S",
                "%Y年%-m月%-d日 %H:%M:%S",
                "%Y年%m月%d日 %H:%M:%S.%f",
                "%Y年%-m月%-d日 %H:%M:%S.%f",
            )
            for fmt in fmts:
                try:
                    return datetime.datetime.strptime(value, fmt).timestamp()
                except ValueError:
                    pass

            raise ValueError(f"无法解析的时间字符串: {value}")
        raise TypeError(f"不支持的类型 {type(value)}")

    @property
    def dt(self) -> datetime.datetime:
        """返回datetime格式对象
        其他属性依赖这个属性，输出时区就作用在这个属性上
        """
        if self._output_tz == "auto":
            return datetime.datetime.fromtimestamp(self._ts).astimezone()
        if isinstance(self._output_tz, str):
            return datetime.datetime.fromtimestamp(self._ts, tz=ZoneInfo(self._output_tz))
        return datetime.datetime.fromtimestamp(self._ts, tz=self._output_tz)

    @property
    def ts(self) -> float:
        """返回时间戳"""
        return self._ts

    @property
    def iso(self) -> str:
        """返回时间标准输出格式"""
        return self.dt.isoformat()

    @property
    def date_str(self) -> str:
        """返回日期字符串"""
        return self.dt.strftime("%Y-%m-%d")

    @property
    def year_month(self) -> str:
        """返回年月6位字符串"""
        return self.dt.strftime("%Y%m")

        # 新增：星期相关属性

    @property
    def weekday(self) -> int:
        """返回星期几 (0=周一, 6=周日)"""
        return self.dt.weekday()

    @property
    def weekday_cn(self) -> str:
        """返回中文星期几"""
        # week_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        week_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
        return week_map[self.dt.weekday()]

    @property
    def isoweekday(self) -> int:
        """返回ISO星期几 (1=周一, 7=周日)"""
        return self.dt.isoweekday()

    def format(self, out_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """自定义格式输出"""
        return self.dt.strftime(out_format)

    def change_tz(self, output_tz: TzTypes = None) -> "TimeGod":
        """修改输出时区，返回一个新的实例"""
        return TimeGod(self._ts, output_tz=output_tz)

    # ---------- 魔术方法 ----------
    def __str__(self) -> str:
        """支持str方法"""
        return self.iso

    @staticmethod
    def timezones():
        return sorted(available_timezones())


# ========== timedelta 格式化工具函数 ==========
def format_delta(delta: datetime.timedelta, fmt: str = "zh") -> str:
    """美化输出 timedelta

    fmt选项:
        'zh': '2天3小时15分钟'
        'short': '2d3h15m'
        'iso': 'P2DT3H15M'
        'total_hours': '51.25' (总小时数)
        'total_seconds': '184500' (总秒数)
    """
    total_seconds = int(delta.total_seconds())
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if fmt == "zh":
        parts = []
        if days:
            parts.append(f"{days}天")
        if hours:
            parts.append(f"{hours}小时")
        if minutes:
            parts.append(f"{minutes}分钟")
        if seconds and not days:
            parts.append(f"{seconds}秒")
        return "".join(parts) or "0秒"

    if fmt == "short":
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds and not days:
            parts.append(f"{seconds}s")
        return "".join(parts) or "0s"

    if fmt == "iso":
        return f"P{days}DT{hours}H{minutes}M{seconds}S"

    if fmt == "total_hours":
        return f"{total_seconds / 3600:.2f}"

    if fmt == "total_seconds":
        return str(total_seconds)

    raise ValueError(f"未知格式: {fmt}")
