// Trắc nghiệm gợi ý nhóm công nghệ cho mục Định hướng công nghệ quốc gia (chấm điểm trên máy, không gửi đi đâu ngoài phụ huynh khi con bật chia sẻ).
// w: điểm cộng cho từng nhóm (id trong national-data.js). Gợi ý theo sở thích, không phải đánh giá năng lực.
window.NATIONAL_QUIZ = {
 subjects: ['Toán', 'Vật lí', 'Hóa học', 'Sinh học', 'Tin học', 'Tiếng Anh', 'Địa lí'],
 questions: [
  {
   "q": "Cuối tuần rảnh, em thích nhất việc nào?",
   "options": [
    {
     "t": "Tự mày mò làm game, ứng dụng hoặc trang web",
     "w": {
      "so": 2,
      "an": 1
     }
    },
    {
     "t": "Lắp ráp, tháo máy, làm mô hình chạy được",
     "w": {
      "robot": 2,
      "rail": 1,
      "chip": 1
     }
    },
    {
     "t": "Làm thí nghiệm, trồng cây, chăm con vật",
     "w": {
      "sinh": 2,
      "nl": 1
     }
    },
    {
     "t": "Xem phim khoa học về vũ trụ, máy bay, đại dương",
     "w": {
      "hk": 2,
      "bien": 1
     }
    }
   ]
  },
  {
   "q": "Điều nào làm em tò mò nhất?",
   "options": [
    {
     "t": "AI trả lời được như người là nhờ đâu",
     "w": {
      "so": 2,
      "an": 1
     }
    },
    {
     "t": "Tin nhắn, video bay trong không khí tới điện thoại thế nào",
     "w": {
      "mang": 2,
      "chip": 1
     }
    },
    {
     "t": "Con chip bé xíu mà tính toán được nhiều đến vậy",
     "w": {
      "chip": 2,
      "so": 1
     }
    },
    {
     "t": "Tàu chạy rất nhanh mà vẫn êm và an toàn",
     "w": {
      "rail": 2,
      "robot": 1
     }
    }
   ]
  },
  {
   "q": "Thử thách nào em muốn thử?",
   "options": [
    {
     "t": "Giải mật mã, tìm lỗi bảo mật trong một chương trình",
     "w": {
      "an": 2,
      "so": 1
     }
    },
    {
     "t": "Thiết kế cây cầu hoặc con đường chịu được xe nặng",
     "w": {
      "rail": 2,
      "bien": 1
     }
    },
    {
     "t": "Điều khiển máy bay mô hình hoặc xe điều khiển từ xa",
     "w": {
      "hk": 2,
      "robot": 1
     }
    },
    {
     "t": "Khám phá hang động, đá khoáng, đáy biển",
     "w": {
      "bien": 2,
      "nl": 1
     }
    }
   ]
  },
  {
   "q": "Em muốn công nghệ giúp ích cho cuộc sống ở điểm nào?",
   "options": [
    {
     "t": "Chữa bệnh, làm thuốc, bảo vệ sức khỏe",
     "w": {
      "sinh": 2
     }
    },
    {
     "t": "Có điện sạch, pin bền, bớt ô nhiễm",
     "w": {
      "nl": 2
     }
    },
    {
     "t": "Bảo vệ mọi người khỏi lừa đảo, tin giả, tin tặc",
     "w": {
      "an": 2,
      "so": 1
     }
    },
    {
     "t": "Đi lại nhanh, an toàn, kết nối mọi nơi",
     "w": {
      "rail": 2,
      "hk": 1,
      "mang": 1
     }
    }
   ]
  },
  {
   "q": "Em hợp với kiểu làm việc nào?",
   "options": [
    {
     "t": "Ngồi máy tính nhiều, viết chương trình",
     "w": {
      "so": 2,
      "an": 1,
      "mang": 1
     }
    },
    {
     "t": "Phòng thí nghiệm: đo đạc, thử nghiệm",
     "w": {
      "sinh": 1,
      "nl": 1,
      "chip": 2
     }
    },
    {
     "t": "Xưởng: lắp đặt, vận hành máy móc",
     "w": {
      "robot": 2,
      "rail": 1,
      "nl": 1
     }
    },
    {
     "t": "Ngoài hiện trường, được đi nhiều nơi",
     "w": {
      "bien": 2,
      "rail": 1,
      "hk": 1
     }
    }
   ]
  },
  {
   "q": "Em tự hào nhất khi nào?",
   "options": [
    {
     "t": "Chương trình hoặc máy em làm chạy đúng",
     "w": {
      "so": 1,
      "robot": 2
     }
    },
    {
     "t": "Em tìm ra lỗi mà người khác bỏ sót",
     "w": {
      "an": 2,
      "chip": 1
     }
    },
    {
     "t": "Em hiểu cơ thể hoặc sinh vật hoạt động ra sao",
     "w": {
      "sinh": 2
     }
    },
    {
     "t": "Em tính ra được con số chính xác",
     "w": {
      "chip": 1,
      "hk": 1,
      "nl": 1,
      "mang": 1
     }
    }
   ]
  },
  {
   "q": "Nếu làm một dự án, em chọn dự án nào?",
   "options": [
    {
     "t": "Ứng dụng AI hỗ trợ học tập",
     "w": {
      "so": 2
     }
    },
    {
     "t": "Robot tự dọn bàn học",
     "w": {
      "robot": 2
     }
    },
    {
     "t": "Hệ thống đèn chạy bằng pin mặt trời",
     "w": {
      "nl": 2,
      "chip": 1
     }
    },
    {
     "t": "Tên lửa nước hoặc máy bay mô hình",
     "w": {
      "hk": 2
     }
    }
   ]
  },
  {
   "q": "Thế giới nào làm em hứng thú nhất?",
   "options": [
    {
     "t": "Internet, sóng điện thoại, vệ tinh liên lạc",
     "w": {
      "mang": 2,
      "hk": 1
     }
    },
    {
     "t": "Tế bào, gen, vi khuẩn",
     "w": {
      "sinh": 2
     }
    },
    {
     "t": "Biển sâu, dầu khí, lòng đất",
     "w": {
      "bien": 2
     }
    },
    {
     "t": "Vật liệu mới: nhẹ hơn, bền hơn, dẫn điện tốt hơn",
     "w": {
      "nl": 2,
      "chip": 1
     }
    }
   ]
  },
  {
   "q": "Gặp bài khó, em thường làm gì?",
   "options": [
    {
     "t": "Thử đi thử lại trên máy tính",
     "w": {
      "so": 1,
      "an": 1
     }
    },
    {
     "t": "Vẽ sơ đồ, tính toán bằng công thức",
     "w": {
      "chip": 1,
      "mang": 1,
      "hk": 1,
      "rail": 1
     }
    },
    {
     "t": "Làm thí nghiệm thật để kiểm tra",
     "w": {
      "sinh": 1,
      "nl": 1,
      "bien": 1
     }
    },
    {
     "t": "Tháo ra lắp lại cho hiểu",
     "w": {
      "robot": 2,
      "rail": 1
     }
    }
   ]
  },
  {
   "q": "Em thích làm việc theo cách nào?",
   "options": [
    {
     "t": "Một mình, tập trung thật sâu",
     "w": {
      "an": 1,
      "so": 1,
      "chip": 1
     }
    },
    {
     "t": "Nhóm nhỏ cùng làm một sản phẩm",
     "w": {
      "robot": 1,
      "nl": 1,
      "mang": 1
     }
    },
    {
     "t": "Đội lớn ở hiện trường",
     "w": {
      "bien": 1,
      "rail": 1,
      "hk": 1
     }
    },
    {
     "t": "Cùng bác sĩ, nhà khoa học nghiên cứu",
     "w": {
      "sinh": 2
     }
    }
   ]
  }
 ]
};
