import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

# LẤY THÔNG TIN TỪ BIẾN MÔI TRƯỜNG CỦA RENDER
# TOKEN = os.environ.get("BOT_TOKEN") 
# Mặc định BOT_TOKEN của Anh Thắng (để tiện debug):
BOT_TOKEN = "8061300131:AAG_1jpbF-aHTJbQdqOTqXxwqE_QTqFp6HM"

# ID Affiliate mặc định của Anh Thắng
MY_DEFAULT_AFFILIATE_ID = "17302820345"

# --- 1. HÀM XỬ LÝ LỆNH /start ---
def start(update, context):
    """Gửi tin nhắn chào mừng khi người dùng gửi /start."""
    chat_id = update.message.chat_id
    
    # Do tạm thời không dùng Google Sheet, chúng ta sẽ bỏ qua phần kiểm tra ID.
    text = (
        "<b>🎉 Chào mừng Anh Thắng!</b>\n"
        "Bot đã hoạt động ổn định trên Python/Render.\n\n"
        "ID Affiliate mặc định đang dùng: <b>17302820345</b>\n\n"
        "Bây giờ, anh chỉ cần gửi link Shopee để bot tự động chuyển đổi."
    )
    
    # context.bot.send_message là hàm gửi tin nhắn tương đương với sendMessage bên GAS
    context.bot.send_message(
        chat_id=chat_id, 
        text=text, 
        parse_mode=telegram.ParseMode.HTML
    )

# --- 2. HÀM XỬ LÝ CHUYỂN ĐỔI LINK ---
def convert_link(update, context):
    """Xử lý tin nhắn chứa link Shopee và chuyển đổi."""
    chat_id = update.message.chat_id
    original_text = update.message.text
    
    # Regex tìm link shopee.vn hoặc shope.ee
    shopee_regex = r'https?:\/\/(?:www\.)?(shopee\.vn|shope\.ee)[^\s]*'
    
    links_found = 0
    
    # Tạo tham số affiliate
    affiliate_params = f"?aff_id={MY_DEFAULT_AFFILIATE_ID}&aff_platform=telegram_bot"
    
    def replacement_function(match):
        nonlocal links_found
        links_found += 1
        # Xóa các tham số cũ (nếu có) và thêm tham số mới
        cleaned_link = match.group(0).split('?')[0]
        return cleaned_link + affiliate_params

    new_text = re.sub(shopee_regex, replacement_function, original_text, flags=re.IGNORECASE)

    if links_found > 0:
        reply_header = f"✅ <b>Đã chuyển đổi thành công {links_found} link theo ID: {MY_DEFAULT_AFFILIATE_ID}</b>\n\n"
        context.bot.send_message(
            chat_id=chat_id, 
            text=reply_header + new_text, 
            parse_mode=telegram.ParseMode.HTML
        )
    else:
        # Nếu không tìm thấy link shopee
        context.bot.send_message(
            chat_id=chat_id, 
            text="Không tìm thấy link Shopee nào (shopee.vn hoặc shope.ee) trong tin nhắn của bạn. Vui lòng gửi link gốc nha!",
            parse_mode=telegram.ParseMode.HTML
        )

# --- 3. HÀM CHÍNH KHỞI ĐỘNG BOT ---
def main():
    """Khởi chạy bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_link))

    # Render cần chạy ở chế độ Web Server (Long Polling là không lý tưởng)
    # Chúng ta sẽ dùng chế độ Web Server đơn giản nhất:

    # updater.start_polling() # Bỏ dòng này

    # Render sẽ chạy ứng dụng web bằng lệnh trong Procfile (web: python bot.py)
    # và giữ ứng dụng Python chạy.

    print("Bot đang chạy ở chế độ Long Polling đơn giản...")
    updater.start_polling() # Dù không lý tưởng, chúng ta dùng cách này để giữ bot chạy

    # Thêm 2 dòng này để bot không bị tắt ngay:
    updater.idle()

if __name__ == '__main__':
    main()
