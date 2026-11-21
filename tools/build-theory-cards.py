#!/usr/bin/env python3
"""Dựng lại phần lý thuyết các bài (Toán 12, Vật lí 12, ...) sang dạng thẻ (xem tools/theory-cards/). Chạy: python3 tools/build-theory-cards.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'theory-cards'))
import toan12_ch1, toan12_ch2, toan12_ch34, toan12_ch56, ly12_ch1, ly12_ch2, ly12_ch3, ly12_ch4
for m in [toan12_ch1, toan12_ch2, toan12_ch34, toan12_ch56, ly12_ch1, ly12_ch2, ly12_ch3, ly12_ch4]:
    m.run()
print('Đã dựng thẻ lý thuyết.')
