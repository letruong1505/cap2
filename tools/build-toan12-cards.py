#!/usr/bin/env python3
"""Dựng lại phần lý thuyết Toán 12 sang dạng thẻ (xem tools/toan12-cards/). Chạy: python3 tools/build-toan12-cards.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toan12-cards'))
import ch1, ch2, ch34, ch56
for m in [ch1, ch2, ch34, ch56]:
    m.run()
print('Đã dựng thẻ Toán 12.')
