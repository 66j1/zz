"""
أدوات مساعدة
Utility Functions
"""

import discord
from config import MAX_RESULTS


def create_hadith_embed(result: dict) -> discord.Embed:
    """
    إنشاء رسالة منسقة للحديث
    
    Args:
        result: بيانات الحديث المنسقة
        
    Returns:
        discord.Embed: رسالة منسقة
    """
    embed = discord.Embed(
        title=f"نتيجة {result['index']} - البحث عن: {result['topic']}",
        color=discord.Color.green()
    )
    
    # إضافة نص الحديث
    if result.get('text'):
        text_content = str(result['text'])
        # تقليل النص إذا كان طويلاً جداً (حد Discord: 1024 حرف للحقل)
        if len(text_content) > 1024:
            text_content = text_content[:1021] + "..."
        # تنظيف النص من أي أحرف قد تسبب مشاكل
        text_content = text_content.replace('\x00', '').strip()
        if text_content:
            embed.add_field(name="الحديث", value=text_content, inline=False)
    
    # إضافة المصدر
    if result.get('source'):
        source = str(result['source'])[:256]  # حد Discord للحقول
        embed.add_field(name="المصدر", value=source, inline=True)
    
    # إضافة الدرجة
    if result.get('grade'):
        grade = str(result['grade'])[:256]
        embed.add_field(name="الدرجة", value=grade, inline=True)
    
    # إضافة الرابط
    if result.get('link'):
        link = str(result['link'])
        # التحقق من أن الرابط صحيح
        if link.startswith('http'):
            embed.add_field(name="الرابط", value=link[:512], inline=False)
    
    # إضافة عدد النتائج في آخر رسالة
    if result['is_last']:
        embed.set_footer(
            text=f"تم العثور على {result['total_results']} نتيجة. عرض {result['shown_results']} نتيجة."
        )
    
    return embed


def create_error_embed(error_message: str) -> discord.Embed:
    """
    إنشاء رسالة خطأ منسقة
    
    Args:
        error_message: رسالة الخطأ
        
    Returns:
        discord.Embed: رسالة خطأ منسقة
    """
    embed = discord.Embed(
        title="❌ خطأ",
        description=error_message,
        color=discord.Color.red()
    )
    return embed


def create_help_embed() -> discord.Embed:
    """
    إنشاء رسالة المساعدة
    
    Returns:
        discord.Embed: رسالة المساعدة
    """
    embed = discord.Embed(
        title="مساعدة البوت",
        description="هذا البوت يبحث في الموسوعة الحديثية من موقع الدرر السنية",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="طريقة الاستخدام",
        value="اكتب الموضوع الذي تريد البحث عنه مباشرة في الرسالة، أو استخدم الأمر:\n`!بحث [الموضوع]`",
        inline=False
    )
    embed.add_field(
        name="مثال",
        value="`!بحث الصلاة`\nأو ببساطة اكتب: `الصلاة`",
        inline=False
    )
    embed.add_field(
        name="الأوامر المتاحة",
        value="`!بحث [الموضوع]` - البحث عن موضوع\n`!مساعدة` - عرض هذه الرسالة",
        inline=False
    )
    return embed

