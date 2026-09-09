"""Lightweight process diagnostics; never imports torch or loads a checkpoint."""

import os
from pathlib import Path


def memory_diagnostics(settings):
    limit = settings.balnlp_memory_limit_mb
    rss = None
    peak = None
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("faults", wintypes.DWORD)] + [
                (name, ctypes.c_size_t)
                for name in (
                    "peak",
                    "rss",
                    "peak_paged",
                    "paged",
                    "peak_nonpaged",
                    "nonpaged",
                    "pagefile",
                    "peak_pagefile",
                )
            ]

        data = Counters()
        data.cb = ctypes.sizeof(data)
        handle = ctypes.windll.kernel32.GetCurrentProcess
        handle.restype = wintypes.HANDLE
        query = ctypes.windll.psapi.GetProcessMemoryInfo
        query.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        if query(handle(), ctypes.byref(data), data.cb):
            rss, peak = data.rss / 1048576, data.peak / 1048576
    else:
        try:
            values = dict(
                line.split(":", 1)
                for line in Path("/proc/self/status").read_text().splitlines()
                if ":" in line
            )
            rss = int(values["VmRSS"].split()[0]) / 1024
            peak = int(values["VmHWM"].split()[0]) / 1024
        except (OSError, KeyError, ValueError):
            pass
        for filename in (
            "/sys/fs/cgroup/memory.max",
            "/sys/fs/cgroup/memory/memory.limit_in_bytes",
        ):
            try:
                value = int(Path(filename).read_text().strip()) / 1048576
                if value < 1048576:
                    limit = min(limit, value) if limit else value
            except (OSError, ValueError):
                continue
    return {
        "rss_mb": round(rss, 2) if rss is not None else None,
        "peak_rss_mb": round(peak, 2) if peak is not None else None,
        "limit_mb": limit,
        "minimum_model_budget_mb": settings.balnlp_min_model_memory_mb,
        "mode": settings.balnlp_memory_mode,
    }
