#!/usr/bin/env python3
# EasyTinySAConnector
# Версия 0.1 (Alpha)
# Создано Corvax

from __future__ import annotations
from dataclasses import dataclass

import tinysaeasyconnector.lib as lib


@dataclass(frozen=True)
class SearchedObj:
    dB: float
    freq: int | float

class TinySAConnector:
    nv: lib.tinySA
    freq_start: int | float
    freq_stop: int | float
    frequencies: list[float] | None

    def __init__(self, freq_start=0, freq_stop=0):
        self.nv = lib.tinySA(lib.getport())
        self.freq_start = freq_start
        self.freq_stop = freq_stop
        self.frequencies = self.nv.frequencies

    def scan(self) -> list[int]:
        return self.nv.scan()

    def set_freq(self, freq_start: int, freq_stop: int):
        self.freq_start = freq_start
        self.freq_stop = freq_stop
        self.nv.set_sweep(self.freq_start, self.freq_stop)
        self.nv.fetch_frequencies()
        self.frequencies = self.nv.frequencies

    def debug(self) -> bool:
        self.set_freq(100, 400)
        scan_var = self.nv.data(0)
        if len(self.nv.frequencies) == len(scan_var):
            return True
        else:
            return False

    def capture(self, file_name: str):
        img = self.nv.capture()
        img.save(file_name + '.png')

    def get_graph(self):
        self.nv.logmag(self.nv.data(0))

    def default_searcher(self, freq_start: int, freq_stop: int, infelicity: int, warn_level: int, time=3) -> [SearchedObj]:
        from statistics import median
        from time import sleep

        self.set_freq(freq_start * 1000000, freq_stop * 1000000)
        sleep(time)
        scan_var = self.nv.data(0)
        median_freq = median(scan_var)

        levelPerFreq = []
        for i in range(len(self.frequencies) - 1):
            levelPerFreq.append([scan_var[i], self.frequencies[i]])

        for i in range(len(levelPerFreq) - 1):
            for j in range(len(levelPerFreq) - 1 - i):
                if levelPerFreq[j][0] > levelPerFreq[j + 1][0]:
                    levelPerFreq[j], levelPerFreq[j + 1] = levelPerFreq[j + 1], levelPerFreq[j]

        searched = []
        for i in reversed(levelPerFreq):
            if i[0] - median_freq > warn_level:
                if not searched:
                    searched.append(SearchedObj(i[0], i[1] / 1000000))
                for x in searched:
                    if -infelicity <= x.freq - i[1] / 1000000 <= infelicity or x.freq == i[1]:
                        break
                else:
                    searched.append(SearchedObj(i[0], i[1] / 1000000))
            else:
                break

        return searched
