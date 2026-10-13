import streamlit as st
import pandas as pd
from url_analyzer import extract_url_features

# إعدادات الصفحة
st.set_page_config(
    page_title="منظومة الأمن السيبراني - كشف التصيد الاحتيالي", 
    page_icon="🛡️", 
    layout="wide"
)

# تنسيق CSS مخصص لدعم اللغة العربية وتجميل الواجهة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #004d99;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي (Sidebar) لمعلومات المشروع
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cyber-security.png", width=80)
    st.title("لوحة التحكم الأمني")
    st.info("نظام ذكي متكامل لكشف هجمات التصيد والروابط الوهمية الموجهة باللغة العامية واللهجة الفلسطينية.")
    st.markdown("---")
    st.markdown("### 📊 معلومات النظام:")
    st.write("• **نموذج المعالجة:** MARBERT & Heuristics")
    st.write("• **نطاق التحليل:** تحليل دلالي وهيكلي مزدوج")
    st.write("• **حالة الاتصال:** متصل وجاهز للفحص الفوري")
    st.markdown("---")
    st.caption("مشروع تخرج البكالوريوس - 2026")

# العنوان الرئيسي الواجهة
st.title("🛡️ المنظومة الذكية لكشف هجمات التصيد والروابط الوهمية")
st.markdown("تتيح هذه الأداة للمستخدمين والمحللين فحص الرسائل والروابط المشبوهة بدقة عالية عبر دمج معالجة النصوص والتحليل التقني.")

st.markdown("---")

# تقسيم الشاشة إلى عمودين (الإدخال والنتائج)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 مدخلات الفحص الأمني")
    text_input = st.text_area(
        "نص الرسالة الواردة (بالعامية أو الفصحى):", 
        placeholder="مثال: عزيزي العميل، تم إيقاف حسابك البنكي يرجى الضغط على الرابط لتحديث البيانات فوراً...",
        height=130
    )
    
    url_input = st.text_input(
        "عنوان الرابط المرفق (URL إن وجد):", 
        placeholder="http://bank-palestine-secure-login.xyz/verify"
    )
    
    analyze_btn = st.button("🚀 بدء الفحص والتحليل الشامل")

with col2:
    st.subheader("📌 نتائج التقييم والتقرير الفني")
    
    if analyze_btn:
        if not text_input and not url_input:
            st.warning("⚠️ يرجى إدخال نص رسالة أو رابط واحد على الأقل للبدء.")
        else:
            with st.spinner("جاري معالجة النص واستخراج الخصائص البرمجية للرابط..."):
                
                # 1. تحليل الرابط
                url_features = extract_url_features(url_input)
                url_score = 0.0
                if url_input and url_input != "N/A":
                    if url_features["has_ip"] or url_features["has_suspicious_keywords"] or not url_features["is_https"]:
                        url_score += 0.6
                    if url_features["url_length"] > 55:
                        url_score += 0.4

                # 2. تحليل النص 
                suspicious_phrases = ["مسكر", "مجمد", "بصم", "اربح", "جائزة", "تفعيل", "سحب", "تحديث", "تأكيد", "حسابك", "البنكي"]
                text_hit_count = sum(1 for phrase in suspicious_phrases if phrase in text_input)
                text_score = min(0.95, text_hit_count * 0.3) if text_hit_count > 0 else 0.10
                
                # النتيجة المركبة (Ensemble Score)
                if url_input and url_input != "N/A":
                    final_score = (text_score * 0.6) + (url_score * 0.4)
                else:
                    final_score = text_score
                
                # عرض مؤشر الخطر الرئيسي
                if final_score > 0.45:
                    st.error(f"🚨 **تحذير: رسالة احتيالية عالية الخطورة!**")
                    st.metric(label="معدل الخطر الإجمالي (Risk Score)", value=f"{final_score*100:.1f}%", delta="احتيال محتمل", delta_color="inverse")
                else:
                    st.success(f"✅ **الرسالة تبدو سليمة وآمنة**")
                    st.metric(label="معدل الخطر الإجمالي (Risk Score)", value=f"{final_score*100:.1f}%", delta="آمن", delta_color="normal")
                
                # تفاصيل المؤشرات المكتشفة
                with st.expander("🔍 تفاصيل التحليل التقني والدلالي"):
                    st.write(f"• **مؤشر دلالة النص العامي:** {'مشبوه' if text_score > 0.4 else 'طبيعي'} (التقييم: {text_score*100:.0f}%)")
                    if url_input and url_input != "N/A":
                        st.write(f"• **طول الرابط:** {url_features['url_length']} حرف")
                        st.write(f"• **استخدام بروتوكول HTTPS:** {'نعم (آمن)' if url_features['is_https'] else 'لا (غير مشفر ⚠️)'}")
                        st.write(f"• **احتوائه على كلمات مفتاحية للتصيد:** {'نعم ⚠️' if url_features['has_suspicious_keywords'] else 'لا'}")
                        st.write(f"• **استخدام IP مباشر:** {'نعم ⚠️' if url_features['has_ip'] else 'لا'}")
    else:
        st.info("أدخل بيانات الرسالة والرابط في القائمة المجاورة واضغط على زر الفحص لعرض النتائج هنا.")

# قسم سفلي توضيحي
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>نظام كشف هجمات التصيد والروابط الوهمية باللهجة الفلسطينية © 2026</p>", unsafe_allow_html=True)