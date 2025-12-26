"""
الملف الرئيسي للبوت
Main Bot File
"""

import discord
from discord.ext import commands
import sys
import io
from config import TOKEN, CLIENT_ID, COMMAND_PREFIX
from api_handler import search_hadith, format_hadith_results
from utils import create_hadith_embed, create_error_embed
from config import MAX_RESULTS

# إصلاح مشاكل الترميز في Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# إنشاء البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """حدث عند جاهزية البوت"""
    print("=" * 50)
    print(f'Bot {bot.user} is ready!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Client ID: {CLIENT_ID}')
    print(f'Connected to {len(bot.guilds)} server(s)')
    print("=" * 50)
    
    # تحديث حالة البوت
    try:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="الموسوعة الحديثية"
            )
        )
    except:
        pass


@bot.event
async def on_message(message):
    """حدث عند استلام رسالة"""
    # تجاهل رسائل البوت نفسه
    if message.author == bot.user:
        return
    
    # معالجة الأوامر أولاً
    if message.content.startswith(COMMAND_PREFIX):
        await bot.process_commands(message)
        return
    
    # البحث التلقائي عند كتابة أي موضوع
    if message.content.strip():
        topic = message.content.strip()
        await handle_auto_search(message, topic)


async def handle_auto_search(message, topic):
    """معالجة البحث التلقائي"""
    loading_msg = None
    try:
        # إظهار رسالة "جاري البحث..."
        loading_msg = await message.channel.send("🔍 جاري البحث...")
        
        # البحث في API
        data = await search_hadith(topic)
        
        # حذف رسالة "جاري البحث..."
        try:
            if loading_msg:
                await loading_msg.delete()
        except:
            pass
        
        if data:
            # تنسيق النتائج
            results = format_hadith_results(data, topic, MAX_RESULTS)
            
            if results:
                # إرسال النتائج
                for result in results:
                    try:
                        embed = create_hadith_embed(result)
                        await message.channel.send(embed=embed)
                    except Exception as e:
                        print(f"Error sending embed: {e}")
                        # محاولة إرسال نص بسيط
                        text = result.get('text', '')[:1000] if result.get('text') else 'لا يوجد نص'
                        await message.channel.send(f"**نتيجة {result['index']}:**\n{text}")
            else:
                error_embed = create_error_embed(f"لم يتم العثور على نتائج للموضوع: **{topic}**")
                await message.channel.send(embed=error_embed)
        else:
            error_embed = create_error_embed("حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.")
            await message.channel.send(embed=error_embed)
    
    except discord.errors.HTTPException as e:
        print(f"Discord HTTP error: {e}")
        try:
            if loading_msg:
                await loading_msg.delete()
        except:
            pass
        await message.channel.send("❌ حدث خطأ في إرسال الرسالة. قد يكون النص طويلاً جداً.")
    except Exception as e:
        print(f"Error in handle_auto_search: {e}")
        import traceback
        traceback.print_exc()
        try:
            if loading_msg:
                await loading_msg.delete()
        except:
            pass
        try:
            error_embed = create_error_embed(f"حدث خطأ أثناء البحث: {str(e)[:200]}")
            await message.channel.send(embed=error_embed)
        except:
            await message.channel.send("❌ حدث خطأ أثناء البحث.")


@bot.command(name='بحث')
async def search_command(ctx, *, topic):
    """أمر للبحث عن موضوع في الموسوعة الحديثية"""
    await handle_auto_search(ctx.message, topic)


@bot.command(name='مساعدة', aliases=['مساعده'])
async def help_command(ctx):
    """عرض رسالة المساعدة"""
    from utils import create_help_embed
    embed = create_help_embed()
    await ctx.send(embed=embed)


# تشغيل البوت
if __name__ == "__main__":
    try:
        print("Starting bot...")
        print(f"Token length: {len(TOKEN)}")
        print(f"Client ID: {CLIENT_ID}")
        bot.run(TOKEN, reconnect=True)
    except discord.LoginFailure:
        print("ERROR: Invalid token!")
        print("Please check your TOKEN in config.py")
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"ERROR starting bot: {e}")
        import traceback
        traceback.print_exc()

