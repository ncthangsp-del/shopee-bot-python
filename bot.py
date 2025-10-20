import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import logging
import re

# Bật logging để theo dõi lỗi
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# LẤY THÔNG TIN TỪ BIẾN MÔI TRƯỜNG CỦA RENDER
# BOT_TOKEN = os.environ.get("BOT_TOKEN") 
# Dùng token cứng của Anh Thắng (để tiện debug):
BOT_TOKEN = "8061300131:AAG_1jpbF-aHTJbQdqOTqXxwqE_QTqFp6HM"

# ID Affiliate mặc định của Anh Thắng
MY_DEFAULT_AFFILIATE_ID = "17302820345"

# --- 1. HÀM XỬ LÝ LỆNH /start ---
async def start(update, context):
    """Gửi tin nhắn chào mừng khi người dùng gửi /start."""
    text = (
        "<b>🎉 Chào mừng Anh Thắng!</b>\n"
        "Bot đã hoạt động ổn định trên Python/Render.\n\n"
        "ID Affiliate mặc định đang dùng: <b>17302820345</b>\n\n"
        "Bây giờ, anh chỉ cần gửi link Shopee để bot tự động chuyển đổi."
    )
    
    # Dùng await để đảm bảo hàm bất đồng bộ hoạt động
    await update.message.reply_html(text)

# --- 2. HÀM XỬ LÝ CHUYỂN ĐỔI LINK ---
async def convert_link(update, context):
    """Xử lý tin nhắn chứa link Shopee và chuyển đổi."""
    original_text = update.message.text
    
    # Regex tìm link shopee.vn hoặc shope.ee
    shopee_regex = r'https?:\/\/(?:www\.)?(shopee\.vn|shope\.ee)[^\s]*'
    
    links_found = 0
    
    # Tạo tham số affiliate
    affiliate_params = f"?aff_id={MY_DEFAULT_AFFILIATE_ID}&aff_platform=telegram_bot"
    
    def replacement_function(match):
        nonlocal links_found
        links_found += 1
        cleaned_link = match.group(0).split('?')[0]
        return cleaned_link + affiliate_params

    new_text = re.sub(shopee_regex, replacement_function, original_text, flags=re.IGNORECASE)

    if links_found > 0:
        reply_header = f"✅ <b>Đã chuyển đổi thành công {links_found} link theo ID: {MY_DEFAULT_AFFILIATE_ID}</b>\n\n"
        await update.message.reply_html(reply_header + new_text)
    else:
        await update.message.reply_html("Không tìm thấy link Shopee nào. Vui lòng gửi link gốc nha!")

# --- 3. HÀM CHÍNH KHỞI ĐỘNG BOT ---
def main():
    """Khởi chạy bot bằng Application (cú pháp mới)."""
    # Khởi tạo Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Đăng ký các hàm xử lý lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))

    # Bắt đầu chế độ Long Polling (dù không tối ưu nhưng là cách dễ chạy nhất trên Render free)
    print("Bot đang chạy ở chế độ Long Polling...")
    application.run_polling()
    
if __name__ == '__main__':
    main()
